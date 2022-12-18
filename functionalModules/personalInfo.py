import qq
import pandas

async def personalInfo(message: qq.Message):
    user = str(message.author)
    try:
        userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
        userInGameInfo = pandas.read_json('./users/' + user + '_inGameInfo.json', typ = 'series')
    except:
        await message.reply('获取失败，请先注册', mention_author = message.author)
        return
    form = '\n天空之尘数量：' + str(userBasicInfo['skyDustAmount']) + ' | 大地之烬：' + str(userBasicInfo['earthDustAmount']) + ' | 累计签到：' + str(userBasicInfo['signedDays']) + ' | 连续签到：' + str(userBasicInfo['continuousSigned'])
    form += '\n当前等级：' + str(userInGameInfo['currentLevel']) + ' | 当前经验值：' + str(userInGameInfo['currentExp']) + ' | 基础生命值：' + str(userInGameInfo['basicHP']) + ' | 基础攻击力：' + str(userInGameInfo['basicAttack'])
    await message.reply(form, mention_author = message.author)