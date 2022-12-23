import pandas

print(str(pandas.read_json('./Indexes/WeaponIndex/lantern.json', orient = 'index').at['attack', 'specific_elem_1']))