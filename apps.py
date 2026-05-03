from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from async_main import bot
from async_main import db_client

import telebot
import keyboards
from datetime import datetime, timezone

app = FastAPI()

@app.get("/pay")
async def pay_page(user_id: int, payment_id: int):
    return HTMLResponse(f"""
    <html>
    <head>
        <title>Оплата</title>
    </head>
    <body style="font-family:sans-serif; text-align:center; margin-top:50px;">

        <h2>🧪 Тестовая оплата</h2>
        <p>Привет Амстердам, это тестовое окно оплаты. Деньги списываться не будут</p>

        <button onclick="pay(true)" style="padding:10px 20px; margin:10px;">
            ✅ Оплатить
        </button>

        <button onclick="pay(false)" style="padding:10px 20px; margin:10px;">
            ❌ Отменить
        </button>

        <script>
        function pay(success) {{
            fetch("https://arrowguardbot.onrender.com/payment-webhook", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{
                    status: success ? "success" : "fail",
                    user_id: {user_id},
                    payment_id: {payment_id}
                }})
            }}).then(() => {{
                document.body.innerHTML = success 
                    ? "<h2>✅ Оплата успешна</h2>"
                    : "<h2>❌ Оплата отменена</h2>";
            }});
        }}
        </script>

    </body>
    </html>
    """)

@app.post("/payment-webhook")
async def payment_webhook(request: Request):
    data = await request.json()

    status = data.get("status")
    user_id = data.get("user_id")
    payment_id = data.get("payment_id")

    payment_data = db_client.get_payment_by_id(payment_id)

    lang = db_client.get_user_lang(user_id)

    if status == "success":
        db_client.update_payment_data(payment_id, status, datetime.now(timezone.utc))
        user_sub = db_client.get_user_subscription(user_id)

        if user_sub:
            db_client.update_current_subscription(user_id=user_id,
                                                  plan=payment_data[2],
                                                  is_trial=False)
        else:
            db_client.create_new_subscription(user_id=user_id,
                                                  plan=payment_data[2],
                                                  is_trial=False)

        kb = keyboards.my_key_kb(lang)
        delete_offer_message(user_id, payment_data[4])

        bot.send_message(chat_id=user_id,
                         text="✅ Оплата прошла!",
                         reply_markup=kb)
    else:
        db_client.update_payment_data(payment_id, status)
        kb = keyboards.back_kb(lang)
        bot.send_message(chat_id=user_id,
                         text="❌ Оплата отменена",
                         reply_markup=kb)

    return {"ok": True}

@app.post("/tg-webhook")
async def tg_webhook(request: Request):
    data = await request.json()

    print("Webhook worked!")

    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])

    return {"ok": True}

def delete_offer_message(user_id, message_id):
    bot.delete_message(chat_id=user_id,
                       message_id=message_id)