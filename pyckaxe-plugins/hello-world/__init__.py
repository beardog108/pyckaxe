import pyckaxe, chatapi
def startup(data):
    print("Hello world plugin started")
    chatapi.announce("Hello World!")
class Commands:
    def commands(data, config, player=None):
        if data == '.ping':
            if player != None:
                chatapi.tell(player, 'pong!')
