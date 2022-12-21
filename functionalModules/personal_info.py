import qq
import pandas

async def personalInfo(message: qq.Message):
    user = str(message.author)
    try:
        user_basic_info = pandas.read_json('./users/' + user + '_basic_info.json', typ = 'series')
        user_in_game_info = pandas.read_json('./users/' + user + '_in_game_info.json', typ = 'series')
    except:
        await message.reply('获取失败，请先注册', mention_author = message.author)
        return
    form = '\n天空之尘数量：' + str(user_basic_info['sky_dust_amount']) + ' | 大地之烬：' + str(user_basic_info['earth_dust_amount']) + ' | 累计签到：' + str(user_basic_info['signed_days']) + ' | 连续签到：' + str(user_basic_info['continuous_signed'])
    form += '\n当前等级：' + str(user_in_game_info['current_level']) + ' | 当前经验值：' + str(user_in_game_info['current_exp']) + ' | 基础生命值：' + str(user_in_game_info['basic_HP']) + ' | 基础攻击力：' + str(user_in_game_info['basic_attack'])
    await message.reply(form, mention_author = message.author)