import time
from javascript import require, On
from botUtils import bot_command,message_pattern,message_pattern_whisper
class Stray_bot(object):
    def __init__(self, host, name, port=25565):
        print("软件作者:StrayMeteor3337")
        # self.tplock = False
        self.enable_log = False  # 启用聊天日志
        self.host = host
        self.name = name
        self.port = port
        # 导入nodejs模块
        self.mineflayer = require("mineflayer")
        self.pathfinder = require('mineflayer-pathfinder').pathfinder
        # self.pathfinder不能用，self.bot.pathfinder才是加载后的寻路插件
        self.Movements = require('mineflayer-pathfinder').Movements
        self.goals = require('mineflayer-pathfinder').goals
        # Viewer = require("prismarine-viewer").mineflayer
        self.bot = self.mineflayer.createBot({
            "host": self.host,  # 服务器地址
            "username": self.name,  # 玩家名称
            "auth": "microsoft",  # 身份验证选项,离线服务器请使用'offline'
            "port": self.port,  # 服务器端口
            "version": "1.21.4"  # Minecraft服务器版本
        })
        self.bot.loadPlugin(self.pathfinder)
        self.bot.on('kicked', self.reconnect)  # 错误时重连
        self.bot.on('error', self.reconnect)  # 错误时重连
        print("加载完成")

        def handleTP(tpaMessage):
            pass

        @On(self.bot, 'login')
        def handleLogin(*args):
            # Viewer(self.bot, {"port": 3007, "firstPerson": False})
            print("\n已进入服务器")
            self.bot.chat("[bot]登录成功 版本1.2")

        @On(self.bot, 'message')
        def handleMsg(this, jsonMsg, position, sender, *args):
            # 记录聊天消息到日志文件
            log = "[{t}]".format(t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + jsonMsg.toString() + "\n"
            if self.enable_log:
                with open("Stray_bot.txt", mode="a+") as file:
                    file.write(log)
            print(log)

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
                #私聊即默认为执行bot命令,因此无需加@bot,若命令不以@bot开头,则添加@bot前缀
                if message.startswith("@bot"):  # @bot为机器人指令标志
                    handle_bot_command(self, sender, message, message_pattern_whisper)
                else:
                    new_msg="@bot {msg}".format(msg=message)
                    handle_bot_command(self, sender, new_msg, message_pattern_whisper)
            except Exception as e:
                self.bot.chat("[bot命令]执行命令时出现错误")
                print(e)

    def send_msg(self, msg):
        self.bot.chat(msg)

    def reconnect(self, *args):
        time.sleep(30)
        print(args[-1])
        Stray_bot(self.host, self.name, self.port)  # 自动重连


def handle_bot_command(bot, sender, command_str, pattern):  # bot参数为Straybot类的实例，pattern参数为机器人聊天消息模板
    params = command_str.split()  # params为命令参数列表，形如["@bot","follow"]
    performer = bot_command.get(params[1])
    if performer:  # 调用命令bot_command字典中的命令执行函数
        performer(bot, sender, pattern)

if __name__ == "__main__":
    server = "43.248.186.253"
    server_port = 20016
    StrayBot = Stray_bot(server, "WaxSeeker068070", server_port)
    while True:
        console_input = input("发送:")
        StrayBot.send_msg(console_input)
