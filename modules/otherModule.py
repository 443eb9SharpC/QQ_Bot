#coding = utf-8
import random
import pandas

import modules.readModule as readModule

#当你看到这条注释的时候你就应该知道你还没写保底机制
def gacha():
    rand = random.randint(1, 100)
    #偶数出武器
    if rand % 2 == 0:
        activityWeaponForm = pandas.read_json('./activities/activityWeaponForm.json', orient = 'index')
        weapon = activityWeaponForm.sample(n = 1, weights = 'weaponRarityRaw', random_state = 1)
        return pandas.Series(weapon.values[0], index = weapon.columns)
    
    #奇数出物品
    else:
        activityItemForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index')
        item = activityItemForm.sample(n = 1, weights = 'itemRarityRaw', random_state = 1)
        return pandas.Series(item.values[0], index = item.columns)
    

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
            res = '\n武器名 | 攻击力 | 稀有度'
            for index, row in f_pandasForm.iterrows():
                res += '\n' + row['weaponName'] + ' | ' + str(row['weaponAttack']) + ' | ' + row['weaponRarity']
        case 'item':
            res = '\n物品名 | 数量 |稀有度'
            for index, row in f_pandasForm.iterrows():
                res += '\n' + row['itemName'] + ' | ' + str(row['itemAmount']) + ' | ' + row['itemRarity']
    return res