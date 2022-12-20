import qq

async def help(message: qq.Message):
    command = message.content.split()
    try:
        moduleName = command[1]
    except:
        await message.reply('请输入正确格式的命令：/帮助||[模块名称]', mention_author = message.author)
        return
    match moduleName:
        case '菜单':
            await message.reply('展示菜单', mention_author = message.author)
        case '注册':
            await message.reply('注册账号，除菜单外一切模块的前提是要有账号', mention_author = message.author)
        case '个人信息':
            await message.reply('展示你有的天空之尘数量，总计签到天数，大地之烬数量，连续签到天数', mention_author = message.author)
        case '个人物品':
            await message.reply('展示你有的所有武器和物品', mention_author = message.author)
        case '签到':
            await message.reply('签到操作，每日签到给10天空之尘，连续签到3天后，从第4天开始，每天签到额外给5天空之尘，每30天一个周期', mention_author = message.author)
        case '活动':
            await message.reply('展示当前正在进行的活动，即卡池', mention_author = message.author)
        case '单抽':
            await message.reply('消耗100天空之尘进行一次单抽，重复获得的每个武器会被转换成25大地之烬，大地之烬可以在商店兑换物品。出货权重：\n0.1 Legendary, 0.2 Epic, 0.3 Rare, 0.4 Common\n其中1/3概率为武器，2/3概率为物品', mention_author = message.author)
        case '十连抽':
            await message.reply('消耗1000天空之尘一次性进行10次单抽', mention_author = message.author)
        case '对战':
            await message.reply(open('./texts/help/fight.txt', mode = 'r', encoding = 'utf8').read(), mention_author = message.author)
        case '猜题':
            await message.reply(open('./texts/help/guessing.txt', mode = 'r', encoding = 'utf8').read(), mention_author = message.author)
        case '帮助':
            await message.reply('使用方法：\n/帮助||[模块名称]\n显示各模块的详细说明', mention_author = message.author)
        case _:
            await message.reply('未找到此模块', mention_author = message.author)