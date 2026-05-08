import sys
import pandas as pd

print("arguments: ",sys.argv)

mounth=int(sys.argv[1])

df= pd.DataFrame({'day':[1,2,3], 'Num_passengers':[4,5,6]})
df['month'] = mounth
print(df.head())
df.to_parquet(f'output={mounth}.parquet')   
print("hello pipeline, month: ", mounth)
