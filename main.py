#coding = utf-8
import qq
from config import appid, token
import logging
import traceback

from FunctionalModules.menu import menu
from FunctionalModules.register import register
from FunctionalModules.personal_info import personalInfo
from FunctionalModules.personal_backpack import personalBackpack
from FunctionalModules.sign import sign
from FunctionalModules.activity import activity
from FunctionalModules.gacha_once import gachaOnce
from FunctionalModules.gacha_ten_times import gachaTenTimes
from FunctionalModules.shop import shop
#from FunctionalModules.fight import fight
#from FunctionalModules.guessing import guessing
from FunctionalModules.help import help
from FunctionalModules.devtool import devtool

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

            if message.channel.id != 13630884 and str(message.author) != '443eb9#C' and '##' in message.content:
                await message.reply('请不要使用开发模式下的命令', mention_author = message.author)
                return
            
            if message.channel.id == 11672109:
                await message.reply('请不要在制造站使用机器人', mention_author = message.author)
                return

            # if message.channel.id == 13630884:
            #     await message.reply('请不要在工程部使用机器人', mention_author = message.author)
            #     return

            if '##菜单' in message.content:
                await menu(message)

            if '##注册' in message.content:
                await register(message)

            if '##个人信息' in message.content:
                await personalInfo(message)

            if '##个人背包' in message.content:
                await personalBackpack(message)

            if '##签到' in message.content:
                await sign(message)

            if '##活动' in message.content:
                await activity(message)

            if '##单抽' in message.content:
                await gachaOnce(message)

            if '##十连抽' in message.content:
                await gachaTenTimes(message)

            if '##商店' in message.content:
                await shop(message)

            if '##对战' in message.content:
                await message.reply('此功能正在开发中（Upgrading），请耐心等待', mention_author = message.author)
                #await fight(self, message)

            if '##猜题' in message.content:
                await message.reply('此功能正在开发中（Delayed），请耐心等待', mention_author = message.author)
                #await guessing(self, message)

            if '##帮助' in message.content:
                await help(message)

            if '##devtool' in message.content:
                await devtool(message)

        except:
            await message.reply('\n发生异常:\n' + traceback.format_exc(), mention_author = message.author)
            print(traceback.format_exc())

client = MyClient()
client.run(token = f'{appid}.{token}')