#~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#File type:                ECE 4564 Assignment 1 Python Script
#File name:                Client File (client.py)
#Description:              Script containing the setup and running of the client
#Inputs/Resources:
#Output/Created files:     Server Side Responses
#Written by:               Team 6
#Created:                  02/16/2018
#Last modified:            02/16/2018
#Version:                  1.0.0
#Example usage:            python3 client.py -s 172.29.89.134 -p 5000 -z 1024 -t "#ECE4564T66"
#Notes:                    Tweet: How many licks does it take to get to the tootsie roll center of a tootsie pop? #ECE4564T66
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#!/usr/bin/env python3


#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
def stream():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    listener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=[HASHTAG])

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        global HASHTAG
        global SERVER
        text_msg = str(status.text)
        print('[Checkpoint] New Tweet: ', text_msg, ' | User: ???')
        text_msg = text_msg.replace(HASHTAG, "")
        key_msg = Fernet.generate_key()
        en_msg = Fernet(key_msg).encrypt(text_msg.encode('utf-8'))
        print('[Checkpoint] Encrypt: Generated Key: ', key_msg, ' | Ciphertext: ',en_msg)
        check_msg = hashlib.md5(en_msg).hexdigest()
        print('[Checkpoint] Generated MD5 Checksum: ', check_msg)
        message_send = (key_msg,en_msg,check_msg)
        pickle_msg = pickle.dumps(message_send)
        try:
            print('[Checkpoint] Connecting to ', SERVER_IP, ' on port ', SERVER_PORT)
            SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SERVER.connect((SERVER_IP, int(SERVER_PORT)))
        except socket.error as error_message:
            if SERVER:
                SERVER.close()
            print("[ERROR] Unable to open the socket: " + str(error_message))
            print('[ERROR] Client CLOSING')
            sys.exit(1)
        print('[Checkpoint] Sending data: ', pickle_msg)
        SERVER.send(pickle_msg)
        print('[Checkpoint] Waiting for response')
        pickle_msg = SERVER.recv(int(SOCKET_SIZE))
        print('[Checkpoint] Received data: ', pickle_msg)
        if pickle_msg:
            message_receive = pickle.loads(pickle_msg)
            if hashlib.md5(message_receive[0]).hexdigest() != message_receive[1]:
                print('[ERROR] Checksum is NOT VALID')
                print('[ERROR] Client CLOSING')
                sys.exit(1)
            else:
                print('[Checkpoint] Checksum is VALID')
                text_msg = Fernet(key_msg).decrypt(message_receive[0])
                print('[Checkpoint] Decrypt: Using Key: ', key_msg, ' | Plaintext: ', text_msg)
                text_msg = text_msg.decode("utf-8")
                cmd = 'espeak "{0}" 2>/dev/null'.format(text_msg)
                os.system(cmd)
                print('[Checkpoint] Speaking: ', text_msg)
        else:
            print('[ERROR] Unknown packet received')
        print('[Checkpoint] Listening for Tweets that contain: ', HASHTAG)

    def on_error(self, status_code):
       if status_code == 420:
            print('[ERROR] False in "on_data" function')
            return False

def loadOptions(argv):
    global SERVER_IP
    global SERVER_PORT
    global SOCKET_SIZE
    global HASHTAG
    options = {}
    while argv:
        if argv[0][0] == '-':
            options[argv[0]] = argv[1]
        argv = argv[1:]
    if (len(options) == 4) and ('-s' in options) and ('-p' in options) and ('-z' in options) and ('-t' in options):
        SERVER_IP = options['-s']
        SERVER_PORT = options['-p']
        SOCKET_SIZE = options['-z']
        HASHTAG = options['-t']
    else:
        return 1
    return 0
"""

from bluetooth import *

if __name__ == '__main__':
	

	services=find_service(name="helloService", 
                            uuid=SERIAL_PORT_CLASS)

	for i in range(len(services)):
		match=services[i]
		if(match["name"]=="helloService"):
			port=match["port"]
			name=match["name"]
			host=match["host"]

			print (name, port, host)

			client_socket=BluetoothSocket( RFCOMM )

			client_socket.connect((host, port))

			client_socket.send("Hello world")

			client_socket.close()

			break
	"""
    if loadOptions(sys.argv):
        print('[ERROR] Arguments missing or are incorrect')
        print('[ERROR] Client CLOSING')
        sys.exit(1)
    print('[Checkpoint] Listening for Tweets that contain: ', HASHTAG)
    stream()
    """

#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
