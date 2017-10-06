#!/usr/bin/env python3

'''
Pyckaxe, a simple Python script demonstrating use of Tmux for Minecraft "vanilla plugins". Not really meant for use yet.
    Copyright (C) 2017 Kevin Froman https://ChaosWebs.net/

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Each plugin creates a table in the users DB

'''

import libtmux, time, signal, sys, random, requests, os, sqlite3, time, datetime, nbt, configparser, imp, glob, pluginLoader

tmuxid = sys.argv[1]

doDelay = sys.argv[2]

if doDelay == 'false':
    time.sleep(15)

def logger(data, config):
    if config['SERVER']['console log'] == 'true':
            if log:
                print(data)
    return

def getPlayerData(data, kind, player):
    retData = ''
    if kind == "nbt":
        nbtFile = nbt.nbt.NBTFile("world/playerdata/" + playerID + ".dat")
        try:
            retData = nbtFile[data].value
        except ValueError:
            retData = None
    elif kind == "db":
        conn = sqlite3.connect(DBPath + getUUID(player) + '.db')
        c = conn.cursor()
        selectData = (player,)
        rowID = 0
        if data == "name":
            rowID = 0
        elif data == "balance":
            rowID = 1
        elif data == "secret":
            rowID = 3
        elif data == "rank":
            rowID = 4
        elif data == "activated":
            rowID = 5
        for row in c.execute('SELECT * FROM Player where name=?', selectData):
            try:
                retData = row[1]
            except IndexError:
                retData = None
    return retData

def doCmd(cmd):
    session.attached_pane.send_keys(cmd)

def substring_after(s, delim):
    return s.partition(delim)[2]

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def signal_handler(signal, frame):
        doCmd('say Pyckaxe 0.1 shutting down')
        sys.exit(0)

def getUUID(player):
    try:
        UUIDCache[player]
        logger('loaded uuid from cache')
        uuid = UUIDCache[player]
    except KeyError:
        uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + player).json()['id']
        UUIDCache[player] = uuid
    return uuid

def isModerator(player):
    if player in config['SERVER']['moderators'].split(' '):
        return True
    else:
        return False

def playerScan():
    for i in glob.glob('world/playerdata/*.dat'):
        pass
signal.signal(signal.SIGINT, signal_handler)
server = libtmux.Server()
session = server.get_by_id('$' + tmuxid)

player = ''
message = ''
number = 0
guesses = 0

userDB = ''

moderators = []

DBPath = 'player-data/players/'

try:
    doCmd('say Pyckaxe 0.1 Initialized')
except AttributeError:
    print('Try re-rerunning this script...')

secret = ''
now = 0
loop = 0

cfgFile = 'pyckaxe-config.cfg'

config = configparser.ConfigParser()

config['SERVER'] = {'name': 'Example Server', 'moderators': 'Notch beardoge', 'loop-speed': '0.5', 'new player check timer': '100', 'enabled-plugins': '', 'console log': 'true'}


if not os.path.exists(cfgFile):
    try:
        with open(cfgFile, 'w') as configfile:
            config.write(configfile)
    except PermissionError:
        print('Unable to load config, no permission.')
        sys.exit(1)
try:
    config.read(cfgFile)
except PermissionError:
    print('Unable to load config, no permission.')
    sys.exit(1)


last = ''

lastMsg = ''

UUIDCache = {}

newPlayerCheckLoops = int(config['SERVER']['new player check timer']) # after how many loops we should check for new players... event driven doesn't work for This
newPlayerLoopCount = 0
pluginLoader.events('startup', '', config)

try:
    while True:
        player = ''
        message = ''
        loop = loop + 1
        time.sleep(float(config['SERVER']['loop-speed']))
        now = datetime.datetime.now()
        now = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second + 1)
        newPlayerLoopCount = newPlayerLoopCount + 1
        if newPlayerLoopCount > newPlayerCheckLoops:
            for i in glob.glob('world/playerdata/*.dat'):
                print(i.replace('.dat', '').replace('world/playerdata/', ''))
                newPlayerLoopCount = 0
        with open('mc.log', 'rb') as log:
            try:
                last = log.readlines()[-1].decode().replace('\n', '')
                last = last[10:]
            except:
                print("Shutting down")
                sys.exit(0)
            # should be starts with?
            if '<' not in last and '>' not in last and '[Server Shutdown Thread/INFO]' in last:
                print('Server shut down')
                sys.exit(0)
            #if '[02:02:36] [Server thread/INFO]: beardoge left the game'
            if 'left the game' in last and '<' not in last and '>' not in last:
                player = find_between(last, '[Server thread/INFO]:', 'left the game').strip()
                pluginLoader.events('leave', int(time.time()), config, player)
            serverTime = last.split(']')[0].replace('[', '')
            last = substring_after(last, '[Server thread/INFO]: ')
            if not last.startswith('*'):
                player = find_between(last, '<', '>')
                message = substring_after(last, '>').lstrip()
                if lastMsg != message:
                    logger(player + ': ' + message, config)
                    pluginLoader.events('commands', message, config, player)
                    lastMsg = message
            else:
                logger('Possible attack: ' + last)
except KeyboardInterrupt:
    pass
'''
except:
    doCmd('say Pyckaxe has experienced a fatal error and will now exit.')
    print(sys.exc_info()[0])
    sys.exit(1)
'''
