@echo off
chcp 65001 >nul
title Antigravity v2.33.0 一键汉化
cd /d "%~dp0"
set PYTHONUTF8=1

where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0Antigravity-Patcher.py"
    if %errorlevel% neq 0 pause
    exit /b %errorlevel%
)

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%~dp0Antigravity-Patcher.py"
    if %errorlevel% neq 0 pause
    exit /b %errorlevel%
)

echo [错误] 未检测到 Python 环境，请先安装 Python 3.8+ 并勾选 "Add Python to PATH"。
pause
exit /b 1
