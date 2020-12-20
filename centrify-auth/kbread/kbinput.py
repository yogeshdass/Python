'''
Created on Jun 28, 2017

@author: shashank_dixit
'''
import sys
import platform
if (platform.system() == 'Windows'):
    import msvcrt
import logging

shouldExit = False

def readInput( caption, queue):
    sys.stdout.write('%s :'%caption)
    sys.stdout.flush()
    input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        global shoudExit
        if shouldExit == True :
            logging.info("User used the URL. No need for password input")
            return False
        
    queue.put(input)
    return True
