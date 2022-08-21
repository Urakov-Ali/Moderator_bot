import logging
#file buttons is imported to check if the user has been subscribed to our channel
import buttons as key
#all the data is in the config file [channel, admin, chat_id] lar
import config as cfg
#wee need asyncio to wait for 5 seconds before the message is deleted
import asyncio
#datetime is imported to calculate the until_date modul until_date = \
#datetime.datetime.now() + datetime.timedelta(minutes=int(message.text[6:]))
import datetime
 
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

#1) the bot checks if the user has been subscribed to our channel or not
#2) bot takes the username of user and asks him/her to join the channel
@dp.message_handler(content_types=["new_chat_members"])
async def new_comer(message: types.Message):
	await message.reply(f"Hi 👋 {message.from_user.username} \nWelcome to the group\
		\n to be member of our group please join our channel first !!!", reply_markup=key.channel)

#we make a function to check if the user has been subscribed to our channel or not
#chat_member takes the value of(await bot.get_chat_member(chat_id= cfg.CHANNEL_ID, user_id= message.from_user.id))
def check_sub_channel(chat_member):
	return chat_member['status'] != "left"

#function to ban the user for certain time
@dp.message_handler(commands=['mute'], commands_prefix= "/")
async def muted(message: types.Message):
	#we check if the order is given by admin
	if str(message.from_user.id) == cfg.ADMIN_ID:
		#if the admin doesn't make a reply to the message of the user, then appears those words
		if not message.reply_to_message:
			await message.reply("This should be replied command")
		else:
		#lets's make until_date / int(message.text[6:]) bu /unmute 10
			until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(message.text[6:]))
			#the user is blocked for a certain time / [message.reply_to_message.from_user.id] bu biz so'zini\
			#id of the user that we made a reply to his/her message
			await message.chat.restrict(user_id=message.reply_to_message.from_user.id, can_send_messages=False, until_date=until_date)
			await message.reply(f'Dear {message.reply_to_message.from_user.username}\
			 \nthe admin banned you for {message.text[6:]} minutes for sending banned words')
			
			await message.reply("Please don't use banned words \nYour message will be deleted in 5 seconds")
			await asyncio.sleep(5)
			await message.reply_to_message.delete()
#order to let the user write again
@dp.message_handler(commands=['unmute'], commands_prefix= "/")
async def mutet(message: types.Message):
	await message.chat.restrict(user_id=message.reply_to_message.from_user.id, can_send_messages=True)

@dp.message_handler(commands= ['start'], commands_prefix ="/")
async def checker(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id= cfg.CHANNEL_ID, user_id= message.from_user.id)):
		await message.answer(f"Hello {message.from_user.username} \nYou can use our bot for free")
	else:
		await message.answer(f"Dear {message.from_user.username}\
		 \nto use the bot, please subscribe our channel first !!!", reply_markup=key.channel)

#handler to check if the banned word is written on group
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


#[#test] know your id by sending this order
@dp.message_handler(commands=["test"], commands_prefix="#")
async def testing(message: types.Message):
	if check_sub_channel(await bot.get_chat_member(chat_id = cfg.CHANNEL_ID, user_id= message.from_user.id)):
		await bot.send_message(message.from_user.id, f"Your ID: {message.from_user.id}")
	else: 
		await bot.send_message(message.from_user.id, 'You are not subscribed !!!')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
