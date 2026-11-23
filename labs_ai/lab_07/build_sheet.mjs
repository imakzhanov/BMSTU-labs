import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile, FileBlob} from '@oai/artifact-tool';
const dir=path.dirname(fileURLToPath(import.meta.url));
if(process.argv.includes('--polish')){
 const target=path.join(dir,'outputs/mnist_perceptron.xlsx');
 const book=await SpreadsheetFile.importXlsx(await FileBlob.load(target));
 const summary=book.worksheets.getItem('Summary');
 summary.getRange('B21').formulas=[['=ROUNDUP(ROUND(B20/((1-B16)*B17^2),8),0)']];
 summary.getRange('A22').values=[['N без ошибок для p >= 0.999 (99% доверие)']];
 for(const a of ['B19','B21','B22'])summary.getRange(a).setNumberFormat('#,##0');
 summary.getRange('B20').setNumberFormat('0.000000');
 book.recalculate();
 if(summary.getRange('B21').values[0][0]!==99900)throw Error('Sample size rounding failed');
 const img=await book.render({sheetName:'Summary',range:'A1:E22',scale:1,format:'png'});
 await fs.writeFile(path.join(dir,'results/preview_Summary.png'),new Uint8Array(await img.arrayBuffer()));
 const output=await SpreadsheetFile.exportXlsx(book);await output.save(target);
 console.log('Polished Summary: N =',summary.getRange('B21').values[0][0]);
 process.exit(0);
}
const ref=JSON.parse(await fs.readFile(path.join(dir,'results/sheet_reference.json'),'utf8'));
const wb=Workbook.create();
const sheets=Object.fromEntries(['Summary','Forward','Backward','Weights','Data','Curve'].map(n=>[n,wb.worksheets.add(n)]));
function col(n){let s='';for(;n>0;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function val(s,r,c,a){const width=Math.max(...a.map(row=>row.length));const rows=a.map(row=>Array.from({length:width},(_,i)=>row[i]??null));sheets[s].getRangeByIndexes(r-1,c-1,rows.length,width).values=rows;}
function form(s,r,c,a){sheets[s].getRangeByIndexes(r-1,c-1,a.length,a[0].length).formulas=a;}
function block(s,range){return sheets[s].getRange(range);}
for(const s of Object.values(sheets)){s.showGridLines=false;s.getRange('A1:BA210').format.font={name:'Arial',size:10};s.getRange('A1:BA210').format.columnWidth=12;s.freezePanes.freezeRows(4);}
val('Summary',2,1,[['MNIST: полносвязный перцептрон 784–16–10']]);
val('Summary',4,1,[['Параметр','Значение'],['Шаг обучения',.2],['Эпохи для макроса',100],['Текущая эпоха',0],['Цель accuracy',.999]]);
val('Summary',10,1,[['Точность обучения'],['Точность теста'],['Ошибка обучения'],['Ошибка теста']]);
form('Summary',10,2,[['=AVERAGE(Forward!AX5:AX104)'],['=AVERAGE(Forward!AX105:AX204)'],['=AVERAGE(Forward!AY5:AY104)'],['=AVERAGE(Forward!AY105:AY204)']]);
val('Summary',16,1,[['Доверие P',.99],['Погрешность eps',.001],['Дисперсия: худший случай',.25],['N проверки: худший случай'],['Дисперсия при p = 0.999'],['N проверки: при p = 0.999'],['N без ошибок для p >= 0.999 (99% доверие)']]);
form('Summary',19,2,[['=ROUNDUP(B18/((1-B16)*B17^2),0)'],['=B8*(1-B8)'],['=ROUNDUP(ROUND(B20/((1-B16)*B17^2),8),0)'],['=ROUNDUP(LN(1-B16)/LN(B8),0)']]);
val('Summary',24,1,[['N в строках 19–22 относится к ПРОВЕРКЕ, а не к обучению.'],['Данные: 100 обучающих + 100 тестовых MNIST. Seed = 42.'],['Желтые ячейки — параметры. Веса обновляет макрос TrainMNIST.'],['Все операции нейросети и градиенты — формулы SUMPRODUCT, MAX, EXP, LN.'],['Для полного эксперимента см. Curve: результаты Python для той же архитектуры.']]);
val('Summary',30,1,[['Эпоха','Train loss','Train accuracy','Test loss','Test accuracy']]);
val('Data',2,1,[['MNIST: метка, 784 пикселя / 255, константа смещения 1']]);
val('Data',3,1,[['Источник: локальные оригинальные IDX MNIST. Первые 100 строк — train, следующие 100 — test.']]);
val('Data',4,1,[['label',...Array.from({length:784},(_,i)=>`pixel_${i}`),'bias']]);
val('Data',5,1,[...ref.X.map((x,i)=>[ref.y[i],...x]),...ref.test_X.map((x,i)=>[ref.test_y[i],...x])]);
const last=col(786);
val('Weights',2,1,[['W1: 16 нейронов × (784 пикселя + bias). W2: 10 × (16 + bias).']]);
val('Weights',4,1,[['Текущие W1']]);val('Weights',24,1,[['Текущие W2']]);
val('Weights',44,1,[['Следующие W1 = W1 - lr * gradient']]);val('Weights',64,1,[['Следующие W2']]);
val('Weights',84,1,[['Начальные W1 (ResetMNIST)']]);val('Weights',104,1,[['Начальные W2']]);
val('Weights',5,2,ref.W1);val('Weights',25,2,ref.W2);val('Weights',85,2,ref.W1);val('Weights',105,2,ref.W2);
val('Forward',2,1,[['Прямой проход: ReLU, logits, exp(logit-max), softmax, ответ и cross-entropy']]);
val('Forward',4,1,[['label',...Array.from({length:16},(_,i)=>`h${i}`),'bias',...Array.from({length:10},(_,i)=>`logit${i}`),...Array.from({length:10},(_,i)=>`exp${i}`),...Array.from({length:10},(_,i)=>`p${i}`),'ответ','верно','loss','max logit','sum exp']]);
form('Forward',5,1,Array.from({length:200},(_,i)=>{
 const r=i+5;return [`=Data!A${r}`,...Array.from({length:16},(_,h)=>`=MAX(0,SUMPRODUCT(Data!B${r}:${last}${r},Weights!B${h+5}:${last}${h+5}))`),'=1',
 ...Array.from({length:10},(_,k)=>`=SUMPRODUCT(B${r}:R${r},Weights!B${25+k}:R${25+k})`),
 ...Array.from({length:10},(_,k)=>`=EXP(${col(19+k)}${r}-AZ${r})`),
 ...Array.from({length:10},(_,k)=>`=${col(29+k)}${r}/BA${r}`),
 `=MATCH(MAX(AM${r}:AV${r}),AM${r}:AV${r},0)-1`,`=IF(AW${r}=A${r},1,0)`,
 `=-LN(MAX(INDEX(AM${r}:AV${r},1,A${r}+1),1E-300))`,`=MAX(S${r}:AB${r})`,`=SUM(AC${r}:AL${r})`];
}));
val('Backward',2,1,[['Обратный проход: delta output = p-y; delta hidden = delta output * W2 * ReLU derivative']]);
val('Backward',4,1,[['label',...Array.from({length:10},(_,k)=>`delta${k}`),'',...Array.from({length:16},(_,h)=>`dh${h}`)]]);
form('Backward',110,2,Array.from({length:16},(_,h)=>Array.from({length:10},(_,k)=>`=Weights!${col(h+2)}${k+25}`)));
form('Backward',5,1,Array.from({length:100},(_,i)=>{const r=i+5;return [`=Data!A${r}`,...Array.from({length:10},(_,k)=>`=Forward!${col(39+k)}${r}-IF(A${r}=${k},1,0)`),'',...Array.from({length:16},(_,h)=>`=IF(Forward!${col(h+2)}${r}>0,SUMPRODUCT(B${r}:K${r},B${h+110}:K${h+110}),0)`)];}));
form('Weights',45,2,Array.from({length:16},(_,h)=>Array.from({length:785},(_,p)=>`=${col(p+2)}${h+5}-Summary!$B$5*SUMPRODUCT(Data!${col(p+2)}$5:${col(p+2)}$104,Backward!${col(h+13)}$5:${col(h+13)}$104)/100`)));
form('Weights',65,2,Array.from({length:10},(_,k)=>Array.from({length:17},(_,h)=>`=${col(h+2)}${k+25}-Summary!$B$5*SUMPRODUCT(Forward!${col(h+2)}$5:${col(h+2)}$104,Backward!${col(k+2)}$5:${col(k+2)}$104)/100`)));
console.log('Formulas built; recalculating');
wb.recalculate();
function maxDiff(a,b){const bf=b.flat();return Math.max(...a.flat().map((x,i)=>Math.abs(x-bf[i])));}
const check={initial_loss:block('Summary','B12').values[0][0],expected_loss:ref.initial_loss,
 w1_max_error:maxDiff(block('Weights',`B45:${last}60`).values,ref.next_W1),
 w2_max_error:maxDiff(block('Weights','B65:R74').values,ref.next_W2),
 probabilities_max_error:maxDiff(block('Forward','AM5:AV104').values,ref.probabilities)};
if(!Number.isFinite(check.w1_max_error)||check.w1_max_error>1e-9||check.w2_max_error>1e-9||check.probabilities_max_error>1e-9)throw Error(JSON.stringify(check));
console.log('Independent NumPy comparison:',check);
// Probe an editable driver; restore it before export. Bulk weight iteration belongs to Calc.
val('Summary',5,2,[[0]]);wb.recalculate();
check.zero_lr_w1_error=maxDiff(block('Weights',`B45:${last}60`).values,ref.W1);
if(check.zero_lr_w1_error>1e-12)throw Error('Learning rate driver failed');
val('Summary',5,2,[[.2]]);
check.numpy_after_step_loss=ref.next_loss;
val('Summary',31,1,[[0,...ref.history[0].slice(1)]]);
let curve;
while(!curve){try{curve=JSON.parse(await fs.readFile(path.join(dir,'results/learning_curve.json'),'utf8'));}
catch{console.log('Waiting for learning curve experiment');await new Promise(r=>setTimeout(r,30000));}}
val('Curve',2,1,[['Зависимость точности от размера обучающей выборки']]);
val('Curve',4,1,[['N train','Train mean','Test mean','Test SD','Цель']]);
val('Curve',5,1,curve.summary.map(r=>[r.n,r.train_mean,r.test_mean,r.test_std,.999]));
val('Curve',13,1,[['Сеть 784–16–10, SGD 0.1, batch 128, до 60 эпох, 3 seed.'],['Ранний останов: accuracy train >= 0.999. Тест не используется для остановки.'],['Тест: все 10 000 исходных тестовых изображений MNIST.'],['Формула Чебышева оценивает объем проверки, не число примеров для обучения.']]);
val('Curve',19,1,[['Подгонка test error = a * N^(-b) + c'],['a',curve.fit.a??null],['b',curve.fit.b??null],['c',curve.fit.c??null],['Оценка N для 0.999',curve.fit.estimated_n_for_0999??'Не получена: подгонка не пересекает цель']]);
for(const name of ['Summary','Curve']){const s=sheets[name];s.getRange('A1:A32').format.columnWidth=57;s.getRange('B1:E32').format.columnWidth=18;s.getRange('A2:E2').format.font={name:'Arial',size:14,bold:true};}
block('Summary','A4:B4').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true}};
block('Summary','B5:B6').format.fill='#FFF2CC';block('Summary','B8').format.fill='#FFF2CC';block('Summary','B16:B17').format.fill='#FFF2CC';
block('Summary','B10:B11').setNumberFormat('0.0%');block('Summary','B12:B13').setNumberFormat('0.000000');block('Summary','B16:B18').setNumberFormat('0.000');block('Summary','B19:B22').setNumberFormat('#,##0');block('Summary','B20').setNumberFormat('0.000000');
block('Summary','A30:E30').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true}};
block('Curve','A4:E4').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true}};
block('Curve','B5:E10').setNumberFormat('0.0000');
const chart=sheets.Curve.charts.add('line',block('Curve','A4:C10'));chart.title='Точность на обучении и тесте';chart.setPosition('G4','Q18');
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Summary!A4:B22',include:'values,formulas',tableMaxRows:20,tableMaxCols:2})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A',options:{useRegex:true,maxResults:10},maxChars:2000})).ndjson);
await fs.writeFile(path.join(dir,'results/sheet_verification.json'),JSON.stringify(check,null,2));
for(const [name,range] of [['Summary','A1:E22'],['Forward','A2:H12'],['Backward','A2:K12'],['Weights','A2:H20'],['Data','A2:H12'],['Curve','A1:Q18']]){
 const img=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(path.join(dir,`results/preview_${name}.png`),new Uint8Array(await img.arrayBuffer()));
}
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(path.join(dir,'outputs/mnist_perceptron.xlsx'));
console.log('Saved outputs/mnist_perceptron.xlsx');
