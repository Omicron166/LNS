@echo off
rmdir /S /Q dist
mkdir dist
cd client
tar -cvf ..\dist\client.tar.gz cli.py lns.py
cd ..\server
tar -cvf ..\dist\server.tar.gz *
cd ..
@echo on