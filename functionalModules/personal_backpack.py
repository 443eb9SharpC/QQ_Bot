import qq
import pandas

import ToolModules.other_module as other_module

async def personalBackpack(message: qq.Message):
    user = str(message.author)
    try:
        user_weapon_form = pandas.read_json('./users/' + user + '_weapon_form.json', orient = 'index')
        user_item_form = pandas.read_json('./users/' + user + '_item_form.json', orient = 'index')
    except:
        await message.reply('获取失败，请先注册', mention_author = message.author)
        return
    res = ''
    #判断是否为空
    if user_weapon_form.empty == True and user_item_form.empty == True:
        await message.reply('你还没有获得过任何武器或物品', mention_author = message.author)
    else:
        if user_weapon_form.empty != True:
            res += other_module.convertToOutputForm(pandas_form = user_weapon_form, form_type = 'weapon')
        else:
            res += '你还没有获得任何武器\n'
        res += '\n'
        if user_item_form.empty != True:
            res += other_module.convertToOutputForm(pandas_form = user_item_form, form_type = 'item')
        else:
            res += '你还没有获得任何物品'
        await message.reply(res, mention_author = message.author)