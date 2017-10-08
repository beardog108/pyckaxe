#!/bin/bash

if [ ! -f mc.jar ]; then
    echo "There is not a file named mc.jar in this directory. Exiting.";
    exit 1;
fi

if ! [ -x "$(command -v tmux)" ]; then
  echo 'Error: tmux is not installed.' >&2
  exit 1;
fi

tmux new-session -P -d -n minecraft-pyckaxe "java -jar mc.jar nogui > mc.log"> tmuxid.txt
