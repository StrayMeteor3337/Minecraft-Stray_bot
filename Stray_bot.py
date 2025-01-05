import sys
import time
import threading
from javascript import require, On

class Stray_bot():
    def __init__(self, host,name,port=25565,isMain=True):
        print("软件作者:StrayMeteor3337")
        self.tplock = False
        self.enable_log = False
        self.host = host
        self.name = name
        self.port = port
        self.isMain = isMain

        mineflayer = require("mineflayer")
        #Viewer = require("prismarine-viewer").mineflayer
        self.bot = mineflayer.createBot({
            "host": self.host,  # minecraft server ip
            "username": self.name,  # username or email, switch if you want to change accounts
            "auth": "offline",  # for offline mode servers, you can set this to 'offline'
            "port": self.port,  # only set if you need a port that isn't 25565
            "version": "1.20.2",
            "defaultChatPatterns": False,
            #"respawn": False
            #"loadInternalPlugins": False,
            # only set if you need a specific version or snapshot (ie: 1.8.9 or 1.16.5), otherwise it's set automatically
            # password: '12345678'        # set if you want to use password-based auth (may be unreliable). If specified, the `username` must be an email
        })
        self.bot.on('kicked', self.reconnect)
        self.bot.on('error', self.reconnect)
        print("加载完成")

        def handleTP(tpaMessage):

            start_str = "玩家"
            end_str = "向你申请传送至你的位置"
            player_name_start = tpaMessage.find("玩家") + len(start_str)
            player_name_end = tpaMessage.find("向你申请传送至你的位置")
            player_name = tpaMessage[player_name_start:player_name_end]
            # [TPA]玩家StrayMeteor3337向你申请传送至你的位置!有效时间60秒
            self.bot.chat("/tpa accept {name}".format(name = player_name))
            time.sleep(2)

        @On(self.bot, 'login')
        def handleLogin(*args):
            #Viewer(self.bot, {"port": 3007, "firstPerson": False})
            print("\n已进入服务器")
            self.bot.chat("/reg Stray3337 Stray3337")
            time.sleep(1)
            # self.bot.chat("/logout")
            time.sleep(2)
            self.bot.chat("/login Stray3337")
            time.sleep(2)
            self.bot.chat("[bot]登录成功 版本1.0")
            self.bot.chat("/tpa go StrayMeteor3337")


        @On(self.bot, 'message')
        def handleMsg(this, jsonMsg, position, sender, *args):
            log = "[{t}]".format(t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + jsonMsg.toString() + "\n"
            if self.enable_log:
                with open("Stray_bot.txt",mode="a+") as file:
                    file.write(log)
            if isMain:
                print(log)

            if jsonMsg.toString().startswith("[TPA]") and isMain and self.enable_log == False:#只有主机器人才启用日志功能
                self.enable_log = True

            #处理tpa请求
            if "向你申请传送至你的位置" in jsonMsg.toString():
                if self.tplock:
                    self.bot.chat("[bot命令]拒绝请求，您没有权限在在tplock开启时传送机器人")
                    #self.bot.chat("/deny")
                handleTP(jsonMsg.toString())

        @On(self.bot, 'chat')
        def handleChat(this, sender, message, *args):

            # print("\n获取信息", sender, message)
            if message.startswith("@bot") and len(message.split()) >= 2:
                if message.split()[1] == "tl":
                    self.tplock = not self.tplock
                    if self.tplock:
                        self.bot.chat("[bot命令]tplock已开启")
                    else:
                        self.bot.chat("[bot命令]tplock已关闭")
                if message.split()[1] == "d":
                    self.bot.chat("[bot命令]正在断开连接")
                # bot.quit()
                # sys.exit()

            """
            if 'has sent you a teleport here request' in message:
                if tplock:
                    self.bot.chat("[bot命令]拒绝请求，您没有权限在在tplock开启时传送机器人")
                    self.bot.chat("/deny")
                    return
                self.bot.chat("/accept")
                time.sleep(2)
            """

    def send_msg(self, msg):
        self.bot.chat(msg)

    def reconnect(self,*args):
        time.sleep(30)
        print(args[-1])
        restart_bot(Stray_bot(self.host, self.name, self.port,self.isMain))

def fork(bots):
    bot_sum = len(bots)
    new_bot_name = "{name}_{num}".format(name=bots["Main"].name,num=str(bot_sum + 1))
    bots[new_bot_name] = Stray_bot(bots["Main"].host,new_bot_name,bots["Main"].port,False)

def handle_bot_command(command_str,bots):
    command_list = command_str.split()
    method = bot_command.get(command_list[1])
    if method:
        method(bots)

def restart_bot(new_bot_instance):
    bots[new_bot_instance.name] = new_bot_instance

bot_command = {"fork":fork,"tl":print}

if __name__ == "__main__":
    server = "mc.freespace.host"
    server_port = 20033
    StrayBot = Stray_bot(server,"Stray_bot_test",server_port)
    bots = {"Main":StrayBot}#用于管理多个Stray_bot实例
    while True:
        console_input = input("发送:")
        if console_input.startswith("@bot"):
            handle_bot_command(console_input,bots)
