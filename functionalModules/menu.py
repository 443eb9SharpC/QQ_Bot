import qq

async def Menu(message: qq.Message):
    menu_file = open('./Texts/menu.txt', mode = 'r', encoding = 'utf8')
    menu = menu_file.read()
    menu_file.close()
    await message.reply(menu, mention_author=message.author)