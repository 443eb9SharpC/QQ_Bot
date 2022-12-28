import random
import qq
import asyncio
import pandas

import ToolModules.other_module as other_module

#用于触发对战
async def Fight(self: qq.Client, message: qq.Message):
    host = str(message.author)
    #检查用户是否注册
    try:
        checker = open('./Users/' + host + '.isregistered')
    except:
        await message.reply('发起失败，请先注册', mention_author = message.author)
        return
    else:
        checker.close()
    try:
        guest = message.content.split('##')[1].split()[1]
    except:
        await message.reply('请输入有效的命令：/对战 [对方的名字]', mention_author = message.author)
        return
    #检测是否自己和自己对战
    if host == guest:
        await message.reply('请不要向自己发起对战', mention_author = message.author)
        return
    #检测注册状况
    try:
        checker = open('./Users/' + guest + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到用户“' + guest + '”，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    #检查命令格式
    try:
        host = str(message.author)
        await message.reply('正在等待' + guest + '作出回答...', mention_author = message.author)
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
            await message.reply('请不要回答除接受与拒绝之外的其他回答，请重新输入', mention_author = answer.author)
    #对战
    winner, loser = await FightMain(self = self, host_message = message, guest_message = answer)
    #奖惩计算
    await FightAward(winner = winner, loser = loser, message = message)


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
    effect_index = pandas.read_json('./Indexes/EffectIndex/main_effect_index.json', orient = 'index')
    potion_index = pandas.read_json('./Indexes/PotionIndex/main_potion_index.json', orient = 'index')
    skill_index = pandas.read_json('./Indexes/SkillIndex/main_skill_index.json', orient = 'index')
    weapon_index = pandas.read_json('./Indexes/WeaponIndex/main_weapon_index.json', typ = 'series')

    #创建对战会话
    host_in_session_info = pandas.Series(index = ['HP', 'attack', 'defence', 'crit_rate', 'steps_per_round'], data = [host_in_game_info['basic_HP'], host_in_game_info['basic_attack'], host_in_game_info['basic_defence'], host_in_game_info['basic_crit_rate'], host_in_game_info['steps_per_round']])
    host_in_session_effects = pandas.Series()
    host_in_session_basic_strengthen = pandas.DataFrame([[0, 0], [0, 0], [0, 0], [0, 0]], columns = ['intensity', 'duration'], index = ['HP', 'attack', 'defence', 'crit_rate'])

    guest_in_session_info = pandas.Series(index = ['HP', 'attack', 'defence', 'crit_rate', 'steps_per_round'], data = [guest_in_game_info['basic_HP'], guest_in_game_info['basic_attack'], guest_in_game_info['basic_defence'], guest_in_game_info['basic_crit_rate'], guest_in_game_info['steps_per_round']])
    guest_in_session_effects = pandas.Series()
    guest_in_session_basic_strengthen = pandas.DataFrame([[0, 0], [0, 0], [0, 0], [0, 0]], columns = ['intensity', 'duration'], index = ['HP', 'attack', 'defence', 'crit_rate'])

    #获取guest技能
    await guest_message.reply(f'请由{guest}选取技能（最多3种）', mention_author = guest_message.author)
    while True:
        #获取回答
        try:
            command_message: qq.Message = await self.wait_for(event = 'message', check = VerifyGuest, timeout = 120)
        except:
            await guest_message.reply(f'超过2分钟{guest}未回应默认投降', mention_author = guest_message.author)
            return host, guest
        #判断命令格式
        if '/' in command_message.content:
            command = command_message.content.split('##')[1].split()
            guest_skill_form = []
            reply_message = ''
            if '跳过' in command_message.content:
                await guest_message.reply(f'{guest}未选取技能')
                break
            #检查技能是否存在
            if len(command) >= 3:
                if not command[2] + '技能书' in guest_item_form.index:
                    await guest_message.reply(f'无效的技能：{command[2]}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                    continue
                reply_message = '，' + command[2] + reply_message
            if len(command) >= 2:
                if not command[1] + '技能书' in guest_item_form.index:
                    await guest_message.reply(f'无效的技能：{command[1]}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                    continue
                reply_message = '，' + command[1] + reply_message
            if len(command) >= 1:
                if not command[0] + '技能书' in guest_item_form.index:
                    await guest_message.reply(f'无效的技能：{command[0]}，请检查该技能是否存在且拥有，并重新输入', mention_author = guest_message.author)
                    continue
                reply_message = command[0] + reply_message
            #再次检查长度,格式化技能
            if len(command) >= 3:
                guest_skill_form.append(command[2])
            if len(command) >= 2:
                guest_skill_form.append(command[1])
            if len(command) >= 1:
                guest_skill_form.append(command[0])
            if len(command) > 3 or len(command) < 1:
                await guest_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]，或直接输入 /跳过 来不选取技能', mention_author = guest_message.author)
                continue
            await guest_message.reply(f'{guest}选取了：{reply_message}')
            #创建用户技能表
            break
        else:
            await guest_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]，或直接输入 /跳过 来不选取技能', mention_author = guest_message.author)

    #获取host技能
    await host_message.reply(f'请由{host}选取技能（最多3种）', mention_author = host_message.author)
    while True:
        #获取回答
        try:
            command_message: qq.Message = await self.wait_for(event = 'message', check = VerifyHost, timeout = 120)
        except:
            await host_message.reply(f'超过2分钟{host}未回应默认投降', mention_author = host_message.author)
            return guest, host
        #判断命令格式
        if '/' in command_message.content:
            command = command_message.content.split('##')[1].split()
            host_skill_form = []
            reply_message = ''
            if '跳过' in command_message.content:
                await host_message.reply(f'{host}未选取技能')
                break
            #检查技能是否存在
            if len(command) >= 3:
                if not command[2] + '技能书' in host_item_form.index:
                    await host_message.reply(f'无效的技能：{command[2]}，请检查该技能是否存在且拥有，并重新输入', mention_author = host_message.author)
                    continue
                reply_message = '，' + command[2] + reply_message
            if len(command) >= 2:
                if not command[1] + '技能书' in host_item_form.index:
                    await host_message.reply(f'无效的技能：{command[1]}，请检查该技能是否存在且拥有，并重新输入', mention_author = host_message.author)
                    continue
                reply_message = '，' + command[1] + reply_message
            if len(command) >= 1:
                if not command[0] + '技能书' in host_item_form.index:
                    await host_message.reply(f'无效的技能：{command[0]}，请检查该技能是否存在且拥有，并重新输入', mention_author = host_message.author)
                    continue
                reply_message = command[0] + reply_message
            #再次检查长度,格式化技能
            if len(command) >= 3:
                host_skill_form.append(command[2])
            if len(command) >= 2:
                host_skill_form.append(command[1])
            if len(command) >= 1:
                host_skill_form.append(command[0])
            if len(command) > 3 or len(command) < 1:
                await host_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]，或直接输入 /跳过 来不选取技能', mention_author = host_message.author)
                continue
            await host_message.reply(f'{host}选取了：{reply_message}')
            #创建用户技能表
            break
        else:
            await host_message.reply('请输入有效的命令：/[技能1] [技能2] [技能3]，或直接输入 /跳过 来不选取技能', mention_author = host_message.author)

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
            armor = command_message.content.split('##')[1]
            if not armor in guest_armor_form.index:
                await host_message.reply(f'无效的盔甲：{armor}，请检查该盔甲是否存在且拥有，并重新输入', mention_author = guest_message.author)
                continue
            guest_armor = armor
            #重新计算行动点
            guest_in_session_info['steps_per_round'] -= guest_armor_form.at[armor, 'armor_step']
            break
        else:
            await host_message.reply('请输入有效的命令：/[盔甲名]', mention_author = guest_message.author)

    #获取host盔甲
    await host_message.reply(f'请由{host}选取盔甲', mention_author = host_message.author)
    while True:
        try:
            command_message = await self.wait_for(event = 'message', check = VerifyHost, timeout = 120)
        except:
            await host_message.reply(f'超过2分钟{host}未回应默认投降', mention_author = host_message.author)
            return host, host
        #判断命令格式
        if '/' in command_message.content:
            armor = command_message.content.split('##')[1]
            if not armor in host_armor_form.index:
                await host_message.reply(f'无效的盔甲：{armor}，请检查该盔甲是否存在且拥有，并重新输入', mention_author = host_message.author)
                continue
            host_armor = armor
            host_in_session_info['steps_per_round'] -= host_armor_form.at[armor, 'armor_step']
            break
        else:
            await host_message.reply('请输入有效的命令：/[盔甲名]', mention_author = host_message.author)

    #初始化
    current_user_weapon_form = guest_weapon_form
    current_user_item_form = guest_item_form
    current_user_armor_form = guest_armor_form
    current_user_armor = guest_armor
    current_user_skill_form = guest_skill_form
    current_user_in_game_info = guest_in_game_info
    current_user_in_session_info = guest_in_session_info
    current_user_in_session_effects = guest_in_session_effects
    current_user_in_session_basic_strengthen = guest_in_session_basic_strengthen
    current_user_message = guest_message
    current_user = guest

    waiting_user_weapon_form = host_weapon_form
    waiting_user_item_form = host_item_form
    waiting_user_armor_form = host_armor_form
    waiting_user_armor = host_armor
    waiting_user_skill_form = host_skill_form
    waiting_user_in_game_info = host_in_game_info
    waiting_user_in_session_info = host_in_session_info
    waiting_user_in_session_effects = host_in_session_effects
    waiting_user_in_session_basic_strengthen = host_in_session_basic_strengthen
    waiting_user_message = host_message
    waiting_user = host


    #创建对局参数
    round_count = 1

    while True:
        #给当前回合玩家应用效果
        if current_user_in_session_effects.empty != True:
            for effect_name in current_user_in_session_effects.index:
                #减1持续时间
                current_user_in_session_effects[effect_name] -= 1
                #若效果结束，则删除效果并且恢复属性
                if current_user_in_session_effects[effect_name] == -1:
                    if effect_index.at[effect_name, 'is_permanent'] == 'True':
                        continue
                    else:
                        for attribute_affected in effect_index.loc[effect_name]:
                            current_user_in_session_info[attribute_affected] -= current_user_in_session_effects[attribute_affected] * current_user_in_game_info['basic_' + attribute_affected]
                    current_user_in_session_effects.drop(effect_name)
                #遍历效果列表,并把效果影响的属性提取
                for attribute_affected in effect_index.loc[effect_name]:
                    #应用效果
                    current_user_in_session_info[attribute_affected] += current_user_in_session_effects[attribute_affected] * current_user_in_game_info['basic_' + attribute_affected]
                #特殊效果检查
                match effect_name:
                    case '恐惧':
                        if random.uniform(0, 1) <= 0.1:
                            round_count += 1
                            continue
                    case '冻结':
                        round_count += 1
                        continue

        #给当前回合玩家应用基础属性提升
        if current_user_in_session_basic_strengthen.empty != True:
            for strengthen_attribute in current_user_in_session_basic_strengthen.index:
                current_user_in_session_info[strengthen_attribute] *= 1 + current_user_in_session_basic_strengthen.at[strengthen_attribute, 'intensity']
                current_user_in_session_basic_strengthen.at[strengthen_attribute, 'duration'] -= 1
            #检测持续时间
            if current_user_in_session_basic_strengthen.at[strengthen_attribute, 'duration'] == -1:
                current_user_in_session_basic_strengthen.at[strengthen_attribute, 'intensity'] = 0

        form = '玩家 | 生命值 | 可用行动力\n' + host + ' | ' + str(host_in_session_info['HP']) + ' | ' + str(int(host_in_session_info['steps_per_round'])) + '\n' + guest + ' | ' + str(guest_in_session_info['HP']) + ' | ' + str(int(guest_in_session_info['steps_per_round']))
        await host_message.reply('当前状态：\n' + form)
        await host_message.reply(f'回合{round_count}，请{current_user}行动', mention_author = current_user_message.author)

        #定义检查函数
        def VerifyCurrentUser(message: qq.Message):
            return str(message.author) == current_user

        #获取用户操作
        while True:
            try:
                user_action_message: qq.Message = await self.wait_for(event = 'message', check = VerifyCurrentUser, timeout = 120)
            except:
                await host_message.reply(f'{current_user}超过2分钟没有回答，默认投降')
                return waiting_user, current_user
            #检查命令格式
            if '/' in user_action_message.content:
                user_action = user_action_message.content.split('##')[1].split()
                #再检查一遍
                if len(user_action) == 2:
                    action_type = user_action[0]
                    action_content = user_action[1]
                    match action_type:

                        case '武器':
                            weapon_name = action_content
                            if weapon_name in current_user_weapon_form.index:
                                #检查行动点
                                if current_user_in_session_info['steps_per_round'] >= current_user_weapon_form.at[weapon_name, 'weapon_step']:
                                    attack = 0
                                    current_user_in_session_info['steps_per_round'] -= current_user_weapon_form.at[weapon_name, 'weapon_step']
                                    if current_user_weapon_form.at[weapon_name, 'weapon_rarity'] == 'Legendary':
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

                                            #基础属性加成
                                            if index == 'attack':
                                                if random.uniform(0,1) <= weapon_detail.at['attack', 'chance']:
                                                    #对比攻击力加强的强度
                                                    if weapon_detail.at['attack', 'intensity'] >= current_user_in_session_basic_strengthen.at['attack', 'intensity']:
                                                        #更新
                                                        current_user_in_session_basic_strengthen.at['attack', 'intensity'] = weapon_detail.at['attack', 'intensity']
                                                        current_user_in_session_basic_strengthen.at['attack', 'duration'] = weapon_detail.at['attack', 'duration']

                                            #元素克制
                                            armor_elem = current_user_armor_form.at[current_user_armor, 'armor_element']
                                            weapon_elem_1 = weapon_detail.at['specific_attack', 'specific_elem_1']
                                            weapon_elem_2 = weapon_detail.at['specific_attack', 'specific_elem_2']
                                            if (armor_elem == weapon_elem_1 or armor_elem == weapon_elem_2) and str(armor_elem) != 'None':
                                                attack_elem = weapon_detail.at['specific_attack', 'intensity'] * current_user_in_game_info['basic_attack']
                                                attack = attack_elem
                                    
                                    #攻击力计算
                                    attack_weapon = current_user_weapon_form.at[weapon_name, 'weapon_attack']
                                    attack_strengthen = current_user_in_session_basic_strengthen.at['attack', 'intensity'] * current_user_in_game_info['basic_attack']
                                    attack_weaken = (waiting_user_in_session_info['defence'] + current_user_armor_form.at[current_user_armor, 'armor_defence']) * random.uniform(0.8, 1)
                                    attack_session = current_user_in_session_info['attack']
                                    attack += attack_weapon + attack_strengthen + attack_session
                                    #暴击率计算
                                    crit_rate = current_user_in_game_info['basic_crit_rate'] + current_user_armor_form.at[current_user_armor, 'armor_crit_rate']
                                    #计算是否触发暴击
                                    if random.uniform(0, 1) <= crit_rate:
                                        attack *= 1.5
                                        crit_sign = '暴击！'
                                    else:
                                        crit_sign = ''
                                    #应用伤害
                                    waiting_user_in_session_info['HP'] -= attack - attack_weaken
                                    await host_message.reply(crit_sign + current_user + '使用' + weapon_name + '对' + waiting_user + '造成了' + str(attack - attack_weaken) + '点伤害，step-' + str(current_user_weapon_form.at[weapon_name, 'weapon_step']))

                                else:
                                    await host_message.reply('攻击失败，行动点少于' + str(current_user_weapon_form.at[weapon_name, 'weapon_step']) + '[' + str(int(current_user_in_session_info['steps_per_round'])) + ']')
                            else:
                                await host_message.reply(f'未找到武器：{weapon_name}', mention_author = current_user_message.author)

                        case '物品':
                            item_name = action_content
                            if item_name in current_user_item_form.index:
                                #判断物品是否为药水
                                if '药水' in item_name:
                                        #判断行动点
                                        if current_user_in_session_info['steps_per_round'] >= current_user_item_form.at[item_name, 'item_step']:
                                            for attribute_affected in potion_index.columns:
                                                #应用药效
                                                current_user_in_session_info[attribute_affected] += potion_index.at[item_name, attribute_affected] * current_user_in_game_info['basic_' + attribute_affected]
                                            current_user_in_session_info['steps_per_round'] -= current_user_item_form.at[item_name, 'item_step']
                                            await host_message.reply(f'{current_user}使用了{item_name}，step-' + str(current_user_item_form.at[item_name, 'item_step']))
                                        else:
                                            await host_message.reply('使用失败，当前行动点少于' + str(current_user_item_form.at[item_name, 'item_step']) + '[' + str(current_user_in_session_info['steps_per_round']) + ']', mention_author = current_user_message.author)
                                else:
                                    #匹配特殊物品
                                    match item_name:
                                        case '净化之歌':
                                            if current_user_in_session_info['steps_per_round'] >= 3:
                                                current_user_in_session_effects = pandas.Series()
                                                current_user_in_session_info['steps_per_round'] -= 3
                                                await host_message.reply(f'{current_user}使用了净化之歌清除了所有效果，step-3')
                                            else:
                                                await host_message.reply('使用失败，当前行动点少于3[' + str(int(current_user_in_session_info['steps_per_round'])) + ']', mention_author = current_user_message.author)
                                                continue
                                        case '旺旺大礼包':
                                            await host_message.reply('物品不可用：旺旺大礼包', mention_author = current_user_message.author)
                                            continue
                                    break
                                #减物品
                                current_user_item_form.at[item_name, 'item_amount'] -= 1
                                #去除数量为0的物品
                                if current_user_item_form.at[item_name, 'item_amount'] == 0:
                                    current_user_item_form.drop(index = [item_name]).to_json('./Users/' + current_user + '_item_form.json', indent = 4, orient = 'index')
                            else:
                                await host_message.reply(f'未找到物品：{item_name}', mention_author = current_user_message.author)
                                continue

                        #技能也算一种物品
                        case '技能':
                            skill_name = action_content
                            #检查是否被选取
                            if skill_name in current_user_skill_form:
                                #检测行动点
                                if current_user_in_session_info['steps_per_round'] >= current_user_item_form.at[skill_name + '技能书', 'item_step']:
                                    #应用增强
                                    for strengthen_attribute in skill_index.columns:
                                        if skill_index.at[skill_name, strengthen_attribute] > 0:
                                            current_user_in_session_basic_strengthen.at[strengthen_attribute, 'intensity'] = skill_index.at[skill_name, strengthen_attribute]
                                            current_user_in_session_basic_strengthen.at[strengthen_attribute, 'duration'] = skill_index.at[skill_index, 'duration']
                                        elif skill_index.at[skill_name, strengthen_attribute] < 0:
                                            waiting_user_in_session_basic_strengthen.at[strengthen_attribute, 'intensity'] = skill_index.at[skill_name, strengthen_attribute]
                                            waiting_user_in_session_basic_strengthen.at[strengthen_attribute, 'duration'] = skill_index.at[skill_index, 'duration']
                                else:
                                    await host_message.reply('使用失败，当前行动点少于' + str(current_user_item_form.at[skill_name + '技能书', 'item_step']) + '[' + str(int(current_user_in_session_info['steps_per_round'])) + ']', mention_author = current_user_message.author)
                                    continue
                            else:
                                await host_message.reply(f'你未在本次对战中选取{skill_name}', mention_author = current_user_message.author)
                                continue
                        case _:
                            await host_message.reply('请输入正确的行动类型：武器 物品 技能', mention_author = user_action_message.author)
                            continue
                elif len(user_action) == 1:
                    if user_action[0] == '跳过':
                        await host_message.reply(f'{current_user}跳过了此回合')
                        break
                    else:
                        await host_message.reply('请输入有效的命令格式：/[武器/物品/技能] [名字]，或输入 /跳过 来结束此回合', mention_author = user_action_message.author)
                        continue
                else:
                    await host_message.reply('请输入有效的命令格式：/[武器/物品/技能] [名字]，或输入 /跳过 来结束此回合', mention_author = user_action_message.author)
                    continue
            else:
                await host_message.reply('请输入有效的命令格式：/[武器/物品/技能] [名字]，或输入 /跳过 来结束此回合', mention_author = user_action_message.author)
                continue
            await host_message.reply('你还剩' + str(int(current_user_in_session_info['steps_per_round'])) + '行动点')

            #胜负检查
            if waiting_user_in_session_info['HP'] <= 0:
                if round_count % 2 == 1:
                    return host, guest
                else:
                    return guest, host

        #重置行动力
        current_user_in_session_info['steps_per_round'] = current_user_in_game_info['steps_per_round'] - current_user_armor_form.at[current_user_armor, 'armor_step']

        round_count += 1
        #切换用户
        current_user_weapon_form, waiting_user_weapon_form = waiting_user_weapon_form, current_user_weapon_form
        current_user_item_form, waiting_user_item_form = waiting_user_item_form, current_user_item_form
        current_user_armor_form, waiting_user_armor_form = waiting_user_armor_form, current_user_armor_form
        current_user_armor, waiting_user_armor = waiting_user_armor, current_user_armor
        current_user_skill_form, waiting_user_skill_form = waiting_user_skill_form, current_user_skill_form
        current_user_in_game_info, waiting_user_in_game_info = waiting_user_in_game_info, current_user_in_game_info
        current_user_in_session_info, waiting_user_in_session_info = waiting_user_in_session_info, current_user_in_session_info
        current_user_in_session_effects, waiting_user_in_session_effects = waiting_user_in_session_effects, current_user_in_session_effects
        current_user_in_session_basic_strengthen, waiting_user_in_session_basic_strengthen = current_user_in_session_basic_strengthen, waiting_user_in_session_basic_strengthen
        current_user_message, waiting_user_message = waiting_user_message, current_user_message
        current_user, waiting_user = waiting_user, current_user


