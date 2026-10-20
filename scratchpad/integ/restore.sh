cd "/c/Users/Grandpawarbucks/OneDrive/Desktop/Chem Modpack Dev/Warbucks-Chemistry-Pack"
for f in scratchpad/integ/tools_backup/quests/*.py; do b=$(basename $f); case $b in tips.py) ;; *) cp "$f" tools/quests/$b;; esac; done
rm -f tools/quests/generators.py tools/quests/integrated.py
cd scratchpad/integ && ../../.venv/Scripts/python.exe split.py && ../../.venv/Scripts/python.exe post_split.py
../../.venv/Scripts/python.exe retire.py rmap.json > retire_log.txt 2>&1; head -1 retire_log.txt
../../.venv/Scripts/python.exe kits.py
