from socket import *
from threading import *
from tkinter import *

sendFlag = 0
flag = 0

def getport():
    port=int(input_portno.get())
    if port<0 and port>65536:
        print("ERROR:PORT Number out of range.")
        return -1
    return port

def SendMsgB():
    global sendFlag
    sendFlag=1

def SendMsg(connection,address):
    while True:
        re=''
        global sendFlag

        while(sendFlag!=1):
            pass

        re=input_sendmsg.get()
        sendFlag=0

        input_sendmsg.delete(0,END)
        global flag
        if flag==0:
            connection.send(re.encode('UTF-8'))
            if(re=="!"):
                connection.close()
                break
        else:
            flag=0
            break

    connection.close()

def receiveMsg(connection,address):
    while TRUE:
        re=connection.recv(1024).decode('UTF-8')
        if re:
            text_recvMsg.configure(text=f'CLIENT:{re}')
            if re=="!":
                global flag
                flag=1
                re+='!'
                connection.close()
                break

def main(server,d):
    while TRUE:
        connection,address=server.accept()

        input_sendmsg.configure(state=NORMAL)
        button_sendmsg.configure(state=ACTIVE)
        text_recvMsg.configure(text="CONNECTED")

        thread1=Thread(target=SendMsg,args=(connection,address))
        thread2=Thread(target=receiveMsg,args=(connection,address))
        
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        connection.close()

        input_sendmsg.configure(state=DISABLED)
        button_sendmsg.configure(state=DISABLED)
        button_hostsocket.configure(state=ACTIVE)
        input_portno.configure(state=NORMAL)
        text_recvMsg.configure(text="NOT CONNECTED")


def hostSocket():
    port=getport()
    
    if port==-1:
        return
    address="127.0.0.1"
    server=socket(AF_INET,SOCK_STREAM) 
    #Here, AF_INET is the address family that is used for IPv4 addresses, 
    #and SOCK_STREAM is the type of socket that is used for TCP connections.
    server.bind((address,port))
    server.listen(1)
    button_hostsocket.configure(state=DISABLED)
    input_portno.configure(state=DISABLED)
    mainthread=Thread(target=main,args=(server,5))
    mainthread.start()




window=Tk()
window.title("Server")
window.geometry("650x380")
window.minsize(650,380)
window.maxsize(650,380)

text_portno=Label(window,font=("Arial",13),text="Port Number->",padx=8)
text_portno.place(y=20,anchor="nw") 

text_recvMsg=Label(window,borderwidth=3,font=("arial",13),
                   text="Not connected yet",padx=30,pady=30,
                   bg="white",width=54,height=3)
text_recvMsg.place(relx=0.07,rely=0.22,anchor=NW)

input_portno=Entry(window,font=("Arial",13))
input_portno.place(y=21,x=130)

button_hostsocket=Button(window,command=hostSocket,text="Start Listening",
                         font=("Arial",11,"bold"),relief=RAISED,bd=5,bg="white",
                         fg="black",activebackground='white',activeforeground='grey',state=ACTIVE)
button_hostsocket.place(relx=0.92,rely=0.025,x=-2,y=2,anchor=NE)

input_sendmsg=Entry(window,font=('arial',13),width=50,state=DISABLED)
input_sendmsg.place(relx=0.07,rely=0.6)

button_sendmsg=Button(window,command=SendMsgB,text="SEND MESSAGE",
                      font=("Arial",11,"bold"),relief=RAISED,bd=5,
                      bg="white",fg="black",activebackground="white",activeforeground="grey")
button_sendmsg.place(relx=0.767,rely=0.7)
window.mainloop()
