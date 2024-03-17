from fastapi import FastAPI
# from routes.route import router
from routes.auth import authRoute
from routes.mail import mailRoute
from routes.bot import botRoute
# from telegram.ext import *
from fastapi.middleware.cors import CORSMiddleware
# import Constants as keys
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(router)
app.include_router(authRoute)
app.include_router(mailRoute)
app.include_router(botRoute)


# token="6530501862:AAHn2PpBLrAy-LgZJZFXz8OdoSRK62_-HJM"

# def start_command(update,context):
#     text=str(update.message.text).lower()
#     update.message.reply_text("This is an automated message")
# updater=Updater(token,)
# dp=updater.dispatcher
# dp.add_handler(CommandHandler("start",start_command))
# updater.start_polling()
# updater.idle()
