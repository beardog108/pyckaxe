#!/bin/bash

TMUXID=$(cat tmuxid.txt);
if [ -f "pyckaxe-lockfile.txt" ]
then
    echo "Lock file exists. Server jar already running?"
    ./pyckaxe.py "$TMUXID" "true";
else
  tmux new-session -P -d -n minecraft-pyckaxe "echo 'delete me if server crashed' > pyckaxe-lockfile.txt; java -jar mc.jar nogui > mc.log; rm pyckaxe-lockfile.txt" | tr -d : > tmuxid.txt
  ./pyckaxe.py "$TMUXID" "false"
fi
