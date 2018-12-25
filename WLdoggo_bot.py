from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
from bs4 import BeautifulSoup
import praw, random
from telegram import ChatAction
from functools import wraps
import os

LIST_OF_ADMINS = ["246483057"]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

@restricted
def my_handler(bot, update):
    pass  # only accessible if `user_id` is in `LIST_OF_ADMINS`.


TOKEN = "655656312:AAEv54Q9OTxZXrqVWMetHM-j60hPaBFVxsU"
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://<doggo-bot-wl>.herokuapp.com/" + TOKEN)
updater.idle()



reddit = praw.Reddit(client_id='VbyvQMoXEEqDTg', 
                     client_secret='9ajN1x4d8WESSCWoJLrOOvhq2hw',
                     user_agent='Reddit_Scraping',
                     username='JS075',
                     password='yaorenzhen07')

def get_EarthPorn_url():
    subreddit = reddit.subreddit('EarthPorn')
    top_subreddit = subreddit.top(limit=800)   # Might take a while to get image!!
    random_post_number = random.randint(0,800)
    for i, post in enumerate(top_subreddit):
        if i == random_post_number:
            url = post.url
            title = post.title
            return url, title

def EarthPorn(bot, update):
    url, title = get_EarthPorn_url()
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = 'upload_photo')
    bot.send_photo(chat_id = chat_id, photo = url, caption = title)
    

def joke(bot, update):
    url = "https://icanhazdadjoke.com/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    soup.prettify()
    meta_tag = soup.find('meta', attrs = {'name': 'twitter:description'})
    joke = meta_tag['content']
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.TYPING)
    bot.sendMessage(chat_id = chat_id, text = joke)

def start(bot, update):
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.TYPING)
    bot.sendMessage(chat_id = chat_id, text = "I'm a bf bot on behalf of JS, what can I do for you?")

def quote(bot, update):
    contents = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en").json()
    quote = contents["quoteText"]
    quote_author = contents["quoteAuthor"]
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.TYPING)
    bot.sendMessage(chat_id = chat_id, text = quote + "\n" + quote_author + "\nStill feeling down? Talk to JS directly @JS075")

def shibe(bot, update):
    contents = requests.get("http://shibe.online/api/shibes?count=1").json()
    cute = contents[0]
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.UPLOAD_PHOTO)
    bot.send_photo(chat_id = chat_id, photo = cute)


def get_cat_url():
    contents = requests.get("https://api.thecatapi.com/v1/images/search").json()
    url = contents[0]["url"]
    return url

def get_cat_image_url():
    allowed_extensions = ["jpg"]
    file_extension = " "
    while file_extension not in allowed_extensions:
        url = get_cat_url()
        # If a regex group matches multiple times, only the last match is accessible:
        file_extension = re.search("([^.]*)$",url).group(1).lower()  
    return url

def meow(bot, update):
    url = get_cat_image_url()
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.UPLOAD_PHOTO)
    bot.send_photo(chat_id = chat_id, photo = url)

################# 

def get_url():
    contents = requests.get("https://random.dog/woof.json").json()
    url = contents["url"]
    return url

def get_image_url():
    allowed_extensions = ["jpg","jpeg",'png']
    file_extension = " "
    while file_extension not in allowed_extensions:
        url = get_url()
        # If a regex group matches multiple times, only the last match is accessible:
        file_extension = re.search("([^.]*)$",url).group(1).lower()  
    return url

def dog(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.UPLOAD_PHOTO)
    bot.send_photo(chat_id = chat_id, photo = url)


def get_gif_url():
    allowed_extensions = ["gif"]
    file_extension = " "
    while file_extension not in allowed_extensions:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url
      
def gif(bot, update):
    url = get_gif_url()
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id = chat_id, action = ChatAction.UPLOAD_VIDEO)
    bot.send_animation(chat_id = chat_id, animation = url)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Arf-arf, I don't understand that command.")


def main():
    updater = Updater('655656312:AAEv54Q9OTxZXrqVWMetHM-j60hPaBFVxsU')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('shibe', shibe))
    dp.add_handler(CommandHandler('dog',dog))
    dp.add_handler(CommandHandler('gif', gif))
    dp.add_handler(CommandHandler('meow', meow))
    dp.add_handler(CommandHandler('quote', quote))
    dp.add_handler(CommandHandler('joke', joke))
    dp.add_handler(CommandHandler('EarthPorn', EarthPorn))     # filtering all commands not recognised by previous handlers and regard as 'unknown'
    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)
    # start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()