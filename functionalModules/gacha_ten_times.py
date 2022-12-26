import qq
import pandas
import datetime

import ToolModules.other_module as other_module

async def GachaTenTimes(message: qq.Message):
    activity_info = pandas.read_json('./Activities/activity_info.json', typ = 'series')
    start_time = datetime.date(activity_info['startYear'], activity_info['startMonth'], activity_info['startDay'])
    end_time = datetime.date(activity_info['endYear'], activity_info['endMonth'], activity_info['endDay'])
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
    if user_basic_info['sky_dust_amount'] < 1000:
        await message.reply('天空之尘不足', mention_author = message.author)
        return
    user_weapon_form = pandas.read_json('./Users/' + user + '_weapon_form.json', orient = 'index')
    user_item_form = pandas.read_json('./Users/' + user + '_basic_info.json', orient = 'index')
    output_weapon_form = pandas.DataFrame(columns = ['weapon_attack', 'weapon_rarity', 'weapon_rarity_raw'])
    output_item_form = pandas.DataFrame(columns = ['item_amount', 'item_rarity', 'item_rarity_raw'])
    output_earth_dust_amount = 0
    output_sky_dust_amount = 0
    final_output_form = ''
    user_basic_info['sky_dust_amount'] -= 1000
    for i in range(10):
        result = other_module.Gacha()
        #判断抽到的东西的类型
        #武器
        if 'weapon_attack' in result.columns:
            #判断是否重复
            if result.index[0] in user_weapon_form.index:
                result.rename(index = {result.index[0]: result.index[0] + '（重复）'}, inplace = True)
                output_weapon_form = pandas.concat(objs = [output_weapon_form, result])
                output_earth_dust_amount += 25
                user_basic_info['earth_dust_amount'] += 25
            else:
                output_weapon_form = pandas.concat(objs = [output_weapon_form, result])
                user_weapon_form = pandas.concat(objs = [user_weapon_form, result])
        #物品
        else:
            #判断是否是天空之尘
            if '天空之尘' in result.index[0]:
                output_sky_dust_amount += int(result.iat[0, 0])
                user_basic_info['sky_dust_amount'] += result.iat[0, 0]
            else:
                #判断是否重复
                if result.index[0] in user_item_form.index:
                    user_item_form.at[result.index[0], 0] += result.iat[0, 0]
                else:
                    user_item_form = pandas.concat(objs = [user_item_form, result])
                #判断是否与最终的输出表格重复
                if result.index[0] in output_item_form.index:
                    output_item_form.at[result.index[0], 'item_amount'] += result.iat[0, 0]
                else:
                    output_item_form = pandas.concat(objs = [output_item_form, result])
    #保存数据
    user_basic_info.to_json('./Users/' + user + '_basic_info.json', indent = 4)
    user_weapon_form.to_json('./Users/' + user + '_weapon_form.json', indent = 4, orient = 'index')
    user_item_form.to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
    #处理表格数据
    final_output_form += other_module.ConvertToOutputForm(pandas_form = output_weapon_form, form_type = 'weapon')
    final_output_form += '\n'
    final_output_form += other_module.ConvertToOutputForm(pandas_form = output_item_form, form_type = 'item')
    final_output_form += '\n\n总计获得' + str(output_sky_dust_amount) + '个天空之尘及' + str(output_earth_dust_amount) + '个大地之烬'
    await message.reply(final_output_form, mention_author = message.author)