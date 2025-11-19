import os
import socket
import sys
import threading
import time


def workder(conn, addr):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(HOST, PORT)
        s.listen(1)
        print(f'Start server with {sys.argv}')
        while True:
            try:
                conn, addr = s.accept()
                    thread = threading.Thread(target=worker, args=(conn, addr))
                    thread start()
                    print(f'Start child worker {thread}')
            except KeyboardInterrupt:
                print('Shutdown server')
                for thread in threading.enumerate():
                    if thread.getName() == 'MainThread':
                        continue
                    print('Join thread {0}'.format(thread))
                    thread.join(timeout=1)
                    
                break
