import qq
import pandas

"""
Delayed WIP
"""

async def guessing(self: qq.Client, message: qq.Message):
    command = message.content.split()
    try:
        questionType = command[1]
    except:
        await message.reply('请输入有效的命令：/猜题 [题库类型]，或输入 /帮助 猜题 来获得详细帮助', mention_author = message.author)
        return
    #匹配问题种类
    match questionType:
        case 'MC':
            questionItem = pandas.read_json('./questions/questionItem/minecraft.json', typ = 'series').sample(n = 1)
            itemID = questionItem.index[0]
            item_name = questionItem.values[0]
            questionDetail = pandas.read_json('./questions/questionDetail/' + itemID + '.json', typ = 'series')
        case '题库':
            await message.reply('当前题库：\nMC', mention_author = message.author)
        case _:
            await message.reply('没有你想找的题库，请检查你的题库名字，或输入 /猜题 题库 来查看可用的题库类型', mention_author = message.author)
    await message.reply('你选择了MC的题库', mention_author = message.author)
    #正式开始
    detailShowed, answer: qq.Message = guessingGame(self = self, message = message, item_name = item_name, questionDetail = questionDetail)
    #判断是否是超时结束
    if detailShowed == 'timeout':
        await message.reply('超出5分钟没有人回答，游戏已结束', mention_author = message.author)
        return
    winner = str(answer.author)
    user_basic_info = pandas.read_json('./users/' + winner + '_basic_info.json', typ = 'series')
    #奖励计算
    skyDustAwarded = 500 - detailShowed * 20
    if skyDustAwarded <= 100:
        skyDustAwarded = 100
    await answer.reply('恭喜你回答正确，获得' + skyDustAwarded + '天空之尘', mention_author = answer.author)
    user_basic_info['sky_dust_amount'] += skyDustAwarded
    user_basic_info.to_json('./users/' + winner + '_basic_info.json', indent = 4)


async def guessingGame(self: qq.Client, message: qq.Message, item_name, questionDetail: pandas.DataFrame):
    detailShowed = 0
    while True:
        #抽取提示
        detail = questionDetail.sample(n = 1)
        questionDetail.drop(detail.index, inplace = True)
        await message.reply(detail, mention_author = message.author)
        detailShowed += 1
        while True:
            try:
                answer: qq.Message = await self.wait_for(event = 'message', check = verify, timeout = 300)
            except:
                return 'timeout', message
            answerItem = answer.content.split()[2]
            #检查回答是否正确
            if answerItem == item_name:
                return detailShowed, answer
            else:
                await message.reply('回答错误', mention_author = message.author)


async def verify(message: qq.Message):
    command = message.content.split()
    if len(command) != 3:
        await message.reply('请输入有效的命令：我猜是 [你的答案]', mention_author = message.author)
        return False
    return command[1] == '我猜是'