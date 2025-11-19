import os
import sys
import socket
import time
import multiprocessing

def worker(conn, addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f'Start server with {sys.argv}')
        while True:
            try:
                conn, addr = s.accept()
                process = multiprocessing.Process(target=worker, args=(conn, addr))
                process.start()
                print(f'Start child worker {process}')
            except KeyboardInterrupt:
                print('Shutdown server')
                for process in  multiprocessing.active_children():
                    print('Terminate process {0}'.format(process))
                    process.terminate()
                    process.join()
                breakㄹ