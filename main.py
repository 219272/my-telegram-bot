import asyncio
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from flask import Flask
from threading import Thread

# ১. আপনার তথ্য এখানে দিন
TOKEN = 'আপনার_বট_টোকেন_এখানে'
FB_LINK = "আপনার_ফেসবুক_লিংক" 

# ২. সার্ভার সচল রাখার জন্য Flask setup
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "শুরু করুন"),
        BotCommand("menu", "মেনু দেখুন")
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔵 Follow Facebook", url=FB_LINK)],
                [InlineKeyboardButton("✅ ভেরিফাই করুন", callback_data='verify')]]
    await update.message.reply_text("👋 আগে ফেসবুক ফলো করে ভেরিফাই বাটনে চাপ দিন।", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'verify':
        context.user_data['verified'] = True
        keyboard = [[InlineKeyboardButton("🚀 Attack", callback_data='at')], [InlineKeyboardButton("💣 Bomb", callback_data='bm')]]
        await query.message.edit_text("✅ সফল! এখন নিচের অপশন বেছে নিন:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'at': await query.message.reply_text("🌐 নিয়ম: `/attack [URL]`")
    elif query.data == 'bm': await query.message.reply_text("💣 নিয়ম: `/bomb [Number] [Amount]`")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('verified'): return await update.message.reply_text("❌ আগে ভেরিফাই করুন।")
    await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে...")

async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('verified'): return await update.message.reply_text("❌ আগে ভেরিফাই করুন।")
    await update.message.reply_text("💣 বম্বিং শুরু হচ্ছে...")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("bomb", bomb))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()
  
