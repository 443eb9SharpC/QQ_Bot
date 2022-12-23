import qq
import pandas

import ToolModules.other_module as other_module

async def Shop(message: qq.Message):
    user = str(message.author)
    command = message.content.split('/')[1]
    weapon_shop = pandas.read_json('./Shop/weapon_shop.json', orient = 'index')
    item_shop = pandas.read_json('./Shop/item_shop.json', orient = 'index')
    armor_shop = pandas.read_json('./Shop/armor_shop.json', orient = 'index')
    user_basic_info = pandas.read_json('./Users/' + user + '_basic_info.json', typ = 'series')
    match len(command):
        case 1:
            final_shop = other_module.ConvertToOutputForm(pandas_form = pandas.read_json('./Shop/weapon_shop.json', orient = 'index'), form_type = 'weapon', priceIncluded = True) + '\n' + other_module.ConvertToOutputForm(pandas_form = pandas.read_json('./Shop/item_shop.json' ,orient = 'index'), form_type = 'item', priceIncluded = True)
            await message.reply(final_shop + '\n\n输入 /商店 [武器/物品/盔甲] [名字] 即可购买', mention_author = message.author)
        case 2:
            await message.reply('请输入有效的命令：/商店 [武器/物品/盔甲] [名字]', mention_author = message.author)
        case 3:
            wanted_type = command[1]
            wanted_elem = command[2]

            #区分种类
            if wanted_type == '武器':
                #检查是否存在这个商品
                if wanted_elem in weapon_shop.index:
                    user_weapon_form = pandas.read_json('./Users/' + user + '_weapon_form.json', orient = 'index')
                    #检查是否重复购买
                    if wanted_elem in user_weapon_form.index:
                        await message.reply('请不要重复购买武器', mention_author = message.author)
                    else:
                        #检查大地之烬够不够
                        if user_basic_info['earth_dust_amount'] >= weapon_shop.at[wanted_elem, 'weapon_price']:
                            user_basic_info['earth_dust_amount'] -= weapon_shop.at[wanted_elem, 'weapon_price']
                            user_basic_info.to_json('./Users/' + user + '_basic_info.json', indent = 4, orient = 'index')
                            pandas.concat(objs = [user_weapon_form, pandas.DataFrame([[weapon_shop.at[wanted_elem, 'weapon_attack'], weapon_shop.at[wanted_elem, 'weapon_rarity'], weapon_shop.at[wanted_elem, 'weapon_rarity_raw'], weapon_shop.at[wanted_elem, 'weapon_step']]], columns = ['weapon_attack', 'weapon_rarity', 'weapon_rarity_raw'], index = [wanted_elem])]).to_json('./Users/' + user + '_weapon_form.json', indent = 4, orient = 'index')
                            await message.reply('购买' + wanted_elem + '成功，你可以 /个人背包 来查看', mention_author = message.author)
                        else:
                            await message.reply('该商品需要' + str(weapon_shop.at[wanted_elem, 'weapon_price']) + '个大地之烬，你还差' + str(weapon_shop.at[wanted_elem, 'weapon_price'] - user_basic_info['earth_dust_amount']) + '个大地之烬', mention_author = message.author)
                else:
                    await message.reply('未找到该商品，你可以输入 /商店 来查看有哪些商品')

            elif wanted_type == '物品':
                #检查是否存在这个商品
                if wanted_elem in item_shop.index:
                    #检查大地之烬够不够
                    if user_basic_info['earth_dust_amount'] >= item_shop.at[wanted_elem, 'item_price']:
                        user_basic_info['earth_dust_amount'] -= item_shop.at[wanted_elem, 'item_price']
                        user_item_form = pandas.read_json('./Users/' + user + '_item_form.json', orient = 'index')
                        #检查是否重复购买
                        if wanted_elem in user_item_form.index:
                            user_item_form.at[wanted_elem, 'item_amount'] += item_shop.at[wanted_elem, 'item_amount']
                            user_item_form.to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
                        else:
                            user_item_form.to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
                            pandas.concat(objs = [user_item_form, pandas.DataFrame([[item_shop.at[wanted_elem, 'item_amount'], item_shop.at[wanted_elem, 'item_rarity'], item_shop.at[wanted_elem, 'item_rarity_raw'], item_shop.at[wanted_elem, 'item_step']]], columns = ['item_amount', 'item_rarity', 'item_rarity_raw'], index = [wanted_elem])]).to_json('./Users/' + user + '_item_form.json', indent = 4, orient = 'index')
                        user_basic_info.to_json('./Users/' + user + '_basic_info.json', indent = 4)
                        await message.reply('购买' + wanted_elem + '成功，你可以 /个人背包 来查看', mention_author = message.author)
                    else:
                        await message.reply('该商品需要' + str(item_shop.at[wanted_elem, 'item_price']) + '个大地之烬，你还差' + str(item_shop.at[wanted_elem, 'item_price'] - user_basic_info['earth_dust_amount']) + '个大地之烬', mention_author = message.author)
                else:
                    await message.reply('未找到该商品，你可以输入 /商店 来查看有哪些商品')

            elif wanted_type == '盔甲':
                if wanted_elem in armor_shop.index:
                    user_armor_form = pandas.read_json('./User/' + user + '_armor_form.json', orient = 'index')
                    if wanted_elem in user_armor_form.index:
                        await message.reply('请不要重复购买盔甲', mention_author = message.author)
                    else:
                        if user_basic_info['earth_dust_amount'] >= armor_shop.at[wanted_elem, 'armor_price']:
                            user_basic_info['earth_dust_amount'] -= armor_shop.at[wanted_elem, 'weapon_price']
                            user_basic_info.to_json('./Users/' + user + '_basic_info.json', indent = 4, orient = 'index')
                            pandas.concat(objs = [user_armor_form, pandas.DataFrame([[armor_shop.at[wanted_elem, 'armor_defence'], armor_shop.at[wanted_elem, 'armor_rarity'], armor_shop.at[wanted_elem, 'armor_rarity_raw'], armor_shop.at[wanted_elem, 'armor_step']]], columns = ['armor_defence', 'armor_rarity', 'armor_rarity_raw'], index = [wanted_elem])]).to_json('./Users/' + user + '_armor_form.json', indent = 4, orient = 'index')
                            await message.reply('购买' + wanted_elem + '成功，你可以 /个人背包 来查看', mention_author = message.author)
                        else:
                            await message.reply('该商品需要' + str(armor_shop.at[wanted_elem, 'armor_price']) + '个大地之烬，你还差' + str(armor_shop.at[wanted_elem, 'armor_price'] - user_basic_info['earth_dust_amount']) + '个大地之烬', mention_author = message.author)
                else:
                    await message.reply('未找到该商品，你可以输入 /商店 来查看有哪些商品')

            else:
                await message.reply('请输入有效的商品类型：武器或物品')