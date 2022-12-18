import qq
import pandas
import datetime

import toolModules.otherModule as otherModule

async def gachaOnce(message: qq.Message):
    activityInfo = pandas.read_json('./activities/activityInfo.json', typ = 'series')
    endTime = datetime.date(activityInfo['endYear'], activityInfo['endMonth'], activityInfo['endDay'])
    daysRemain = endTime.__sub__(datetime.date.today()).days
    if daysRemain <= 0:
        await message.reply('当前无正在进行的活动', mention_author = message.author)
        return
    user = str(message.author)
    try:
        userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
    except:
        await message.reply('抽卡失败，请先注册', mention_author = message.author)
        return
    if userBasicInfo['skyDustAmount'] < 100:
        await message.reply('天空之尘不足', mention_author = message.author)
        return
    userBasicInfo['skyDustAmount'] -= 100
    result = otherModule.gacha()
    #判断抽到的东西的类型
    #武器
    if 'weaponName' in result.columns:
        #判断是否重复
        userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
        if result.index[0] in userWeaponForm.index:
            await message.reply('重复获得' + result.index[0] + '，已转化为25大地之烬', mention_author = message.author)
            userBasicInfo['earthDustAmount'] += 25
        else:
            await message.reply('获得了' + result.index[0], mention_author = message.author)
            pandas.concat(objs = [userWeaponForm, result]).to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
    #物品
    else:
        #判断是否是天空之尘
        if '天空之尘' in result.index[0]:
            await message.reply('获得了' + str(result.iat[0, 0]) + '个天空之尘', mention_author = message.author)
            userBasicInfo['skyDustAmount'] += result.iat[0, 0]
        else:
            userItemForm = pandas.read_json('./users/' + user + '_basicInfo.json', orient = 'index')
            await message.reply('获得了' + str(result.iat[0, 0]) + '个' + result.index[0], mention_author = message.author)
            #判断是否重复
            if result.index[0] in userItemForm['itemName']:
                userItemForm.at[result.index[0], 'itemAmount'] += result.iat[0, 0]
            else:
                pandas.concat(objs = [userItemForm, result]).to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
    #保存基础数据
    userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)