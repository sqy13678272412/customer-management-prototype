@echo off
setlocal
if not defined KIMI_API_KEY (
  echo Please set KIMI_API_KEY first.
  exit /b 1
)
python "%~dp0kimi_call.py" %*
