import pandas
import os

for fileName in os.listdir('./debugging/input/'):
    if 'weapon' in fileName:
        df1 = pandas.DataFrame(data = [[0, 0, 0]], columns = ['weapon_attack', 'weapon_rarity', 'weapon_rarity_raw'], index = [0])
        df2 = pandas.read_json('./debugging/input/' + fileName, orient = 'index')
        pandas.concat(objs = [df1, df2]).to_json('./debugging/input/' + fileName, indent = 4, orient = 'index')
        print('Converted ' + fileName)
    elif 'item' in fileName:
        df1 = pandas.DataFrame(data = [[0, 0, 0]], columns = ['item_amount', 'item_rarity', 'item_rarity_raw'], index = [0])
        df2 = pandas.read_json('./debugging/input/' + fileName, orient = 'index')
        pandas.concat(objs = [df1, df2]).to_json('./debugging/input/' + fileName, indent = 4, orient = 'index')
        print('Converted ' + fileName)
    else:
        print('Skip ' + fileName)