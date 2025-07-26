import os
import logging
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# --- Setup logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
TOKEN = "8239040625:AAEaJJZEAmm95Q5cGxaGjZkbyZ_LIKNbwNY"  # Replace with your bot token
PASSWORD = "123"  # Optional password for clearing images
TESSERACT_PATH = os.path.join(os.getcwd(), "Tesseract-OCR", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- Commands ---

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(f"""
👋 Hello {user.first_name or 'there'}!

📸 This bot is used to extract text from images

/start
/help
/dev


✅ Just send a clear photo that contains text and I’ll reply with what it says.
""")

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(f""" 
        📌Just send a photo with text and I'll reply with the extracted text:)
            use cases:
                                    
            - Extract text from:
                - Scanned books
                - Recognize handwriting
                                    

        For support...use /dev""")

async def dev(update: Update, context: CallbackContext):
    await update.message.reply_text("Need help or found any bug(oh shittt)...contact me then @A13X60 👈🏼")

async def clear_images(update: Update, context: CallbackContext):
    entered_password = ' '.join(context.args)
    if entered_password == PASSWORD:
        clear_temp_images()
        await update.message.reply_text("🧹 All temporary images have been cleared.")
    else:
        await update.message.reply_text("🔒 Invalid password.")

# --- Image Handler ---

async def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id

    await update.message.reply_text("Image received....")
    await update.message.reply_text("Extracting text... Please wait ⏳")

    # Download photo
    photo_file = await update.message.photo[-1].get_file()
    image_path = os.path.join(DOWNLOAD_FOLDER, f"{chat_id}_photo.jpg")
    await photo_file.download_to_drive(image_path)

    # OCR
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="amh+eng")

        if text.strip():
            await update.message.reply_text(f"📝 Extracted Text:\n\n{text.strip()}")
        else:
            await update.message.reply_text("⚠️ No readable text found in the image.")
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        await update.message.reply_text("❌ Something went wrong during text extraction.\nPlease try again with a clearer image.")
    finally:
        try:
            os.remove(image_path)
            logger.info(f"Deleted temporary image: {image_path}")
        except Exception as e:
            logger.warning(f"Failed to delete image: {e}")

# --- Helper Function ---

def clear_temp_images():
    for f in os.listdir(DOWNLOAD_FOLDER):
        if f.endswith("_photo.jpg"):
            try:
                os.remove(os.path.join(DOWNLOAD_FOLDER, f))
                logger.info(f"Removed temp file: {f}")
            except Exception as e:
                logger.warning(f"Could not delete {f}: {e}")

# --- Bot Entry Point ---

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dev", dev))
    application.add_handler(CommandHandler("clearimages", clear_images))  # password protected
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 OCR Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
