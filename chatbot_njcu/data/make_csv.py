import os, glob, pandas as pd

folder_rel = r'..\..\..\data'
folder = os.path.abspath(folder_rel)

# find qa.xlsx/qa.xls in that folder
cands = []
for name in ('qa.xlsx', 'qa.xls'):
    p = os.path.join(folder, name)
    if os.path.exists(p):
        cands.append(p)
if not cands:
    for ext in ('*.xlsx','*.xls'):
        cands.extend(glob.glob(os.path.join(folder, ext)))
if not cands:
    raise FileNotFoundError(f'No Excel file found in {folder}')

xls_path = cands[0]
print('Reading:', xls_path)

df = pd.read_excel(xls_path)

# choose question/answer columns (fallback to first two)
def pick(cols, names):
    lower = [str(c).strip().lower() for c in cols]
    for n in names:
        if n in lower:
            return cols[lower.index(n)]
    return None

cols = list(df.columns)
q = pick(cols, {'question','questions','q','prompt'}) or cols[0]
a = pick(cols, {'answer','answers','a','response','reply'}) or cols[1]

out_path = os.path.join(folder, 'qa.csv')
df[[q, a]].rename(columns={q:'question', a:'answer'}).to_csv(out_path, index=False, encoding='utf-8')
print('Wrote:', out_path)
