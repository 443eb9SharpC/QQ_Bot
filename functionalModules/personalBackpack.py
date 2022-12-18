import qq
import pandas

import toolModules.otherModule as otherModule

async def personalBackpack(message: qq.Message):
    user = str(message.author)
    try:
        userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
        userItemForm = pandas.read_json('./users/' + user + '_itemForm.json', orient = 'index')
    except:
        await message.reply('获取失败，请先注册', mention_author = message.author)
        return
    res = ''
    #判断是否为空
    if userWeaponForm.empty == True and userItemForm.empty == True:
        await message.reply('你还没有获得过任何武器或物品', mention_author = message.author)
    else:
        if userWeaponForm.empty != True:
            res += otherModule.convertToOutputForm(f_pandasForm = userWeaponForm, f_formType = 'weapon')
        else:
            res += '你还没有获得任何武器\n'
        res += '\n'
        if userItemForm.empty != True:
            res += otherModule.convertToOutputForm(f_pandasForm = userItemForm, f_formType = 'item')
        else:
            res += '你还没有获得任何物品'
        await message.reply(res, mention_author = message.author)