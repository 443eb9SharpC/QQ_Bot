import qq
import pandas
import datetime

import ToolModules.other_module as other_module

async def Activity(message: qq.Message):
    activity_info = pandas.read_json('./Activities/activity_info.json', typ = 'series')
    start_time = datetime.date(activity_info['start_year'], activity_info['start_month'], activity_info['start_day'])
    end_time = datetime.date(activity_info['end_year'], activity_info['end_month'], activity_info['end_day'])
    days_before_start = start_time.__sub__(datetime.date.today()).days
    days_before_end = end_time.__sub__(datetime.date.today()).days
    if days_before_end < 0:
        await message.reply('当前无正在进行的活动', mention_author = message.author)
        return
    elif days_before_start > 0:
        if days_before_start < 5:
            await message.reply('活动' + activity_info['activityName'] + '即将在' + str(days_before_start) + '天后开启', mention_author = message.author)
        else:
            await message.reply('当前无正在进行的活动', mention_author = message.author)
        return
    else:
        activity_weapon_form = other_module.ConvertToOutputForm(pandas_form = pandas.read_json('./Activities/activity_weapon_form.json', orient = 'index'), form_type = 'weapon')
        activity_item_form = other_module.ConvertToOutputForm(pandas_form = pandas.read_json('./Activities/activity_item_form.json', orient = 'index'), form_type = 'item')
        await message.reply('\n\n当前活动：' + activity_info['activityName'] + '\n该活动会在' + str(days_before_end) + '天后结束\n' + activity_weapon_form + '\n' + activity_item_form, mention_author = message.author)