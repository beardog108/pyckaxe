import pyckaxe, sanitize
def announce(text, color='white'):
    text = sanitize.sanitize(text)
    color = sanitize.sanitize(color)
    pyckaxe.doCmd('tellraw @p ["",{"text":"' + text + '","color":"' + color + '","bold":true}]')
def tell(player, text, color='white'):
    player = sanitize.sanitize(player)
    color = sanitize.sanitize(color)
    text = sanitize.sanitize(text)
    pyckaxe.doCmd('tellraw ' + player + ' ["",{"text":"' + text + '","color":"' + color + '","bold":true}]')
