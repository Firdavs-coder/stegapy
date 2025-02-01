# Documentation for Secret Image Bot and Web Application

## Secret Image Bot

### Overview
The [Secret Image Bot](https://t.me/SecretImageBot) is a Telegram bot that allows users to hide messages within images and reveal hidden messages from images. It supports both photo and document formats.

### Features
- **Encode Messages**: Users can send an image with a caption, and the bot will hide the caption text within the image.
- **Decode Messages**: Users can send an image file to extract any hidden messages.
- **User-Friendly Interface**: The bot provides feedback and instructions to users through Telegram messages.

### Commands
- `/start`: Displays a welcome message with instructions on how to use the bot.

### Usage
1. **To Hide a Message**:
   - Send an image with a caption (the message to hide).
   - The bot will respond with the encoded image.

2. **To Reveal a Hidden Message**:
   - Send the image as a **file** (not a photo).
   - The bot will respond with the hidden message, if any.

### Bot Token
To create a `.env` file, you can add the following line to it:

    BOT_TOKEN=your_bot_token_here

Make sure to replace 'your_bot_token_here' with the actual token you received from the BotFather on Telegram. This file should be placed in the root directory of your project to ensure that the bot can access the token securely.
# End Generation Here



### Requirements
- `pyTelegramBotAPI` library
- `stegano` library
- `Pillow` library for image processing

## Web Application

### Overview
The web application provides a user interface for encoding and decoding messages within PNG images using steganography.

### Features
- **Encode Messages**: Users can upload a PNG image and a message to hide. The application will return a new image with the message embedded.
- **Decode Messages**: Users can upload a PNG image to extract any hidden messages.

### Endpoints
- **`/encode`**: Accepts a POST request with an image file and a message. Returns the encoded image.
- **`/decode`**: Accepts a POST request with an image file. Returns the hidden message.

### Usage
1. **To Hide a Message**:
   - Navigate to the web application.
   - Upload a PNG image and enter the message to hide.
   - Submit the form to receive the encoded image.

2. **To Reveal a Hidden Message**:
   - Navigate to the web application.
   - Upload a PNG image that may contain a hidden message.
   - Submit the form to receive the extracted message.

### Requirements
- `Flask` framework
- `Pillow` library for image processing

### Installation
1. Clone the repository.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Run the application using `python main.py`.

### Note
Ensure that the upload folder exists and has the correct permissions for saving images.

