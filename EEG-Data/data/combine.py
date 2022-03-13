import pandas as pd
import sys

name = sys.argv[1]
df = pd.read_csv(sys.argv[2])
if all(df.iloc[0].values[1:] == 0):
    print("change")
    df.at[1, 'Frequency'] = df.at[0, 'Frequency']
    df.at[1, 'Color Code'] = df.at[0, 'Color Code']
    df = df[1:]

for fname in sys.argv[3:]:
    temp = pd.read_csv(fname)
    if all(temp.iloc[0].values[1:] == 0):
        print("change")
        temp.at[1, 'Frequency'] = temp.at[0, 'Frequency']
        temp.at[1, 'Color Code'] = temp.at[0, 'Color Code']
        temp = temp[1:]
    df = pd.concat((df, temp))

df.to_csv(f'COMBINED_{name}.csv', index=False)