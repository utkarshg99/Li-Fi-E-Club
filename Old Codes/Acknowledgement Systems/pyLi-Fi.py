import serial
import time
import os

recport=input("Input Receiver Port : ")
traport=input("Input Transmitter Port : ")

ser = serial.Serial()
ser.baudrate=230400
ser.port=recport #Receiver-(Slave/Master)
ser.open()

serftr = serial.Serial()
serftr.baudrate=9600
serftr.port=traport #Transmitter-(Master-Slave)
serftr.open()

queue = [0,0,0,0,0,0,0,0,0,0]
start_seq = [1,1,0,0,0,1,0,0,0,1]
end_seq=[0,1,1,0,1,0,0,1,1,1]
x2={'11110':0,
'01001':1,
'10100':2,
'10101':3,
'01010':4,
'01011':5,
'01110':6,
'01111':7,
'10010':8,
'10011':9,
'10110':10,
'10111':11,
'11010':12,
'11011':13,
'11100':14,
'11101':15}

def queuecomp(queue1, queue2) :
    if(queue1!=queue2):
        return False
    return True

ch=input("Type (T)ransmitter or (R)eceiver : ")

if(ch[0]=='T'):
    print("Initialising Transmitter. Please Wait ...")
    time.sleep(5)

    lines = []
    print("Start Entering Input")
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    response=""
    flag=0
    trans=''
    ind=0
    t1=0
    t2=0
    while (ind<len(lines)):
        trans=lines[ind]+'\n'
        serftr.write(trans.encode())
        t1=time.time()
        while  True :
            t2=time.time()
            if(t2-t1>0.5):
                serftr.write(trans.encode())
                t1=t2
            while queuecomp(queue, start_seq) == False :
                val = int(ser.readline().decode('ascii')[0])
                queue.pop(0)
                queue.append(val)
                t2=time.time()
                if(t2-t1>0.05):
                    serftr.write(trans.encode())
                    t1=t2
            while True:
                q=[]
                for i in range(10):
                    queue.pop(0)
                    val = (ser.readline().decode('ascii')[0])
                    queue.append(int(val))
                    q.append(val)
                if(queuecomp(queue, end_seq)==True):
                    flag=1
                    break
                queuex=''.join(q)
                q1=x2[queuex[0:5]]
                q2=x2[queuex[5:]]
                num=q1*16+q2
                response=response+chr(num)
            if(flag==1):
                if(response[0]=='N'):
                    response=''
                    break
                elif(response[0]=='Y'):
                    response=''
                    ind+=1
                    break
                else:
                    flag=0
elif(ch[0]=='R'):
    st1=''
    st2=''
    flag=0
    while  True :
        while queuecomp(queue, start_seq) == False :
            val = int(ser.readline().decode('ascii')[0])
            queue.pop(0)
            queue.append(val)
        while True:
            q=[]
            for i in range(10):
                queue.pop(0)
                val = (ser.readline().decode('ascii')[0])
                queue.append(int(val))
                q.append(val)
            if(queuecomp(queue, end_seq)==True):
                if(st1!=st2):
                    flag=1
                    st1=st2
                    break
                else:
                    flag=2
                    break
            queuex=''.join(q)
            q1=x2[queuex[0:5]]
            q2=x2[queuex[5:]]
            num=q1*16+q2
            st2=st2+chr(num)
        if(flag==1):
            st1=st2
            print(st2[:len(st2)-1])
            st2=''
            serftr.write('Y\n'.encode())
        if(flag==2):
            st2=''
            serftr.write('Y\n'.encode())
else:
    print("Wrong Choice. Start pyLi-Fi again.")