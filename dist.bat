@echo off

rem #dist clean
rmdir /S /Q dist
mkdir dist

rem #client package
cd client
tar -cvf ..\dist\client.tar.gz cli.py lns.py
pyinstaller cli.py --onefile
copy .\dist\cli.exe ..\dist\cli.exe

rem #server-fs package
cd ..\server-fs
tar -cvf ..\dist\server-fs.tar.gz *

rem #server-bin package
cd ..\server-bin
pyinstaller server.py --onefile
copy .\dist\server.exe ..\dist\server.exe
@echo on