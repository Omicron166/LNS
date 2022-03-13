#!/bin/bash
#unmainetained
rm -rf dist
mkdir dist
cd client
tar -cvf ../dist/client.tar.gz cli.py lns.py
cd ../server-fs
tar -cvf ../dist/server-fs.tar.gz *
cd ..