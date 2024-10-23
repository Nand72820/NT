import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram.error import BadRequest

# Define states for the conversation
GMAIL, METHOD = range(2)

CHANNEL_ID = -1002204134287  # Replace with your channel ID

# Function to check if the user is a member of the channel
async def is_user_member(update: Update, context):
    user_id = update.message.from_user.id
    try:
        member_status = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member_status.status in ['member', 'administrator', 'creator']
    except BadRequest:
        return False

# Function to generate random name with 5 letters
def generate_random_name(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Function to generate variations of a Gmail address with exactly two dots
def generate_gmail_dot_variations(gmail: str, count: int = 50):
    local, domain = gmail.split('@')

    if domain != 'gmail.com':
        return ["This bot works only with Gmail addresses."]

    variations = set()  # Use a set to avoid duplicates
    n = len(local)

    # Generate variations with exactly two dots
    for i in range(1, n):  # First dot can be placed from position 1 to n-1
        for j in range(i + 1, n + 1):  # Second dot must be after the first dot
            variation = local[:i] + '.' + local[i:j] + '.' + local[j:] + '@' + domain
            variations.add(variation)
            if len(variations) >= count:  # Stop generating if we have enough variations
                break
        if len(variations) >= count:
            break

    return list(variations)[:count]  # Return only the requested number of variations

# Function to generate variations using the + (random name) method
def generate_gmail_plus_variations(gmail: str, count: int = 50):
    local, domain = gmail.split('@')

    if domain != 'gmail.com':
        return ["This bot works only with Gmail addresses."]

    variations = set()  # Use a set to avoid duplicates

    for _ in range(count):
        random_name = generate_random_name()
        variation = f"{local}+{random_name}@{domain}"
        variations.add(variation)

    return list(variations)  # Return all generated variations

# Escape special characters for MarkdownV2
def escape_markdown_v2(text: str) -> str:
    return text.replace('.', '\\.').replace('-', '\\-').replace('+', '\\+').replace('@', '\\@').replace('_', '\\_')

# Start command to welcome users
async def start(update: Update, context):
    # Check if the user is a member of the channel
    if not await is_user_member(update, context):
        keyboard = [[InlineKeyboardButton("Join Channel", url="https://t.me/creativeydv")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please join our channel to use this bot:", reply_markup=reply_markup)
        return

    # Continue with the conversation if user is a member
    await update.message.reply_text("Welcome To NY CREATION! Please enter your Gmail address.")
    return GMAIL

# Function to handle the Gmail input
async def handle_gmail(update: Update, context):
    context.user_data['gmail'] = update.message.text  # Store the Gmail address
    await update.message.reply_text("Great! Now please choose the method for generating variations:\n"
                                     "1. Type 'dot' for dot variations.\n"
                                     "2. Type '+' for random name variations.")
    return METHOD

# Function to handle the method input and generate 50 variations
async def handle_method(update: Update, context):
    method = update.message.text.lower()
    gmail_address = context.user_data['gmail']  # Retrieve the stored Gmail address

    if method not in ['dot', '+']:
        await update.message.reply_text("Please enter a valid method ('dot' or '+').")
        return METHOD

    if method == 'dot':
        variations = generate_gmail_dot_variations(gmail_address, count=50)
    else:
        variations = generate_gmail_plus_variations(gmail_address, count=50)

    if not variations:
        await update.message.reply_text("No variations generated.")
    else:
        response = '\n'.join(f"`{escape_markdown_v2(variation)}`" for variation in variations)
        await update.message.reply_text(response, parse_mode='MarkdownV2')

    return ConversationHandler.END

# Function to cancel the conversation
async def cancel(update: Update, context):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# Main function to run the bot
def main():
    token = "7641720331:AAGTC6NffxpeScuodj5oafB8sixJw6NtsUY"  # Replace with your bot token

    # Create the application
    app = ApplicationBuilder().token(token).build()

    # Set up the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gmail)],
            METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_method)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Add the conversation handler to the application
    app.add_handler(conv_handler)

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
