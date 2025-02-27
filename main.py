#!/usr/bin/env python
import logging
import io
import re
import numpy as np
import matplotlib.pyplot as plt
import requests
from asteval import Interpreter

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

import speech_recognition as sr
from pydub import AudioSegment

# Apply nest_asyncio to allow nested event loops
import nest_asyncio
nest_asyncio.apply()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Configuration: API Keys directly in code ---
TELEGRAM_BOT_TOKEN = "#API KEY PUT HERE#"
CURRENCY_API_KEY = "YOUR_CURRENCY_API_KEY"
STOCK_API_KEY = "YOUR_STOCK_API_KEY"

# --- Modes ---
MODE_SCIENTIFIC = "scientific"
MODE_FINANCIAL = "financial"
MODE_STATISTICAL = "statistical"

# --- Safe Evaluator ---
aeval = Interpreter(usersyms={"np": np})

# --- Bot Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start command: Welcomes the user and presents mode selection.
    """
    keyboard = [
        [InlineKeyboardButton("Scientific", callback_data=MODE_SCIENTIFIC)],
        [InlineKeyboardButton("Financial", callback_data=MODE_FINANCIAL)],
        [InlineKeyboardButton("Statistical", callback_data=MODE_STATISTICAL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(
            "Welcome to the Unique Calculator Bot.\nChoose your mode:", reply_markup=reply_markup
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles inline button presses to set the calculation mode.
    """
    query = update.callback_query
    await query.answer()
    selected_mode = query.data
    context.chat_data["mode"] = selected_mode
    await query.edit_message_text(
        text=f"Mode set to: {selected_mode.capitalize()}.\nSend your calculation request."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes incoming text messages and directs them to the appropriate function.
    """
    text = update.message.text.strip()
    mode = context.chat_data.get("mode", MODE_SCIENTIFIC)  # Default mode

    try:
        # Check for plot commands
        if re.search(r"^\s*plot", text, re.IGNORECASE):
            await plot_expression(update, context, text)
        # Check for currency conversion requests
        elif re.search(r"convert\s+\d+(\.\d+)?\s+[A-Za-z]{3}\s+to\s+[A-Za-z]{3}", text, re.IGNORECASE):
            await currency_conversion(update, context, text)
        # Check for stock lookup requests
        elif re.search(r"^\s*stock\s+[A-Za-z]+", text, re.IGNORECASE):
            await stock_calculation(update, context, text)
        else:
            # Safely evaluate expression using asteval
            result = aeval(text)
            if aeval.error:
                raise Exception("Error in evaluation")
            await update.message.reply_text(f"Result: {result}")
    except Exception as e:
        logger.exception("Error processing text message")
        await update.message.reply_text(f"Error processing your request: {e}")

async def plot_expression(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """
    Processes a plot command.
    Expected format (e.g.,): "plot sin(x) from 0 to 10"
    """
    try:
        # Default values
        expr = "np.sin(x)"
        x_start, x_end = 0.0, 10.0

        # Extract expression and range using regex
        expr_match = re.search(r"plot\s+(.+?)\s+(from|$)", text, re.IGNORECASE)
        if expr_match:
            expr = expr_match.group(1).strip()

        range_match = re.search(r"from\s+([\d\.]+)\s+to\s+([\d\.]+)", text, re.IGNORECASE)
        if range_match:
            x_start = float(range_match.group(1))
            x_end = float(range_match.group(2))

        x = np.linspace(x_start, x_end, 400)
        aeval.symtable["x"] = x
        y = aeval(expr)
        if aeval.error:
            raise Exception("Invalid expression for plotting.")

        plt.figure()
        plt.plot(x, y)
        plt.title(f"Graph of {expr}")
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        await update.message.reply_photo(photo=buf)
    except Exception as e:
        logger.exception("Error plotting expression")
        await update.message.reply_text(f"Error plotting expression: {e}")

async def currency_conversion(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """
    Processes currency conversion requests.
    Expected format (e.g.,): "convert 100 USD to EUR"
    """
    try:
        match = re.search(
            r"convert\s+([\d\.]+)\s+([A-Za-z]{3})\s+to\s+([A-Za-z]{3})", text, re.IGNORECASE
        )
        if not match:
            await update.message.reply_text("Format error. Use: convert <amount> <FROM> to <TO>")
            return

        amount = float(match.group(1))
        from_currency = match.group(2).upper()
        to_currency = match.group(3).upper()

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"].get(to_currency)
        if rate:
            converted = amount * rate
            await update.message.reply_text(f"{amount} {from_currency} = {converted:.2f} {to_currency}")
        else:
            await update.message.reply_text("Currency not supported.")
    except Exception as e:
        logger.exception("Error in currency conversion")
        await update.message.reply_text(f"Error in currency conversion: {e}")

async def stock_calculation(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """
    Processes stock lookup requests.
    Expected format (e.g.,): "stock AAPL"
    """
    try:
        match = re.search(r"stock\s+([A-Za-z]+)", text, re.IGNORECASE)
        if not match:
            await update.message.reply_text("Please provide a stock symbol, e.g., stock AAPL")
            return

        stock_symbol = match.group(1).upper()
        # Dummy value for demonstration; replace with a real API call if needed
        stock_price = 150.00
        await update.message.reply_text(f"Stock {stock_symbol}: ${stock_price}")
    except Exception as e:
        logger.exception("Error in stock lookup")
        await update.message.reply_text(f"Error in stock lookup: {e}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes voice messages by converting them to text and handling the result.
    """
    try:
        voice_file = await update.message.voice.get_file()
        voice_file_path = "voice.ogg"
        await voice_file.download_to_drive(voice_file_path)
        
        # Convert OGG to WAV using pydub (requires ffmpeg)
        audio = AudioSegment.from_ogg(voice_file_path)
        wav_path = "voice.wav"
        audio.export(wav_path, format="wav")
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio_data)
        
        await update.message.reply_text(f"You said: {recognized_text}")
        await handle_text(update, context)
    except Exception as e:
        logger.exception("Error processing voice message")
        await update.message.reply_text(f"Error processing voice message: {e}")

async def main() -> None:
    """
    Main function to initialize and start the bot.
    """
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # This will run the bot until interrupted.
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
