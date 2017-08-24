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

'''

import libtmux, time, signal, sys, random, requests, os, sqlite3, time, datetime, nbt, configparser

def logger(data):
	log = False
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

class Kits:
	def __init__(self):
		return
	def starter():
		return (('5', 'apple'), ('1', 'stone_axe'), ('1', 'stone_sword'), ('1', 'boat'))
	starter = starter()

def claimKit(wantedKit):
	func = getattr(kits, wantedKit)
	items = func
	for item in items:
		doCmd('give ' + player + ' ' + item[1] + ' ' + item[0])

signal.signal(signal.SIGINT, signal_handler)
server = libtmux.Server()
session = server.list_sessions()[-1]

player = ''
message = ''
number = 0
guesses = 0

userDB = ''

moderators = []

DBPath = 'player-data/players/'

doCmd('say Pyckaxe 0.1 Initialized')

UUIDCache = {}

antiSpam = {} # players who have recently done a command

spamClearLoops = 25
spamClearLoopCount = 0
maxSpam = 5
secret = ''
now = 0
loop = 0
lastSpamTime = 0

tpDelayLoops = 3
tpDelayLoopCount = 0
spawnQueue = []
spawnCords = '57.325 69.51 -80.401'

# Define kits
kits = Kits()


cfgFile = 'pyckaxe-config.cfg'

config = configparser.ConfigParser()

config['SERVER'] = {'name': 'Example Server', 'moderators': 'Notch', 'loop-speed': '0.5', 'enabled-plugins': ''}


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

try:
	while True:
		spamClearLoopCount = spamClearLoopCount + 1
		tpDelayLoopCount = tpDelayLoopCount + 1
		player = ''
		message = ''
		loop = loop + 1
		time.sleep(int(config['loop-speed']))
		now = datetime.datetime.now()
		now = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second + 1)
		if tpDelayLoopCount > tpDelayLoops:
			#print('tping peeps')
			for x in spawnQueue:
				#print(x)
				doCmd('tp ' + x + ' ' + spawnCords)
			spawnQueue.clear()
			tpDelayLoopCount = 0
		if spamClearLoopCount > spamClearLoops:
			logger('cleared spam loop' + str(random.randint(1, 1000)))
			spamClearLoopCount = 0
			antiSpam.clear()
		with open('mc.log', 'rb') as log:
			last = log.readlines()[-1].decode().replace('\n', '')
			serverTime = last.split(']')[0].replace('[', '')
			last = substring_after(last, '[Server thread/INFO]: ')
			#print(serverTime + ' - ' + now)
			if not last.startswith('*'):
				player = find_between(last, '<', '>')
				message = substring_after(last, '>').lstrip()
			else:
				logger('Possible attack: ' + last)
			if player != '' and message != '':
				try:
					antiSpam[player]
				except KeyError:
					antiSpam[player] = 0

				if lastSpamTime != serverTime:
					antiSpam[player] = antiSpam[player] + 1
					if antiSpam[player] > maxSpam:
						doCmd('kick ' + player + ' kicked for spam! repeat offenders are temp banned!')
						antiSpam[player] = 0
				lastSpamTime = serverTime
				if message == '.ping':
					doCmd('say ' + player + ': pong!')
				elif message == '.account create':
					uuid = getUUID(player)
					if not os.path.exists(DBPath + uuid + '.db'):
						doCmd('msg ' + player + ' creating account with uuid: ' + uuid)
						conn = sqlite3.connect(DBPath + uuid + '.db')
						c = conn.cursor()
						secret = str(time.time() + random.randint(random.randint(1, 10), random.randint(11, 9999)))
						insertData = (player, 0, '', secret, str(int(time.time())), 0, 0)
						c.execute('''CREATE TABLE Player
							 (NAME TEXT NOT NULL,
							  BALANCE INT NOT NULL,
							  PASSWORD TEXT NOT NULL,
							  SECRET TEXT NOT NULL,
							  DATE INT NOT NULL,
							  RANK INT NOT NULL,
							  ACTIVATED INT NOT NULL);''')
						c.execute('INSERT INTO Player (NAME, BALANCE, PASSWORD, SECRET, DATE, RANK, ACTIVATED) VALUES (?, ?, ?, ?, ?, ?, ?)', insertData)
						conn.commit()
						conn.close()
						doCmd('msg ' + player + ' Created your account!')
					else:
						doCmd('msg ' + player + ' you already have an account!')
					#UUIDs
				elif message == '.account secret':
					uuid = getUUID(player)
					conn = sqlite3.connect(DBPath + uuid + '.db')
					c = conn.cursor()
					selectData = (player)
					for row in c.execute('SELECT SECRET FROM Player where NAME=?', (selectData,)):
						doCmd('say ' + player + '\'s secret code is ' + row[0])
				elif message == '.test':
					logger(getPlayerData('balance', 'db', player))
				elif message.startswith('.smite '):
					if player in moderators:
						doCmd('execute @e[name=' + message.split(' ')[1] + '] ~ ~ ~ /summon Lightning_Bolt')
					else:
						doCmd('say ' + player + ' is not a moderator!')
				elif message.startswith('.kick '):
					if player in moderators:
						doCmd('kick ' + message.split(' ')[1])
					else:
						doCmd('say ' + player + ' is not a moderator!')
				elif message == '.spawn':
					doCmd('msg ' + player + ' Teleporting to spawn soon...')
					#spawnQueue[player] = true
					spawnQueue[:0] = [player]
				elif message == '.numberguess':
					doCmd('say I\'m thinking of a number between 1 & 100, what is it?')
					number = random.randint(1, 101)
				elif message == '.clear':
					doCmd('clear ' + player
					)
				elif message.startswith('.kit '):
					wantedKit = message.split()[1]
					if hasattr(kits, wantedKit):
						claimKit(wantedKit)
					else:
						doCmd('msg ' + player + ' That kit does not exist')
				elif message.startswith('.guess'):
					if number != 0:
						guess = substring_after(message, '.guess ')
						guesses = guesses + 1
						if int(guess) == number:
							doCmd('say Yes! ' + player + ' guessed correctly after ' + str(guesses) + ' overall guesses!')
							number = 0
							guesses = 0
						elif int(guess) > number:
							doCmd('say Nope! Sorry, too high')
						elif int(guess) < number:
							doCmd('say Nope! Sorry, too low')
		#doCmd('placeholder') # here to prevent commands from running twice
except KeyboardInterrupt:
	pass
'''
except:
	doCmd('say Pyckaxe has experienced a fatal error and will now exit.')
	print(sys.exc_info()[0])
	sys.exit(1)
'''
