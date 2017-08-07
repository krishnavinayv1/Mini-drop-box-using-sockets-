import string
import socket  # Import socket module
import sys
import datetime
import time
import os
import mimetypes
import hashlib
import glob
import re

outputlog = open('outbox', 'a+')
argfg=True
logfile = open('history', 'a+')
querycheckfile = open('queryresults', 'a+')
errorlog = open('errors', 'a+')

class udp_client:
    def send(self, message, file_request, ip, directory):
        argflag=True
        try:
            s = self.connect(ip)
        except Exception, e:
            print str(e)
            argflag=False
            errorlog.write(str(e))
            return
        data = ""
        receiving = True
        validity = True
        outputlog.write(message)
        header = True
        tuplearg=(ip,60001)
        s.sendto(message, tuplearg)

        if file_request and argflag:
            try:
                sequence_number = 0
                sendarg=message.split('?')[1].strip()
                file_path = os.path.join(directory,sendarg)
                dirname=os.path.dirname(file_path)
                if not os.path.exists(dirname):
                    try:
                        os.makedirs(dirname)
                        outputlog.write("made a directory with name")
                    except Exception, e:
                        pristr=str(e) + ' : Could not create the directory'
                        print pristr                  
                        errorlog.write(str(e) )
                        return
                with open(file_path, 'wb') as f:
                    while receiving and argflag:
                        data, addr = s.recvfrom(1024)
                        if data == '#END#' and argflag :
                            receiving = False
                            break
                        if data == "#101" or data == '#102':
                            validity = False
                        if data == "#102":
                            return 'Please give path to file in shared folder'
                        if not data:
                            break
                        if header and len(data.split('?')) > 4:
                            printstr='Received File \n' + data.split('?')[0] + '\n' + data.split('?')[1] + '\n' + \
                                  data.split('?')[2] + '\n' + data.split('?')[3] + '\n' + "End of header"
                            f.write(data.split('?')[4])
                            querycheckfile.write(data.split('?')[4])
                            sendtuple=(ip,60001)
                            print printstr
                            s.sendto('0',sendtuple)
                            outputlog.write('0')
                            header = False
                        elif validity == True and argflag:
                            if data.split('#NEXT#')[0] == str(sequence_number + 1):
                                sendtuple=(ip,60001)
                                sequence_number += 1
                                s.sendto(str(sequence_number),sendtuple)
                                outputlog.write(str(sequence_number))
                                f.write(data.split('#NEXT#')[1])
                                querycheckfile.write(data.split('#NEXT#')[1])
                            else:
                                sendtup=(ip,60001)
                                s.sendto('-1',sendtup)
                s.close()
                f.close()
                if validity and argflag:
                    return "File read"

            except Exception, e:
                print str(e)
                argflag=False
                errorlog.write(str(e))
        else:
            try:
                while receiving:
                    data_cur, addr = s.recvfrom(1024)
                    if data_cur == '#END#' and argflag:
                        receiving = False
                        break
                    data += data_cur
                s.close()
                return data
            except Exception, e:
                print str(e)
                errorlog.write(str(e))

    def connect(self, ip):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class tcp_client:
    def connect(self, ip):
        s = socket.socket()
        print "connected to server"
        s.connect((ip, 60005))
        return s

    def send(self, message, file_request, ip, directory):
        try:
            s = self.connect(ip)


        except Exception, e:
            pristr=str(e) + ' : Failed to connect'
            errorlog.write(pristr)
            return
        data = ""
        outputlog.write(message)
        receiving = True
        s.send(message)
        validity = True
        header = True


        if file_request:
            direrr=': Cant create a directory'
            try:
                sendvar=message.split('?')[1].strip()
                file_path = os.path.join(directory,sendvar)
                if not os.path.exists(os.path.dirname(file_path)):
                    try:
                        os.makedirs(os.path.dirname(file_path))
                    except Exception, e:
                        pristr=str(e)+direrr
                        print pristr
                        errorlog.write(pristr)
                        return
                with open(file_path, 'wb') as f:
                    while True:
                        data = s.recv(1024)
                        if data == '#END#':
                            receiving = False
                            break
                        if data == "#101" or data == '#102':
                            validity = False
                        if data == "#102":
                            return 'Please give path to file in shared folder'
                        if not data:
                            break
                        if header and len(data.split('?')) > 4:
                            printstr='Received File \n' + data.split('?')[0] + '\n' + data.split('?')[1] + '\n' + \
                                  data.split('?')[2] + '\n' + data.split('?')[3] + '\n' + "End of header"
                            f.write(data.split('?')[4])
                            print printstr
                            querycheckfile.write(data.split('?')[4])
                            header = False
                        elif validity == True:
                            f.write(data)
                            querycheckfile.write(data.split('?')[4])
                            # write data to a file
                f.close()

                s.close()
                if validity:
                    return "File read"

            except Exception, e:
                printstr=str(e) + ' : Unable to fetch file from server, please enter the correct command'
                print printstr
                errorlog.write(printstr)

        else:
            try:
                while receiving:

                    data_cur = s.recv(1024)
                    if not data_cur:
                        receiving = False
                        print "2"
                    data += data_cur

                querycheckfile.write(data)
                s.close()

                return data
            except Exception, e:
                printstr= str(e) + ' : Unable to fetch data'
                print printstr
                errorlog.write(printstr)




