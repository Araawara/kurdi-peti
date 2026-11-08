@echo off
rem گەشەپێدانی ڕۆژانەی فەرهەنگی کوردیی پەتی (Windows Task Scheduler)
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
if not exist data mkdir data
echo ===== %date% %time% ===== >> data\daily.log
type daily_prompt.md | "%USERPROFILE%\.local\bin\claude.exe" -p --allowedTools "Read" "Write" "Edit" "Grep" "Glob" "Bash(python grow.py:*)" >> data\daily.log 2>&1
