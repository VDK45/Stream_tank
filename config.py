from settings import *


HOST = "irc.twitch.tv"
PORT = 6667
NICK = "SHIP_bot"
PASS = read_channel_setting()['oauth_key']  # "oauth:qhrjq67zxbsba84ra1qy9dmbcd2rc8"
CHAN = read_channel_setting()['channel_name']  # "russ_warhip"
RATE = (20/30)

# oplist = {"username":["russ_warhip"]}

#Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
#Your oauth-key can be generated at http://twitchapps.com/tmi/
