@echo off
rem زیادکردنی بە کۆمەڵی وشە لە ویکیپیدیای کوردی: kurdi-peti-bulk.cmd [ژمارەی جار، بنەڕەت 3]
rem Windows Task Scheduler: ئەرکی KurdiPeti-Bulk هەموو شەوێک کاتژمێر ٣ی بەیانی
setlocal EnableDelayedExpansion
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
set RUNS=%1
if "%RUNS%"=="" set RUNS=3
python grow.py sync >> data\bulk.log 2>&1
for /L %%i in (1,1,%RUNS%) do (
  echo ===== bulk %%i/%RUNS% !date! !time! ===== >> data\bulk.log
  type bulk_prompt.md | "%USERPROFILE%\.local\bin\claude.exe" -p --allowedTools "Read" "Write" "Edit" "Grep" "Glob" "Bash(python grow.py:*)" >> data\bulk.log 2>&1
)
python grow.py publish >> data\bulk.log 2>&1
python grow.py commit >> data\bulk.log 2>&1
echo ===== done !date! !time! ===== >> data\bulk.log
