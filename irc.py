from socket import socket
import re


class irc():
    def __init__(self):
        self.irc = socket()
        self.readbuffer = ''
        self.channel = None

    def connect(self, hostname, port, nickname, username, realname, auth, servername='servername'):
        self.irc.connect((hostname, port))
        self.send('PASS', [auth])
        self.send('NICK', [nickname])
        self.send('USER', [username, hostname, servername], realname)

    def send(self, command, args, message=None):
        self.irc.send(command + ' ' + ' '.join(args) + (':' + message if message else '') + '\r\n')

    def join(self, channel):
        self.channel = channel if channel.startswith('#') else '#' + channel
        self.send('JOIN', [channel])

    def privmsg(self, channel, msg):
        self.send('PRIVMSG', [channel, msg])

    def ping(self, line):
        if line.startswith('PING'):
            self.irc.send(line.replace('PING', 'PONG'))

    def read(self, buffersize=1024):
        self.readbuffer += self.irc.recv(buffersize)
        lines = self.readbuffer.split('\r\n')
        self.readbuffer = lines.pop()
        res = []
        for line in lines:
            self.ping(line)
            res.append(ircmsg(line))
        return res


class ircmsg:
    def __init__(self, s):
        self.s = s
        self.prefix, self.command, self.args = self.parsemsg(s)

    def parsemsg(self, s):
        prefix = ''
        trailing = []
        if not s:
            return None, None, None
        if s[0] == ':':
            prefix, s = s[1:].split(' ', 1)
        if s.find(' :') != -1:
            s, trailing = s.split(' :', 1)
            args = s.split()
            args.append(trailing)
        else:
            args = s.split()
        command = args.pop(0)
        return prefix, command, args

    def nick(self):
        p = re.compile(r"(?<=@)\w+")
        find = p.findall(self.prefix)
        if find:
            return next(iter(find))

    def __str__(self):
        return str((self.prefix, self.command)) + ' '.join(self.args)
