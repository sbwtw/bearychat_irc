# -*- coding: utf-8 -*-
import configparser
import threading

import irc3
from irc3.utils import IrcString
from irc3.plugins.command import command

from bearychat import Bearychat

from bc_ws import BC_Server
from bc_api import BC_API
import logger

@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read("config.ini")
        users = config["bot"]["ignore_users"]
        self.ignore_users = [u for u in users.split("\n") if len(u.strip()) > 0]

        self.bc = Bearychat()

        self.bc_server = BC_Server(self.bot)

        # run bc ws client in background
        threading.Thread(target=self.bc_server.start_server).start()


    @irc3.event(irc3.rfc.PRIVMSG)
    def recv_msg(self, mask, event, target, data):
        msg = "[%s]: %s" %(mask.nick, data)
        if mask.nick not in self.ignore_users:
            self.bc.say(msg)
            logger.log("irc => bc: %s" % msg)


    '''
    @irc3.event(irc3.rfc.JOIN)
    def say_hi(self, mask, channel):
        """Say hi when someone join a channel"""
        print(type(channel))
        print(channel)
        print(IrcString("hello"))
        if mask.nick != self.bot.nick:
            self.bot.privmsg(channel, 'Hi %s!' % mask.nick)
    '''

    @command(permission='view')
    def echo(self, mask, target, args):
        """Echo

            %%echo <message>...
        """
        yield ' '.join(args['<message>'])


