import csv
import time
from telegram import Bot
from telegram.constants import ParseMode
import schedule

BOT_TOKEN = '8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk'
CHANNEL_ID = '@MyPostBot2025_bot'
CSV_FILE_PATH = 'products.csv'
POST_INTERVAL_MINUTES = 20

def generate_post_text(row):
    call_to_action = "ההצעה הזאת בדיוק בשבילכם! 🎯"
    description = f"{row['Title']} 🎉"
    feature_1 = "🔧 איכות מעולה וחומרים חזקים"
    feature_2 = "📦 נשלח עם אחריות מהחנות"
    feature_3 = "🎨 מתאים לבית, עבודה או מתנה מושלמת"

    sale_price = row['SalePrice']
    original_price = row['OriginalPrice']
    buy_link = row['BuyLink']

    price_line = f"מחיר מבצע: [{sale_price} ש"ח]({buy_link}) (מחיר מקורי: {original_price} ש"ח)"
    discount_line = f"💸 חסכון: {row['Discount']}%"
    rating_line = f"⭐ דירוג: {row['Rating']}%"
    orders_line = f"📦 {row['Orders']} הזמנות" if int(float(row['Orders'])) >= 50 else "🆕 פריט חדש לחברי הערוץ"
    shipping_line = "🚚 משלוח חינם בהזמנות מעל 38 ₪ או 7.49 ₪ בלבד"

    coupon_code = row.get('CouponCode', '').strip()
    coupon_line = f"🎁 קופון לחברי הערוץ בלבד: {coupon_code}" if coupon_code else ""

    order_link_line = f"להזמנה מהירה לחצו כאן👉 {buy_link}"
    item_number_line = f"מספר פריט: {str(row['ItemNumber']).replace('.0','')}"
    join_channel_line = "להצטרפות לערוץ לחצו עליי👉 https://t.me/+LCv-Xuy6z9RjY2I0"
    disclaimer_line = "כל המחירים והמבצעים תקפים למועד הפרסום ועשויים להשתנות."

    post_text = (
        f"{call_to_action}

"
        f"{description}

"
        f"{feature_1}
"
        f"{feature_2}
"
        f"{feature_3}

"
        f"{price_line}
"
        f"{discount_line}
"
        f"{rating_line}
"
        f"{orders_line}
"
        f"{shipping_line}
"
        f"{coupon_line}

"
        f"{order_link_line}
"
        f"{item_number_line}
"
        f"{join_channel_line}
"
        f"{disclaimer_line}"
    )
    return post_text

def send_post_to_channel(row):
    bot = Bot(token=BOT_TOKEN)
    text = generate_post_text(row)
    image_url = row.get('Image', '').strip()
    video_url = row.get('Video', '').strip()

    try:
        if video_url:
            bot.send_video(
                chat_id=CHANNEL_ID,
                video=video_url,
                caption=text,
                parse_mode=ParseMode.MARKDOWN
            )
            print(f"🎥 וידאו נשלח: {row['ItemNumber']}")
        elif image_url:
            bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=image_url,
                caption=text,
                parse_mode=ParseMode.MARKDOWN
            )
            print(f"🖼️ תמונה נשלחה: {row['ItemNumber']}")
        else:
            print(f"⚠️ אין מדיה לפריט: {row['ItemNumber']}")
    except Exception as e:
        print(f"❌ שגיאה בשליחת הפוסט {row['ItemNumber']}: {e}")

def run_scheduled_posts():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for i, row in enumerate(rows):
        schedule.every(POST_INTERVAL_MINUTES * i).minutes.do(send_post_to_channel, row=row)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_scheduled_posts()
