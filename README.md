# Rclone-Telegram-Bot
This is Rclone Bot in Telegram made for your ease.


Step 1. Copy code to your VPS or local machine
---------------------------------
_Before everything, install python3. Because we use python as our programing language._

### Download Rclone ###

**For Linux system**: Install
[latest rclone](https://rclone.org/downloads/#script-download-and-install). 
If in Debian/Ubuntu, directly use this command
```
sudo apt-get install screen git && curl https://rclone.org/install.sh | sudo bash
```
After all dependency above are successfully installed, run this command
```
sudo git clone https://github.com/xyou365/AutoRclone && cd AutoRclone && sudo pip3 install -r requirements.txt
```

**For Window system**: Install
[latest rclone](https://rclone.org/downloads/)


### Download Python Telegram Bot ###
You can install or upgrade python-telegram-bot with:
```
    $ pip install python-telegram-bot --upgrade
```
Or you can install from source with:
```
    $ git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
    $ cd python-telegram-bot
    $ python setup.py install
```
In case you have a previously cloned local repository already, you should initialize the added urllib3 submodule before installing with:
```
    $ git submodule update --init --recursive
```
Step 2. Prerequisite For Starting The Bot
---------------------------------
* Configure the Rclone like- adding the drive to rclone
* Add this to config file 
  ```
  server_side_across_configs = true
  ```
  To find the location of Rclone Config File type
  ```
  rclone config file
  ```

Step 3. Start The Bot
---------------------------------
Open Terminal or CMD in the directory/folder where the bot.py is stored
To start bot type 
```
python bot.py
```
HOW TO USE THIS BOT!
---------------------------------
* ### /start ###
  This command will start the bot 

* ###  /help  ###
  To Know About the Commands and How to use them
* ### /rclone [command]
  To Run Shell or Rclone Command, for example to list folder in drive1
  ```
  /rclone lsf --csv "drive1"
  ```
  Don't run copy command it will ####BAN your bot
* ### /rclonecopy [command] ###
  To Copy Files from drive1 to drive2, for example
  ```
  /rclonecopy rclone copy "drive1:subfolder" "drive2:subfolder" -P
  ```
* ### /folder ###
  To Show Inline View of Folder in Drive
  Change it to your drive before Running the Code 
* ### /password [password] ###
  To Get Authorize to use the Bot
  The default password is **password**
  i.e
  ```
  /password password
  ```
  
