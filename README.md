# Rclone-Telegram-Bot
This is Rclone Bot in Telegram made for your ease.
Code has been updated for latest Python [CODE](https://github.com/Shubham0Rajput/Rclone-Telegram-Bot/blob/master/bot(12-September-2020).py)


Step 1. Copy code to your VPS or local machine
---------------------------------
_Before everything, install python3. Because we use python as our programing language._

### Download Rclone ###

** For Linux system**: Install
[latest rclone](https://rclone.org/downloads/#script-download-and-install). 
If in Debian/Ubuntu, directly use this command
```
sudo apt-get install screen git && curl https://rclone.org/install.sh | sudo bash
```
After all dependency above are successfully installed, run this command
```
sudo git clone https://github.com/xyou365/AutoRclone && cd AutoRclone && sudo pip3 install -r requirements.txt
```

** For Window system**: Install
[latest rclone](https://rclone.org/downloads/)
 
** Bot Along with Rclone files
[Download](https://github.com/Shubham0Rajput/Rclone-Telegram-Bot/blob/master/rclone-v1.53.0-windows-amd64.zip)


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
* Also Install Some pip files
  ```
  pip install subprocess.run
  ```
  ```
  pip install subprocess32
  ```
  subprocess is updated recently

Step 3. Start The Bot
---------------------------------
* Complete the code by adding your Drive details ** Line-38,235 for best experience ** also Line-42,230 for best experience 
* Copy the Bot where rclone.exe is present(in case of windows)
* Just run bot anywhere in case of Linux
* Open Terminal or CMD in the directory/folder where the bot.py is stored
To start bot type 
```
python bot.py
```
HOW TO USE THIS BOT!
---------------------------------
* ### /start ###
  This command to check is bot runing or not

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
  /rclonecopy rclone copy drive1:subfolder drive2:subfolder -P
  ```
* ### /folder ###
  To Show Inline View of Folder in Drive
  Change it to your drive before Running the Code 

* ### /backup ###
  To Create the Backup 
  i.e
  ```
  /backup
  ```
![](https://github.com/Shubham0Rajput/Rclone-Telegram-Bot/blob/master/result.gif) 
