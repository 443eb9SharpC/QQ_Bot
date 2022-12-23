import random
import qq
import asyncio
import pandas


#用于触发对战
async def Fight(self: qq.Client, message: qq.Message):
    request = message.content.split('/')[1]
    host = str(message.author)
    guest = request[1]
    #检测是否自己和自己对战
    if host == guest:
        await message.reply('请不要向自己发起对战', mention_author = message.author)
        return
    #检测注册状况
    try:
        checker = open('./users/' + host + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到' + host + '，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    try:
        checker = open('./users/' + guest + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到' + guest + '，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    #检查命令格式
    try:
        host = str(message.author)
        guest = request[1]
        await message.reply('正在等待' + guest + '作出回答.', mention_author = message.author)
    except:
        await message.reply('请输入正确的命令格式：/对战 [对方的名字]', mention_author = message.author)
        return
    #获取回答
    def Verify(msg: qq.Message):
        return str(msg.author) == guest
    while True:
        try:
            answer: qq.Message = await self.wait_for(event = 'message', check = Verify, timeout = 60)
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
    winner, loser = await FightMain(self = self, host_message = message, guest_message = answer)


#对战主函数
async def FightMain(self: qq.Client, host_message: qq.Message, guest_message: qq.Message):
    host = str(host_message.author)
    guest = str(guest_message.author)

    await host_message.reply(f'由{host}发起的{host}-{guest}对战开始')

    def VerifyGuest(message: qq.Message):
        return str(message.author) == guest
    def VerifyHost(message: qq.Message):
        return str(message.author) == host

    #读取所有用户信息
    host_weapon_form = pandas.read_json('./Users/' + host + '_weapon_form.json', orient = 'index')
    host_item_form = pandas.read_json('./Users/' + host + '_item_form.json', orient = 'index')
    host_armor_form = pandas.read_json('./Users/' + host + '_armor_form.json', orient = 'index')
    host_in_game_info = pandas.read_json('./Users/' + host + '_in_game_info.json', typ = 'series')

    guest_weapon_form = pandas.read_json('./Users/' + guest + '_weapon_form.json', orient = 'index')
    guest_item_form = pandas.read_json('./Users/' + guest + '_item_form.json', orient = 'index')
    guest_armor_form = pandas.read_json('./Users/' + guest + '_armor_form.json', orient = 'index')
    guest_in_game_info = pandas.read_json('./Users/' + guest + '_in_game_info.json', typ = 'series')

    #读取各种索引
    buff_index = pandas.read_json('./Indexes/BuffIndex/main_buff_index.json', orient = 'index')
    debuff_index = pandas.read_json('./Indexes/DebuffIndex/main_debuff_index.json', orient = 'index')
    potion_index = pandas.read_json('./Indexes/PotionIndex/main_potion_index.json', orient = 'index')
    skill_index = pandas.read_json('./Indexes/SkillIndex/main_skill_index.json', orient = 'index')
    weapon_index = pandas.read_json('./Indexes/WeaponIndex/main_weapon_index.json', typ = 'series')
    armor_index = pandas.read_json('./Indexes/ArmorIndex/main_armor_index.json', typ = 'series')

    #创建对战会话
    host_in_session_info = pandas.Series(index = ['HP', 'attack', 'defence', 'crit_rate', 'steps_per_round'], data = [host_in_game_info['basic_HP'], host_in_game_info['basic_attack'], host_in_game_info['basic_defence'], host_in_game_info['basic_crit_rate'], host_in_game_info['steps_per_round']])
    host_in_session_effects = pandas.Series()
    host_in_session_attack_boost = [0, 0] #intensity, duration

    guest_in_session_info = pandas.Series(index = ['HP', 'attack', 'defence', 'crit_rate', 'steps_per_round'], data = [guest_in_game_info['basic_HP'], guest_in_game_info['basic_attack'], guest_in_game_info['basic_defence'], guest_in_game_info['basic_crit_rate'], host_in_game_info['steps_per_round']])
    guest_in_session_effects = pandas.Series()
    guest_in_session_attack_boost = [0, 0]

    #获取guest技能
    await host_message.reply(f'请由{guest}选取技能（最多3种）', mention_author = guest_message.author)
    while True:
        #获取回答
        try:
            command_message: qq.Message = await self.wait_for(event = 'message', check = VerifyGuest, timeout = 120)
        except:
            await host_message.reply(f'超过2分钟{guest}未回应默认投降', mention_author = guest_message.author)
            return host, guest
        #判断命令格式
        if '/' in command_message.content:
            command = command_message.content.split('/')[1].split()
            #再次检查长度,格式化技能
            match len(command):
                case 1:
                    skill_1 = command[0]
                case 2:
                    skill_1 = command[0]
                    skill_2 = command[1]
                case 3:
                    skill_1 = command[0]
                    skill_2 = command[1]
                    skill_3 = command[2]
                case _:
                    await host_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]', mention_author = guest_message.authoweapon_detailr)
                    continue
            #检查技能是否存在
            if not skill_1 + '技能书' in guest_item_form.index:
                await host_message.reply(f'无效的技能：{skill_1}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            elif not skill_2 + '技能书' in guest_item_form.index:
                await host_message.reply(f'无效的技能：{skill_2}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            elif not skill_3 + '技能书' in guest_item_form.index:
                await host_message.reply(f'无效的技能：{skill_3}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            #创建用户技能表
            guest_skill_form = [skill_1, skill_2, skill_3]
            break
        else:
            await host_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]', mention_author = guest_message.author)

    #获取host技能
    await host_message.reply(f'请由{host}选取技能（最多3种）', mention_author = host_message.author)
    while True:
        #获取回答
        try:
            command_message: qq.Message = await self.wait_for(event = 'message', check = VerifyGuest, timeout = 120)
        except:
            await host_message.reply(f'超过2分钟{host}未回应默认投降', mention_author = host_message.author)
            return guest, host
        #判断命令格式
        if '/' in command_message.content:
            command = command_message.content.split('/')[1].split()
            #再次检查长度,格式化技能
            match len(command):
                case 1:
                    skill_1 = command[0]
                case 2:
                    skill_1 = command[0]
                    skill_2 = command[1]
                case 3:
                    skill_1 = command[0]
                    skill_2 = command[1]
                    skill_3 = command[2]
                case _:
                    await host_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]', mention_author = guest_message.author)
                    continue
            #检查技能是否存在
            if not skill_1 + '技能书' in host_item_form.index:
                await host_message.reply(f'无效的技能：{skill_1}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            elif not skill_2 + '技能书' in host_item_form.index:
                await host_message.reply(f'无效的技能：{skill_2}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            elif not skill_3 + '技能书' in host_item_form.index:
                await host_message.reply(f'无效的技能：{skill_3}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            #创建用户技能表
            host_skill_form = [skill_1, skill_2, skill_3]
            break
        else:
            await host_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]', mention_author = guest_message.author)

    #获取guest盔甲
    await host_message.reply(f'请由{guest}选取盔甲', mention_author = guest_message.author)
    while True:
        try:
            command_message = await self.wait_for(event = 'message', check = VerifyGuest, timeout = 120)
        except:
            await host_message.reply(f'超过2分钟{guest}未回应默认投降', mention_author = guest_message.author)
            return host, guest
        #判断命令格式
        if '/' in command_message.content:
            armor = command_message.content.split('/')[1]
            if not armor in guest_armor_form.index:
                await host_message.reply(f'无效的盔甲：{armor}，请检查该盔甲是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            guest_armor = pandas.read_json('./Indexes/ArmorIndex/' + armor_index[armor] + '.json', typ = 'series')
            #重新计算防御力
            guest_in_session_info['defence'] += guest_armor['defence']
            #重新计算行动点
            guest_in_session_info['steps_per_round'] -= guest_armor['armor_step']
            break
        else:
            await host_message.reply('请输入有效的命令：/[盔甲名]', mention_author = guest_message.author)

    #获取host盔甲
    await host_message.reply(f'请由{host}选取盔甲', mention_author = host_message.author)
    while True:
        try:
            command_message = await self.wait_for(event = 'message', check = VerifyHost, timeout = 120)
        except:
            await host_message.reply(f'超过2分钟{host}未回应默认投降', mention_author = guest_message.author)
            return guest, host
        #判断命令格式
        if '/' in command_message.content:
            armor = command_message.content.split('/')[1]
            if not armor in host_armor_form.index:
                await host_message.reply(f'无效的盔甲：{armor}，请检查该盔甲是否存在且拥有，并重新输入', mention_author = host_message.author)
                continue
            host_armor = pandas.read_json('./Indexes/ArmorIndex/' + armor_index[armor] + '.json', typ = 'series')
            host_in_session_info['defence'] += host_armor['defence']
            host_in_session_info['steps_per_round'] -= host_armor['armor_step']
            break
        else:
            await host_message.reply('请输入有效的命令：/[盔甲名]', mention_author = guest_message.author)

    #创建对局参数
    round_count = 0

    while True:
        round_count += 1
        #切换用户
        if round_count == 1:
            current_user_weapon_form = guest_weapon_form
            current_user_item_form = guest_item_form
            current_user_armor = guest_armor
            current_user_skill_form = guest_skill_form
            current_user_in_game_info = guest_in_game_info
            current_user_in_session_info = guest_in_session_info
            current_user_in_session_effects = guest_in_session_effects
            current_user_in_session_attack_boost = guest_in_session_attack_boost
            current_user_message = guest_message
            current_user = guest

            waiting_user_weapon_form = host_weapon_form
            waiting_user_item_form = host_item_form
            waiting_user_armor = host_armor
            waiting_user_skill_form = host_skill_form
            waiting_user_in_game_info = host_in_game_info
            waiting_user_in_session_info = host_in_session_info
            waiting_user_in_session_effects = host_in_session_effects
            waiting_user_in_session_attack_boost = host_in_session_attack_boost
            waiting_user_message = host_message
            waiting_user = host
        else:
            current_user_weapon_form = host_weapon_form
            current_user_item_form = host_item_form
            current_user_armor = host_armor
            current_user_skill_form = host_skill_form
            current_user_in_game_info = host_in_game_info
            current_user_in_session_info = host_in_session_info
            current_user_in_session_effects = host_in_session_effects
            current_user_in_session_attack_boost = host_in_session_attack_boost
            current_user_message = host_message
            current_user = host

            waiting_user_weapon_form = guest_weapon_form
            waiting_user_item_form = guest_item_form
            waiting_user_armor = guest_armor
            waiting_user_skill_form = guest_skill_form
            waiting_user_in_game_info = guest_in_game_info
            waiting_user_in_session_info = guest_in_session_info
            waiting_user_in_session_effects = guest_in_session_effects
            waiting_user_in_session_attack_boost = guest_in_session_attack_boost
            waiting_user_message = guest_message
            waiting_user = guest

        #给当前回合玩家应用效果
        if current_user_in_session_effects.empty != True:
            for effect_name in current_user_in_session_effects.index:
                #减1持续时间
                current_user_in_session_effects[effect_name] -= 1
                #若效果结束，则删除效果并且恢复属性
                if current_user_in_session_effects[effect_name] == -1:
                    for attribute_affected in buff_index.loc[effect_name]:
                        current_user_in_session_info[attribute_affected] -= current_user_in_session_effects[attribute_affected] * current_user_in_game_info['basic_' + attribute_affected]
                    current_user_in_session_effects.drop(effect_name)
                #遍历效果列表,并把效果影响的属性提取
                for attribute_affected in buff_index.loc[effect_name]:
                    #应用效果
                    current_user_in_session_info[attribute_affected] += current_user_in_session_effects[attribute_affected] * current_user_in_game_info['basic_' + attribute_affected]
        
        form = '玩家 | 生命值 | 可用行动力\n' + host + ' | ' + host_in_session_info['HP'] + ' | ' + host_in_session_info['steps_per_round'] + '\n' + guest + ' | ' + guest_in_session_info['HP'] + ' | ' + guest_in_session_info['steps_per_round']
        await host_message.reply('当前状态：\n' + form)
        await host_message.reply(f'回合{round_count}，请{current_user}行动', mention_author = current_user_message.author)

        #定义检查函数
        def VerifyCurrentUser(message: qq.Message):
            return str(message.author) == current_user

        #获取用户操作
        while True:
            user_action_message: qq.Message = await self.wait_for(event = 'message', check = VerifyCurrentUser)
            #检查命令格式
            if '/' in user_action_message.content:
                user_action = user_action_message.content.split('/')[1].split()
                #再检查一遍
                if len(user_action) == 2:
                    action_type = user_action[0]
                    action_content = user_action[1]
                    match action_type:

                        case '武器':
                            weapon_name = action_content
                            if action_content in current_user_weapon_form.index:
                                #检索出英文id,即文件名
                                weapon_id = weapon_index[weapon_name]
                                weapon_detail = pandas.read_json('./Indexed/WeaponIndex/' + weapon_id + '.json', orient = 'index')
                                #应用武器效果
                                for index in weapon_detail:

                                    #效果附加
                                    if 'apply_' in index:
                                        #获取效果名称
                                        effect_name = index.split('_')[1]
                                        #随机是否含有这个效果
                                        if random.uniform(0, 1) <= weapon_detail.at['apply_' + effect_name, 'chance']:
                                            #判断是buff还是debuff
                                            if 'debuff' in effect_name:
                                                waiting_user_in_session_effects[effect_name] = weapon_detail.at['apply_' + effect_name, 'duration']
                                            else:
                                                current_user_in_session_effects[effect_name] = weapon_detail.at['apply' + effect_name, 'duration']

                                    #攻击力概率性加成
                                    if 'attack' in index:
                                        if random.uniform(0,1) <= weapon_detail.at['attack', 'chance']:
                                            #对比攻击力加强的强度
                                            if weapon_detail.at['attack', 'intensity'] >= current_user_in_session_attack_boost[0]:
                                                #更新
                                                current_user_in_session_attack_boost[0] = weapon_detail.at['attack', 'intensity']
                                                current_user_in_session_attack_boost[1] = weapon_detail.at['attack', 'duration']

                                    #元素克制
                                    armor_elem = current_user_armor['element']
                                    weapon_elem_1 = weapon_detail.at['specific_attack', 'specific_elem_1']
                                    weapon_elem_2 = weapon_detail.at['specific_attack', 'specific_elem_2']
                                    if (armor_elem == weapon_elem_1 or armor_elem == weapon_elem_2) and str(armor_elem) != 'None':
                                        elem_attack = weapon_detail.at['specific_attack', 'intensity'] * current_user_in_game_info['basic_attack']

                                    #攻击力计算
                                    attack = current_user_weapon_form.at[weapon_name, 'weapon_attack'] + current_user_in_session_attack_boost[0] * current_user_in_game_info['basic_attack'] + current_user_in_session_info['attack'] - waiting_user_in_session_info['defence'] * random.uniform(0.8, 1) + elem_attack

                                    #暴击率计算
                                    crit_rate = current_user_in_game_info['basic_crit_rate'] + current_user_armor['crit_rate']

                                    #计算是否触发暴击
                                    if random.uniform(0, 1) <= crit_rate:
                                        attack *= 1.5
                                        crit_sign = '暴击！'

                                    #应用伤害
                                    waiting_user_in_session_info['HP'] -= attack
                                    current_user_in_session_info['steps_per_round'] -= current_user_weapon_form['weapon_step']
                                    await host_message.reply(crit_sign + f'{current_user}使用{weapon_name}对{waiting_user}造成了{attack}点伤害')
                                    break
                            else:
                                await host_message.reply(f'未找到武器：{weapon_name}', mention_author = current_user_message.author)

                        case '物品':
                            item_name = action_content
                            if action_content in current_user_item_form:
                                #判断物品是否为药水
                                if '药水' in item_name:
                                    if item_name in current_user_item_form.index:
                                        for attribute_affected in potion_index.columns:
                                            #应用药效
                                            current_user_in_session_info[attribute_affected] += potion_index.at[item_name, attribute_affected] * current_user_in_game_info['basic_' + attribute_affected]
                                        current_user_in_session_info['steps_per_round'] -= current_user_item_form['potion_step']
                                        #减物品
                                        current_user_item_form.at[item_name, 'item_amount'] -= 1
                                        #去除数量为0的物品
                                        if current_user_item_form.at[item_name, 'item_amount'] == 0:
                                            current_user_item_form.drop(index = ['item_name'])
                                        await host_message.reply(f'{current_user}使用了{item_name}')
                                        break
                                    else:
                                        await host_message.reply(f'未找到物品或物品不可用：{item_name}')
                                else:
                                    #匹配特殊物品
                                    match item_name:
                                        case '净化之歌':
                                            current_user_in_session_effects = pandas.Series()
                                            current_user_in_session_info['steps_per_round'] -= 3
                                            await host_message.reply(f'{current_user}使用了净化之歌清除了所有效果')
                                        case '旺旺大礼包':
                                            await host_message.reply(f'未找到物品或物品不可用：{item_name}', mention_author = current_user_message.author)
                                    break
                            else:
                                await host_message.reply(f'未找到物品或物品不可用：{item_name}', mention_author = current_user_message.author)

                        case _:
                            await host_message.reply('请输入正确的行动类型：武器 物品 技能', mention_author = user_action_message.author)
                else:
                    await host_message.reply('请输入有效的命令格式：/[武器/物品/技能] [名字]', mention_author = user_action_message.author)
            else:
                await host_message.reply('请输入有效的命令格式：/[武器/物品/技能] [名字]', mention_author = user_action_message.author)