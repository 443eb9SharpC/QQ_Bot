import qq
import pandas
import datetime

import ToolModules.other_module as other_module

async def GachaOnce(message: qq.Message):
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
    user = str(message.author)
    try:
        user_basic_info = pandas.read_json('./Users/' + user + '_basic_info.json', typ = 'series')
    except:
        await message.reply('抽卡失败，请先注册', mention_author = message.author)
        return
    if user_basic_info['sky_dust_amount'] < 100:
        await message.reply('天空之尘不足', mention_author = message.author)
        return
    user_basic_info['sky_dust_amount'] -= 100
    result = other_module.Gacha()
    #判断抽到的东西的类型
    #武器
    if 'weaponName' in result.columns:
        #判断是否重复
        user_weapon_form = pandas.read_json('./Users/' + user + '_weapon_form.json', orient = 'index')
        if result.index[0] in user_weapon_form.index:
            await message.reply('重复获得' + result.index[0] + '，已转化为25大地之烬', mention_author = message.author)
            user_basic_info['earth_dust_amount'] += 25
        else:
            await message.reply('获得了' + result.index[0], mention_author = message.author)
            pandas.concat(objs = [user_weapon_form, result]).to_json('./Users/' + user + '_weapon_form.json', indent = 4, orient = 'index')
    #物品
    else:
        #判断是否是天空之尘
        if '天空之尘' in result.index[0]:
            await message.reply('获得了' + str(result.iat[0, 0]) + '个天空之尘', mention_author = message.author)
            user_basic_info['sky_dust_amount'] += result.iat[0, 0]
        else:
            user_item_form = pandas.read_json('./Users/' + user + '_basic_info.json', orient = 'index')
            await message.reply('获得了' + str(result.iat[0, 0]) + '个' + result.index[0], mention_author = message.author)
            #判断是否重复
            if result.index[0] in user_item_form['item_name']:
                user_item_form.at[result.index[0], 'item_amount'] += result.iat[0, 0]
            else:
                pandas.concat(objs = [user_item_form, result]).to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
    #保存基础数据
    user_basic_info.to_json('./Users/' + user + '_basic_info.json', indent = 4)