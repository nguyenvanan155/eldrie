from telethon import TelegramClient, events
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import random

# Thông tin API Telegram
API_ID = '25727222'
API_HASH = '5f36b5ce8197b8e3fea1bf292e4a5972'
PHONE_NUMBER = '0398213010'
receiver_username = '@zingpanel_bot'  # Tên bot nhận tin nhắn

# Khởi tạo client và scheduler
client = TelegramClient('session_name', API_ID, API_HASH)
scheduler = AsyncIOScheduler()

# Biến lưu giá trị ngẫu nhiên mỗi ngày
daily_values = {}

def generate_daily_values():
    """Tạo các giá trị ngẫu nhiên mới mỗi ngày vào 00:00"""
    global daily_values
    daily_values = {
        "checkin_hour": random.randint(6, 7),
        "checkin_minute": random.randint(0, 40),
        "report_hour": random.randint(19, 22),
        "report_minute": random.randint(0, 59),
        "xx": random.randint(3, 9),  # Số người Tawk
        "yy": random.randint(1, 5)   # Số người Sp trung
    }
    schedule_daily_jobs()

async def send_report():
    """Gửi lệnh /report, sau đó gửi tin nhắn xác nhận và chờ phản hồi"""
    chat_id = receiver_username

    # Gửi lệnh /report
    await client.send_message(chat_id, '/report')
    print("✅ Đã gửi lệnh /report")

    # Gửi tin nhắn xác nhận ngay sau đó
    await client.send_message(chat_id, "Đã báo cáo công việc.")
    print("✅ Đã gửi tin nhắn xác nhận báo cáo.")

    # Chờ 2 phút rồi gửi tin nhắn cuối cùng với giá trị ngẫu nhiên của ngày
    await asyncio.sleep(120)

    final_message = f"Tawk: {daily_values['xx']} người, Sp trung: {daily_values['yy']} người , Rao VPS done"
    await client.send_message(chat_id, final_message)
    print(f"✅ Đã gửi tin nhắn cuối: {final_message}")

# Sự kiện lắng nghe tin nhắn phản hồi
@client.on(events.NewMessage(chats=receiver_username, pattern="✅ Báo cáo công việc của bạn đã được ghi nhận!"))
async def handle_report_confirmation(event):
    """Xử lý khi nhận được tin nhắn xác nhận báo cáo"""
    print("🎯 Hệ thống xác nhận: Đã report thành công!")

def schedule_daily_jobs():
    """Cập nhật lịch trình với giá trị ngẫu nhiên của ngày"""
    scheduler.remove_all_jobs()

    scheduler.add_job(send_report, 'cron', hour=daily_values['report_hour'], minute=daily_values['report_minute'])

    print(f"🕒 Đã đặt lịch báo cáo vào {daily_values['report_hour']}:{daily_values['report_minute']:02d} hàng ngày.")
    print(f"📊 Giá trị cho hôm nay: xx = {daily_values['xx']}, yy = {daily_values['yy']}")

# Lên lịch reset lịch trình hàng ngày vào 00:00
scheduler.add_job(generate_daily_values, 'cron', hour=0, minute=0)

async def main():
    """Khởi chạy bot"""
    await client.start(PHONE_NUMBER)
    generate_daily_values()  # Tạo giá trị ngẫu nhiên ngay khi khởi động
    scheduler.start()
    print("🚀 Bot đang chạy...")
    await client.run_until_disconnected()

# Chạy bot
asyncio.run(main())
