from fastapi import FastAPI,HTTPException,Depends
from aiogram import Dispatcher,Router,Bot
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update,Message,CallbackQuery
from fastapi import Request
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
token = '7765823701:AAHOvzXghdY3JE2t3VUJ7gvEOGH_E1m4-5k'
WEB_HOOK = 'https://peniel-bot-code-9aptqrjig-williams-projects-41e575ef.vercel.app/webhook'
bot=Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp= Dispatcher(bot)
router = Router()
dp.include_router(router)

#NOTE - startup package for the server
@asynccontextmanager
async def lifespan(app:FastAPI):
    await bot.set_webhook(WEB_HOOK)
    logger.info("Webhook has been set.")
    yield
    await bot.session.close()

#NOTE - Fastapi initialization 
app = FastAPI(lifespan=lifespan,title="William's Fraud",debug=True)


def main_menu()->InlineKeyboardMarkup:
    btn1= InlineKeyboardButton(text='Enter wetin dey your mind',url='wetin dey your mind WIlliam',callback_data='Your mind')
    btn2= InlineKeyboardButton(text='Fraudster enter your mind',url='Your mind',callback_data='Your mind')
    builder = InlineKeyboardBuilder()
    builder.row(btn1,btn2)
    return builder.as_markup()
    
@router.message(CommandStart())
async def start_command(msg:Message)-> None:
    await bot.send_message(chat_id=msg.from_user.id,text='wrt your mind',reply_markup=main_menu())
    
@router.callback_query()
async def handle_it(callback_query:CallbackQuery):
    #TODO- Handle callback where neccesary
    ...

@app.post('/webhook')
async def handle_webhook(request:Request):
    try:
        json_data = await request.json()
        update = Update(**json_data)
        await dp.feed_update(bot,update)
    except Exception:
        return HTTPException(status_code=400,detail='Invalid payload')
    return {'OK':True}
