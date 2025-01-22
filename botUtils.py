import botCommandPerformer as bcp

# 机器人聊天消息模板，用于在接收到私聊指令后用私聊回复
message_pattern = "{msg}"
message_pattern_whisper = "/msg {name} {msg}"

# 更新命令时在这里添加
bot_command = {"here": bcp.bot_command_here,
               "stop": bcp.bot_command_stop,
               "bed": bcp.bot_command_bed,
               "where": bcp.bot_command_where,
               "help": bcp.bot_command_help,
               "about": bcp.bot_command_about}

bot_command_offline = {"here": bcp.bot_command_here,
                       "stop": bcp.bot_command_stop,
                       "bed": bcp.bot_command_bed,
                       "where": bcp.bot_command_where,
                       "help": bcp.bot_command_help,
                       "about": bcp.bot_command_about}
