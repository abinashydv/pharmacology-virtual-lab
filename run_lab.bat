@echo off
title Pharmacol Virtual Lab
echo ========================================================
echo       🧪 Starting Pharmacol Virtual Laboratory
echo   Developed using Python, Streamlit, and RDKit
echo ========================================================
echo.
cd /d "%~dp0"
py -m streamlit run app.py
pause
