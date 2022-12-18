import pandas

df1 = pandas.read_json('./debugging/frame1.json', orient = 'index')
df2 = pandas.read_json('./debugging/frame2.json', orient = 'index')
print(pandas.concat(objs = [df1, df2]))