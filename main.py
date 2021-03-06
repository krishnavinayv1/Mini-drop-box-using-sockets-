#!/bin/python

from threading import Thread
import time
import server
import client
import sys

def start_tcp_server(threadName):
    arg = 'Share/'
    print 'TCP server starting'
    arg1 = sys.argv[1]
    if len(sys.argv) < 4:
        server.tcp_main(arg1, arg) #The folder I share with other clients
    else:
        server.tcp_main(arg1, sys.argv[3]+'/' if sys.argv[3][len(sys.argv[3])-1]!='/' else sys.argv[3])

def start_udp_server(threadName):
    print ' UDP server starting'
    arg = 'Share/'
    arg1= sys.argv[1]
    if len(sys.argv) < 4:
        server.udp_main(arg1, arg) #The folder I share with other clients
    else:
        server.udp_main(arg1, sys.argv[3]+'/' if sys.argv[3][len(sys.argv[3])-1]!='/' else sys.argv[3])

def start_client(threadName):
    print 'Client started'
    if len(sys.argv) < 4:
        client.main(sys.argv[2], 'ShareDown/') #My downloads get downloaded here
    else:
        client.main(sys.argv[2], sys.argv[3]+'/' if sys.argv[3][len(sys.argv[3])-1]!='/' else sys.argv[3])


t2 = Thread( target=start_udp_server, args=("Server2", ) )
t2.daemon = True
t2.start()
time.sleep(1)
t1 = Thread( target=start_tcp_server, args=("Server1", ) )
t1.daemon = True
t1.start()
time.sleep(1)
t3 = Thread( target=start_client, args=("Client", ) )
t3.start()
       
t3.join()
sys.exit()
