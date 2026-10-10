@echo off
title LuxeCart E-Commerce Platform Server
chcp 65001 > nul
echo ===================================================
echo   🚀 LuxeCart Premium E-Commerce Platform
echo ===================================================
echo.
echo  جاري تشغيل السيرفر المحلي...
echo  رابط الفتح في المتصفح: http://localhost:8000
echo.
python "%~dp0server.py"
pause
