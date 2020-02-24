import logging
import time
import os
import re
from subprocess import Popen, PIPE 
from datetime import date
from telegram import  ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
	update.message.reply_text('Hi! To Authorize do /password [password] ')


def help(update, context):
	update.message.reply_text('/start- To Start the Bot \n /help- To Know About the Commands \n '
	'/rclone [COMMAND]- To Run Shell or Rclone Command (except copy) \n'
	'/rclonecopy [COMMAND]- To Copy Files \n'
	'/folder- To Inline View of Folder in Drive \n'
	'/password [PASSWORD]- To Get Authorize \n'
	'/adminpasswprd [Password]- To authorize to use rclone and rclonecopy \n'
	'/backup- to create backup to other drive \n')


def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def createfile():
	f=open("user.txt","w")
	f.close()


if os.path.exists("user.txt") == False :
	createfile()


def createfileA():
	f=open("userA.txt","w")
	f.close()


if os.path.exists("userA.txt") == False :
	createfileA()


def folder(update, context):
	if os.path.exists("adress.txt") == True :
		os.remove("adress.txt")
	if os.path.exists("link.txt") == True :
		os.remove("link.txt")
	f=open("adress.txt","w")
	command='____________RCLONE COMMAND FOR FOLDER VIEW______________'
	f.write(command)
	f.close()
	f=open("link.txt","w")
	linkp='______________HTTP LINK OF BOT_____________'
	f.write(linkp)
	f.close()
	key = []
	del key[:]
	inID=update.message.from_user.id
	checku(update, context, inID)
	if flag==True:
		for path in run(command):
			print path
			key.append([InlineKeyboardButton(path,callback_data=path)])
		
		key.append([InlineKeyboardButton("Cancel", callback_data="Cancel")])
		reply_markup = InlineKeyboardMarkup(key)
		update.effective_message.reply_text('Please choose:', reply_markup=reply_markup)
	else :
		update.message.reply_text("Enter Password!!")  


def button(update, context):
	query = update.callback_query
	query.edit_message_text(text="Selected option: {}".format(query.data))
	txt = query.data
	x = re.findall("/$", txt)     
	if (x):
		f = open("adress.txt", "a")
		f.write(txt)
		f.close()
		f = open("link.txt", "a")
		f.write(txt)
		f.close()
		folder1(update, context) 
	if "Cancel" ==txt:
		return 
	if ['/'] != x:
		f = open("link.txt", "r")
		link=f.readlines()
		f.close()
		addr=str(link[0])
		addr=addr+str(txt)
		addr=addr.replace(" ","%20")
		update.effective_message.reply_text("Link:{}".format(addr))


def folder1(update, context):
	
	f = open("adress.txt", "r")
	command=f.readline()
	f.close()
	key = []
	del key[:]
	print command
	for path in run(command):
		print path
		key.append([InlineKeyboardButton(path,callback_data=path)])
	key.append([InlineKeyboardButton("Cancel", callback_data="Cancel")])
	reply_markup = InlineKeyboardMarkup(key)
	update.effective_message.reply_text('Please choose:', reply_markup=reply_markup)


def checku(update, context, inID):
	f = open("user.txt", "r")
	global flag
	flag=False
	t1= '\n'
	ch= str(inID)+ t1
	for x in f:
		if x==ch :
			print "User Found"
			flag=True
		else :
			print "User Not Found"


def checkuA(update, context, inID):
	f = open("userA.txt", "r")
	global flagA
	flagA=False
	t1= '\n'
	ch= str(inID)+ t1
	for x in f:
		if x==ch :
			print "User Found"
			flagA=True
		else :
			print "User Not Found"


def addu(update, context, Uid):
	f = open("user.txt", "a")
	t2='\n'
	txt=str(Uid)+t2
	print txt
	f.write(txt)
	f.close()
	f = open("user.txt", "r")
	print(f.readlines())


def adduA(update, context, Uid):
	f = open("userA.txt", "a")
	t2='\n'
	txt=str(Uid)+t2
	print txt
	f.write(txt)
	f.close()
	f = open("userA.txt", "r")
	print(f.readlines())


def rclone(update, context):
	txt=update.message.text 
	if "/rclone" == txt.strip()[:7]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
	inID=update.message.from_user.id
	checkuA(update, context, inID)
	if flagA == True :
		for path in run(command):
			print path
			update.message.reply_text(path)
	else:
		update.message.reply_text("Enter Admin Password!")


def rclonecopy(update, context):
	txt=update.message.text 
	if "/rclonecopy" == txt.strip()[:11]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
	inID=update.message.from_user.id
	checkuA(update, context, inID)
	if flagA == True :
		rclonecopyprocess(update, context, command)
	else:
		update.message.reply_text("Enter Admin Password!")
	update.message.reply_text("Done!!")


def rclonecopyprocess(update, context, command):
	bot = context.bot
	message=update.message.reply_text("STATUS")
	mid=message.message_id
	percent=""
	percent1=""
	working=""
	working1=""
	prog=""
	for toutput in run(command):
		print toutput
		y= re.findall("^Transferred:", toutput)
		z= re.findall("^ * ", toutput)
		if (y):
			val=str(toutput)
			val=val.split(",")
			percent=str(val[1])
			statu=val[1].replace("%","")
			if statu != " -":
				statu=int(statu)
				prog=status(statu)

		if (z):
			working=str(toutput)

		if working1 != working or percent1 != percent :
			bot.edit_message_text(chat_id=message.chat_id,message_id=mid,text="{} \n {} \n {}".format(percent,prog,working))
			percent1=percent
			working1=working


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


def run(command):
	process=Popen(command,stdout=PIPE,shell=True)
	while True:
		line=process.stdout.readline().rstrip()
		if not line:
			break
		yield line


def backup(update, context):
	inID=update.message.from_user.id
	checkuA(update, context, inID)
	today=date.today()
	if flagA == True :
		rclonecopyprocess(update, context, '________RCLONE COMMAND TO CREATE BACKUP______________')
		
	else:
		update.message.reply_text("Enter Admin Password!")
	update.message.reply_text("Done!!")


def adminpassword(update, context):  
	txt = update.message.text

	if "/adminpassword" == txt.strip()[:14]:
		admin_password = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correctly")
	if 'ADMINPASSWORD' == admin_password :
		update.message.reply_text('Correct Password')
		Uid=update.message.from_user.id
		adduA(update, context, Uid)
		addu(update, context, Uid)
	else:
		update.message.reply_text('Incorrect Password')


def password(update, context):  
	txt = update.message.text

	if "/password" == txt.strip()[:9]:
		used_password = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correctly")
	if 'USERPASSWORD' == used_password :
		update.message.reply_text('Correct Password')
		Uid=update.message.from_user.id
		addu(update, context, Uid)
	else:
		update.message.reply_text('Incorrect Password')


def main():
	updater = Updater("TOKEN", use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("rclone", rclone))
	dp.add_handler(CommandHandler("rclonecopy", rclonecopy))
	dp.add_handler(CommandHandler("password", password))
	dp.add_handler(CommandHandler("adminpassword", adminpassword))
	dp.add_handler(CommandHandler("folder", folder))
	dp.add_handler(CommandHandler("backup", backup))
	dp.add_handler(CallbackQueryHandler(button))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
