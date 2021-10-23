'''
Author: Jacob Howard-Parker

Functions for converting text to speech

'''

import pyttsx3
import os
import pandas as pd

def read_comment(comment, output_dir, rate=225):
    '''
    Convert a comment to speech
    Inputs: comment string, output filename dir string, integer rate
    Outputs: None. Saves mp3 file to output filename
    '''
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.save_to_file(comment, output_dir+'.mp3')
    engine.runAndWait()

def read_comment_list(comment_list, output_dir):
    '''
    Convert list of comments to speech
    Inputs: list of comments, output filename
    Outputs: None, saves mp3s to output filename + index based
            on list index
    '''
    for idx in range(len(comment_list)):
        read_comment(comment_list[idx], output_dir+f'_{idx}')
    