async def FightAward(winner, loser, message: qq.Message):
    #获取个人信息
    winner_in_game_info = pandas.read_json('./Users/' + winner + '_in_game_info.json', typ = 'series')
    loser_in_game_info = pandas.read_json('./Users/' + loser + '_in_game_info.json', typ = 'series')
    winner_basic_info = pandas.read_json('./Users/' + winner + '_basic_info.json', typ = 'series')
    loser_basic_info = pandas.read_json('./Users/' + loser + '_basic_info.json', typ = 'series')

    level_difference = winner_in_game_info['current_level'] - loser_in_game_info['current_level']
    #根据等级差计算奖励
    loser_sky_dust_amount = loser_basic_info['sky_dust_amount']
    
    if level_difference >= 10:
        sky_dust_changed = int(random.uniform(0.4, 0.5) * loser_sky_dust_amount)
        exp_changed = random.randint(10000, 15000)
    elif level_difference >=7:
        sky_dust_changed = int(random.uniform(0.35, 0.45) * loser_sky_dust_amount)
        exp_changed = random.randint(7500, 1000)
    elif level_difference >= 5:
        sky_dust_changed = int(random.uniform(0.3, 0.4) * loser_sky_dust_amount)
        exp_changed = random.randint(5000, 7500)
    elif level_difference >= 3:
        sky_dust_changed = int(random.uniform(0.25, 0.35) * loser_sky_dust_amount)
        exp_changed = random.randint(2500, 5000)
    else:
        sky_dust_changed = int(random.uniform(0.2, 0.3) * loser_sky_dust_amount)
        exp_changed = random.randint(1000, 2500)

    if sky_dust_changed < 70:
        sky_dust_changed = 70

    winner_basic_info['sky_dust_amount'] += sky_dust_changed
    winner_in_game_info['current_exp'] += exp_changed
    loser_basic_info['sky_dust_amount'] -= sky_dust_changed
    winner_basic_info.to_json('./Users/' + winner + '_basic_info.json', indent = 4)
    winner_in_game_info.to_json('./Users/' + winner + '_in_game_info.json', indent = 4)
    loser_basic_info.to_json('./Users/' + loser + '_basic_info.json', indent = 4)

    other_module.UpdateUserInGameInfo(winner)
    await message.reply(f'本次对战结束，{winner}胜利，获得{sky_dust_changed}个天空之尘和{exp_changed}点经验')