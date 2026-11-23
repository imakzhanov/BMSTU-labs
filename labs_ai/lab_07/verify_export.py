"""Read-only checks on the final exported XLSX, including cached formula results."""
from pathlib import Path
import json
import zipfile
import xml.etree.ElementTree as ET
import openpyxl

here=Path(__file__).resolve().parent
target=here/'outputs/mnist_perceptron.xlsx'
book=openpyxl.load_workbook(target,read_only=True,data_only=True)
assert len(book.sheetnames)==6
assert book['Summary']['B21'].value==99900
assert abs(book['Summary']['B12'].value-2.3026364551786553)<1e-10
ref=json.loads((here/'results/sheet_reference.json').read_text())
actual=list(book['Weights'].iter_rows(min_row=45,max_row=60,min_col=2,max_col=786,values_only=True))
err=max(abs(a-b) for row,expected in zip(actual,ref['next_W1']) for a,b in zip(row,expected))
assert err<1e-10
book.close()
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
formula_count=0
errors=[]
with zipfile.ZipFile(target) as archive:
    sheets=[n for n in archive.namelist() if n.startswith('xl/worksheets/sheet') and n.endswith('.xml')]
    for name in sheets:
        root=ET.fromstring(archive.read(name))
        formula_count+=len(root.findall('.//s:f',ns))
        errors.extend((name,c.attrib.get('r')) for c in root.findall('.//s:c',ns) if c.attrib.get('t')=='e')
    charts=[n for n in archive.namelist() if '/charts/' in n and n.endswith('.xml')]
assert not errors, errors
assert len(charts)==1
result=dict(sheets=len(sheets),formula_count=formula_count,formula_errors=errors,cached_w1_max_error=err,chebyshev_target_n=99900,charts=len(charts))
(here/'results/export_verification.json').write_text(json.dumps(result,indent=2))
print(result)
