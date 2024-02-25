import json, sys, os
import discord
from discord.ext import commands
from core import Context


def updateDB(guildID, data):
  with open("database1.json", "r") as config:
    config = json.load(config)
  config["guilds"][str(guildID)] = data
  newdata = json.dumps(config, indent=4, ensure_ascii=False)
  with open("database1.json", "w") as config:
    config.write(newdata)


def getDB(guildID):
  with open("database1.json", "r") as config:
    data = json.load(config)
  if str(guildID) not in data["guilds"]:
    defaultConfig = {
      "welcome": {
        "autodel": 0,
        "channel": [],
        "color": "",
        "embed": False,
        "footer": "",
        "image": "",
        "message": "<<user.mention>> Welcome To <<server.name>>",
        "ping": False,
        "title": "",
        "thumbnail": ""
      },
      "autorole": {
        "bots": [],
        "humans": []
      },
      "vcrole": {
        "bots": "",
        "humans": ""
      }
    }
    updateDB(guildID, defaultConfig)
    return defaultConfig
  return data["guilds"][str(guildID)]


def getConfig(guildID):
  with open("config.json", "r") as config:
    data = json.load(config)
  if str(guildID) not in data["guilds"]:
    defaultConfig = {
      "antiSpam": False,
      "antiLink": False,
      "whitelisted": [],
      "admins": [],
      "adminrole": None,
      "punishment": "ban",
      "prefix": "a!",
      "staff": None,
      "vip": None,
      "girl": None,
      "guest": None,
      "frnd": None,
      "wlrole": None,
      "reqrole": None
    }
    updateConfig(guildID, defaultConfig)
    return defaultConfig
  return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
  with open("config.json", "r") as config:
    config = json.load(config)
  config["guilds"][str(guildID)] = data
  newdata = json.dumps(config, indent=4, ensure_ascii=False)
  with open("config.json", "w") as config:
    config.write(newdata)


def add_user_to_blacklist(user_id: int) -> None:
  with open("blacklist.json", "r") as file:
    file_data = json.load(file)
    if str(user_id) in file_data["ids"]:
      return

    file_data["ids"].append(str(user_id))
  with open("blacklist.json", "w") as file:
    json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int) -> None:
  with open("blacklist.json", "r") as file:
    file_data = json.load(file)
    file_data["ids"].remove(str(user_id))
  with open("blacklist.json", "w") as file:
    json.dump(file_data, file, indent=4)


def blacklist_check():

  def predicate(ctx):
    with open("blacklist.json") as f:
      data = json.load(f)
      if str(ctx.author.id) in data["ids"]:
        return False
      return True

  return commands.check(predicate)


def restart_program():
  python = sys.executable
  os.execl(python, python, *sys.argv)


def getbadges(userid):
  with open("badges.json", "r") as f:
    data = json.load(f)
  if str(userid) not in data:
    default = []
    makebadges(userid, default)
    return default
  return data[str(userid)]


def makebadges(userid, data):
  with open("badges.json", "r") as f:
    badges = json.load(f)
  badges[str(userid)] = data
  new = json.dumps(badges, indent=4, ensure_ascii=False)
  with open("badges.json", "w") as w:
    w.write(new)


def getanti(guildid):
  with open("anti.json", "r") as config:
    data = json.load(config)
  if str(guildid) not in data["guilds"]:
    default = "off"
    updateanti(guildid, default)
    return default
  return data["guilds"][str(guildid)]


def updateanti(guildid, data):
  with open("anti.json", "r") as config:
    config = json.load(config)
  config["guilds"][str(guildid)] = data
  newdata = json.dumps(config, indent=4, ensure_ascii=False)
  with open("anti.json", "w") as config:
    config.write(newdata)


def add_channel_to_ignore(user_id: int) -> None:
  with open("ignore.json", "r") as file:
    file_data = json.load(file)
    if str(user_id) in file_data["ids"]:
      return

    file_data["ids"].append(str(user_id))
  with open("ignore.json", "w") as file:
    json.dump(file_data, file, indent=4)


def remove_channel_from_ignore(user_id: int) -> None:
  with open("ignore.json", "r") as file:
    file_data = json.load(file)
    file_data["ids"].remove(str(user_id))
  with open("ignore.json", "w") as file:
    json.dump(file_data, file, indent=4)


def ignore_check():

  def predicate(ctx):
    with open("ignore.json") as f:
      data = json.load(f)
      if str(ctx.channel.id) in data["ids"]:
        return False
      return True

  return commands.check(predicate)


def getlogger(guildid):
  with open("logs.json", "r") as ok:
    data = json.load(ok)
  if str(guildid) not in data:
    default = {"channel": ""}
    makelogger(guildid, default)
    return default
  return data[str(guildid)]


def makelogger(guildid, data):
  with open("logs.json", "r") as f:
    logs = json.load(f)
  logs[str(guildid)] = data
  new = json.dumps(logs, indent=4, ensure_ascii=False)
  with open("logs.json", "w") as idk:
    idk.write(new)


def updateHacker(guildID, data):
  with open("events.json", "r") as config:
    config = json.load(config)
  config["guilds"][str(guildID)] = data
  newdata = json.dumps(config, indent=4, ensure_ascii=False)
  with open("events.json", "w") as config:
    config.write(newdata)


def getHacker(guildID):
  with open("events.json", "r") as config:
    data = json.load(config)
  if str(guildID) not in data["guilds"]:
    defaultConfig = {
      "antinuke": {
        "antirole-delete": True,
        "antirole-create": True,
        "antirole-update": True,
        "antichannel-create": True,
        "antichannel-delete": True,
        "antichannel-update": True,
        "antiban": True,
        "antikick": True,
        "antiwebhook": True,
        "antibot": True,
        "antiserver": True,
        "antiping": True,
        "antiprune": True,
        "antiemoji-delete": True,
        "antiemoji-create": True,
        "antiemoji-update": True,
        "antimemberrole-update": True
      }
    }
    updateHacker(guildID, defaultConfig)
    return defaultConfig
  return data["guilds"][str(guildID)]

