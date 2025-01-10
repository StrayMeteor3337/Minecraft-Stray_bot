def bot_command_follow(bot,sender,**kwarg):#bot参数为机器人类Straybot的实例
    # 判断距离最近的玩家进行跟随
    target = bot.bot.players[sender]
    print(target)
    if target.entity:
        bot_movements = bot.Movements(bot.bot)  # 机器人移动配置
        bot_movements.canDig = False  # 禁止破坏方块
        bot_movements.allow1by1towers = False  # 禁止搭方块
        bot.bot.pathfinder.setMovements(bot_movements)  # 加载移动配置
        p = target.entity.position
        bot.bot.pathfinder.setGoal(bot.goals.GoalNear(p.x, p.y, p.z, 1))  # 设置目标
        bot.bot.chat("[bot命令]我正在过来")
    else:
        bot.bot.chat("[bot命令]无法找到玩家,请走近一些")