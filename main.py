
import pandas as pd
import random
import asyncio
from telegram import Bot, ParseMode
from flask import Flask
import threading

app = Flask(__name__)

TOKEN = "8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk"
CHANNEL_ID = "@LCv_Xuy6z9RjY2I0"
CSV_FILE = "products.csv"

def create_post(row):
    title = row['Title']
    sale_price = row['SalePrice']
    original_price = row['OriginalPrice']
    discount = row['DiscountPercent']
    rating = row['PositiveRate']
    orders = row['Orders']
    image_url = row['Image']
    buy_link = row['BuyLink']
    item_id = row['ItemId']
    coupon_code = row['CouponCode']

    post_lines = []
    call_to_action = random.choice([
        "📦 שדרגו את הבית עם הדיל הבא!",
        "🔥 המוצר הזה פשוט חובה!",
        "💡 זה הזמן לקנות חכם!",
        "🎯 הדיל שחיכיתם לו הגיע!"
    ])
    post_lines.append(call_to_action)

    post_lines.append(f"{title}")
    post_lines.append(f"⭐ דירוג: {rating}%")
    post_lines.append(f"📦 מספר הזמנות: {orders}" if int(orders) >= 50 else "🆕 פריט חדש לחברי הערוץ")

    price_line = f"מחיר מבצע: [{sale_price} ש"ח]({buy_link}) (מחיר מקורי: {original_price} ש"ח)"
    post_lines.append(price_line)
    post_lines.append(f"💸 חיסכון של {discount}%!")
    if coupon_code and coupon_code.strip():
        post_lines.append(f"🎁 קופון לחברי הערוץ בלבד: {coupon_code}")

    post_lines.append(f"👇🛍הזמינו עכשיו🛍👇")
    post_lines.append(f"{buy_link}")
    post_lines.append(f"מספר פריט: {item_id}")
    post_lines.append(f"[להצטרפות לערוץ לחצו עליי👉](https://t.me/+LCv-Xuy6z9RjY2I0)")

    return "
".join(post_lines), image_url

async def send_posts():
    bot = Bot(token=TOKEN)
    df = pd.read_csv(CSV_FILE)
    for _, row in df.iterrows():
        message, image_url = create_post(row)
        await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=message, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(1200)

def run_bot():
    asyncio.run(send_posts())

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(debug=False, host='0.0.0.0', port=8080)
