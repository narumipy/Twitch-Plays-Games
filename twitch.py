from pymouse import PyMouse

from irc import irc


class Twitch(irc):
    def __init__(self, user, auth, channel):
        irc.__init__(self)
        self.connect('irc.twitch.tv', 6667, user, user, user, auth)
        self.join(channel)

    def run(self):
        while True:
            for msg in self.read():
                if msg.command == 'PRIVMSG' and 'click' in msg.args[1]:
                    m = PyMouse()
                    m.click(0, 0)


USERNAME = 'username'
AUTH = 'oauth:xxxxxxxxxxxxxxxxxxxx'
CHANNEL = '#channel'

bot = Twitch(USERNAME, AUTH, CHANNEL)
bot.run()
