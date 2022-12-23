import qq
import pandas

async def Register(message: qq.Message):
    #尝试增加文件
    user = str(message.author)
    if ' ' in user:
        await message.reply('无效用户名，请不要使用带有空格的用户名', mention_author = message.author)
        return
    try:
        user_basic_info = open('./Users/' + user + '.isregistered', mode = 'x', encoding = 'utf8')
    except:
        await message.reply('注册失败，请不要重复注册', mention_author=message.author)
        return
    #文件初始化
    user_basic_info.close()
    #basic_info
    pandas.Series(index = ['sky_dust_amount', 'signed_days', 'last_activity', 'earth_dust_amount', 'continuous_signed'], data = [0, 0, 0, 0, 0]).to_json('./Users/' + user + '_basic_info.json', indent = 4)
    #weapon_form
    pandas.DataFrame(data = [[0, 0, 0, 0], [50, 'Special', -1, 2]], columns = ['weapon_attack', 'weapon_rarity', 'weapon_rarity_raw', 'weapon_step'], index = [0, '新手剑']).to_json('./Users/' + user + '_weapon_form.json', indent = 4, orient = 'index')
    #item_form
    pandas.DataFrame(data= [[0, 0, 0], [1, 'Common', 0.4, 2]], columns = ['item_amount', 'item_rarity', 'item_rarity_raw', 'item_step'], index = [0, '生命药水']).to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
    #armor_form
    pandas.DataFrame(data = [[0, 0, 0, 0], [10, 'Special', -1, 1]], columns = ['armor_defence', 'armor_rarity', 'armor_rarity_raw', 'armor_step'], index = [0, '新手长袍']).to_json('./Users/' + user + '_armor_form.json', indent = 4, orient = 'index')
    #in_game_info
    pandas.Series(index = ['current_level', 'basic_HP', 'basic_attack', 'basic_defence', 'basic_crit_rate', 'current_exp', 'steps_per_round'], data = [0, 2000, 200, 20, 0.05 ,0 , 10]).to_json('./Users/' + user + '_in_game_info.json', indent = 4)
    await message.reply('注册成功，如果你不知道如何使用这个机器人，你可以输入 /菜单', mention_author = message.author)