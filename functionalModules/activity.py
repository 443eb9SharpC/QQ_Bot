import qq
import pandas
import datetime

import toolModules.otherModule as otherModule

async def activity(message: qq.Message):
    activityInfo = pandas.read_json('./activities/activityInfo.json', typ = 'series')
    startTime = datetime.date(activityInfo['startYear'], activityInfo['startMonth'], activityInfo['startDay'])
    endTime = datetime.date(activityInfo['endYear'], activityInfo['endMonth'], activityInfo['endDay'])
    daysBeforeStart = startTime.__sub__(datetime.date.today()).days
    daysBeforeEnd = endTime.__sub__(datetime.date.today()).days
    if daysBeforeEnd <= 0:
        await message.reply('当前无正在进行的活动', mention_author = message.author)
    elif daysBeforeStart >=0:
        if daysBeforeStart <= 2:
            await message.reply('活动' + activityInfo['activityName'] + '即将在' + str(daysBeforeStart) + '天后开启', mention_author = message.author)
        else:
            await message.reply('当前无正在进行的活动', mention_author = message.author)
    else:
        activityWeaponForm = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./activities/activityWeaponForm.json', orient = 'index'), f_formType = 'weapon')
        activityItemForm = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index'), f_formType = 'item')
        await message.reply('\n\n当前活动：' + activityInfo['activityName'] + '\n该活动会在' + str(daysBeforeEnd) + '天后结束\n' + activityWeaponForm + '\n' + activityItemForm, mention_author = message.author)