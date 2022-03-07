@echo off
rmdir /S /Q dist
mkdir dist
cd client
tar -cvf ..\dist\client.tar.gz cli.py lns.py
pyinstaller cli.py --onefile
copy .\dist\cli.exe ..\dist\cli.exe
cd ..\server
tar -cvf ..\dist\server.tar.gz *
cd ..
@echo on