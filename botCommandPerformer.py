def bot_command_about(sbot, sender, pattern, **kwargs):
    sbot.bot.chat(pattern.format(name=sender, msg="本机器人使用mineflayer开源项目为框架,开发者StrayMeteor3337,感谢支持"))
    sbot.bot.chat(pattern.format(name=sender, msg="机器人开源地址: https://github.com/StrayMeteor3337/Minecraft-Stray_bot"))


def bot_command_help(sbot, sender, pattern, **kwargs):
    sbot.bot.chat(pattern.format(name=sender, msg="请到开源仓库获取机器人命令的详细信息,使用@bot about来获取开源仓库地址"))


def bot_command_here(sbot, sender, pattern, **kwargs):  # sbot参数为机器人类Stray_bot的实例
    # 判断距离最近的玩家进行跟随
    target = sbot.bot.players[sender]
    if target.entity:
        bot_movements = sbot.Movements(sbot.bot)  # 机器人移动配置
        bot_movements.canDig = False  # 禁止破坏方块
        bot_movements.allow1by1towers = False  # 禁止搭方块
        sbot.bot.pathfinder.setMovements(bot_movements)  # 加载移动配置
        p = target.entity.position
        sbot.bot.pathfinder.setGoal(sbot.goals.GoalNear(p.x, p.y, p.z, 1))  # 设置目标
        sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]我正在过来"))
    else:
        sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]无法找到玩家,请走近一些"))


def bot_command_stop(sbot, sender, pattern, **kwargs):
    sbot.bot.pathfinder.stop()#终止寻路
    #sbot.bot.pathfinder.setGoal(None)#确保终止寻路
    sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]已停止所有寻路"))


def bot_command_bed(sbot, sender, pattern, **kwargs):
    if sbot.bot.game.dimension == "the_nether" or sbot.bot.game.dimension == "the_end":
        sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]不允许在下界或末地使用床,因为这会导致爆炸"))
        return
    bed_pos = sbot.bot.findBlock({"matching": sbot.bot.isABed, "maxDistance": 5})
    if bed_pos:
        if sbot.bot.time.isDay:
            sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]请在夜晚设置重生点"))
            return
        sbot.bot.activateBlock(bed_pos)  # 右键使用床来设置重生点
        sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]重生点已设置"))
    else:
        sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]无法找到床"))


def bot_command_where(sbot, sender, pattern, **kwargs):
    botX = sbot.bot.player.entity.position.x
    botY = sbot.bot.player.entity.position.y
    botZ = sbot.bot.player.entity.position.z
    sbot.bot.chat(pattern.format(name=sender, msg="[bot命令]当前位置 {x} {y} {z}".format(x=botX, y=botY, z=botZ)))


# 离线版本专有执行器
def bot_command_fork(sbot, sneder, pattern, **kwargs):
    bots = kwargs["bots"]
    bot_sum = len(bots)
    new_bot_name = "{name}_{num}".format(name=bots["Main"].name, num=str(bot_sum + 1))
    # bots[new_bot_name] = Stray_bot_offline.Stray_bot(bots["Main"].host, new_bot_name, bots["Main"].port, False)
