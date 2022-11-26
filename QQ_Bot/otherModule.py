﻿#coding = utf-8
import random
import readModule

#当你看到这条注释的时候你就应该知道你还没写保底机制
def gacha():
    rand = random.randint(1, 100)

    #偶数出武器
    if rand % 2 == 0:
        weaponDic = readModule.readActivityWeapon()
        weaponNameList = weaponDic['weaponNameList']
        weaponAmountList = weaponDic['weaponAmountList']
        if rand > 90:
            #计算武器索引值
            index = rand % weaponAmountList[0]
        elif rand > 70:
            index = rand % weaponAmountList[1] + weaponAmountList[0]
        elif rand > 50:
            index = rand % weaponAmountList[2] + weaponAmountList[1] + weaponAmountList[0]
        else:
            index = rand % weaponAmountList[3] + weaponAmountList[2] + weaponAmountList[1] + weaponAmountList[0]
    #返回武器名和武器种类
        return [weaponNameList[index], 'weapon']
    
    #奇数出物品
    else:
        itemDic = readModule.readActivityItem()
        itemNameList = itemDic['itemNameList']
        itemAmountList = itemDic['itemAmountList']
        if rand > 90:
            index = rand % itemAmountList[0]
        elif rand > 70:
            index = rand % itemAmountList[1] + itemAmountList[0]
        elif rand > 50:
            index = rand % itemAmountList[2] + itemAmountList[1] + itemAmountList[0]
        else:
            index = rand % itemAmountList[3] + itemAmountList[2] + itemAmountList[1] + itemAmountList[0]
        return [itemNameList[index], 'item']
    

def genUserBasicInfoList(user):
    userBasicInfoDic = readModule.readUserBasicInfo(user)
    skyDustAmount = userBasicInfoDic['skyDustAmount']
    signedDays = userBasicInfoDic['signedDays']
    lastActivity = userBasicInfoDic['lastActivity']
    earthDustAmount = userBasicInfoDic['earthDustAmount']
    continuousSigned = userBasicInfoDic['continuousSigned']
    currentLevel = userBasicInfoDic['currentLevel']
    basicHP = userBasicInfoDic['basicHP']
    basicAttack = userBasicInfoDic['basicAttack']
    totalExp = userBasicInfoDic['totalExp']

    form = '当前等级：'