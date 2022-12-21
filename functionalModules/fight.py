import qq
import pandas
import asyncio
import random

import ToolModules.other_module as other_module

async def fight(self: qq.Client, message: qq.Message):
    request = message.content.split('||')
    user1 = str(message.author)
    user2 = request[1]
    #检测是否自己和自己对战
    if user1 == user2:
        await message.reply('请不要向自己发起对战', mention_author = message.author)
        return
    #检测注册状况
    try:
        checker = open('./users/' + user1 + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到' + user1 + '，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    try:
        checker = open('./users/' + user2 + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到' + user2 + '，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    #检查命令格式
    try:
        user1 = str(message.author)
        user2 = request[1]
        await message.reply('正在等待' + user2 + '作出回答.', mention_author = message.author)
    except:
        await message.reply('请输入正确的命令格式：/对战||[对方的名字]', mention_author = message.author)
        return
    #获取回答
    def verify(msg: qq.Message):
        return str(msg.author) == user2
    while True:
        try:
            answer: qq.Message = await self.wait_for(event = 'message', check = verify, timeout = 60)
        #超时
        except asyncio.TimeoutError:
            await message.reply('对方超出1分钟未给出回应', mention_author = message.author)
            return
        if '拒绝' in answer.content:
            await message.reply('对方拒绝了你的对战请求', mention_author = message.author)
            return
        elif '接受' in answer.content:
            await message.reply('对方接受了你的对战请求', mention_author = message.author)
            break
        #乱回答
        else:
            await message.reply('请不要回答除接受与拒绝之外的其他回答', mention_author = answer.author)
    winner, loser = await fightGame(self = self, host_message = message, guest_message = answer, host = user1, guest = user2)
    #读取二人的信息
    winner_basic_info = pandas.read_json('./users/' + winner + '_basic_info.json', typ = 'series')
    winner_in_game_info = pandas.read_json('./users/' + winner + '_in_game_info.json', typ = 'series')
    loser_basic_info = pandas.read_json('./users/' + loser + '_basic_info.json', typ = 'series')
    loser_in_game_info = pandas.read_json('./users/' + loser + '_in_game_info.json', typ = 'series')
    #根据等级差计算奖励
    level_difference = winner_in_game_info['current_level'] - loser_in_game_info['current_level']
    if level_difference >= 10:
        if int(loser_basic_info['sky_dust_amount'] * 0.5) < 5000:
            sky_dust_amount_minused = loser_basic_info['sky_dust_amount']  + 10
        else:
            sky_dust_amount_minused = int(loser_basic_info['sky_dust_amount'] * 0.5)
        current_exp_added = random.randint(32767, 65536)
        sky_dust_amountAdded = random.randint(2000, 4000)
    elif level_difference >= 5:
        if int(loser_basic_info['sky_dust_amount'] * 0.3) < 1000:
            sky_dust_amount_minused = loser_basic_info['sky_dust_amount'] + 10
        else:
            sky_dust_amount_minused = int(loser_basic_info['sky_dust_amount'] * 0.3)
        current_exp_added = random.randint(8192, 16384)
        sky_dust_amountAdded = random.randint(1000, 2000)
    elif level_difference >= 3:
        if int(loser_basic_info['sky_dust_amount'] * 0.2) < 500:
            sky_dust_amount_minused = loser_basic_info['sky_dust_amount'] + 10
        else:
            sky_dust_amount_minused = int(loser_basic_info['sky_dust_amount'] * 0.2)
        current_exp_added = random.randint(1024, 4096)
        sky_dust_amountAdded = random.randint(500, 1000)
    else:
        if int(loser_basic_info['sky_dust_amount'] * 0.1) < 250:
            sky_dust_amount_minused = loser_basic_info['sky_dust_amount'] + 10
        else:
            sky_dust_amount_minused = int(loser_basic_info['sky_dust_amount'] * 0.1)
        current_exp_added = random.randint(256, 1024)
        sky_dust_amountAdded = random.randint(250, 500)
    await message.reply('对战结束：\n' + winner + '获得：天空之尘 +' + str(sky_dust_amountAdded) + '  经验值 +' + str(current_exp_added) + '\n' + loser + '失去：天空之尘 -' + str(sky_dust_amount_minused))
    winner_basic_info['sky_dust_amount'] += sky_dust_amountAdded
    winner_in_game_info['current_exp'] += current_exp_added
    loser_basic_info['sky_dust_amount'] -= sky_dust_amount_minused
    winner_basic_info.to_json('./users/' + winner + '_basic_info.json', indent = 4)
    winner_in_game_info.to_json('./users/' + winner + '_in_game_info.json', indent = 4, orient = 'index')
    loser_basic_info.to_json('./users/' + loser + '_basic_info.json', indent = 4)
    loser_in_game_info.to_json('./users/' + loser + '_in_game_info.json', indent = 4, orient = 'index')
    other_module.updateUser_in_game_info(user = winner)


async def fightGame(self: qq.Client, host_message: qq.Message, guest_message: qq.Message, host, guest):
    #读取相关数据
    host_weapon_form = pandas.read_json('./users/' + host + '_weapon_form.json', orient = 'index')
    host_item_form = pandas.read_json('./users/' + host + '_item_form.json', orient = 'index')
    host_in_game_info = pandas.read_json('./users/' + host + '_in_game_info.json', typ = 'series')

    guest_weapon_form = pandas.read_json('./users/' + guest + '_weapon_form.json', orient = 'index')
    guest_item_form = pandas.read_json('./users/' + guest + '_item_form.json', orient = 'index')
    guest_in_game_info = pandas.read_json('./users/' + guest + '_in_game_info.json', typ = 'series')

    #定义检查回复的函数
    def verifyHost(msg: qq.Message):
        return str(msg.author) == host
    def verifyGuest(msg: qq.Message):
        return str(msg.author) == guest

    #开始对战
    round = 1
    current_user_number = 0
    while True:
        #根据回合判定
        if current_user_number % 2 == 0:
            current_user_in_game_info = guest_in_game_info
            current_user_weapon_form = guest_weapon_form
            current_user_item_form = guest_item_form
            current_user_message = guest_message
            current_user = guest

            waiting_user_in_game_info = host_in_game_info
            waiting_user_message = host_message
            waiting_user = host
            verify = verifyGuest
        elif current_user_number % 2 == 1:
            current_user_in_game_info = host_in_game_info
            current_user_weapon_form = host_weapon_form
            current_user_item_form = host_item_form
            current_user_message = host_message
            current_user = host

            waiting_user_in_game_info = guest_in_game_info
            waiting_user_message = guest_message
            waiting_user = guest
            verify = verifyHost

        await host_message.reply('当前生命值：\n' + current_user + '：' + str(current_user_in_game_info['basic_HP']) + '  ' + waiting_user + '：' + str(waiting_user_in_game_info['basic_HP']))
        await host_message.reply('当前为第' + str(round) + '回合，请' + current_user + '行动', mention_author = current_user_message.author)

        while True:
            try:
                current_user_action_reply: qq.Message = await self.wait_for(event = 'message', check = verify, timeout = 300)
            except asyncio.TimeoutError:
                await host_message.reply(current_user + '超出时间未操作，默认投降', mention_author = waiting_user_message.author)
                return waiting_user, current_user
            else:
                if '跳过' in current_user_action_reply.content:
                    await host_message.reply('对方放弃了本回合', mention_author = waiting_user_message.author)
                    current_user_number += 1
                    break
                #切分用户消息,获得道具种类和名字
                try:
                    current_user_action_type = current_user_action_reply.content.split()[1]
                    current_user_action_content = current_user_action_reply.content.split()[2]
                except:
                    await host_message.reply('请输入有效的命令：[武器/物品]||[名字]', mention_author = current_user_message.author)
                    continue
                #区分种类
                if current_user_action_type == '武器':
                    #检测武器是否存在
                    if current_user_action_content in current_user_weapon_form.index:
                        #攻击
                        waiting_user_in_game_info['basic_HP'] -= current_user_weapon_form.at[current_user_action_content, 'weapon_attack'] + current_user_in_game_info['basic_attack']
                    else:
                        await host_message.reply('未找到武器：' + current_user_action_content, mention_author = current_user_message.author)
                        continue
                elif current_user_action_type == '物品':
                    #检测用户的物品是否为空
                    if current_user_item_form.empty == True:
                        await host_message.reply('空物品背包', mention_author = current_user_message.author)
                        continue
                    #检测物品是否存在
                    if current_user_action_content in current_user_item_form.index:
                        affected_prop: dict = indexItem(current_user = current_user, item_name = current_user_action_content)
                        #检测是否有此物品
                        if affected_prop == 'NoSuchItem':
                            await host_message.reply('未找到物品：' + current_user_action_content, mention_author = current_user_message.author)
                            continue
                        #若物品数量=0,则删除这一个物品
                        current_user_item_form.at[current_user_action_content, 'item_amount'] -= 1
                        if current_user_item_form.at[current_user_action_content, 'item_amount'] == 0:
                            current_user_item_form.drop(index = current_user_action_content, inplace = True)
                        current_user_item_form.to_json('./users/' + current_user + '_item_form.json', indent = 4, orient = 'index')
                        #应用物品带来的效果
                        for affected_attribute, affects in affected_prop.items():
                            current_user_in_game_info[affected_attribute] += affects
                else:
                    await guest_message.reply('请输入有效的道具种类：武器或物品', mention_author = current_user_message.author)
                    continue
            current_user_number += 1
            round += 1
            #判断双方血量
            if host_in_game_info['basic_HP'] <= 0:
                return guest, host
            elif guest_in_game_info['basic_HP'] <= 0:
                return host, guest
            break


def indexItem(current_user, item_name):
    user_item_form = pandas.read_json('./users/' + current_user + '_item_form.json', orient = 'index')
    user_item_form.set_index(keys = 'item_name')
    match item_name:
        case '生命药水':
            return {'basic_HP': 1000}
        case '力量药水':
            return {'basic_HP': 200}
        case '恢复药水':
            return {'basic_HP': 1000, 'basic_attack': 200}
        case _:
            return 'NoSuchItem'