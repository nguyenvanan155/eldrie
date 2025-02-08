import json
import os
from datetime import datetime
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
import pyotp
import base64

# Các khóa bí mật để tạo mã OTP
AMAZON_KEY = "YZ7XEF24TJHR6CX2NHZK6XJHXSBWVZPD5QO53Y3REIRYNWIYXAYA"
ADS_KEY = "RZHUKFS5ND2P6JBVGJ3RJFYXSHRHOE4F"
DISCORD_KEY = "ATHDGYBLS6ANH7A3"
MICROSOFT_KEY = "FLPJCVOKMYYO7VC2"
AMAZON_GOC_KEY = 'ZUYCHKQAVLWSTIRF6476EAC6SWFQYHP4GLIQYX3JCXPE2GFREE6A'
CHAT_GPT = "655RRQJKVRB2TOWCAK5IMT43HGI6AMNI"

USER_DATA_FILE = "users.json"

FULL_ADMIN_IDS = [5201276631]  # ID người quản trị đầy đủ
LIMITED_ADMIN_IDS = [2112221324]  # ID người quản trị hạn chế

# Hàm trợ giúp để tạo OTP
def generate_otp(secret):
    padded_secret = secret + "=" * ((8 - len(secret) % 8) % 8)
    try:
        base64.b32decode(padded_secret, casefold=True)
    except Exception as e:
        raise ValueError(f"Khóa Base32 không hợp lệ: {e}")
    totp = pyotp.TOTP(padded_secret)
    return totp.now()

