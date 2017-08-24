#!/bin/bash
tmux new-session -P -d -n minecraft-pyckaxe "java -jar mc.jar nogui > mc.log"> tmuxid.txt
