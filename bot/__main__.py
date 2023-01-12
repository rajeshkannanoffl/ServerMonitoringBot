import os
import psutil
import telebot
import subprocess
from dotenv import load_dotenv

# data to be entered in config.env loacted at root-folder
# add bot-token in API_KEY
# add True for emoji ui deployment
load_dotenv('config.env', override=True)
API_KEY = os.getenv("API_KEY")
EMOJI_UI = os.getenv("EMOJI_UI")

# connecting to the telegram bot
bot = telebot.TeleBot(API_KEY)

# start command (/start)
@bot.message_handler(commands=['start'])
def start(message):
    if EMOJI_UI=="True":
        ui_msg = '''
Hello Mate, ✌️
→ Welcome to Server Monitoring Bot. 🤖
→ With me you can get to know the status of your Server, VPS, VM or even your PC/Laptop.
[👨‍💻 Connect with Dev @rajeshkannanoffl 🙋‍♂️]
        '''
        bot.send_message(message.chat.id, ui_msg)
    else:
        msg = '''
Hello Mate,
→ Welcome to Server Monitoring Bot.
→ With me you can get to know the status of your Server, VPS, VM or even your PC/Laptop.
[Connect with Dev @rajeshkannanoffl]
        '''
        bot.send_message(message.chat.id, msg)

# help command (/help)
@bot.message_handler(commands=['help'])
def help(message):
    msg = '''
Hi, I'm Server Monitoring Bot.
Here are some Commands you can send me,
/status → Health of the Server.
/disk → Disk Usage Details (in GB).
/sysinfo → CPU (%) and RAM Usage (in GB).
/uptime → Uptime of the Server.
/serverinfo → Some Description of the Server.
/help → I'm open to Help You.
    '''
    bot.send_message(message.chat.id, msg)

# up status (/status)
@bot.message_handler(commands=['status'])
def check(message):
    if EMOJI_UI=="True":
        ui_msg = '''
Hey, My Health is Good 🟢.
Stay Safe 😷, Stay Healthy ❤️.
        '''
        bot.send_message(message.chat.id, ui_msg)
    else:
        msg = '''
Hey, My Health is Good.
Stay Safe, Stay Healthy.
        '''
        bot.send_message(message.chat.id, msg)

# disk usage (/disk) in GB
@bot.message_handler(commands=['disk'])
def disk(message):
    diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))      # kb*mb*gb
    diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
    diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
    diskPercent = psutil.disk_usage('/').percent

    if EMOJI_UI=="True":
        ui_msg = '''
╭─《 💾 DISK INFO 💾 》
├ 💽 Total = {} GB
├ 🗒️ Used = {} GB
├ 🆓 Available = {} GB
╰ 🧻 Usage = {} %
        '''.format(diskTotal,diskUsed,diskAvail,diskPercent)
        bot.send_message(message.chat.id,ui_msg)
    else:
        msg = '''
╭─《 DISK INFO 》
├ Total = {} GB
├ Used = {} GB
├ Available = {} GB
╰ Usage = {} %
        '''.format(diskTotal,diskUsed,diskAvail,diskPercent)
        bot.send_message(message.chat.id,msg)

# cpu & ram (/sysinfo) (cpu in percent & ram in GB)
@bot.message_handler(commands=['sysinfo'])
def sysinfo(message):
    cpuUsage = psutil.cpu_percent(interval=1)
    ramTotal = int(psutil.virtual_memory().total/(1024*1024*1024)) #GB
    ramUsage = int(psutil.virtual_memory().used/(1024*1024*1024)) #GB
    ramFree = int(psutil.virtual_memory().free/(1024*1024*1024)) #GB
    ramUsagePercent = psutil.virtual_memory().percent

    if EMOJI_UI=="True":
        ui_msg = '''
╭─《 🛠️ CPU INFO 🛠️ 》
├ 🖥️ CPU Usage = {} %  
│
├《 💠 RAM INFO 💠 》
├ 💿 Total = {} GB     
├ 🗒️ Used = {} GB      
├ 🆓 Available = {} GB 
╰ 🧻 Usage = {} %
        '''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)
        bot.send_message(message.chat.id,ui_msg)
    else:
        msg = '''
╭─《 CPU INFO 》
├ CPU Usage = {} %  
│
├《 RAM INFO 》
├ Total = {} GB     
├ Used = {} GB      
├ Available = {} GB 
╰ Usage = {} %
        '''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)
        bot.send_message(message.chat.id,msg)
    

# uptime (/uptime)
@bot.message_handler(commands=['uptime'])
def uptime(message):
    upTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')
    if EMOJI_UI=="True":
        ui_msg = '''
⌛ {}
        '''.format(upTime)
        bot.send_message(message.chat.id,ui_msg)
    else:
        msg = '''
{}
        '''.format(upTime)
        bot.send_message(message.chat.id,msg)


# server desc (/serverinfo)
@bot.message_handler(commands=['serverinfo'])
def server(message):
    uname = subprocess.check_output(['uname','-rsoi']).decode('UTF-8')
    host = subprocess.check_output(['hostname']).decode('UTF-8')
    ipAddr = subprocess.check_output(['hostname','-I']).decode('UTF-8')

    if EMOJI_UI=="True":
        ui_msg = '''
《 ⚙️ SERVER INFO ⚙️ 》

☢️ OS = {} 
🆔 Hostname = {}
🔑 IP Address = {}
        '''.format(uname,host,ipAddr)
        bot.send_message(message.chat.id,ui_msg)
    else:
        msg = '''
《 SERVER INFO 》
OS = {} 
Hostname = {}
IP Address = {}
        '''.format(uname,host,ipAddr)
        bot.send_message(message.chat.id,msg)

# listen to telegram commands
bot.polling()