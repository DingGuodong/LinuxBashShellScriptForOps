@echo off
rem restart explorer.exe
rem restart explorer.exe can resolve almost common failure in Windows 10 GUI hang

taskkill /f /im explorer.exe
start explorer.exe
