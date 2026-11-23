"""Reproducible MNIST experiments and numerical reference for the sheet."""
from pathlib import Path
import os
import sys
sys.path.insert(0, str(Path(__file__).parent / '.deps'))
os.environ.setdefault('MPLBACKEND', 'Agg')
import argparse
import csv
import json
import platform
import time
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results'


def data():
    raw = HERE / 'data' / 'MNIST' / 'raw'
    def read(name, offset):
        return np.fromfile(raw / name, dtype=np.uint8, offset=offset)
    return (read('train-images-idx3-ubyte', 16).reshape(-1, 784).astype(np.float32)/255,
            read('train-labels-idx1-ubyte', 8).astype(np.int64),
            read('t10k-images-idx3-ubyte', 16).reshape(-1, 784).astype(np.float32)/255,
            read('t10k-labels-idx1-ubyte', 8).astype(np.int64))


def sheet_reference():
    X, y, T, ty = data()
    rng = np.random.default_rng(42)
    # Balanced, reproducible small sample; all 784 pixels are retained.
    idx = np.concatenate([rng.choice(np.flatnonzero(y == k), 10, replace=False) for k in range(10)])
    ti = np.concatenate([rng.choice(np.flatnonzero(ty == k), 10, replace=False) for k in range(10)])
    X = np.c_[X[idx], np.ones(len(idx))].astype(float)
    T = np.c_[T[ti], np.ones(len(ti))].astype(float)
    y, ty = y[idx], ty[ti]
    W1 = np.c_[rng.normal(0, np.sqrt(2/784), (16, 784)), np.zeros(16)]
    W2 = np.c_[rng.normal(0, np.sqrt(2/16), (10, 16)), np.zeros(10)]
    def step(a, labels, w1, w2):
        z = a @ w1.T
        h = np.c_[np.maximum(z, 0), np.ones(len(a))]
        logits = h @ w2.T
        ex = np.exp(logits-logits.max(1, keepdims=True))
        p = ex/ex.sum(1, keepdims=True)
        loss = -np.log(np.maximum(p[np.arange(len(a)), labels], 1e-300)).mean()
        do = p - np.eye(10)[labels]
        dh = (do @ w2[:, :16]) * (z > 0)
        return loss, float((p.argmax(1) == labels).mean()), dh.T@a/len(a), do.T@h/len(a), p
    initial = step(X, y, W1, W2)
    nw1, nw2 = W1-.2*initial[2], W2-.2*initial[3]
    history = []
    a, b = W1.copy(), W2.copy()
    for epoch in range(301):
        loss, acc, g1, g2, _ = step(X, y, a, b)
        tl, ta, *_ = step(T, ty, a, b)
        history.append([epoch, loss, acc, tl, ta])
        if epoch < 300:
            a -= .2*g1
            b -= .2*g2
    payload = dict(X=X.tolist(), y=y.tolist(), test_X=T.tolist(), test_y=ty.tolist(),
                   train_indices=idx.tolist(), test_indices=ti.tolist(), W1=W1.tolist(), W2=W2.tolist(),
                   next_W1=nw1.tolist(), next_W2=nw2.tolist(),
                   initial_loss=initial[0], initial_accuracy=initial[1],
                   next_loss=step(X,y,nw1,nw2)[0], probabilities=initial[4].tolist(),
                   trained_W1=a.tolist(), trained_W2=b.tolist(), history=history)
    (OUT/'sheet_reference.json').write_text(json.dumps(payload), encoding='utf-8')
    print('Sheet numerical reference:', history[0], history[-1], flush=True)


def notebook():
    """Execute the supplied code cells; only adapt installation, paths, plotting and device probe."""
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(42)
    source = HERE / 'examples_provided.ipynb'
    nb = json.loads(source.read_text(encoding='utf-8'))
    env = {}
    old = Path.cwd()
    executed, adaptations = [], []
    try:
        os.chdir(HERE)
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] != 'code' or not ''.join(cell['source']).strip():
                continue
            code = ''.join(cell['source'])
            if any(line.lstrip().startswith('%pip') for line in code.splitlines()):
                adaptations.append('cell 0: dependencies installed separately')
                continue
            if i == 18:
                code = code.replace('model(X)', 'model(X.to(device))')
                adaptations.append('cell 18: input moved to model device (CPU result unchanged)')
            code = code.replace('plt.show()', f'plt.savefig(r"{OUT / ("notebook_cell_"+str(i)+".png")}"); plt.close("all")')
            code = code.replace('"model"', '"results/notebook_model.pt"')
            print('Executing notebook cell', i, flush=True)
            exec(compile(code, f'{source.name}:cell{i}', 'exec'), env)
            executed.append(i)
        env['model'].eval()
        X,y,T,ty = data()
        with torch.no_grad():
            pred = env['model'](torch.from_numpy(T).reshape(-1,1,28,28).to(env['device'])).argmax(1).cpu().numpy()
        (OUT/'notebook_check.json').write_text(json.dumps(dict(executed_cells=executed, adaptations=adaptations,
            accuracy=float((pred==ty).mean()), torch=torch.__version__, seed=42), indent=2), encoding='utf-8')
    finally:
        os.chdir(old)


