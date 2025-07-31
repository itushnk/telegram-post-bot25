
import os
import pandas as pd
from telegram import Bot, InputMediaPhoto
from telegram.constants import ParseMode
from time import sleep

BOT_TOKEN = "8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk"
CHANNEL_ID = "@LCvXuy6z9RjY2I0"

bot = Bot(token=BOT_TOKEN)
df = pd.read_csv("products.csv")

for index, row in df.iterrows():
    try:
        item_id = int(row['ProductId'])
        image_url = row['ImageUrl']
        title = row['Title']
        sale_price = row['SalePrice']
        original_price = row['OriginalPrice']
        discount = row['Discount']
        orders = int(row['Orders'])
        rating = float(row['Rating'].strip('%'))
        buy_link = row['BuyLink']
        coupon_code = row.get('CouponCode', '').strip()

        # קריאה לפעולה
        intro_line = "🛍️ אל תפספסו את הדיל הזה!"

        # תיאור קצר
        description = f"{title} 🛒"

        # שורות תכונות (לדוגמה בלבד)
        features = "✨ איכות גבוהה וחומרים מעולים\n🎨 מגוון צבעים ומידות\n📦 מתאים כמתנה מושלמת"

        # שורת מחיר עם קישור
        price_line = f'מחיר מבצע: [{sale_price} ש"ח]({buy_link}) (מחיר מקורי: {original_price} ש"ח)'

        # הנחה
        discount_line = f"💸 חיסכון של {discount}"

        # דירוג
        rating_line = f"⭐ דירוג: {rating}%"

        # הזמנות
        order_line = f"📦 {orders} הזמנות" if orders >= 50 else "🆕 פריט חדש לחברי הערוץ"

        # משלוח
        shipping_line = "🚚 משלוח חינם בהזמנות מעל 38 ₪ או 7.49 ₪"

        # קופון אם קיים
        coupon_line = f"🎁 קופון לחברי הערוץ בלבד: {coupon_code}" if coupon_code else ""

        # קישור להזמנה
        order_now_line = f'[להזמנה מהירה לחצו כאן👉]({buy_link})'

        # סיום
        item_id_line = f"מספר פריט: {item_id}\n[הצטרפות לערוץ לחצו עליי👉](https://t.me/+LCv-Xuy6z9RjY2I0)"
        validity_line = "כל המחירים והמבצעים תקפים למועד הפרסום ועשויים להשתנות."

        # שילוב הכל
        message = "\n\n".join([
            intro_line,
            description,
            features,
            price_line,
            discount_line,
            rating_line,
            order_line,
            shipping_line,
            coupon_line,
            order_now_line,
            item_id_line,
            validity_line
        ])

        # שליחת הפוסט עם תמונה
        bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=message, parse_mode=ParseMode.MARKDOWN)
        print(f"🖼️ תמונה נשלחה: {item_id}")
        sleep(3)

    except Exception as e:
        print(f"שגיאה בפריט {row.get('ProductId', 'ללא מזהה')}: {e}")
