import logging
import time
import os
import re
import subprocess 
from datetime import date
from telegram import  ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
	update.message.reply_text('Hi! Enjoy the Bot!! ')


def help(update, context):
	update.message.reply_text('/start- To Start the Bot \n /help- To Know About the Commands \n '
	'/rclone [COMMAND]- To Run Shell or Rclone Command (except copy) \n'
	'/rclonecopy [COMMAND]- To Copy Files \n'
	'/folder- To Inline View of Folder in Drive \n'
	'/backup- to create backup to other drive \n')


def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def folder(update, context):
	if os.path.exists("adress.txt") == True :
		os.remove("adress.txt")
	if os.path.exists("link.txt") == True :
		os.remove("link.txt")
	f=open("adress.txt","w")
	command='rclone lsf --csv testdrive:'
	f.write(command)
	f.close()
	f=open("link.txt","w")
	linkp='https://drive.mechabot.ga/0:/MECHATRONICS/'
	f.write(linkp)
	f.close()
	key = []
	del key[:]

	p = subprocess.Popen(command, stdout=subprocess.PIPE)
	for path in iter(p.stdout.readline,b''):
		print(path.decode('utf-8'))
		path =	path.decode('utf-8')
		path1 =	path
		n=len(path)
		if n > 15:
			t1 = path.strip()[:10]
			t2 = path.strip()[n-5:]
			path=t1+"....."+t2
			print(path)
			key.append([InlineKeyboardButton(path,callback_data=path1)])
		else :
			print(path)
			key.append([InlineKeyboardButton(path,callback_data=path)])
		
	key.append([InlineKeyboardButton("Cancel", callback_data="Cancel")])
	reply_markup = InlineKeyboardMarkup(key)
	update.effective_message.reply_text('Please choose:', reply_markup=reply_markup)
  

def button(update, context):
	query = update.callback_query
	query.edit_message_text(text="Selected option: {}".format(query.data))
	txt = query.data
	txt1 = txt.replace(" ","_")
	print(txt1)
	x = re.findall("/$", txt)
	txt=txt.split()[0]
	txt2=txt.split()[0]
	print(txt)     
	if (x):
		with open("adress.txt", "a") as myfile:
			myfile.write(txt2)
		f = open("link.txt", "a")
		f.write(txt2)
		f.close()
		folder1(update, context) 
	if "Cancel" ==txt:
		return 
	if ['/'] != x:
		f = open("link.txt", "r")
		link=f.readlines()
		f.close()
		addr=str(link[0])
		txt1=txt1.replace("_"," ")
		addr=addr+str(txt1)
		addr=addr.replace(" ","%20")
		update.effective_message.reply_text("Link:{}".format(addr))


def folder1(update, context):
	
	f = open("adress.txt", "r")
	command=f.readline()
	f.close()
	key = []
	del key[:]
	print(command)

	result = subprocess.run(command, stdout=subprocess.PIPE,shell=True)
	print(result.stdout)
	t = result.stdout
	line=t.splitlines()
	for path in line:
		print(path)
		path1 = path
		n=len(path)
		if n > 15:
			t1 = path.strip()[:10]
			t2 = path.strip()[n-5:]
			path=t1+"....."+t2
			print(path)
			key.append([InlineKeyboardButton(path,callback_data=path1)])
		else :
			print(path)
			key.append([InlineKeyboardButton(path,callback_data=path)])
			
	key.append([InlineKeyboardButton("Cancel", callback_data="Cancel")])
	reply_markup = InlineKeyboardMarkup(key)
	update.effective_message.reply_text('Please choose:', reply_markup=reply_markup)


def rclone(update, context):
	txt=update.message.text 
	if "/rclone" == txt.strip()[:7]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
		txt=update.message.text 
	
	print(command)
	result = subprocess.run(command, stdout=subprocess.PIPE,shell=True)
	print(result.stdout)
	t = result.stdout
	line=t.splitlines()
	for tx in line:
		print(tx)
		update.message.reply_text(tx)


def rclonecopy(update, context):
	txt=update.message.text 
	if "/rclonecopy" == txt.strip()[:11]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  

	rclonecopyprocess(update, context, command)


def rclonecopyprocess(update, context, command):
	bot = context.bot
	message=update.message.reply_text("STATUS")
	mid=message.message_id
	percent=""
	percent1=""
	working=""
	working1=""
	prog=""
	p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1)
	for toutput in iter(p.stdout.readline,b''):
		print(toutput.decode('utf-8'))
		y= re.findall("^Transferred:", toutput.decode('utf-8'))
		z= re.findall("^ * ", toutput.decode('utf-8'))
		if (y):
			val=str(toutput.decode('utf-8'))
			val=val.split(",")
			percent=str(val[1])
			statu=val[1].replace("%","")
			if statu != " -":
				statu=int(statu)
				prog=status(statu)

		if (z):
			working=str(toutput.decode('utf-8'))

		if working1 != working or percent1 != percent :
			bot.edit_message_text(chat_id=message.chat_id,message_id=mid,text="{} \n {} \n {}".format(percent,prog,working))
			percent1=percent
			working1=working
	p.stdout.close()		


def status(val):
	if val<10 :
		ss= "[                         ]"

	if val>=10 and val<=19:
		ss= "[#                      ]"

	if val>=20 and val<=29:
		ss= "[##                    ]"

	if val>=30 and val<=39:
		ss= "[###                 ]"

	if val>=40 and val<=49:
		ss= "[####               ]"
		
	if val>=50 and val<=59:
		ss= "[#####            ]"

	if val>=60 and val<=69:
		ss= "[######          ]"

	if val>=70 and val<=79:
		ss= "[#######       ]"

	if val>=80 and val<=89:
		ss= "[########     ]"
		
	if val>=90 and val<=99:
		ss= "[#########  ]"
		
	if val==100:
		ss= "[##########]"
	return ss


def backup(update, context):
	
	rclonecopyprocess(update, context, 'rclone copy testdrive:testfolder1 testdrive:testfolder2 -P')
		


def main():
	updater = Updater("965545478:AAEHLnNT39b8F96Xl1CJZfIwg9O-CrxeAWE", use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("rclone", rclone))
	dp.add_handler(CommandHandler("rclonecopy", rclonecopy))
	dp.add_handler(CommandHandler("folder", folder))
	dp.add_handler(CommandHandler("backup", backup))
	dp.add_handler(CallbackQueryHandler(button))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()