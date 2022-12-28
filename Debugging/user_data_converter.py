import pandas
import os

rec_user = ''
for file_name in os.listdir('./Debugging/Input'):
    if '.isregistered' in file_name:
        cur_usr = file_name.split('.')[0]
        print(f'Skip {file_name}')
    elif '_basicInfo' in file_name:
        ubi = pandas.read_json('./Debugging/Input/' + file_name, typ = 'series')
        pandas.Series(data = [ubi['skyDustAmount'], ubi['signedDays'], 2022, 12, ubi['lastActivity'], ubi['earthDustAmount'], ubi['continuousSigned']], index = ['sky_dust_amount', 'signed_days', 'last_activity_year', 'last_activity_month', 'last_activity_day', 'earth_dust_amount', 'continuous_signed']).to_json(f'./Debugging/Output/{cur_usr}_basic_info.json', indent = 4)
        print(f'Converted{file_name}')
    elif '_inGameInfo' in file_name:
        pandas.Series(data = [0.0, 2000.0, 150.0, 20.0, 0.05, 0.0, 7.0], index = ['current_level', 'basic_HP', 'basic_attack', 'basic_defence', 'basic_crit_rate', 'current_exp', 'steps_per_round']).to_json(f'./Debugging/Output/{cur_usr}_in_game_info.json', indent = 4)
        print(f'Converted{file_name}')
    elif '_weaponForm' in file_name:
        pandas.DataFrame(data = [[0, 0, 0, 0], [50, 'Special', -1, 2]], columns = ['weapon_attack', 'weapon_rarity', 'weapon_rarity_raw', 'weapon_step'], index = [0, '新手剑']).to_json(f'./Debugging/Output/{cur_usr}_weapon_form.json', indent = 4, orient = 'index')
        print(f'Converted{file_name}')
    elif '_itemForm' in file_name:
        pandas.DataFrame(data= [[0, 0, 0, 0], [1, 'Common', 0.4, 2]], columns = ['item_amount', 'item_rarity', 'item_rarity_raw', 'item_step'], index = [0, '生命药水']).to_json(f'./Debugging/Output/{cur_usr}_item_form.json', indent = 4, orient = 'index')
        print(f'Converted{file_name}')
    if cur_usr != rec_user:
        pandas.DataFrame(data = [[0, 0, 0, 0, '0', 0], [10, 'Special', -1, 0.02, 'spirit', 1]], columns = ['armor_defence', 'armor_rarity', 'armor_rarity_raw','armor_crit_rate', 'armor_element', 'armor_step'], index = [0, '新手长袍']).to_json('./Debugging/Output/' + cur_usr +'_armor_form.json', indent = 4, orient = 'index')
        rec_user = cur_usr
        print(f'Created{cur_usr}_armor_form.json')