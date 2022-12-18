import qq
import pandas
import datetime

async def sign(message: qq.Message):
    #检测是否注册
    try:
        userBasicInfo = pandas.read_json('./users/' + str(message.author) + '_basicInfo.json', typ = 'series')
    except:
        await message.reply('签到失败，请先注册', mention_author = message.author)
        return
    #检测签到间隔时间
    currentTime = datetime.date.today().day
    if currentTime == userBasicInfo['lastActivity']:
        await message.reply('签到失败，请不要在一天之内多次签到', mention_author = message.author)
    else:
        #检测连续签到天数
        if currentTime - userBasicInfo['lastActivity'] == 1:
            userBasicInfo['continuousSigned'] += 1
            if userBasicInfo['continuousSigned'] > 3:
                #连续签到3天后,每天额外获得5个天空之尘
                userBasicInfo['skyDustAmount'] += (userBasicInfo['continuousSigned'] - 3) % 30 * 5
        else:
            #重置连续签到
            userBasicInfo['continuousSigned'] = 1
        userBasicInfo['signedDays'] += 1
        userBasicInfo['skyDustAmount'] += 10
        userBasicInfo['lastActivity'] = currentTime
        userBasicInfo.to_json('./users/' + str(message.author) + '_basicInfo.json', indent = 4, orient = 'index')
        if userBasicInfo['continuousSigned'] > 3:
            await message.reply('你目前有' + str(userBasicInfo['skyDustAmount']) + '个天空之尘，已累计签到' + str(userBasicInfo['signedDays']) + '天，已连续签到' + str(userBasicInfo['continuousSigned']) + '天，额外获得' + str((userBasicInfo['continuousSigned'] - 3) % 30 * 5) + '个天空之尘', mention_author = message.author)
        else:
            await message.reply('你目前有' + str(userBasicInfo['skyDustAmount']) + '个天空之尘，已累计签到' + str(userBasicInfo['signedDays']) + '天，已连续签到' + str(userBasicInfo['continuousSigned']) + '天', mention_author = message.author)