from telebot import types
import json

with open("data_texts.json", "r", encoding="utf-8") as file:
    msg_data = json.load(file)

def choose_language_kb():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Русский 🇷🇺", callback_data="change_lang_to_ru"),
        types.InlineKeyboardButton(text="English 🇬🇧", callback_data="change_lang_to_eng")
    )

def start_kb(lang):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["buy_vpn"], callback_data="buy_vpn"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["subscribe"], callback_data="subscribe"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["account"], callback_data="account")
    )

def accept_tou_kb(lang):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["accept_tou"], callback_data="accept_tou"))