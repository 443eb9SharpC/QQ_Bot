#coding = utf-8
import random
import pandas

def gacha():
    rand = random.randint(1, 3)
    #1/3出武器
    if rand == 1:
        activityWeaponForm = pandas.read_json('./activities/activityWeaponForm.json', orient = 'index')
        weapon = activityWeaponForm.sample(n = 1, weights = 'weaponRarityRaw', ignore_index = True)
        return weapon
    
    #2/3出物品
    else:
        activityItemForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index')
        item = activityItemForm.sample(n = 1, weights = 'itemRarityRaw', ignore_index = True)
        return item
    

def genUserBasicInfoList(f_user):
    try:
        userBasicInfoDic = pandas.read_json('./users/' + f_user + '_basicInfo.json', typ = 'series')
    except Exception:
        return '未找到用户，请先注册'
    skyDustAmount = userBasicInfoDic['skyDustAmount']
    signedDays = userBasicInfoDic['signedDays']
    earthDustAmount = userBasicInfoDic['earthDustAmount']
    continuousSigned = userBasicInfoDic['continuousSigned']

    form = '\n天空之尘数量：' + str(skyDustAmount) + '\n累计签到：' + str(signedDays) + '\n连续签到：' + str(continuousSigned) + '\n大地之烬：' + str(earthDustAmount)
    return form


def convertToOutputForm(f_pandasForm: pandas.DataFrame, f_formType):
    match f_formType:
        case 'weapon':
            result = '\n武器名 | 攻击力 | 稀有度'
            if f_pandasForm.empty == True:
                result += '\n无武器'
            else:
                for index, row in f_pandasForm.iterrows():
                    result += '\n' + row['weaponName'] + ' | ' + str(row['weaponAttack']) + ' | ' + row['weaponRarity']
        case 'item':
            result = '\n物品名 | 数量 |稀有度'
            if f_pandasForm.empty == True:
                result += '\n无物品'
            else:
                for index, row in f_pandasForm.iterrows():
                    result += '\n' + row['itemName'] + ' | ' + str(row['itemAmount']) + ' | ' + row['itemRarity']
    return result


def updateUserLevel(f_user):
    userInGameInfo = pandas.read_json('./users/' + f_user + '_inGameInfo.json', typ = 'series')
    while True:
        if userInGameInfo['currentLevel'] == 100:
            return
        elif userInGameInfo['currentLevel'] >= 80:
            expNeeded = 1048576 #2 ** 20
        elif userInGameInfo['currentLevel'] >= 50:
            expNeeded = 524288 #2 ** 19
        elif userInGameInfo['currentLevel'] >= 30:
            expNeeded = 131072 #2 ** 17
        elif userInGameInfo['currentLevel'] >= 20:
            expNeeded = 65536 #2 ** 16
        elif userInGameInfo['currentLevel'] >= 10:
            expNeeded = 4096 #2 ** 12
        else:
            expNeeded = 512 #2 ** 9
        if userInGameInfo['currentExp'] > expNeeded:
            userInGameInfo['currentLevel'] += 1
        else:
            break
    userInGameInfo.to_json('./users/' + f_user + '_inGameInfo.json', indent = 4)