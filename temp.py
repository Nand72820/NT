from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Define callback data for each button
CREATE_GMAIL, JOIN_CHANNEL, ALL_HANDLES, CONTACT_OWNER = range(4)

# Start command to display the keyboard with "Choose an Option" in bold
async def start(update: Update, context):
    # Keyboard buttons layout
    keyboard = [
        ['Create GMaiL 😎', 'Join oFFiciaL ChanneL ❤️‍🔥', 'All Handles 💟'],
        ['Contact Owner ⚠️']  # Single button on the second row
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    # Send the bold text "Choose an Option"
    await update.message.reply_text("**Choose an Option**", reply_markup=reply_markup, parse_mode='MarkdownV2')

# Function to handle button presses
async def handle_message(update: Update, context):
    user_input = update.message.text

    if user_input == "Create GMaiL 😎":
        await update.message.reply_text("Create GMaiL button pressed. Perform relevant action here.")  # Replace with your desired action
    elif user_input == "Join oFFiciaL ChanneL ❤️‍🔥":
        keyboard = [[InlineKeyboardButton("JOIN NOW 💟", url="https://t.me/creativeydv")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("THANK YOU FOR YOUR INTEREST TAP THE BELOW BUTTON TO JOIN", reply_markup=reply_markup)
    elif user_input == "All Handles 💟":
        keyboard = [[InlineKeyboardButton("TAP HERE 💟", url="https://t.me/addlist/RpDpFE1rHFFiYWJl")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("THANK YOU FOR YOUR INTEREST TAP THE BELOW BUTTON TO JOIN", reply_markup=reply_markup)
    elif user_input == "Contact Owner ⚠️":
        await update.message.reply_text("**DM - @TMZEROO ✅**", parse_mode='MarkdownV2')

def main():
    token = "7641720331:AAGTC6NffxpeScuodj5oafB8sixJw6NtsUY"  # Replace with your bot token
    app = ApplicationBuilder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))  # This handles the /start command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # To handle button presses

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
