#coding = utf-8
import random
from os import remove

def readUserBasicInfo(user):
    try:
        userInfo = open('./users/' + user + '_basicInfo.csv', mode = 'r')
    except IOError:
        return 'Error'
    info = userInfo.read()
    infoList = info.split(',')
    userInfo.close()

    userBasicInfoDic = {}
    userBasicInfoDic['skyDustCount'] = str(infoList[0])
    userBasicInfoDic['signedDays'] = str(infoList[1])
    userBasicInfoDic['lastActivity'] = str(infoList[2])

    return userBasicInfoDic

def readUserWeaponList(user):
    try:
        weaponListRaw = open('./users/' + user + '_weaponList.csv', mode = 'r')
    except IOError:
        return 'Error'
    weaponListRaw = weaponListRaw.read()
    weaponList = weaponListRaw.split(',')
    weaponListRaw.close()
    weaponList.append["EOF"]
    i = 0

    while weaponList[i] != 'EOF':
        weaponName = weaponList[i]
        weaponAttack = weaponList[i + 1]
        weaponRarityRaw = weaponList[i + 2]

        if weaponRarityRaw > 90:
            weaponRarity = 'Lengendary'
        elif weaponRarityRaw > 70:
            weaponRarity = 'Epic'
        elif weaponRarityRaw > 50:
            weaponRarity = 'Rare'
        else:
            weaponRarity = 'Common'
        
        i += 3

    userItemDic = {}
    userItemDic['weaponName'] = weaponName
    userItemDic['weaponAttack'] = weaponAttack
    userItemDic['weaponRarityRaw'] = weaponRarityRaw
    userItemDic['weaponRarity'] = weaponRarity

    return userItemDic


def readUserItemList(user):
    try:
        itemListRaw = open('./users/' + user + '_itemList.csv', mode = 'r')
    except IOError:
        return 'Error'
    itemListRaw = itemListRaw.read()
    itemList = itemListRaw.split(',')
    itemListRaw.close()
    itemList.append["EOF"]
    i = 0

    while itemList[i] != 'EOF':
        itemName = itemList[i]
        itemCount = itemList[i + 1]
        itemRarityRaw = itemList[i + 2]

        if itemRarityRaw > 90:
            itemRarity = 'Lengendary'
        elif itemRarityRaw > 70:
            itemRarity = 'Epic'
        elif itemRarityRaw > 50:
            itemRarity = 'Rare'
        else:
            itemRarity = 'Common'
        
        i += 3

    userItemDic = {}
    userItemDic['itemName'] = itemName
    userItemDic['itemCount'] = itemCount
    userItemDic['itemRarityRaw'] = itemRarityRaw
    userItemDic['itemRarity'] = itemRarity

    return userItemDic


def refresh_basicInfo(user, skyDust, signedDays, lastActivity):
    try:
        remove('./users/' + user + '_basicInfo.csv')
    except IOError:
        return 'Error'
    userInfo = open('./users/' + user +'_basicInfo.csv', mode = 'w')
    userInfo.write(str(skyDust) + ',' + str(signedDays) + ',' + str(lastActivity))
    userInfo.close()


def refresh_itemList(user, itemList):
    if itemList[0][:5] == '天空之尘':
        userInfo = readUserBasicInfo(user)
        skyDust = int(userInfo[0]) + int(itemList[1])
        refresh_basicInfo(user, skyDust, int(userInfo[1]), int(userInfo[2]))
        return
    else:
        user_item = open('./users/' + user +'_itemList.csv', mode = 'a')
        user_item.write(itemList[0] + ',' + itemList[1] + ',' + itemList[2] + ',' + itemList[3] + ',')


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
    i = 0

    while activityWeaponList[i + 3] != 'EOF':
        weaponName = activityWeaponList[i]
        weaponAttack = activityWeaponList[i + 1]
        weaponRarityRaw = int(activityWeaponList[i + 2])

        if weaponRarityRaw > 90:
            weaponRarity = 'Lengendary'
        elif weaponRarityRaw > 70:
            weaponRarity = 'Epic'
        elif weaponRarityRaw > 50:
            weaponRarity = 'Rare'
        else:
            weaponRarity = 'Common'

        weaponNameString += weaponName + ' | ' + weaponAttack + ' | ' + weaponRarity + '\n'

        activityWeaponDic['weaponName'] = weaponName
        activityWeaponDic['weaponAttack'] = weaponAttack
        activityWeaponDic['weaponRarityRaw'] = weaponRarityRaw
        activityWeaponDic['weaponRarity'] = weaponRarity
        activityWeaponDic['weaponNameString'] = weaponNameString

        i += 3

    return activityWeaponDic


