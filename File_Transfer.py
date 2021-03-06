import os
import subprocess

global conn_OR_socket, Path, SENDER_NAME


class Send:

    # INITIALIZING "conn"
    def __init__(self, connection, path, name):

        global conn_OR_socket, Path, SENDER_NAME
        conn_OR_socket = connection
        Path = path
        SENDER_NAME = name

        # GET THE LOCAL DISK FROM THE FILE PATH( eg: 'C' FROM 'C:\Users\DELL\Desktop\Notes\report.pdf')
        local_disk = Path.split(":")[0] + ":"
        print(local_disk)
        os.chdir("C:")
        print(os.getcwd(), Path)

        '''========================================== THREAD SEND ==========================================='''

    # DEFINITION OF CLASS "Send"
    class Send:

        @staticmethod
        def run():

            try:
                print(Path)
                with open(Path.lstrip('\u202a'), 'rb') as file:

                    # SENDING DATA OF THE FILE IN A LOOP
                    for data in file:
                        # SENDING DATA TO RECEIVER
                        conn_OR_socket.send(data)

                    conn_OR_socket.send(bytes("FILE EXIT".encode()))
                    print("file sent")
                    # file.close()

            except Exception as e:
                print(type(e).__name__, e)
                print("file could not be transferred")
                print("pleas try again")
                conn_OR_socket.send(bytes("TRANSFER FILED".encode()))

    @staticmethod
    def start():

        # EXECUTE "run" METHOD USING CLASS-NAME SINCE "run" IS A STATIC-METHOD
        Send.Send.run()


class Receive:

    def __init__(self, connection, path):

        global conn_OR_socket, Path
        conn_OR_socket = connection

        # PATH CREATION FOR THE RECEIVING FILE
        path_list = path.split("\\")
        Path = "C:\\Airdroid\\" + path_list[-1]

        # CREATING DIRECTORY TO STORE THE RECEIVED FILE
        os.chdir("C:")
        print(os.getcwd(), Path)
        subprocess.Popen("mkdir Airdroid", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)

        '''========================================= THREAD RECEIVE ========================================='''

    # DEFINITION OF CLASS "Receive"
    class Receive:

        @staticmethod
        def run():

            try:
                with open(Path.lstrip('\u202a'), 'wb') as file:
                    print("file opened at the path : ", Path)

                    while True:

                        # RECEIVING DATA FORM SENDER
                        data = conn_OR_socket.recv(1024)

                        if "TRANSFER FILED" in str(data):
                            print("transfer failed")
                            # file.close()
                            break

                        if "FILE EXIT" not in str(data):
                            # WRITING "data" ON TO THE FILE
                            file.write(data)

                        else:
                            # CLOSE THE FILE WHEN "FILE EXIT" MESSAGE IS RECEIVED
                            print("file received")
                            # file.close()
                            break

            except Exception as e:
                print(type(e).__name__, e)
                file.close()

    @staticmethod
    def start():

        # EXECUTE "run" METHOD USING CLASS-NAME SINCE "run" IS A STATIC-METHOD
        Receive.Receive.run()
