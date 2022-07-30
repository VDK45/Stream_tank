import config
import urllib.request as urllib2


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode())





