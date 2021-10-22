'''
Author: Jacob Howard-Parker

Functions for converting text to speech

'''

import pyttsx3
import os
import pandas as pd

def read_comment(comment, output_dir, rate=225 ):
    '''
    Inputs:
    Outputs:
    '''
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.save_to_file(comment, output_dir+'.mp3')
    engine.runAndWait()

def read_comment_list(comment_list, output_dir):
    '''
    Inputs:
    Outputs
    '''
    for idx in range(len(comment_list)):
        read_comment(comment_list[idx], output_dir+f'_{idx}')
    
if __name__ == '__main__':
    read_comment(None, None)