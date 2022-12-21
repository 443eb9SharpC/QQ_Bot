import qq
import pandas
import datetime

async def sign(message: qq.Message):
    #检测是否注册
    try:
        user_basic_info = pandas.read_json('./users/' + str(message.author) + '_basic_info.json', typ = 'series')
    except:
        await message.reply('签到失败，请先注册', mention_author = message.author)
        return
    #检测签到间隔时间
    current_time = datetime.date.today().day
    if current_time == user_basic_info['last_activity']:
        await message.reply('签到失败，请不要在一天之内多次签到', mention_author = message.author)
    else:
        #检测连续签到天数
        if current_time - user_basic_info['last_activity'] == 1:
            user_basic_info['continuous_signed'] += 1
            if user_basic_info['continuous_signed'] > 3:
                #连续签到3天后,每天额外获得5个天空之尘
                user_basic_info['sky_dust_amount'] += (user_basic_info['continuous_signed'] - 3) % 30 * 5
        else:
            #重置连续签到
            user_basic_info['continuous_signed'] = 1
        user_basic_info['signed_days'] += 1
        user_basic_info['sky_dust_amount'] += 10
        user_basic_info['last_activity'] = current_time
        user_basic_info.to_json('./users/' + str(message.author) + '_basic_info.json', indent = 4, orient = 'index')
        if user_basic_info['continuous_signed'] > 3:
            await message.reply('你目前有' + str(user_basic_info['sky_dust_amount']) + '个天空之尘，已累计签到' + str(user_basic_info['signed_days']) + '天，已连续签到' + str(user_basic_info['continuous_signed']) + '天，额外获得' + str((user_basic_info['continuous_signed'] - 3) % 30 * 5) + '个天空之尘', mention_author = message.author)
        else:
            await message.reply('你目前有' + str(user_basic_info['sky_dust_amount']) + '个天空之尘，已累计签到' + str(user_basic_info['signed_days']) + '天，已连续签到' + str(user_basic_info['continuous_signed']) + '天', mention_author = message.author)