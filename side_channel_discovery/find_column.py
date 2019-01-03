import pandas as pd

df = pd.read_csv('../feature_diff/feature_libskia_ftrace_CapitolOne.csv')
x='generateGlyphImage'
cols = [c for c in df.columns if x in c ]

df = df[cols]

df.to_csv('../results/separated_file.csv')



