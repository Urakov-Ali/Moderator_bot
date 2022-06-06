import logging
#kanalga ulanganini tekshirish uchun buttons faylini import qilamiz
import buttons as key
#config faylda hamma dannila bor [channel, admin, chat_id] lar
import config as cfg
#asyncio bizga habar o'chishidan oldin 5 soniya kutish uchun kerak
import asyncio
#until_date ni hisoblash uchun datetime ni import qilamiz until_date = \
#datetime.datetime.now() + datetime.timedelta(minutes=int(message.text[6:]))
import datetime
 
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

#1) bot foydalanuvchi kanalga qo'shilgan qo'shilmaganini tekshiradi
#2) bot yangi kirgan foydalanuchini username sini olib kanalga qo'shilishni so'raydi
@dp.message_handler(content_types=["new_chat_members"])
async def new_comer(message: types.Message):
	await message.reply(f"Hi 👋 {message.from_user.username} \nWelcome to the group\
		\n to be member of our group please join our channel first !!!", reply_markup=key.channel)

#foydalanuvchi kanalga qo'shilgan qo'shilmaganini tekshiruvchi funksiya yasavolamiz
#chat_member bizda (await bot.get_chat_member(chat_id= cfg.CHANNEL_ID, user_id= message.from_user.id)) \
#qiymatini oladi
def check_sub_channel(chat_member):
	return chat_member['status'] != "left"

#foydalanuchini malum muddatga ban qilib qo'yuvchi funksiya
@dp.message_handler(commands=['mute'], commands_prefix= "/")
async def muted(message: types.Message):
	#buyruqnu admin berganligini tekshiramiz
	if str(message.from_user.id) == cfg.ADMIN_ID:
		#agar admin buyruqni foydalanuchi habariga reply qilmasa pasdagi yozuv chiqadi
		if not message.reply_to_message:
			await message.reply("This should be replied command")
		else:
		#until_date yasab olamz / int(message.text[6:]) bu /unmute 10 yani buyruqdagi raqamlarni teruvchi qismi
			until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(message.text[6:]))
			#foydalanuvchini malum muddatga bloklaymiz / [message.reply_to_message.from_user.id] bu biz so'zini\
			#reply qilgan foydalanuvhimizning id si
			await message.chat.restrict(user_id=message.reply_to_message.from_user.id, can_send_messages=False, until_date=until_date)
			await message.reply(f'Dear {message.reply_to_message.from_user.username}\
			 \nthe admin banned you for {message.text[6:]} minutes for sending banned words')
			
			await message.reply("Please don't use banned words \nYour message will be deleted in 5 seconds")
			await asyncio.sleep(5)
			await message.reply_to_message.delete()
#qayta yozishga ruhsat berish buyrug'i
@dp.message_handler(commands=['unmute'], commands_prefix= "/")
async def mutet(message: types.Message):
	await message.chat.restrict(user_id=message.reply_to_message.from_user.id, can_send_messages=True)

#start bosilganda bot foydalnuvchi kanalga ulanganmi yoqmi tekshiradi
@dp.message_handler(commands= ['start'], commands_prefix ="/")
async def checker(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id= cfg.CHANNEL_ID, user_id= message.from_user.id)):
		await message.answer(f"Hello {message.from_user.username} \nYou can use our bot for free")
	else:
		await message.answer(f"Dear {message.from_user.username}\
		 \nto use the bot, please subscribe our channel first !!!", reply_markup=key.channel)

#taqiqlangan so'z bor yoqligini tekshiruvchi handler
@dp.message_handler()
async def ask_to_join_channel(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id= cfg.CHANNEL_ID, user_id= message.from_user.id)):
		text = message.text.lower()
		for word in cfg.WORDS:
			if word in text:
				await message.reply("Please don't use banned words \nYour message will be deleted in 5 seconds")
				await asyncio.sleep(5)
				await message.delete()
	else:
		await message.answer(f"Dear {message.from_user.username}\
		 \nto use the bot, please subscribe our channel first !!!", reply_markup=key.channel)


#[#test] buyrugini yozish orqali oz id ingizni biling
@dp.message_handler(commands=["test"], commands_prefix="#")
async def testing(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id = cfg.CHANNEL_ID, user_id= message.from_user.id)):
		await bot.send_message(message.from_user.id, f"Your ID: {message.from_user.id}")
	else: 
		await bot.send_message(message.from_user.id, 'You are not subscribed !!!')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)