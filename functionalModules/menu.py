import qq

async def menu(message: qq.Message):
    menuFile = open('./texts/menu.txt', mode = 'r', encoding = 'utf8')
    menu = menuFile.read()
    menuFile.close()
    await message.reply(menu, mention_author=message.author)