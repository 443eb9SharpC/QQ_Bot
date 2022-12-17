import pandas
df = pandas.DataFrame(columns = ['itemName', 'itemAmount', 'itemRarity', 'itemRarityRaw'])
df1 = pandas.read_json('./homework/homework.xslx')
print(df)
print(df1)
pandas.concat(objs = [df, df1], ignore_index = True)
print(df)