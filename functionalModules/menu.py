import qq

async def menu(message: qq.Message):
    menu_file = open('./texts/menu.txt', mode = 'r', encoding = 'utf8')
    menu = menu_file.read()
    menu_file.close()
    await message.reply(menu, mention_author=message.author)