def main(ip, directory):
    tcpconnection = tcp_client()
    type_raw = input("1.general 2.automatic")
    udpconnection = udp_client()

    if type_raw == 1:
        while True:
            input_raw = raw_input()
            try:
                bigstr=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\t' + input_raw + '\n'
                if 'index' in input_raw and 'shortlist' in input_raw:
                    logfile.write(bigstr)
                    inputs = input_raw.split(' ')
                    querycheckfile.write(bigstr)
                    messageserver = 'index shortlist ?' + inputs[2] + ' ' + inputs[3] + ' ' + inputs[4] + ' ' + inputs[
                        5] + ' ' + inputs[6] + ' ? ' + inputs[7] + ' ' + inputs[8] + ' ' + inputs[9] + ' ' + inputs[
                                        10] + ' ' + inputs[11]
                    if 'TCP' in input_raw:
                        res = tcpconnection.send(messageserver, False, ip, directory)
                        print res
                        querycheckfile.write('results are:' + res)
                    elif 'UDP' in input_raw:
                        res = udpconnection.send(messageserver, False, ip, directory)
                        print res
                        sendstr='results are '+res
                        querycheckfile.write(sendstr)
                    if res:
                        print res
                if 'index' in input_raw and 'longlist' in input_raw:
                    logfile.write(bigstr)
                    querycheckfile.write(bigstr)

                    if 'TCP' in input_raw:
                        res = tcpconnection.send("index longlist", False, ip, directory)
                        print res
                        querycheckfile.write(res)
                    elif 'UDP' in input_raw:
                        res = udpconnection.send("index longlist", False, ip, directory)
                        print res
                        querycheckfile.write('results are' + res)
                    if res:
                        print res

                if 'index' in input_raw and 'regex' in input_raw:
                    querycheckfile.write(bigstr)
                    logfile.write(bigstr)
                    messageserver = 'index regex ?' + input_raw.split(' ')[2]
                    if 'TCP' in input_raw:
                        res = tcpconnection.send(messageserver, False, ip, directory)
                        print res
                        querycheckfile.write('results' + res)
                    elif 'UDP' in input_raw:
                        res = udpconnection.send(messageserver, False, ip, directory)
                        print res
                        querycheckfile.write('results' + res)
                    else:
                        res = udpconnection.send(messageserver, False, ip, directory)
                        print res
                        querycheckfile.write('results' + res)

                if 'download' in input_raw:
                    logfile.write(bigstr)
                    querycheckfile.write(input_raw + '\n')
                    messageserver = 'download ? '
                    cnt = 0
                    for com in input_raw.split(' '):
                        if cnt >= 2:
                            messageserver += com
                        cnt += 1
                    if 'TCP' in input_raw:
                        res = udpconnection.send(messageserver, True, ip, directory)
                        print res
                    elif 'UDP' in input_raw:
                        res = udpconnection.send(messageserver, True, ip, directory)
                        print res
                    print res
                FAILSTR="Failed to get the hash"
                if 'hash' in input_raw:
                    logfile.write(bigstr)
                    messageserver = 'hash ' + input_raw.split(' ')[1] + ' ? '
                    querycheckfile.write(bigstr)
                    cnt = 0
                    cntmax=10000
                    for com in input_raw.split(' '):
                        if cnt >= 2 and cntmax>=0:
                            messageserver += com
                        cntmax-=1
                        cnt += 1
                    if 'TCP' in input_raw:
                        res = tcpconnection.send(messageserver, False, ip, directory)
                    elif 'UDP' in input_raw:
                        res = udpconnection.send(messageserver, False, ip, directory)
                    else:
                        res = udpconnection.send(messageserver, False, ip, directory)
                    if res:
                        print res
                    else:
                        print FAILSTR
            except Exception, e:
                print str(e) + ' : Could not establish connection'
    elif type_raw == 2:
        current=True
        firsttime = 1
        lastsystime = 0
        lasttimedownload = ''
        while (True):
            timer=1
            presentsystime = time.time()
            #print lastsystime,presentsystime
            if (presentsystime - lastsystime > 10):
                presenttime = time.strftime("%c")
                lastsystime = time.time()
                if firsttime and current and timer:
                    res = udpconnection.send("index longlist", False, ip, directory)
                    print res

                else:
                    input_raw = "index shortlist " + lasttimedownload + " " + presenttime
                    current=True
                    inputs = input_raw.split(' ')
                    messageserver = 'index shortlist ?' + inputs[2] + ' ' + inputs[3] + ' ' + inputs[4] + ' ' + \
                                    inputs[5] + ' ' + inputs[6] + ' ? ' + inputs[7] + ' ' + inputs[8] + ' ' + inputs[
                                        9] + ' ' + inputs[10] + ' ' + inputs[11]

                    
                    
                    res = udpconnection.send(messageserver, False, ip, directory)
                    if res == None:
                        continue
                filelist = []
                word = ''
                linebegin = 1
                for line in res:
                    # print line,"completed"
                    

                    if linebegin == 1 and timer:
                        timer+=1
                        if line == '\t':
                            linebegin = 0
                            filelist.append(word)
                            word = ''
                        else:
                            word += line
                    if line == '\n':
                        linebegin = 1
                        timer+=1
                        if not firsttime:
                            filelist.append(word)
                        word = ''
                print filelist
                firsttime = 0
                for word in filelist:
                    input_raw = "download " + word
                    messageserver = 'download ? '
                    timer+=1
                    cnt = 0
                    for com in input_raw.split(' '):
                        if cnt >= 1:
                            timer+=1
                            messageserver += com
                        cnt += 1
                    res = udpconnection.send(messageserver, True, ip, directory)
                    if res:
                        print res
                
                lasttimedownload = presenttime

