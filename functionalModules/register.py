import qq
import pandas

async def register(message: qq.Message):
    #尝试增加文件
    user = str(message.author)
    if ' ' in user:
        await message.reply('无效用户名，请不要使用带有空格的用户名', mention_author = message.author)
        return
    try:
        user_basic_info = open('./users/' + user + '.isregistered', mode = 'x', encoding = 'utf8')
    except:
        await message.reply('注册失败，请不要重复注册', mention_author=message.author)
        return
    #文件初始化
    user_basic_info.close()
    #basicInfo
    pandas.Series(index = ['sky_dust_amount', 'signed_days', 'last_activity', 'earth_dust_amount', 'continuous_signed'], data = [0, 0, 0, 0, 0]).to_json('./users/' + user + '_basic_info.json', indent = 4)
    #weapon_form
    pandas.DataFrame(data = [[0, 0, 0], [20, 'Special', -1]], columns = ['weapon_attack', 'weapon_rarity', 'weapon_rarity_raw', 'weapon_skill'], index = [0, '新手剑']).to_json('./users/' + user + '_weapon_form.json', indent = 4, orient = 'index')
    #item_form
    pandas.DataFrame(data= [[0, 0, 0], [1, 'Common', 0.4]], columns = ['item_amount', 'item_rarity', 'item_rarity_raw'], index = [0, '生命药水']).to_json('./users/' + user + '_item_form.json', indent = 4, orient = 'index')
    #_in_game_info
    pandas.Series(index = ['current_level', 'basic_HP', 'basic_attack', 'current_exp'], data = [0, 2000, 200, 0]).to_json('./users/' + user + '_in_game_info.json', indent = 4)
    await message.reply('注册成功，如果你不知道如何使用这个机器人，你可以输入 /菜单', mention_author = message.author)