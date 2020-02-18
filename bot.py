import logging
import time
import os
import re
from subprocess import Popen, PIPE 
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
	'/password [PASSWORD]- To Get Authorize \n')


def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def createfile():
	f=open("user.txt","w")
	f.close()


if os.path.exists("user.txt") == False :
	createfile()


def folder(update, context):
	if os.path.exists("adress.txt") == True :
		os.remove("adress.txt")
	if os.path.exists("link.txt") == True :
		os.remove("link.txt")
	f=open("adress.txt","w")
	command='rclone lsf --csv "_____________ENTER DRIVE NAME__________"'
	f.write(command)
	f.close()
	f=open("link.txt","w")
	linkp='https://_______bot link___________'
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
	else:
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


def addu(update, context, Uid):
	f = open("user.txt", "a")
	t2='\n'
	txt=str(Uid)+t2
	print txt
	f.write(txt)
	f.close()
	f = open("user.txt", "r")
	print(f.readlines())


def rclone(update, context):
	txt=update.message.text 
	if "/rclone" == txt.strip()[:7]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
	inID=update.message.from_user.id
	checku(update, context, inID)
	if flag == True :
		for path in run(command):
			print path
			update.message.reply_text(path)
	else:
		update.message.reply_text("Enter Password!")


def rclonecopy(update, context):
	txt=update.message.text 
	if "/rclonecopy" == txt.strip()[:11]:
		command = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correct Command")  
	inID=update.message.from_user.id
	checku(update, context, inID)
	if flag == True :
		rclonecopyprocess(update, context, command)
	else:
		update.message.reply_text("Enter Password!")
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
			bot.edit_message_text(chat_id=message.chat_id,message_id=mid,text="Complete:{} \n {} \n {}".format(percent,prog,working))
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


def password(update, context):  
	txt = update.message.text

	if "/password" == txt.strip()[:9]:
		used_password = " ".join(txt.strip().split(" ")[1:])
	else :
		update.message.reply_text("Enter Correctly")    
	if 'password' == used_password :
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
	dp.add_handler(CommandHandler("folder", folder))
	dp.add_handler(CallbackQueryHandler(button))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
