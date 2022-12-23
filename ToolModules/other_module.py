#coding = utf-8
import random
import pandas


def Gacha():
    rand = random.randint(1, 4)
    #1/4出武器
    if rand == 1:
        activity_weapon_form = pandas.read_json('./Activities/activity_weapon_form.json', orient = 'index')
        weapon = activity_weapon_form.sample(n = 1, weights = 'weapon_rarity_raw')
        return weapon
    
    #3/4出物品
    else:
        activity_item_form = pandas.read_json('./Activities/activity_item_form.json', orient = 'index')
        item = activity_item_form.sample(n = 1, weights = 'item_rarity_raw')
        return item


def ConvertToOutputForm(pandas_form: pandas.DataFrame, form_type, price_included = False):
    match form_type:
        case 'weapon':
            if price_included == False:
                result = '\n武器名 | 攻击力 | 稀有度'
            else:
                result = '\n武器名 | 攻击力 | 稀有度 | 价格'
            if pandas_form.empty == True:
                result += '\n无武器'
            else:
                for index, row in pandas_form.iterrows():
                    #跳过占位符
                    if row[0] == 0:
                        continue
                    result += '\n' + index + ' | ' + str(row['weapon_attack']) + ' | ' + row['weapon_rarity']
                    if price_included == True:
                        result += ' | ' + str(row['weapon_price'])

        case 'item':
            if price_included == False:
                result = '\n物品名 | 数量 | 稀有度'
            else:
                result = '\n物品名 | 数量 | 稀有度 | 价格'
            if pandas_form.empty == True:
                result += '\n无物品'
            else:
                for index, row in pandas_form.iterrows():
                    if row[0] == 0:
                        continue
                    result += '\n' + index + ' | ' + str(row['item_amount']) + ' | ' + row['item_rarity']
                    if price_included == True:
                        result += ' | ' + str(row['item_price'])

        case 'armor':
            if price_included == False:
                result = '\n盔甲名 | 防御力 | 稀有度'
            else:
                result = '\n盔甲名 | 防御力 | 稀有度 | 价格'
            if pandas_form.empty == True:
                result += '\n无盔甲'
            else:
                for index, row in pandas_form.iterrows():
                    if row[0] == 0:
                        continue
                    result += '\n' + index + str(row['armor_defence']) + ' | ' + row['armor_rarity']
                    if price_included == True:
                        result += ' | ' + str(row['armor_price'])
    return result


def UpdateUserInGameInfo(user):
    user_in_game_info = pandas.read_json('./Users/' + user + '_in_game_info.json', typ = 'series')
    #更新等级
    while True:
        if user_in_game_info['current_level'] == 100:
            return
        elif user_in_game_info['current_level'] >= 80:
            exp_needed = 262144 #2 ** 18
        elif user_in_game_info['current_level'] >= 50:
            exp_needed = 65536 #2 ** 16
        elif user_in_game_info['current_level'] >= 30:
            exp_needed = 16384 #2 ** 14
        elif user_in_game_info['current_level'] >= 20:
            exp_needed = 4096 #2 ** 12
        elif user_in_game_info['current_level'] >= 10:
            exp_needed = 1024 #2 ** 10
        else:
            exp_needed = 256 #2 ** 8

        if user_in_game_info['current_exp'] > exp_needed:
            user_in_game_info['current_level'] += 1
            user_in_game_info['current_exp'] -= exp_needed
        else:
            break
    #更新基础生命值
    user_in_game_info['basic_HP'] = user_in_game_info['current_level'] * 25 + 2000
    #更新基础攻击力
    user_in_game_info['basic_attack'] = user_in_game_info['current_level'] * 5 + 50
    #更新基础防御力
    user_in_game_info['basic_defence'] = user_in_game_info['current_level'] * 5 + 20
    #更新行动力
    user_in_game_info['steps_per_round'] = user_in_game_info['current_level'] // 10 + 10
    if user_in_game_info['steps_per_round'] > 15:
        user_in_game_info['steps_per_round'] = 15
    #更新基础暴击率
    user_in_game_info['basic_crit_rate'] = user_in_game_info['basic_crit_rate'] * 0.01 + 0.05
    #防止暴击率溢出
    if user_in_game_info['basic_crit_rate'] > 0.3:
        user_in_game_info['basic_crit_rate'] = 0.3
    #保存
    user_in_game_info.to_json('./Users/' + user + '_in_game_info.json', indent = 4)