# Load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user data to the JSON file
def save_user_data(user_data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

# Check if user is a full admin
def is_full_admin(user_id):
    return user_id in FULL_ADMIN_IDS

# Check if user is a limited admin
def is_limited_admin(user_id):
    return user_id in LIMITED_ADMIN_IDS

# Hàm xử lý Inline Query để tự động gợi ý các lệnh
async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if query.startswith('/'):
        results = [
            InlineQueryResultArticle(
                id="1", 
                title="Lệnh /otp", 
                input_message_content=InputTextMessageContent("/otp - Lấy Mã 2FA Amazon Seller")
            ),
            InlineQueryResultArticle(
                id="2", 
                title="Lệnh /ads", 
                input_message_content=InputTextMessageContent("/ads - Lấy Mã 2FA ADS POWER")
            ),
            InlineQueryResultArticle(
                id="3", 
                title="Lệnh /discord", 
                input_message_content=InputTextMessageContent("/discord - Lấy Mã 2FA Discord")
            ),
            InlineQueryResultArticle(
                id="4", 
                title="Lệnh /microsoft", 
                input_message_content=InputTextMessageContent("/microsoft - Lấy Mã 2FA Microsoft")
            ),
            InlineQueryResultArticle(
                id="5", 
                title="Lệnh /amz", 
                input_message_content=InputTextMessageContent("/amz - Lấy Mã 2FA Amazon Gốc")
            ),
            InlineQueryResultArticle(
                id="6", 
                title="Lệnh /chatgpt", 
                input_message_content=InputTextMessageContent("/chatgpt - Lấy Mã 2FA ChatGPT")
            ),
        ]
    
    await update.inline_query.answer(results, cache_time=0, is_personal=True)

# Tạo bàn phím inline với các nút lệnh
def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("/otp - Lấy Mã 2FA Amazon Seller", callback_data='otp'),
            InlineKeyboardButton("/ads - Lấy Mã 2FA ADS POWER", callback_data='ads')
        ],
        [
            InlineKeyboardButton("/discord - Lấy Mã 2FA Discord", callback_data='discord'),
            InlineKeyboardButton("/microsoft - Lấy Mã 2FA Microsoft", callback_data='microsoft')
        ],
        [
            InlineKeyboardButton("/amz - Lấy Mã 2FA Amazon Gốc", callback_data='amz'),
            InlineKeyboardButton("/chatgpt - Lấy Mã 2FA ChatGPT", callback_data='chatgpt')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start."""
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Không xác định"
    start_date = datetime.now().strftime("%Y-%m-%d")
    user_data = load_user_data()

    if user_id in user_data:
        await update.message.reply_text(
            f"Chào mừng trở lại, {username}! "
            "Bạn đã sử dụng bot này trước đó. Chọn lệnh bên dưới:",
            reply_markup=main_menu_keyboard()  # Hiển thị menu chính
        )
    else:
        user_data[user_id] = {
            "username": username,
            "start_date": start_date
        }
        save_user_data(user_data)
        await update.message.reply_text(
            f"Chào mừng, {username}! "
            "Bạn đã được lưu vào hệ thống. Chọn lệnh bên dưới:",
            reply_markup=main_menu_keyboard()  # Hiển thị menu chính
        )

# Hàm xử lý các lệnh như /otp, /ads, /discord, /microsoft, v.v.
async def otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /otp."""
    try:
        otp = generate_otp(AMAZON_KEY)
        message = f"🔐 Mã 2FA AMAZON SELLER của bạn là: {otp}"
        await update.message.reply_text(message, reply_markup=main_menu_keyboard())  # Hiển thị menu sau khi gửi mã OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi khi tạo mã OTP: {e}")

async def ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /ads."""
    try:
        otp = generate_otp(ADS_KEY)
        message = f"🔐 Mã 2FA ADS POWER của bạn là: {otp}\nTài Khoản: dera.coppy@gmail.com\nPass: @17012025tT"
        await update.message.reply_text(message, reply_markup=main_menu_keyboard())  # Hiển thị menu sau khi gửi mã OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi khi tạo mã OTP: {e}")

async def discord(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /discord."""
    user_id = update.effective_user.id
    if not is_full_admin(user_id):
        await update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    try:
        otp = generate_otp(DISCORD_KEY)
        message = f"🔐 Mã 2FA DISCORD của bạn là: {otp}"
        await update.message.reply_text(message, reply_markup=main_menu_keyboard())  # Hiển thị menu sau khi gửi mã OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi khi tạo mã OTP: {e}")

async def microsoft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /microsoft."""
    user_id = update.effective_user.id
    if not is_full_admin(user_id):
        await update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    try:
        otp = generate_otp(MICROSOFT_KEY)
        message = f"🔐 Mã 2FA MICROSOFT của bạn là: {otp}"
        await update.message.reply_text(message, reply_markup=main_menu_keyboard())  # Hiển thị menu sau khi gửi mã OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi khi tạo mã OTP: {e}")

async def amazon_goc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /amz."""
    user_id = update.effective_user.id
    if not (is_full_admin(user_id) or is_limited_admin(user_id)):
        await update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    try:
        otp = generate_otp(AMAZON_GOC_KEY)
        message = f"🔐 Mã 2FA AMAZON GỐC của bạn là: {otp}"
        await update.message.reply_text(message, reply_markup=main_menu_keyboard())  # Hiển thị menu sau khi gửi mã OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi khi tạo mã OTP: {e}")

async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /chatgpt."""
    user_id = update.effective_user.id
    if not (is_full_admin(user_id) or is_limited_admin(user_id)):
        await update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return

    try:
        otp = generate_otp(CHAT_GPT)
        message = f"🔐 Mã 2FA CHATGPT của bạn là: {otp}"
        await update.message.reply_text(message, reply_markup=main_menu_keyboard())  # Hiển thị menu sau khi gửi mã OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Có lỗi khi tạo mã OTP: {e}")

if __name__ == "__main__":
    BOT_TOKEN = "7866055513:AAHUN87Qo_0HJG5uU8fyFx6JaXIeKGSxdo8"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("otp", otp))
    app.add_handler(CommandHandler("ads", ads))
    app.add_handler(CommandHandler("discord", discord))
    app.add_handler(CommandHandler("microsoft", microsoft))
    app.add_handler(CommandHandler("amz", amazon_goc))
    app.add_handler(CommandHandler("chatgpt", chatgpt))
    app.add_handler(InlineQueryHandler(inline_query_handler))  # Thêm handler cho Inline Query

    print("running")
    app.run_polling()
