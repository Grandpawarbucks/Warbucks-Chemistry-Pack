#!/bin/bash
# usage: run.sh <n>   build into scratchpad/tidy/book<n>, gallery for the focus pages, lint
cd "/c/Users/Grandpawarbucks/OneDrive/Desktop/Chem Modpack Dev/Warbucks-Chemistry-Pack"
n=$1
rm -rf scratchpad/tidy/book$n
QUEST_OUT=scratchpad/tidy/book$n .venv/Scripts/python.exe tools/build_quests.py 2>&1 | grep -v "^Section\|^Chapter banners\|^Reward" | tail -6
.venv/Scripts/python.exe test/build_quest_preview.py --gallery --chapters ${CH:-mekanism,create,undergarden,integrated,powah,ae2,storage,harvest} --book scratchpad/tidy/book$n --out scratchpad/tidy/gal$n/gallery.html 2>&1 | tail -1
.venv/Scripts/python.exe tools/layout_lint.py --book scratchpad/tidy/book$n > scratchpad/tidy/lint$n.txt
grep -E "^(chapter|mekanism |create|undergarden|integrated|powah|ae2|storage|harvest)" scratchpad/tidy/lint$n.txt
grep -E "total|tidiness" scratchpad/tidy/lint$n.txt
