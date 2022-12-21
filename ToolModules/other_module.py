#coding = utf-8
import random
import pandas

def gacha():
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

def convertToOutputForm(pandas_form: pandas.DataFrame, form_type, priceIncluded = False):
    match form_type:
        case 'weapon':
            if priceIncluded == False:
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
                    if priceIncluded == True:
                        result += ' | ' + str(row['weapon_price'])
        case 'item':
            if priceIncluded == False:
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
                    if priceIncluded == True:
                        result += ' | ' + str(row['itemPrice'])
    return result


def updateUser_in_game_info(user):
    user_in_game_info = pandas.read_json('./users/' + user + '_in_game_info.json', typ = 'series')
    #更新等级
    while True:
        if user_in_game_info['current_level'] == 100:
            return
        elif user_in_game_info['current_level'] >= 80:
            expNeeded = 262144 #2 ** 18
        elif user_in_game_info['current_level'] >= 50:
            expNeeded = 65536 #2 ** 16
        elif user_in_game_info['current_level'] >= 30:
            expNeeded = 16384 #2 ** 14
        elif user_in_game_info['current_level'] >= 20:
            expNeeded = 4096 #2 ** 12
        elif user_in_game_info['current_level'] >= 10:
            expNeeded = 1024 #2 ** 10
        else:
            expNeeded = 256 #2 ** 8

        if user_in_game_info['current_exp'] > expNeeded:
            user_in_game_info['current_level'] += 1
            user_in_game_info['current_exp'] -= expNeeded
        else:
            break
    #更新基础生命值
    user_in_game_info['basic_HP'] = user_in_game_info['current_level'] * 25 + 2000
    #更新基础攻击力
    user_in_game_info['basic_attack'] = user_in_game_info['current_level'] * 5 + 50
    user_in_game_info.to_json('./users/' + user + '_in_game_info.json', indent = 4)