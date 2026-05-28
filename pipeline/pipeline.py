import sys
import pandas as pd

print('Tham số:', sys.argv)

month = int(sys.argv[1])

print(f'month={month}')

df=pd.DataFrame({"day":[1,2,3,4,5], "price":[12,8,9,0,7]})

print(df.head())

df.to_parquet(f"output_{month}.parquet")