
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import random
import configparser

CONF=configparser.ConfigParser()
CONF.read('config.ini')
TOKEN=CONF['KEYS']['TOKEN']
BOT_USERNAME=CONF['KEYS']['NAME']


FILE=open('final.txt','r')

PARSED_FILE=FILE.read().split('\n')
LENGTH=len(PARSED_FILE)

async def start(update:Update,context:ContextTypes):
    await update.message.reply_text('Hello World!')



async def help(update:Update,context:ContextTypes):
    await update.message.reply_text('Help!')

async def code(update:Update,content:ContextTypes):
    await update.message.reply_text(f'LeetCode question is:https://leetcode.com{PARSED_FILE[random.randint(0,LENGTH)]}')





def handle_response(text:str)->str:
    processed:str=text.lower().strip()
    if "hello" in processed or "hi" in processed:
        return "WHY!"

    return "I don't understand you!"   



async def handle_message(update:Update,context:ContextTypes):
    message_type:str=update.message.chat.type
    text:str=update.message.text

    print(f"USer:{update.message.chat.id} | Type:{message_type} | Text:{text}")

    if(message_type=="group"):
        if(BOT_USERNAME in text):
            new_text:str=text.replace(BOT_USERNAME,'').strip()
            response:str=handle_response(new_text)
        else:
            return
    else:
        response:str=handle_response(text)        


    print(f"BOT:{response}")    
    await update.message.reply_text(response)


async def error(update:Update,context:ContextTypes):
    print(f"Update:{update} caused error :{context.error}")

    


if __name__ =='__main__':
    print("starting.....")
    app=Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('help',help))
    app.add_handler(CommandHandler('code',code))
    

    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_error_handler(error)

    print("polling")
    app.run_polling(poll_interval=3)
