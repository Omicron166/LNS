@echo off
rem #client garbage clear
cd client
del /s /q *.spec
rmdir /s /q build dist __pycache__

rem #server-bin garbage clear
cd ..\server-bin
del /s /q *.spec
rmdir /s /q build dist __pycache__

rem #dist clear
cd ..
rmdir /s /q dist

@echo on