#coding = utf-8
import qq
from config import appid, token
import logging
import traceback

from FunctionalModules.menu import Menu
from FunctionalModules.register import Register
from FunctionalModules.personal_info import PersonalInfo
from FunctionalModules.personal_backpack import PersonalBackpack
from FunctionalModules.sign import Sign
from FunctionalModules.activity import Activity
from FunctionalModules.gacha_once import GachaOnce
from FunctionalModules.gacha_ten_times import GachaTenTimes
from FunctionalModules.shop import Shop
from FunctionalModules.fight import Fight
#from FunctionalModules.guessing import guessing
from FunctionalModules.help import Help
from FunctionalModules.devtool import Devtool

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
                await Menu(message)

            if '##注册' in message.content:
                await Register(message)

            if '##个人信息' in message.content:
                await PersonalInfo(message)

            if '##个人背包' in message.content:
                await PersonalBackpack(message)

            if '##签到' in message.content:
                await Sign(message)

            if '##活动' in message.content:
                await Activity(message)

            if '##单抽' in message.content:
                await GachaOnce(message)

            if '##十连抽' in message.content:
                await GachaTenTimes(message)

            if '##商店' in message.content:
                await Shop(message)

            if '##对战' in message.content:
                await message.reply('ATTENTION:此功能正处于测试状态，可能会存在未修复的bug', mention_author = message.author)
                await Fight(self, message)

            if '##猜题' in message.content:
                await message.reply('此功能正在开发中（Delayed），请耐心等待', mention_author = message.author)
                #await Guessing(self, message)

            if '##帮助' in message.content:
                await Help(message)

            if '##devtool' in message.content:
                await Devtool(message)

        except:
            await message.reply('\n发生异常:\n' + traceback.format_exc(), mention_author = message.author)
            print(traceback.format_exc())

client = MyClient()
client.run(token = f'{appid}.{token}')