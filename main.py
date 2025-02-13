from fastapi import FastAPI, HTTPException, Request
from aiogram import Dispatcher, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from contextlib import asynccontextmanager
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Bot Token (Make sure this is correct)
TOKEN = '7765823701:AAHOvzXghdY3JE2t3VUJ7gvEOGH_E1m4-5k'
WEB_HOOK = 'https://wills-birthday-gift.onrender.com/webhook'

# Initialize bot with default properties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Create Dispatcher and Router
dp = Dispatcher(bot=bot)
router = Router()
dp.include_router(router)

# FastAPI startup event: Sets up webhook when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEB_HOOK)
    logger.info("Webhook has been set.")
    yield
    await bot.session.close()

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan, title="William Bot", debug=True)

# Function to generate the main menu inline keyboard
def main_menu() -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(text='About', callback_data='about')
    btn2 = InlineKeyboardButton(text='Launch app', url='https://t.me/btcforge_miner_bot/Btcsha256')
    
    builder = InlineKeyboardBuilder()
    builder.row(btn1, btn2)  # Buttons on the same row
    return builder.as_markup()

# Handle /start command
@router.message(CommandStart())
async def start_command(msg: Message) -> None:
    await bot.send_message(
        chat_id=msg.from_user.id,
        text='''
<b>Bot Minero SHA-256 BTC</b>

Este avanzado bot minero aprovecha el algoritmo SHA-256 para generar Bitcoin directamente desde tu billetera. Utiliza los BTC que ya están presentes en tu billetera como recurso para facilitar y acelerar el proceso de minería🚀🪙

<b>Características principales:</b>

✅ Minería basada en blockchain: utiliza el algoritmo SHA-256 para una minería segura y eficiente⛏️  
✅ Proceso integrado en la billetera: requiere un saldo de BTC existente para iniciar la minería⛏️  
✅ Actividad en tiempo real: si no hay BTC disponibles, el bot no minará, incluso si aparece actividad minera en la interfaz✅  

⚠️ Para obtener resultados óptimos, asegúrate de que tu billetera tenga un saldo de BTC suficiente antes de comenzar el proceso de minería. ⚠️  
''',
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

# Handle callback queries (button clicks)
@router.callback_query()
async def callback_query_handler(callback_query: CallbackQuery):
    """
    Handles inline button clicks.
    When "About" button is clicked, sends an informational message with a forward/share button.
    """
    if callback_query.data == 'about':
        # Always answer the callback query first
        await callback_query.answer()

        # Create the "Share with Friends" button
        forward_btn = InlineKeyboardButton(
            text="📤 Share with Friends",
            switch_inline_query="Check out this BTC mining bot! 🚀 https://t.me/btcforge_miner_bot"
        )

        builder = InlineKeyboardBuilder()
        builder.row(forward_btn)  # Adds the button

        # Send the response message
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="<b>ℹ️ About the Bot:</b>\n\nThis advanced SHA-256 BTC mining bot helps you mine Bitcoin securely. Share with friends!",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

# Handle webhook updates from Telegram
@app.post('/webhook')
async def handle_webhook(request: Request):
    """
    Webhook endpoint to receive Telegram updates.
    """
    try:
        json_data = await request.json()
        update = Update(**json_data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return HTTPException(status_code=400, detail='Invalid payload')
    return {'OK': True}
