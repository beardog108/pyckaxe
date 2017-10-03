# Copyright 2017 Kevin Froman - MIT License - https://ChaosWebs.net/

import os, imp, sys
pluginFolder = 'pyckaxe-plugins/'
MainModule = "__init__"

def loadPlugin(plugin):
    # Loads a plugin
    return imp.load_module(MainModule, *plugin["info"])

def getPlugins(config):
    # Loads gets a plugin from the plugin folder
    # based on: https://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
    plugins = []
    possiblePlugins = config['SERVER']['enabled-plugins'].replace(' ', '').split(',')
    for i in possiblePlugins:
        location = os.path.join(pluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins

def events(event, data, config, player=None):
    retData = ''
    ranPlugins = []
    for i in getPlugins(config):
        plugin = loadPlugin(i)
        if plugin not in ranPlugins:
            try:
                if event == 'startup':
                    retData = retData + plugin.startup(data)

                elif event == 'commands':
                    plugin.Commands.commands(data, config, player)
                    retData = True
                else:
                    print('Attempted to call unknown event: ' + event)
            except TypeError:
                pass
            except AttributeError:
                pass
            ranPlugins.append(i)
    if retData == '':
        retData = data
    return retData
