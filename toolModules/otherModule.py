#coding = utf-8
import random
import pandas

def gacha():
    rand = random.randint(1, 4)
    #1/4出武器
    if rand == 1:
        activityWeaponForm = pandas.read_json('./activities/activityWeaponForm.json', orient = 'index')
        weapon = activityWeaponForm.sample(n = 1, weights = 'weaponRarityRaw')
        return weapon
    
    #3/4出物品
    else:
        activityItemForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index')
        item = activityItemForm.sample(n = 1, weights = 'itemRarityRaw')
        return item

def convertToOutputForm(f_pandasForm: pandas.DataFrame, f_formType, f_priceIncluded = False):
    match f_formType:
        case 'weapon':
            result = '\n武器名 | 攻击力 | 稀有度'
            if f_pandasForm.empty == True:
                result += '\n无武器'
            else:
                for index, row in f_pandasForm.iterrows():
                    result += '\n' + index + ' | ' + str(row['weaponAttack']) + ' | ' + row['weaponRarity']
                    if f_priceIncluded == True:
                        result += ' | ' + str(row['weaponPrice'])
        case 'item':
            result = '\n物品名 | 数量 |稀有度'
            if f_pandasForm.empty == True:
                result += '\n无物品'
            else:
                for index, row in f_pandasForm.iterrows():
                    result += '\n' + index + ' | ' + str(row['itemAmount']) + ' | ' + row['itemRarity']
                    if f_priceIncluded == True:
                        result += ' | ' + str(row['itemPrice'])
    return result


def updateUserInGameInfo(f_user):
    userInGameInfo = pandas.read_json('./users/' + f_user + '_inGameInfo.json', typ = 'series')
    #更新等级
    while True:
        if userInGameInfo['currentLevel'] == 100:
            return
        elif userInGameInfo['currentLevel'] >= 80:
            expNeeded = 262144 #2 ** 18
        elif userInGameInfo['currentLevel'] >= 50:
            expNeeded = 65536 #2 ** 16
        elif userInGameInfo['currentLevel'] >= 30:
            expNeeded = 16384 #2 ** 14
        elif userInGameInfo['currentLevel'] >= 20:
            expNeeded = 4096 #2 ** 12
        elif userInGameInfo['currentLevel'] >= 10:
            expNeeded = 1024 #2 ** 10
        else:
            expNeeded = 256 #2 ** 8

        if userInGameInfo['currentExp'] > expNeeded:
            userInGameInfo['currentLevel'] += 1
            userInGameInfo['currentExp'] -= expNeeded
        else:
            break
    #更新基础生命值
    userInGameInfo['basicHP'] = userInGameInfo['currentLevel'] * 25 + 2000
    #更新基础攻击力
    userInGameInfo['basicAttack'] = userInGameInfo['currentLevel'] * 5 + 50
    userInGameInfo.to_json('./users/' + f_user + '_inGameInfo.json', indent = 4)