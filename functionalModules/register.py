import qq
import pandas

async def register(message: qq.Message):
    #尝试增加文件
    user = str(message.author)
    try:
        userBasicInfo = open('./users/' + user + '.isregistered', mode = 'x', encoding = 'utf8')
    except:
        await message.reply('注册失败，请不要重复注册', mention_author=message.author)
        return
    #文件初始化
    userBasicInfo.close()
    userBasicInfo = pandas.Series(index = ['skyDustAmount', 'signedDays', 'lastActivity', 'earthDustAmount', 'continuousSigned'], data = [0, 0, 0, 0, 0])
    userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)
    userBasicInfo = pandas.DataFrame(data = [[0, 0, 0], [20, 'Special', -1]], columns = ['weaponAttack', 'weaponRarity', 'weaponRarityRaw'], index = [0, '新手剑'])
    userBasicInfo.to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
    userBasicInfo = pandas.DataFrame(data = [[0, 0, 0], [1, 'Common', 0.4]], columns = ['itemAmount', 'itemRarity', 'itemRarityRaw'], index = [0, '生命药水'])
    userBasicInfo.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
    userBasicInfo = pandas.Series(index = ['currentLevel', 'basicHP', 'basicAttack', 'currentExp'], data = [0, 2000, 200, 0])
    userBasicInfo.to_json('./users/' + user + '_inGameInfo.json', indent = 4)
    await message.reply('注册成功，如果你不知道如何使用这个机器人，你可以输入 /菜单', mention_author = message.author)