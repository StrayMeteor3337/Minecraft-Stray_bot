import time
from javascript import require, On

from botUtils import bot_command_offline, message_pattern, message_pattern_whisper


class Stray_bot():
    def __init__(self, host, name, port=25565, isMain=True):
        print("软件作者:StrayMeteor3337")
        self.tplock = False
        self.enable_log = False
        self.host = host
        self.name = name
        self.port = port
        self.isMain = isMain

        mineflayer = require("mineflayer")
        self.pathfinder = require('mineflayer-pathfinder').pathfinder
        # self.pathfinder不能用，self.bot.pathfinder才是加载后的寻路插件
        self.Movements = require('mineflayer-pathfinder').Movements
        self.goals = require('mineflayer-pathfinder').goals
        # Viewer = require("prismarine-viewer").mineflayer
        self.bot = mineflayer.createBot({
            "host": self.host,  # minecraft server ip
            "username": self.name,  # username or email, switch if you want to change accounts
            "auth": "offline",  # for offline mode servers, you can set this to 'offline'
            "port": self.port,  # only set if you need a port that isn't 25565
            "version": "1.21.4",
        })
        self.bot.loadPlugin(self.pathfinder)
        self.bot.on('kicked', self.reconnect)
        self.bot.on('error', self.reconnect)
        print("加载完成")

        @On(self.bot, 'login')
        def handleLogin(*args):
            # Viewer(self.bot, {"port": 3007, "firstPerson": False})
            print("\n已进入服务器")

        @On(self.bot, 'spawn')
        def handleSpawn(*args):
            self.bot.chat("/reg Stray3337 Stray3337")
            # self.bot.chat("/logout")
            self.bot.chat("/login Stray3337")
            self.bot.chat("[bot]登录成功 版本1.2")
            self.bot.chat("/tpa StrayMeteor3337")

        @On(self.bot, 'message')
        def handleMsg(this, jsonMsg, position, sender, *args):
            log = "[{t}]".format(t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + jsonMsg.toString() + "\n"
            # if self.enable_log:
            # with open("Stray_bot.txt", mode="a+") as file:
            # file.write(log)
            if isMain:
                print(log)

            if jsonMsg.toString().startswith("[TPA]") and isMain and self.enable_log == False:  # 只有主机器人才启用日志功能
                self.enable_log = True

        @On(self.bot, 'chat')
        def handleChat(this, sender, message, *args):
            try:
                if message.startswith("@bot"):  # @bot为机器人指令标志
                    handle_bot_command(self, sender, message, message_pattern)
            except Exception as e:
                self.bot.chat("[bot命令]执行命令时出现错误")
                print(e)

        @On(self.bot, 'whisper')
        def handleWhisper(this, sender, message, *args):
            try:
                # 私聊即默认为执行bot命令,因此无需加@bot,若命令不以@bot开头,则添加@bot前缀
                if message.startswith("@bot"):  # @bot为机器人指令标志
                    handle_bot_command(self, sender, message, message_pattern_whisper)
                else:
                    new_msg = "@bot {msg}".format(msg=message)
                    handle_bot_command(self, sender, new_msg, message_pattern_whisper)
            except Exception as e:
                self.bot.chat("[bot命令]执行命令时出现错误")
                print(e)

    def send_msg(self, msg):
        self.bot.chat(msg)

    def reconnect(self, *args):
        time.sleep(30)
        print(args[-1])
        restart_bot(Stray_bot(self.host, self.name, self.port, self.isMain))


def handle_bot_command(bot, sender, command_str, pattern):  # bot参数为Straybot类的实例，pattern参数为机器人聊天消息模板
    params = command_str.split()  # params为命令参数列表，形如["@bot","follow"]
    performer = bot_command_offline.get(params[1])
    if performer:  # 调用命令bot_command字典中的命令执行函数
        performer(bot, sender, pattern)


def restart_bot(new_bot_instance):
    bots[new_bot_instance.name] = new_bot_instance


if __name__ == "__main__":
    server = "play.simpfun.cn"
    server_port = 12135
    StrayBot = Stray_bot(server, "StrayBot", server_port)
    bots = {"Main": StrayBot}  # 用于管理多个Stray_bot实例
    while True:
        console_input = input("发送:")
        StrayBot.send_msg(console_input)
        # if console_input.startswith("@bot"):
        #    handle_bot_command(console_input, bots)