def curve():
    import torch
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    torch.set_num_threads(1)
    X,y,T,ty = data()
    xt, yt, tt, tty = map(torch.from_numpy, (X,y,T,ty))
    records = []
    if (OUT/'learning_runs.csv').exists():
        with (OUT/'learning_runs.csv').open(encoding='utf-8') as f:
            for r in csv.DictReader(f):
                records.append({k:(int(v) if k in ('seed','n','epochs','threads') else float(v)) for k,v in r.items()})
        for r in records:
            r.setdefault('threads',4)
    for seed in range(3):
        rng = np.random.default_rng(seed)
        # Nested, approximately balanced samples, generated without test labels.
        by_class = [rng.permutation(np.flatnonzero(y == k)) for k in range(10)]
        order = np.concatenate([np.array([a[i] for a in by_class if i < len(a)]) for i in range(max(map(len,by_class)))])
        for n in (100, 500, 2000, 10000, 30000, 60000):
            if any(r['seed']==seed and r['n']==n for r in records):
                continue
            torch.manual_seed(seed)
            model = torch.nn.Sequential(torch.nn.Linear(784,16), torch.nn.ReLU(), torch.nn.Linear(16,10))
            torch.nn.init.kaiming_normal_(model[0].weight, nonlinearity='relu')
            torch.nn.init.zeros_(model[0].bias)
            torch.nn.init.kaiming_normal_(model[2].weight, nonlinearity='linear')
            torch.nn.init.zeros_(model[2].bias)
            opt = torch.optim.SGD(model.parameters(), lr=.1)
            ids = torch.from_numpy(order[:n])
            a,b = xt[ids],yt[ids]
            start = time.perf_counter()
            for epoch in range(1,61):
                model.train()
                for batch in torch.randperm(n).split(128):
                    opt.zero_grad()
                    loss = torch.nn.functional.cross_entropy(model(a[batch]), b[batch])
                    loss.backward()
                    opt.step()
                model.eval()
                with torch.no_grad():
                    train_acc = (model(a).argmax(1)==b).float().mean().item()
                if train_acc >= .999:
                    break
            with torch.no_grad():
                test_acc = (model(tt).argmax(1)==tty).float().mean().item()
            row = dict(seed=seed,n=n,epochs=epoch,train_accuracy=train_acc,test_accuracy=test_acc,seconds=time.perf_counter()-start,threads=1)
            records.append(row)
            print(row, flush=True)
            with (OUT/'learning_runs.csv').open('w',newline='',encoding='utf-8') as f:
                writer=csv.DictWriter(f,fieldnames=list(row)); writer.writeheader(); writer.writerows(records)
    summary=[]
    for n in sorted({r['n'] for r in records}):
        rr=[r for r in records if r['n']==n]
        summary.append(dict(n=n, train_mean=float(np.mean([r['train_accuracy'] for r in rr])),
                            test_mean=float(np.mean([r['test_accuracy'] for r in rr])),
                            test_std=float(np.std([r['test_accuracy'] for r in rr], ddof=1))))
    def power(n,a,b,c): return a*np.power(n,-b)+c
    ns=np.array([r['n'] for r in summary],float); errors=1-np.array([r['test_mean'] for r in summary])
    fit={}
    try:
        pars,_=curve_fit(power,ns,errors,p0=[2,.4,.01],bounds=([0,0,0],[100,3,1]),maxfev=20000)
        fit=dict(a=float(pars[0]),b=float(pars[1]),c=float(pars[2]))
        fit['estimated_n_for_0999']=float((pars[0]/(.001-pars[2]))**(1/pars[1])) if pars[2]<.001 else None
    except (RuntimeError,ValueError) as exc:
        fit={'error':str(exc)}
    result=dict(architecture=[784,16,10],optimizer='SGD',lr=.1,batch_size=128,max_epochs=60,seeds=[0,1,2],
                stopping='train accuracy >= 0.999; no test-based selection',summary=summary,fit=fit,
                python=platform.python_version(),torch=torch.__version__,numpy=np.__version__)
    (OUT/'learning_curve.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    plt.errorbar(ns,1-errors,yerr=[r['test_std'] for r in summary],marker='o',capsize=4,label='Test (mean +/- SD, 3 runs)')
    plt.plot(ns,[r['train_mean'] for r in summary],marker='o',label='Train')
    plt.axhline(.999,color='red',ls='--',label='Target 0.999')
    plt.xscale('log'); plt.xlabel('Training examples'); plt.ylabel('Accuracy'); plt.legend(); plt.grid(alpha=.25)
    plt.tight_layout(); plt.savefig(OUT/'learning_curve.png',dpi=160); plt.close()


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    parser=argparse.ArgumentParser(); parser.add_argument('task',choices=['sheet','notebook','curve','all']); args=parser.parse_args()
    if args.task in ('sheet','all'): sheet_reference()
    if args.task in ('notebook','all'): notebook()
    if args.task in ('curve','all'): curve()
