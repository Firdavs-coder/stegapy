import os
import random
import string
from stegano import lsb
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def generate_random_filename():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT])
async def handle_image(message: types.Message):
    await message.reply("Processing...")
    try:
        # Handle both photo and document formats
        if message.content_type == types.ContentType.PHOTO:
            file_info = await bot.get_file(message.photo[-1].file_id)
        else:
            # Check if document is an image
            if not message.document.mime_type.startswith('image/'):
                await message.reply("Please send an image file")
                return
            file_info = await bot.get_file(message.document.file_id)
            
        downloaded_file = await bot.download_file(file_info.file_path)
        
        # Generate random filenames
        input_filename = generate_random_filename() + '.jpg'
        output_filename = generate_random_filename() + '.png'
        
        # Save received image
        with open(input_filename, 'wb') as new_file:
            new_file.write(downloaded_file.read())
            
        if message.caption and message.content_type == types.ContentType.PHOTO:
            # Encode mode - image has caption text to hide
            secret = lsb.hide(input_filename, message.caption)
            secret.save(output_filename)
            
            # Send encoded image back to user
            with open(output_filename, 'rb') as encoded_image:
                await bot.send_document(message.chat.id, encoded_image, 
                                     caption="Made with @SecretImageBot")
                
        else:
            # Decode mode - extract hidden message
            try:
                revealed_text = lsb.reveal(input_filename)
                if revealed_text:
                    await message.reply(f"Hidden message: <b>{revealed_text}</b>", parse_mode='html')
                else:
                    await message.reply("No hidden message found in this image.")
            except Exception as e:
                await message.reply("No hidden message found in this image.")
                
        # Clean up files
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.copy_message(message.chat.id, -1001421718959, 190)

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
