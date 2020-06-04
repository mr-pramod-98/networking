import os
import subprocess


class Send:

    # INITIALIZING "conn"
    def __init__(self, connection, path, name):

        global conn_OR_socket, Path, SENDER_NAME
        conn_OR_socket = connection
        Path = path
        SENDER_NAME = name

        # GET THE LOCAL DISK FROM THE FILE PATH( eg: 'C' FROM 'C:\Users\DELL\Desktop\Notes\report.pdf')
        local_disk = Path.split(":")[0] + ":"
        os.chdir(local_disk)
        # print(os.getcwd())

        '''========================================== THREAD SEND ==========================================='''

    # DEFINITION OF CLASS "send"
    class send:

        def run(self):

            try:
                print(Path)
                file = open(Path, 'rb')

                # SENDING DATA OF THE FILE IN A LOOP
                for data in file:
                    # SENDING DATA TO RECEIVER
                    conn_OR_socket.send(data)

                conn_OR_socket.send(bytes("FILE EXIT".encode()))
                print("file sent")
                file.close()

            except Exception as e:
                print(type(e).__name__, e)
                print("file could not be transferred")
                print("pleas try again")
                conn_OR_socket.send(bytes("TRANSFER FILED".encode()))

    def start(self):

        # CREATING OBJECT FOR CLASS "send"
        file_out = Send.send()
        file_out.run()


class Receive:

    def __init__(self, connection, path):

        global conn_OR_socket, Path
        conn_OR_socket = connection

        # PATH CREATION FOR THE RECEIVING FILE
        Path_list = path.split("\\")
        Path = "C:\\Airdroid\\" + Path_list[-1]

        # CREATING DIRECTORY TO STORE THE RECEIVED FILE
        os.chdir("C:")
        # print(os.getcwd(), Path)
        subprocess.Popen("mkdir Airdroid", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)

        '''========================================= THREAD RECEIVE ========================================='''

    # DEFINITION OF CLASS "receive"
    class receive():

        def run(self):

            try:
                file = open(Path, 'wb')
                print("file opened at the path : ", Path)

                while True:

                    # RECEIVING DATA FORM SENDER
                    data = conn_OR_socket.recv(1024)

                    if "TRANSFER FILED" in str(data):
                        print("transfer failed")
                        file.close()
                        break

                    if "FILE EXIT" not in str(data):
                        # WRITING "data" ON TO THE FILE
                        file.write(data)

                    else:
                        # CLOSE THE FILE WHEN "FILE EXIT" MESSAGE IS RECEIVED
                        print("file received")
                        file.close()
                        break

            except Exception as e:
                print(type(e).__name__, e)
                file.close()

    def start(self):

        # CREATING OBJECT FOR CLASS "send"
        file_in = Receive.receive()
        file_in.run()
