import qq
import pandas
import datetime

import ToolModules.other_module as other_module

async def activity(message: qq.Message):
    activity_info = pandas.read_json('./Activities/activity_info.json', typ = 'series')
    start_time = datetime.date(activity_info['startYear'], activity_info['startMonth'], activity_info['startDay'])
    end_time = datetime.date(activity_info['endYear'], activity_info['endMonth'], activity_info['endDay'])
    days_before_start = start_time.__sub__(datetime.date.today()).days
    days_before_end = end_time.__sub__(datetime.date.today()).days
    if days_before_end <= 0:
        await message.reply('当前无正在进行的活动', mention_author = message.author)
    elif days_before_start >=0:
        if days_before_start <= 2:
            await message.reply('活动' + activity_info['activityName'] + '即将在' + str(days_before_start) + '天后开启', mention_author = message.author)
        else:
            await message.reply('当前无正在进行的活动', mention_author = message.author)
    else:
        activity_weapon_form = other_module.convertToOutputForm(pandas_form = pandas.read_json('./Activities/activity_weapon_form.json', orient = 'index'), form_type = 'weapon')
        activity_item_form = other_module.convertToOutputForm(pandas_form = pandas.read_json('./Activities/activity_item_form.json', orient = 'index'), form_type = 'item')
        await message.reply('\n\n当前活动：' + activity_info['activityName'] + '\n该活动会在' + str(days_before_end) + '天后结束\n' + activity_weapon_form + '\n' + activity_item_form, mention_author = message.author)