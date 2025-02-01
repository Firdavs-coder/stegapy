import telebot
import os
import random
import string
from stegano import lsb
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def generate_random_filename():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

@bot.message_handler(content_types=['photo', 'document'])
def handle_image(message: telebot.types.Message):
    bot.reply_to(message, "Processing...")
    try:
        # Handle both photo and document formats
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
        else:
            # Check if document is an image
            if not message.document.mime_type.startswith('image/'):
                bot.reply_to(message, "Please send an image file")
                return
            file_info = bot.get_file(message.document.file_id)
            
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Generate random filenames
        input_filename = generate_random_filename() + '.jpg'
        output_filename = generate_random_filename() + '.png'
        
        # Save received image
        with open(input_filename, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        if message.caption and message.content_type == 'photo':
            # Encode mode - image has caption text to hide
            secret = lsb.hide(input_filename, message.caption)
            secret.save(output_filename)
            
            # Send encoded image back to user
            with open(output_filename, 'rb') as encoded_image:
                bot.send_document(message.chat.id, encoded_image, 
                             caption="Made with @SecretImageBot")
                
        else:
            # Decode mode - extract hidden message
            try:
                revealed_text = lsb.reveal(input_filename)
                if revealed_text:
                    bot.reply_to(message, f"Hidden message: <b>{revealed_text}</b>", parse_mode='html')
                else:
                    bot.reply_to(message, "No hidden message found in this image.")
            except Exception as e:
                bot.reply_to(message, "No hidden message found in this image.")
                
        # Clean up files
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """
Welcome to Secret Image Bot!

To hide a message in an image:
1. Send an image with a caption (mandatory)

To reveal a hidden message:
1. Send the image as a file format (mandatory)

The bot will process your image and respond accordingly.
"""
    bot.reply_to(message, welcome_text)

# Start the bot
bot.polling()
