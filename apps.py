from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from async_main import bot

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
            fetch("https://catchhooks.com/api/w/EEb9fdTvtX", {{
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

    if status == "success":
        bot.send_message(user_id, "✅ Оплата прошла!")
    else:
        bot.send_message(user_id, "❌ Оплата отменена")

    return {"ok": True}

@app.post("/tg-webhook")
async def tg_webhook(request: Request):
    data = await request.json()

    print("Webhook worked!")
    print(data)
    print(bot.message_handlers)

    if 'message' in data:
        message = telebot.types.Message.de_json(data['message'])
        bot.process_new_messages([message])

    return {"ok": True}