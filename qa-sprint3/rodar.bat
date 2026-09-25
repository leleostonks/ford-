@echo off
cd /d "%~dp0"
python gerar_docs.py .
code README.md
pause
