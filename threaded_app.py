from threading import Thread

import bot


bot_thread = Thread(target=bot.launch)
bot_thread.start()
bot_thread.join()
