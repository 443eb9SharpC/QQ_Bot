#coding = utf-8
import pandas

def readUserBasicInfo(user):
    #检查是否注册
    try:
        userBasicInfoFile = open('./users/' + user + '_basicInfo.csv', mode = 'r', encoding = 'utf8')
    except IOError:
        return 'Error'
    info = userBasicInfoFile.read()
    infoList = info.split(',')
    userBasicInfoFile.close()

    userBasicInfoDic = {}
    userBasicInfoDic['skyDustAmount'] = int(infoList[0])
    userBasicInfoDic['signedDays'] = int(infoList[1])
    userBasicInfoDic['lastActivity'] = int(infoList[2])
    userBasicInfoDic['earthDustAmount'] = int(infoList[3])
    userBasicInfoDic['continuousSigned'] = int(infoList[4])

    return userBasicInfoDic


def readInGameInfo(user):
    try:
        inGameInfoFile = open('./users/' + user + '_inGameInfo.csv', mode = 'r', encoding = 'utf8')
    except IOError:
        return 'Error'
    inGameInfoListRaw = inGameInfoFile.read()
    inGameInfoList = inGameInfoListRaw.split(',')
    inGameInfoFile.close()

    inGameInfoDic = {}
    inGameInfoDic['currentLevel'] = int(inGameInfoList[0])
    inGameInfoDic['basicHP'] = int(inGameInfoList[1])
    inGameInfoDic['basicAttack'] = int(inGameInfoList[2])
    inGameInfoDic['totalExp'] = int(inGameInfoList[3])

    return inGameInfoDic


def readUserItemList(user):
    try:
        itemFile = open('./users/' + user + '_itemList.csv', mode = 'r', encoding = 'utf8')
    except IOError:
        return 'Error'
    itemListRaw = itemFile.read()
    itemList = itemListRaw.split(',')
    itemList.pop()
    itemFile.close()

    userItemDic = {}
    i = 0

    while True:
        try:
            itemName = itemList[i]
            itemAmount = itemList[i + 1]
            itemRarityRaw = int(itemList[i + 2])
        except IndexError:
            break

        if itemRarityRaw > 90:
            itemRarity = 'Lengendary'
        elif itemRarityRaw > 70:
            itemRarity = 'Epic'
        elif itemRarityRaw > 50:
            itemRarity = 'Rare'
        else:
            itemRarity = 'Common'

        userItemDic[itemName] = [itemName, itemAmount, itemRarityRaw, itemRarity]
        i += 3

    return userItemDic


def readActivityInfo():
    activityInfo = open('./activities/activityInfo.csv', mode = 'r', encoding = 'utf8')
    activityInfoRaw = activityInfo.read()
    activityInfoList = activityInfoRaw.split(',')
    
    #初始化数据
    activityInfoDic = {}

    activityInfoDic['activityName'] = activityInfoList[0]
    activityInfoDic['daysRemain'] = activityInfoList[1]

    return activityInfoDic


def readActivityWeapon():
    activityWeapon = open('./activities/activityWeapon.csv', mode = 'r', encoding = 'utf8')
    activityWeaponRaw = activityWeapon.read()
    activityWeaponList = activityWeaponRaw.split(',')

    #初始化数据
    activityWeaponDic = {}
    weaponNameString = ''
    weaponNameList = []
    i = 0

    legendaryAmount = 0
    epicAmount = 0
    rareAmount = 0
    commonAmount = 0

    while True:
        #判断是否已经遍历完
        try:
            weaponName = activityWeaponList[i]
        except IndexError:
            break
        weaponAttack = activityWeaponList[i + 1]
        weaponRarityRaw = int(activityWeaponList[i + 2])

        if weaponRarityRaw > 90:
            weaponRarity = 'Lengendary'
            legendaryAmount += 1
        elif weaponRarityRaw > 70:
            weaponRarity = 'Epic'
            epicAmount += 1
        elif weaponRarityRaw > 50:
            weaponRarity = 'Rare'
            rareAmount += 1
        elif weaponRarityRaw > 0:
            weaponRarity = 'Common'
            commonAmount += 1

        #此列表用于抽卡检索武器
        weaponNameList.append(weaponName)
        #用于返回列表
        weaponNameString += weaponName + ' | ' + weaponAttack + ' | ' + weaponRarity + '\n'
        activityWeaponDic[weaponName] = [weaponName, weaponAttack, weaponRarityRaw, weaponRarity]
        i += 3

    #此列表用于抽卡时计算索引
    weaponAmountList = [legendaryAmount, epicAmount, rareAmount, commonAmount]

    activityWeaponDic['weaponNameList'] = weaponNameList
    activityWeaponDic['weaponAmountList'] = weaponAmountList
    activityWeaponDic['weaponNameString'] = weaponNameString
    return activityWeaponDic


def readActivityItem():
    activityItem = open('./activities/activityItem.csv', mode = 'r', encoding = 'utf8')
    activityItemRaw = activityItem.read()
    activityItemList = activityItemRaw.split(',')

    activityItemDic = {}
    itemNameString = ''
    itemNameList = []
    i = 0

    legendaryAmount = 0
    epicAmount = 0
    rareAmount = 0
    commonAmount = 0

    while True:
        try:
            itemName = activityItemList[i] + str(activityItemList[i + 1])
        except IndexError:
            break
        itemAmount = activityItemList[i + 1]
        itemRarityRaw = int(activityItemList[i + 2])

        if itemRarityRaw > 90:
            itemRarity = 'Lengendary'
            legendaryAmount += 1
        elif itemRarityRaw > 70:
            itemRarity = 'Epic'
            epicAmount += 1
        elif itemRarityRaw > 50:
            itemRarity = 'Rare'
            rareAmount += 1
        elif itemRarityRaw > 0:
            itemRarity = 'Common'
            commonAmount += 1

        itemNameList.append(itemName)
        itemNameString += itemName + ' | ' + itemAmount + ' | ' + itemRarity + '\n'
        activityItemDic[itemName] = [itemName, itemAmount, itemRarityRaw, itemRarity]
        i += 3

    itemAmountList = [legendaryAmount, epicAmount, rareAmount, commonAmount]

    activityItemDic['itemAmountList'] = itemAmountList
    activityItemDic['itemNameList'] = itemNameList
    activityItemDic['itemNameString'] = itemNameString
    return activityItemDic