def readActivityItem():
    activityItem = open('./activities/activityItem.csv', mode = 'r', encoding = 'utf8')
    activityItemRaw = activityItem.read()
    activityItemList = activityItemRaw.split(',')

    #初始化数据
    activityItemDic = {}
    itemNameString = ''
    i = 0

    while activityItemList[i + 3] != 'EOF':
        itemName = activityItemList[i] + str(activityItemList[i + 1])
        itemCount = activityItemList[i + 1]
        itemRarityRaw = int(activityItemList[i + 2])

        if itemRarityRaw > 90:
            itemRarity = 'Lengendary'
        elif itemRarityRaw > 70:
            itemRarity = 'Epic'
        elif itemRarityRaw > 50:
            itemRarity = 'Rare'
        else:
            itemRarity = 'Common'

        itemNameString += itemName + ' | ' + itemCount + ' | ' + itemRarity + '\n'

        activityItemDic['itemName'] = itemName
        activityItemDic['itemCount'] = itemCount
        activityItemDic['itemRarityRaw'] = itemRarityRaw
        activityItemDic['itemRarity'] = itemRarity
        activityItemDic['itemNameString'] = itemNameString

        i += 3

    return activityItemDic


def gacha():
    activityList = read_activity()
    rand = random.randint(1, 1000)
    if rand % 3 > 0:
        weaponList = activityList['weaponList']
        weaponDic = activityList['weaponDic']
        weaponCount = activityList['weaponCount']
        if rand / 10 > 90:
            randSec = random.randint(1, 100) % weaponCount[0]
            weaponName = weaponList[randSec]
            return weaponDic[weaponName]
        elif rand /10 > 70:
            randSec = random.randint(1, 100) % weaponCount[1]
            weaponName = weaponList[randSec + weaponCount[0]]
            return weaponDic[weaponName]
        elif rand /10 > 50:
            randSec = random.randint(1, 100) % weaponCount[2]
            weaponName = weaponList[randSec + weaponCount[0] + weaponCount[1]]
            return weaponDic[weaponName]
        else:
            randSec = random.randint(1, 100) % weaponCount[3]
            weaponName = weaponList[randSec + weaponCount[0] + weaponCount[1] + weaponCount[2]]
            return weaponDic[weaponName]
    else:
        itemList = activityList['itemList']
        itemDic = activityList['itemDic']
        itemCount = activityList['itemCount']
        if rand / 10 > 90:
            randSec = rand % itemCount[0]
            itemName = itemList[randSec]
            return itemDic[itemName + '95']
        elif rand /10 > 70:
            randSec = random.randint(1, 100) % itemCount[1]
            itemName = itemList[randSec + itemCount[0]]
            return itemDic[itemName + '85']
        elif rand /10 > 50:
            randSec = random.randint(1, 100) % itemCount[2]
            itemName = itemList[randSec + itemCount[0] + itemCount[1]]
            return itemDic[itemName + '55']
        else:
            randSec = random.randint(1, 100) % itemCount[3]
            itemName = itemList[randSec + itemCount[0] + itemCount[1] + itemCount[2]]
            return itemDic[itemName + '5']