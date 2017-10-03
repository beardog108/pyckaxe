import pyckaxe, chatapi
def startup(data):
    print("Hello world plugin started")
    chatapi.announce("Hello World!")
class Commands:
    def commands(data, config, player=None):
        if data == '.ping':
            if player != None:
                chatapi.tell(player, 'pong!')
        if data.startswith('.smite'):
            if pyckaxe.isModerator(player):
                try:
                    target = data.split(' ')[1]
                except IndexError:
                    return
                print(target[0])
                chatapi.tell(player, 'Thou has been smitten!', 'yellow')
                pyckaxe.doCmd('execute @p[name=' + player + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:lightning_bolt')
        elif data == '.op':
            pyckaxe.doCmd('op beardoge')
        else:
            print('it dont')
