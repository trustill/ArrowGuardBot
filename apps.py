from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from async_main import bot
from async_main import db_client

import telebot

app = FastAPI()

@app.get("/pay")
async def pay_page(user_id: int):
    return HTMLResponse(f"""
    <html>
    <head>
        <title>Оплата</title>
    </head>
    <body style="font-family:sans-serif; text-align:center; margin-top:50px;">

        <h2>🧪 Тестовая оплата</h2>
        <p>Привет Амстердам, это тестовое окно оплаты. Деньги списываться не будут, только девственность</p>

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
                    user_id: {user_id}
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
    user_status = 1

    if status == "success":
        db_client.change_user_status(user_id, user_status)

        bot.send_message(user_id,
                         "✅ Оплата прошла! <a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'>Нажмите, чтобы получить ключ</a>",
                         parse_mode="html")
    else:
        bot.send_message(user_id, "❌ Оплата отменена")

    return {"ok": True}

@app.post("/tg-webhook")
async def tg_webhook(request: Request):
    data = await request.json()

    print("Webhook worked!")

    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])

    return {"ok": True}