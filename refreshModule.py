#coding = utf-8
import readModule

def refreshBasicInfo(user, skyDustAmount, signedDays, lastActivity, earthDustAmount, continuousSigned):
    #重新写入信息
    userInfoFile = open('./users/' + user +'_basicInfo.csv', mode = 'w', encoding = 'utf8')
    userInfoFile.write(str(skyDustAmount) + ',' + str(signedDays) + ',' + str(lastActivity) + ',' + str(earthDustAmount) + ',' + str(continuousSigned))
    userInfoFile.close()
    

def refreshInGameInfo(user, currentLevel, basicHP, basicAttack, totalExp):
    inGameInfoFile = open('./users/' + user + '_inGameInfo.csv', mode = 'w', encoding = 'utf8')
    inGameInfoFile.write(str(currentLevel) + ',' + str(basicHP) + ',' + str(basicAttack) + ',' + str(totalExp))


def refreshWeaponList(user, weaponInfoList):
    userWeaponFile = open('./users/' + user + '_weaponList.csv', mode = 'a', encoding = 'utf8')
    userWeaponFile.write(str(weaponInfoList[0]) + ',' + str(weaponInfoList[1]) + ',' + str(weaponInfoList[2]) + ',')
    userWeaponFile.close()


def refreshItemList(user, itemInfoList):
    userItemFile = open('./users/' + user +'_itemList.csv', mode = 'a', encoding = 'utf8')
    userItemFile.write(str(itemInfoList[0]) + ',' + str(itemInfoList[1]) + ',' + str(itemInfoList[2]) + ',')
    userItemFile.close()


def refreshLevel(user):
    userBasicInfoDic = readModule.readUserBasicInfo(user)
    #获取用户经验和等级
    totalExp = userBasicInfoDic['totalExp']
    currentLevel = userBasicInfoDic['currentLevel']
    #获取理论等级
    for i in range(0, 100):
        #0-1需16经验
        if currentLevel == 0:
            if totalExp >= 16:
                currentLevel += 1
        #之后 n级-n+1级 需要 2∧(n+4) 经验
        if 2 ** (i + 3) <= totalExp < 2 ** (i + 4):
            #更新等级
            currentLevel = i
            break
    basicHP = 2000 + currentLevel * 200
    basicAttack = 50 + currentLevel * 10
    refreshBasicInfo(user, userBasicInfoDic['skyDustAmount'], userBasicInfoDic['signedDays'], userBasicInfoDic['lastActivity'], userBasicInfoDic['earthDustAmount'], userBasicInfoDic['countinuousSigned'], currentLevel, basicHP, basicAttack, userBasicInfoDic['totalExp'])