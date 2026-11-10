@echo off
chcp 65001 >nul
title Kitty Corp Enterprise Load Suite - https://thekittycorp.com/
cls
echo ==========================================================
echo          KITTY CORP ADVANCED ENTERPRISE LOAD SUITE         
echo                 made by kitty corp                       
echo         https://thekittycorp.com/ - support us 🩷        
echo ==========================================================
if not exist ".venv" python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
python kitty_tester.py %*
pause
