import qq
import pandas

import ToolModules.other_module as other_module

async def PersonalBackpack(message: qq.Message):
    user = str(message.author)
    try:
        user_weapon_form = pandas.read_json('./Users/' + user + '_weapon_form.json', orient = 'index')
        user_item_form = pandas.read_json('./Users/' + user + '_item_form.json', orient = 'index')
        user_armor_form = pandas.read_json('./Users/' + user + '_armor_form.json', orient = 'index')
    except:
        await message.reply('获取失败，请先注册', mention_author = message.author)
        return
    #判断是否为空
    try:
        command = message.content.split('/')[1].split()
    except:
        await message.reply('请输入有效的命令：/个人背包 [武器/物品/盔甲] [整理]')
    else:
        match len(command):
            case 2:
                match command[1]:
                    case '武器':
                        if user_weapon_form.empty != True:
                            result = other_module.ConvertToOutputForm(pandas_form = user_weapon_form, form_type = 'weapon')
                        else:
                            result = '你还没有获得任何武器\n'
                    case '物品':
                        if user_item_form.empty != True:
                            result = other_module.ConvertToOutputForm(pandas_form = user_item_form, form_type = 'item')
                        else:
                            result = '你还没有获得任何物品'
                    case '盔甲':
                        if user_armor_form.empty != True:
                            result = other_module.ConvertToOutputForm(pandas_form = user_armor_form, form_type = 'armor')
                        else:
                            result = '你还没有获得任何盔甲'
                    case _:
                        result = '请输入有效的命令：/个人背包 [武器/物品/盔甲] [整理]'
            case 3:
                if command[2] == '整理':
                    match command[1]:
                        case '武器':
                            user_weapon_form.sort_values(by = ['weapon_rarity_raw']).to_json('./Users/' + user + '_weapon_form.json', indent = 4, orient = 'index')
                        case '物品':
                            user_item_form.sort_values(by = ['item_rarity_raw']).to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
                        case '盔甲':
                            user_armor_form.sort_values(by = ['armor_rarity_raw']).to_json('./Users/' + user + '_armor_form.json', indent = 4, orient = 'index')
                        case _:
                            result = '请输入有效的命令：/个人背包 [武器/物品/盔甲] [整理]'
                            return
                    result = '整理完成'
                else:
                    result = '请输入有效的命令：/个人背包 [武器/物品/盔甲] [整理]'
            case _:
                result = '请输入有效的命令：/个人背包 [武器/物品/盔甲] [整理]'
    await message.reply(result, mention_author = message.author)