from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import config as cfg 

btnUrlchannel = InlineKeyboardButton(text='link_to_channel', url=cfg.CHANNEL_URL)
channel = InlineKeyboardMarkup(row_width=1)
channel.insert(btnUrlchannel)