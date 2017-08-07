# server.py

import socket                   # Import socket module
import os
from datetime import datetime
import glob
import re
import time
import mimetypes
import hashlib
file_log2 = open('errors_server.py', 'a+')
file_log3 = open('outbox_server.py', 'a+')
file_log1 = open('history_server.py', 'a+')
file_log4 = open('query_server.py', 'a+')
#file logs are for checking errors and outbox and history of commands and queries

def md5(string):
    hash_value = hashlib.md5()
    with open(string, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    temp_str=str(hash_value.hexdigest)
    temp_str1=hash_value.hexdigest()
    file_log4.write(temp_str)
    return temp_str1

class udp_server:

    def init(self,ip):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
        print "UDP server initialized"
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port_number = 60001
        s.bind((ip, port_number))
        temp_str2=str(s)
        file_log4.write(temp_str2)
        return s

    def runServer(self,ip, directory):
        
        print ' UDP server starting'
        s = self.init(ip) #server Initilazing
        while True:

            input2, addr = s.recvfrom(1024)
            input1 = 'Hello server'
            greeting = 'Hello Client'
            if input2 == input1:
                file_log3.write(greeting)
                s.sendto(greeting, addr)
            if "index" in input2:
                if "shortlist" in input2:
                    try:
                        data_arr = input2.split('?')
                        #querycheckfile.write(str(data_arr))
                        time_l = datetime.strptime(data_arr[1].strip(), "%a %b %d %H:%M:%S %Y")
                        time_r = datetime.strptime(data_arr[2].strip(), "%a %b %d %H:%M:%S %Y")
                        #querycheckfile.write(str(time_l))
                        files = []
                        file_endings = []
                        for dp,dd,f in os.walk(directory):
                            for j in range(len(f)):
                                file_name = dp
                                if dp[len(dp)-1] != '/':
                                    file_name += '/'
                                file_name += f[j]
                                file_endings.append(os.path.relpath(file_name, os.path.commonprefix([file_name,directory])))
                                files.append(file_name)
                                #logfile.write(file_name)
                        for f in range(len(files)):
                            filename = files[f]
                            created_time = time.ctime(os.path.getctime(filename))
                            act_time = datetime.strptime(created_time, "%a %b %d %H:%M:%S %Y")
                            #querycheckfile.write(str(created_time))
                            if act_time <= time_r and act_time >= time_l:
                                s.sendto(file_endings[f] + '\n', addr)
                                #outputlog.write(file_endings[f] + '\n')
                        s.sendto('#END#',addr)
                        #outputlog.write('#END#')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        #errorlog.write(str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command')

                if "longlist" in input2:
                    try:
                        files = []
                        file_endings = []
                        for dp,dd,f in os.walk(directory):
                            for j in range(len(f)):
                                flag=0
                                file_name = dp
                                if dp[len(dp)-1] != '/':
                                    file_name += '/'
                                file_name += f[j]
                                if(flag==0):
                                    flag=1
                                file_endings.append(os.path.relpath(file_name, os.path.commonprefix([file_name,directory])))
                                files.append(file_name)
                                file_log1.write(file_name)
                        for f in range(len(files)):
                            ter=1
                            filename = files[f]
                            if(flag==1):
                                flag=0
                            statinfo = os.stat(filename)
                            size = str(statinfo.st_size)
                            file_log4.write(filename)
                            if(ter>20):
                                flag=ter
                            created_time = time.ctime(os.path.getctime(filename))
                            modified_time = time.ctime(os.path.getmtime(filename))
                            
                            file_log4.write(modified_time)
                            type_of_file, encoding = mimetypes.guess_type(filename,True)
                            if type_of_file:
                                s.sendto(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + type_of_file + '\n', addr)  #send file list to server
                                file_log3.write(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + type_of_file + '\n')
                            else:
                                s.sendto(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + 'None' + '\n', addr)  #send file list to server
                                file_log3.write(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + 'None' + '\n')
                        s.sendto('#END#',addr)
                        file_log3.write('#END#')
                    except Exception,e:
                        flag=0
                        file_log2.write(str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command')
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        
                        print 'flag is printing'
                if "regex" in input2:
                    try:
                        invalid = False
                        regex = input2.split('?')[1].strip()
                        file_log4.write(regex)
                        try:
                            re.search(regex,"")

                        except Exception,e:
                            invalid = True
                            print 'Invalid regex'
                            file_log2.write('Invalid regex')
                        if not invalid:
                            files = []
                            file_endings = []
                            for dp,dd,f in os.walk(directory):
                                for j in range(len(f)):
                                    file_name = dp
                                    if dp[len(dp)-1] != '/':
                                        file_name += '/'
                                    file_name += f[j]
                                    file_endings.append(os.path.relpath(file_name, os.path.commonprefix([file_name,directory])))
                                    files.append(file_name)
                                    file_log4.write(file_name)
                            for f in range(len(files)):
                                if re.search(regex,files[f]):
                                    s.sendto(file_endings[f] + '\n', addr)
                                    file_log3.write(file_endings[f] + '\n')
                        s.sendto('#END#', addr)
                        file_log3.write('#ENDE#')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        file_log2.write(str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command')
                        continue

            if "download" in input2:
                try:
                    command,value = input2.split('?')
                    value=value.strip()
                    file_abspath = os.path.abspath(directory + value)
                    if file_abspath.find(os.path.abspath(directory)) != 0:
                        file_log3.write(addr)
                        s.sendto('#102', addr)
                        
                    elif os.path.isfile(directory + value):
                        filename=directory + value
                        file_log4.write(filename)
                        flag=0
                        statinfo = os.stat(filename)
                        size = str(statinfo.st_size)
                        if(size>20):
                            flag=1
                        modified_time = time.ctime(os.path.getmtime(filename))
                        file_log4.write(modified_time)
                        created_time = time.ctime(os.path.getctime(filename))
                        temp=1
                        hash_value = md5(filename)
                        s.sendto(value +'?'+size+'?'+modified_time+'?'+hash_value+'?', addr)
                        file_log3.write(value +'?'+size+'?'+modified_time+'?'+hash_value+'?')
                        input2,addr = s.recvfrom(1024)
                        ter=1
                        f = open(filename,'rb')
                        l = f.read(512)
                        seq_number = 1
                        if(flag==0):
                            seq_number=temp
                        while (l):
                            s.sendto(str(seq_number) + '#NEXT#' + l, addr)
                            terr=str(seq_number) + '#NEXT#' +l
                            file_log3.write(terr)
                            if(ter==1):
                                ter=0
                            input2,addr = s.recvfrom(1024)
                            while input2 != str(seq_number):
                                flag=0
                                terr1=str(seq_number) + '#NEXT#' + l
                                file_log3.write(terr1)
                                s.sendto(str(seq_number) + '#NEXT#' + l, addr)
                                a1=5.0
                                s.settimeout(a1)
                                a2=1024
                                ter1=512
                                input2,addr = s.recvfrom(a2)
                            seq_number += 1
                            if(flag==0):
                                ter1 = 512
                            l = f.read(512)
                        f.close()
                    else:
                        s.sendto("#101",addr)
                        file_log4.write("#101")

                    file_log3.write('#the end#')
                    s.sendto('#END#',addr)
                    
                except Exception,e:
                    file_log2.write(str(e) + ' : An error occured while fetching the file, make sure you enter the correct command')
                    print str(e) + ' : An error occured while fetching the file, make sure you enter the correct command'
                    print 'str(e)'
            
            if "hash" in input2:
                try:
                    if "verify" in input2:
                        flag=0
                        command1,filenameold = input2.split('?')
                        filename = directory + filenameold.strip()
                        if os.path.isfile(filename):
                            if(flag==0):
                                ter=1
                            temp1=filenameold + ' => ' + md5(filename) + ', ' + time.ctime(os.path.getmtime(filename))
                            file_log3.write(temp1)
                            s.sendto(temp1, addr)
                            
                        else:
                            flag=0
                            s.sendto("#101", addr)
                            file_log3.write("#101#")
                        if(flag==0):
                            per=1
                        s.sendto('#END#',addr)
                        file_log3.write('#END#')
                    elif "checkall" in input2:
                        files = []
                        file_starting1 = []
                        file_endings = []
                        flag=0
                        for dp,dd,f in os.walk(directory):
                            for     j in range(len(f)):
                                file_name = dp
                                if dp[len(dp)-1] != '/':
                                    file_name += '/'
                                file_name += f[j]
                                file_starting1+= f[j]
                                file_endings.append(os.path.relpath(file_name, os.path.commonprefix([file_name,directory])))
                                file_log4.write(file_name)
                                if(flag==0):
                                    per=1
                                files.append(file_name)
                        for f in range(len(files)):
                            regg = file_endings[f] + ' => ' + md5(files[f]) + ', ' + time.ctime(os.path.getmtime(files[f])) + '\n'
                            file_log3.write(regg)
                            s.sendto(regg,addr)
                        st = '#END#'
                        file_log3.write(st)
                        s.sendto(st,addr)
                        
                except Exception,e:
                    
                    file_log3.write(str(e) + ' : An error occured while getting the hash of the file(s), make sure you enter the correct command')
                    print str(e) + ' : An error occured while getting the hash of the file(s), make sure you enter the correct command'

class tcp_server:

    def init(self,ip):
        port = 60005             # Reserve a port for your service.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #port has to change everytime
        host = socket.gethostname()     # Get local machine name
        s.bind((ip, port))            # Bind to the port
        aa2=5
        s.listen(aa2)                     # Now wait for client connection.
        return s

    def runServer(self,ip, directory):
        flag=0
        
        file_log4.write('TCP server started')
        print 'TCP server listening....'
        s = self.init(ip)
        while True:
            flag=0
            conn, addr = s.accept()     # Establish connection with client.
            aa3=1024
            input2 = conn.recv(aa3)
            re = "Hello server!"
            if input2==re:
                re1="Hello client!"
                file_log3.write(re1)
                conn.send(re1)
                if(flag==0):
                    flag=1

            if "index" in input2:
                flag=0
                if "shortlist" in input2:
                    try:
                        ter=1
                        new_array = input2.split('?')
                        if(flag==0):
                            ter=0
                        file_log4.write(str(new_array))
                        left_time = datetime.strptime(new_array[1].strip(), "%a %b %d %H:%M:%S %Y")

                        right_time = datetime.strptime(new_array[2].strip(), "%a %b %d %H:%M:%S %Y")
                        file_log4.write(str(left_time))
                        files = []
                        ter=1
                        file_endings = []
                        file_startings=[]
                        for dp,dd,f in os.walk(directory):
                            for j in range(len(f)):
                                if(ter==1):
                                    flag=0;
                                file_name = dp
                                if dp[len(dp)-1] != '/':
                                    file_name += '/'
                                file_name += f[j]
                                file_endings.append(os.path.relpath(file_name, os.path.commonprefix([file_name,directory])))
                                file_log4.write(file_name)
                                files.append(file_name)
                                
                        for f in range(len(files)):
                            filename = files[f]
                            if(flag==0):
                                ter=1
                            created_time = time.ctime(os.path.getctime(filename))
                            act_time = datetime.strptime(created_time, "%a %b %d %H:%M:%S %Y")
                            print ter+'1'
                            if act_time <= right_time and act_time >= left_time:
                                if(flag==0):
                                    print ter+'2'
                                
                                file_log3.write(file_endings[f] + '\n')
                                conn.send(file_endings[f] + '\n')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        file_log3.write(str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command')

                if "longlist" in input2:
                    try:
                        file_flag =1
                        files = []
                        file_starting2= []
                        file_endings = []
                        file_starting2.append('#END')
                        for dp,dd,f in os.walk(directory):
                            for j in range(len(f)):
                                file_name = dp
                                if dp[len(dp)-1] != '/':
                                    file_name += '/'
                                    flag=0
                                if(file_flag==1):
                                    flag=1
                                file_name += f[j]
                                files.append(file_name)
                                aew = os.path.relpath(file_name, os.path.commonprefix([file_name,directory]))
                                file_endings.append(aew)
                                
                        for f in range(len(files)):
                            filename = files[f]
                            statinfo = os.stat(filename)
                            size = str(statinfo.st_size)
                            file_log3.write(filename)
                            modified_time = time.ctime(os.path.getmtime(filename))
                            created_time = time.ctime(os.path.getctime(filename))
                            file_log3.write(modified_time)
                            type_of_file, encoding = mimetypes.guess_type(filename,True)
                            if type_of_file:
                                conn.send(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + type_of_file + '\n')  #send file list to server
                                file_log3.write(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + type_of_file + '\n')
                            else:
                                conn.send(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + 'None' + '\n')  #send file list to server
                                file_log3.write(file_endings[f] + '\t' + size + '\t' + modified_time + '\t' + created_time + '\t' + 'None' + '\n')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        file_log3.write(str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command')

                if "regex" in input2:
                    try:
                        invalid = False
                        regex = input2.split('?')[1].strip()
                        try:
                            re.search(regex,"")
                        except Exception,e:
                            invalid = True
                            print 'Invalid regex'
                            file_log2.write('Invalid regex')
                        if not invalid:
                            files = []
                            file_endings = []
                            for dp,dd,f in os.walk(directory):
                                for j in range(len(f)):
                                    file_name = dp
                                    if dp[len(dp)-1] != '/':
                                        file_name += '/'
                                    file_name += f[j]
                                    file_endings.append(os.path.relpath(file_name, os.path.commonprefix([file_name,directory])))
                                    files.append(file_name)
                                    file_log4.write(file_name)
                            for f in range(len(files)):
                                if re.search(regex,files[f]):
                                    conn.send(file_endings[f] + '\n')
                                    file_log3.write(file_endings[f] + '\n')
                    except Exception,e:
                        print str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command'
                        file_log2.write(str(e) + ' : An error occured while fetching the filelist, make sure you enter the correct command')
                        continue

            if "download" in input2:
                per=1
                try:
                    flag=0
                    command,value = input2.split('?')
                    value=value.strip()
                    if(per==1):
                        flag=1
                    file_abspath = os.path.abspath(directory + value)
                    if file_abspath.find(os.path.abspath(directory)) != 0:
                        if(flag==1):
                            per=1
                        conn.send('#102')
                        file_log3.write('#122')
                    elif os.path.isfile(directory + value):
                        filename=directory + value
                        statinfo = os.stat( filename)
                        file_log4.write(filename)
                        size = str(statinfo.st_size)
                        file_log4.write(size)
                        modified_time = time.ctime(os.path.getmtime(filename))
                        file_log4.write(modified_time)
                        created_time = time.ctime(os.path.getctime(filename))
                        hash_value = md5(filename)
                        strr2=value+'?'+size+'?'+modified_time+'?'+hash_value+'?'
                        file_log3.write(strr2)
                        conn.send(strr2)
                        if(flag==0):
                            per=1
                        f = open(filename,'rb')
                        l = f.read(1024)
                        file_log4.write(per)
                        flag=0
                        while (l):
                            file_log3.write(flag)
                            conn.send(l)
                            file_log3.write(l+'value')
                            if(flag==0):
                                per=1
                            l = f.read(1024)
                        f.close()
                    else:
                        conn.send("#101")
                        file_log3.write("#101")
                except Exception,e:
                    print str(e) + ' : An error occured while fetching the file, make sure you enter the correct command'
                    file_log2.write(str(e) + ' : An error occured while fetching the file, make sure you enter the correct command')

            if "hash" in input2:
                try:
                    flag=0
                    if "verify" in input2:
                        if(flag==0):
                            per=1
                        trr = input2.split('?')
                        command1,filenameold = trr
                        trr1 = filenameold.strip()
                        filename = directory + trr1
                        if os.path.isfile(filename):
                            trr2 = filenameold + ' => ' + md5(filename) + ', ' + time.ctime(os.path.getmtime(filename))
                            file_log3.write(trr2)
                            conn.send(trr2)
                        else:
                            file_log3.write("went into else #102")
                            conn.send("#101")
                            
                    elif "checkall" in input2:
                        flag=0
                        if(flag==0):
                            per=1
                        files = []
                        file_starting=[]
                        file_endings = []
                        for dp,dd,f in os.walk(directory):
                            if(per==1):
                                file_log1.write(per)
                            for j in range(len(f)):
                                file_name = dp
                                if(flag==0):
                                    per=0
                                if dp[len(dp)-1] != '/':
                                    file_name += '/'
                                per=1
                                file_name = file_name + f[j]
                                files.append(file_name)
                                trr3 = os.path.relpath(file_name, os.path.commonprefix([file_name,directory]))
                                file_log4.write(file_name)
                                file_endings.append(trr3)
                                if(per==0):
                                    flag=1
                                file_log2.write(flag)
                        flag1=0
                        for f in range(len(files)):
                            trr4 = file_endings[f] + ' => ' + md5(files[f]) + ', ' + time.ctime(os.path.getmtime(files[f])) + '\n'
                            file_log3.write(trr4)
                            conn.send(trr4)
                        if(flag1==0):
                            per=1
                except Exception,e:
                    flag = 0
                    file_log2.write(str(e) + ' : An error occured while getting the hash of the file(s), make sure you enter the correct command')
                    print str(e) + ' : An error occured while getting the hash of the file(s), make sure you enter the correct command'
                    if(str(e)>10):
                        flag=1
            conn.close()


def tcp_main(ip, directory):
    server = tcp_server()
    print "tcp_main called"
    server.runServer(ip, directory)

def udp_main(ip, directory):
    server = udp_server()
    print "udp_main called"
    server.runServer(ip, directory)
