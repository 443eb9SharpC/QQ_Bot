import qq
import pandas

async def devtool(message: qq.Message):
    #判断身份
    if str(message.author) == '443eb9#C':
        command = message.content.split('||')
        #判断命令
        try:
            #修改指定用户的天空之尘
            if command[1] == 'modifysky_dust_amount':
                user = command[2]
                try:
                    user_basic_info = pandas.read_json('./users/' + user + '_basic_info.json', typ = 'series')
                except:
                    await message.reply('Unknow user: ' + command[2])
                    return
                user_basic_info['sky_dust_amount'] = int(command[3])
                user_basic_info.to_json('./users/' + user + '_basic_info.json', indent = 4, orient = 'index')
                await message.reply('Successfully modified ' + str(command[2]) + '\'s sky dust amount.')
            #展示指定用户个人信息
            if command[1] == 'showBasicInfoFull':
                try:
                    user_basic_info = pandas.read_json('./users/' + user + '_basic_info.json', typ = 'series')
                except:
                    await message.reply('Unknow user: ' + str(command[2]))
                    return
                await message.reply(user_basic_info)
                return
            #显示帮助
            elif command[1] == 'help':
                help_file = open('./texts/commandHelp.txt', mode = 'r' ,encoding = 'utf8')
                help = help_file.read()
                await message.reply(help, mention_author = message.author)
            #无效命令判断
            else:
                await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
        except:
            await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
    else:
        await message.reply('Authentication Failed')