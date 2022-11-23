#coding = utf-8
import random

def readUserBasicInfo(user):
    #检查是否注册
    try:
        userInfo = open('./users/' + user + '_basicInfo.csv', mode = 'r', encoding = 'utf8')
    except IOError:
        return 'Error'
    info = userInfo.read()
    infoList = info.split(',')
    userInfo.close()

    userBasicInfoDic = {}
    userBasicInfoDic['skyDustAmount'] = str(infoList[0])
    userBasicInfoDic['signedDays'] = str(infoList[1])
    userBasicInfoDic['lastActivity'] = str(infoList[2])
    userBasicInfoDic['earthDustAmount'] = str(infoList[3])

    return userBasicInfoDic

def readUserWeaponList(user):
    #检查是否注册
    try:
        weaponFile = open('./users/' + user + '_weaponList.csv', mode = 'r', encoding = 'utf8')
    except IOError:
        return 'Error'
    weaponListRaw = weaponFile.read()
    weaponList = weaponListRaw.split(',')
    weaponFile.close()

    userItemDic = {}
    i = 0

    #读取武器列表
    while weaponList[i] != 'EOF':
        weaponName = weaponList[i]
        weaponAttack = weaponList[i + 1]
        weaponRarityRaw = int(weaponList[i + 2])

        #稀有度判断
        if weaponRarityRaw > 90:
            weaponRarity = 'Lengendary'
        elif weaponRarityRaw > 70:
            weaponRarity = 'Epic'
        elif weaponRarityRaw > 50:
            weaponRarity = 'Rare'
        else:
            weaponRarity = 'Common'
        
        userItemDic[weaponName] = [weaponName, weaponAttack, weaponRarityRaw, weaponRarity]
        i += 3

    return userItemDic


def readUserItemList(user):
    try:
        itemFile = open('./users/' + user + '_itemList.csv', mode = 'r', encoding = 'utf8')
    except IOError:
        return 'Error'
    itemListRaw = itemFile.read()
    itemList = itemListRaw.split(',')
    itemFile.close()

    userItemDic = {}
    i = 0

    while itemList[i] != 'EOF':
        itemName = itemList[i]
        itemAmount = itemList[i + 1]
        itemRarityRaw = int(itemList[i + 2])

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


def refreshBasicInfo(user, skyDust, signedDays, lastActivity, earthDust):
    #重新写入信息
    userInfoFile = open('./users/' + user +'_basicInfo.csv', mode = 'w', encoding = 'utf8')
    userInfoFile.write(str(skyDust) + ',' + str(signedDays) + ',' + str(lastActivity) + ',' + str(earthDust) + ',EOF')
    userInfoFile.close()


def refreshWeaponList(user, weaponInfoList):
    userWeaponFile = open('./users/' + user + '_weaponList.csv', mode = 'a', encoding = 'utf8')
    userWeaponFile.write(str(weaponInfoList[0]) + ',' + str(weaponInfoList[1]) + ',' + str(weaponInfoList[2]) + ',' + str(weaponInfoList[3]) + ',')
    userWeaponFile.close()


def refreshItemList(user, itemInfoList):
    userItemFile = open('./users/' + user +'_itemList.csv', mode = 'a', encoding = 'utf8')
    userItemFile.write(str(itemInfoList[0]) + ',' + str(itemInfoList[1]) + ',' + str(itemInfoList[2]) + ',' + str(itemInfoList[3]) + ',')
    userItemFile.close()


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
        activityWeaponDic[weaponName] = [weaponName, weaponAttack, weaponRarityRaw, weaponRarity, weaponNameString]
        i += 3

    #此列表用于抽卡时计算索引
    weaponAmountList = [legendaryAmount, epicAmount, rareAmount, commonAmount]

    activityWeaponDic['weaponNameList'] = weaponNameList
    activityWeaponDic['weaponAmountList'] = weaponAmountList
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
        activityItemDic[itemName] = [itemName, itemAmount, itemRarityRaw, itemRarity, itemNameString]
        i += 3

    itemAmountList = [legendaryAmount, epicAmount, rareAmount, commonAmount]

    activityItemDic['itemAmountList'] = itemAmountList
    activityItemDic['itemNameList'] = itemNameList
    return activityItemDic


#当你看到这条注释的时候你就应该知道你还没写保底机制
def gacha():
    activityName = readActivityInfo()['activityName']
    rand = random.randint(1, 100)

    #偶数出武器
    if rand % 2 == 0:
        weaponDic = readActivityWeapon()
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
        itemDic = readActivityItem()
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