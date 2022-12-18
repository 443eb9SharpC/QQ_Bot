import qq
import pandas
import datetime

import toolModules.otherModule as otherModule

async def gachaTenTimes(message: qq.Message):
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
    if userBasicInfo['skyDustAmount'] < 1000:
        await message.reply('天空之尘不足', mention_author = message.author)
        return
    userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
    userItemForm = pandas.read_json('./users/' + user + '_basicInfo.json', orient = 'index')
    outputWeaponForm = pandas.DataFrame(columns = ['weaponAttack', 'weaponRarity', 'weaponRarityRaw'])
    outputItemForm = pandas.DataFrame(columns = ['itemAmount', 'itemRarity', 'itemRarityRaw'])
    outputEarthDustAmount = 0
    outputSkyDustAmount = 0
    finalOutputForm = ''
    userBasicInfo['skyDustAmount'] -= 1000
    for i in range(10):
        result = otherModule.gacha()
        #判断抽到的东西的类型
        #武器
        if 'weaponAttack' in result.columns:
            #判断是否重复
            if result.index[0] in userWeaponForm.index:
                result.rename(index = {result.index[0]: result.index[0] + '（重复）'}, inplace = True)
                outputWeaponForm = pandas.concat(objs = [outputWeaponForm, result])
                outputEarthDustAmount += 25
                userBasicInfo['earthDustAmount'] += 25
            else:
                outputWeaponForm = pandas.concat(objs = [outputWeaponForm, result])
                userWeaponForm = pandas.concat(objs = [userWeaponForm, result])
        #物品
        else:
            #判断是否是天空之尘
            if '天空之尘' in result.index[0]:
                outputSkyDustAmount += int(result.iat[0, 0])
                userBasicInfo['skyDustAmount'] += result.iat[0, 0]
            else:
                #判断是否重复
                if result.index[0] in userItemForm.index:
                    userItemForm.at[result.index[0], 0] += result.iat[0, 0]
                else:
                    userItemForm = pandas.concat(objs = [userItemForm, result])
                #判断是否与最终的输出表格重复
                if result.index[0] in outputItemForm.index:
                    outputItemForm.at[result.index[0], 'itemAmount'] += result.iat[0, 0]
                else:
                    outputItemForm = pandas.concat(objs = [outputItemForm, result])
    #保存数据
    userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)
    userWeaponForm.to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
    userItemForm.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
    #处理表格数据
    finalOutputForm += otherModule.convertToOutputForm(f_pandasForm = outputWeaponForm, f_formType = 'weapon')
    finalOutputForm += '\n'
    finalOutputForm += otherModule.convertToOutputForm(f_pandasForm = outputItemForm, f_formType = 'item')
    finalOutputForm += '\n\n总计获得' + str(outputSkyDustAmount) + '个天空之尘及' + str(outputEarthDustAmount) + '个大地之烬'
    await message.reply(finalOutputForm, mention_author = message.author)