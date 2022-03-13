#Written by Omicron166
from lns import Client, IncompatibleServer, NameNotFound, client_version as version

user = 'client' #SPOILER ALERT: this never change (for now)
server = 'undefined' #server netloc
client = None #The future lns.Client instance


#the continue keyword is required inside the while loop to avoid
#the execution of unnecesary code an maybe some bug

while True:
    command = input(user + '@' + server + '> ')
    ####  Start of non connection required commands

    #Exit
    if command.startswith('exit'): break

    elif command.startswith('version'):
        print('LNS client version:', version)
        if not client == None:
            print('LNS server version:', client.index['version'])
        continue

    #Connect to a LNS server
    elif command.startswith('connect'):
        link = command.split(' ')[1] #Get server url
        try:
            print('Trying connection to ', link)
            Client(link)
        except IncompatibleServer:
            print('The server is not valid')
            continue
        client = Client(link)
        print('Connected successfully')
        
        server = link.replace(
            'lns://', ''
        ).replace(
            'lnss://', ''
        ).replace(
            'http://', ''
        ).replace(
            'https://', ''
        )
        continue

    #Disconnect from the server
    elif command.startswith('disconnect'):
        client = None
        server = 'undefined'
        continue

    ####  Filter for connection required commands
    if client == None:
        print('A connection is required before using this command')
        continue

    ####  Start of connection required commands
    #Resolve a name
    if command.startswith('resolve'):

        #name validation begin
        name = command.split(' ')[1]
        try: result = client.resolve(name)
        except NameNotFound:
            print('The name is not registered on the server')
            continue
        #name validation end
        print('Name resolved:')
        print(result)

    #Dig a name registry
    elif command.startswith('dig'):

        #name validation begin
        name = command.split(' ')[1]
        try: result = client.dig(name)
        except NameNotFound:
            print('The name is not registered on the server')
            continue
        #name validation end
        
        #Raw output
        try:
            if command.split(' ')[2] == 'raw':
                print(result)
                continue
        except IndexError:
            pass

        ## Info dig begin
        #Recorder name
        print('Dig of', name)
        if result['recorder'] == '':
            print('Recorder: anonymous')
        else:
            print('Recorder: ', result['recorder'])

        #Record link
        print('Record link: ', result['record']['link'])

        #Record txt
        if result['record']['txt'] != '':
            print('Record TXT entry: ', result['record']['txt'])