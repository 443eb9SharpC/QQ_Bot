#coding = utf-8
import qq
import pandas
from config import appid, token
import logging
import traceback

from functionalModules.menu import menu
from functionalModules.register import register
from functionalModules.personalInfo import personalInfo
from functionalModules.personalBackpack import personalBackpack
from functionalModules.sign import sign
from functionalModules.activity import activity
from functionalModules.gachaOnce import gachaOnce
from functionalModules.gachaTenTimes import gachaTenTimes
from functionalModules.shop import shop
from functionalModules.fight import fight
from functionalModules.help import help
from functionalModules.devtool import devtool

logging.basicConfig(level = logging.DEBUG)

class MyClient(qq.Client):
    async def on_ready(self):
        print(f'以 {self.user} 身份登录（ID：{self.user.id}）')
        print('------')

    async def on_message(self, message: qq.Message):
        try:
            # 我们不希望机器人回复自己
            if message.author.id == self.user.id:
                return

            if message.channel.id == 11672109:
                await message.reply('请不要在制造站使用机器人', mention_author = message.author)
                return

            if message.channel.id == 13630884:
                await message.reply('请不要在工程部使用机器人', mention_author = message.author)
                return

            if '/菜单' in message.content:
                await menu(message)

            if '/注册' in message.content:
                await register(message)

            if '/个人信息' in message.content:
                await personalInfo(message)

            if '/个人物品' in message.content:
                await personalBackpack(message)

            if '/签到' in message.content:
                await sign(message)

            if '/活动' in message.content:
                await activity(message)

            if '/单抽' in message.content:
                await gachaOnce(message)

            if '/十连抽' in message.content:
                await gachaTenTimes(message)

            if '/商店' in message.content:
                await shop(message)

            if '/对战' in message.content:
                await fight(self, message)

            if '/帮助' in message.content:
                await help(message)

            if '/devtool' in message.content:
                await devtool(message)

        except:
            await message.reply('\n发生异常:\n' + traceback.format_exc(), mention_author = message.author)
            print(traceback.format_exc())

client = MyClient()
client.run(token = f'{appid}.{token}')