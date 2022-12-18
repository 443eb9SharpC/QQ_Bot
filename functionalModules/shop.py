import qq
import pandas

import toolModules.otherModule as otherModule

async def shop(message: qq.Message):
    user = str(message.author)
    command = message.content.split('||')
    weaponShop = pandas.read_json('./shop/weaponShop.json', orient = 'index')
    itemShop = pandas.read_json('./shop/itemShop.json' ,orient = 'index')
    userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
    match len(command):
        case 1:
            finalShop = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./shop/weaponShop.json', orient = 'index'), f_formType = 'weapon', f_priceIncluded = True) + '\n' + otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./shop/itemShop.json' ,orient = 'index'), f_formType = 'item', f_priceIncluded = True)
            await message.reply(finalShop + '\n\n输入 /商店||[武器/物品]||[名字] 即可购买', mention_author = message.author)
        case 2:
            await message.reply('请输入有效的命令：/商店||[武器/物品]||[名字]', mention_author = message.author)
        case 3:
            wantedType = command[1]
            wantedElem = command[2]
            #区分种类
            if wantedType == '武器':
                #检查是否存在这个商品
                if wantedElem in weaponShop.index:
                    userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                    #检查是否重复购买
                    if wantedElem in userWeaponForm.index:
                        await message.reply('请不要重复购买武器', mention_author = message.author)
                    else:
                        #检查大地之烬够不够
                        if userBasicInfo['earthDustAmount'] >= weaponShop.at[wantedElem, 'weaponPrice']:
                            userBasicInfo['earthDustAmount'] -= weaponShop.at[wantedElem, 'weaponPrice']
                            userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4,orient = 'index')
                            pandas.concat(objs = [userWeaponForm, pandas.DataFrame([[weaponShop.at[wantedElem, 'weaponAttack'], weaponShop.at[wantedElem, 'weaponRarity'], weaponShop.at[wantedElem, 'weaponRarityRaw']]], columns = ['weaponAttack', 'weaponRarity', 'weaponRarityRaw'], index = [wantedElem])]).to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
                            await message.reply('购买' + wantedElem + '成功，你可以 /个人背包 来查看', mention_author = message.author)
                        else:
                            await message.reply('该商品需要' + str(weaponShop.at[wantedElem, 'weaponPrice']) + '个大地之烬，你还差' + str(weaponShop.at[wantedElem, 'weaponPrice'] - userBasicInfo['earthDustAmount']) + '个大地之烬', mention_author = message.author)
                else:
                    await message.reply('未找到该商品，你可以输入 /商店 来查看有哪些商品')
            elif wantedType == '物品':
                #检查是否存在这个商品
                if wantedElem in itemShop.index:
                    #检查大地之烬够不够
                    if userBasicInfo['earthDustAmount'] >= itemShop.at[wantedElem, 'itemPrice']:
                        userBasicInfo['earthDustAmount'] -= itemShop.at[wantedElem, 'itemPrice']
                        userItemForm = pandas.read_json('./users/' + user + '_itemForm.json', orient = 'index')
                        #检查是否重复购买
                        if wantedElem in userItemForm.index:
                            userItemForm.at[wantedElem, 'itemAmount'] += itemShop.at[wantedElem, 'itemAmount']
                            userItemForm.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
                        else:
                            userItemForm.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
                            pandas.concat(objs = [userItemForm, pandas.DataFrame([[itemShop.at[wantedElem, 'itemAmount'], itemShop.at[wantedElem, 'itemRarity'], itemShop.at[wantedElem, 'itemRarityRaw']]], columns = ['itemAmount', 'itemRarity', 'itemRarityRaw'], index = [wantedElem])]).to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
                        userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)
                        await message.reply('购买' + wantedElem + '成功，你可以 /个人背包 来查看', mention_author = message.author)
                    else:
                        await message.reply('该商品需要' + str(itemShop.at[wantedElem, 'itemPrice']) + '个大地之烬，你还差' + str(itemShop.at[wantedElem, 'itemPrice'] - userBasicInfo['earthDustAmount']) + '个大地之烬', mention_author = message.author)
                else:
                    await message.reply('未找到该商品，你可以输入 /商店 来查看有哪些商品')
            else:
                await message.reply('请输入有效的商品类型：武器或物品')