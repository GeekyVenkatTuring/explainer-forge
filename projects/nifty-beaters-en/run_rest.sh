#!/bin/bash
cd "/Users/appuram/Developer/explainer-forge/projects/nifty-beaters-en"
echo "[$(date +%H:%M)] rendering ch03 ch04 ch05 at concurrency=2..."
python3 build.py render ch03 ch04 ch05
echo "[$(date +%H:%M)] building master..."
python3 build.py master
echo "[$(date +%H:%M)] ALL DONE"
