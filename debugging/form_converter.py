import pandas
import os

for fileName in os.listdir('./debugging/input/'):
    if 'weapon' in fileName:
        pandas.read_json('./debugging/input/' + fileName, orient = 'index').set_index('weaponName').to_json('./debugging/input/' + fileName, indent = 4, orient = 'index')
    if 'item' in fileName:
        pandas.read_json('./debugging/input/' + fileName, orient = 'index').set_index('itemName').to_json('./debugging/input/' + fileName, indent = 4, orient = 'index')
    print('Converted ' + fileName)