'''
Author: Jacob Howard-Parker

Functions for creating simple slide show videos
'''
import moviepy.editor as mpe
from pydub import AudioSegment
import pandas as pd
import os


def create_slide(image, audio, duration=None, lag=0.5):
    '''
    Creates slide of an image with audio
    '''
    if audio:
        sound = mpe.AudioFileClip(audio)
        audio_length = sound.duration
        clip = mpe.ImageClip(image, duration=audio_length+(2*lag))
        clip_final = clip.set_audio(mpe.CompositeAudioClip([sound.set_start(lag)]))
    else:
        clip_final = mpe.ImageClip(image, duration=duration)
    return clip_final

def read_video(video):
    clip = mpe.VideoFileClip(video)
    return clip

def create_slide_movie(slide_list, backing_audio):
    '''
    Creates movie with backing audio from list of slides
    '''

    movie = mpe.concatenate_videoclips(slide_list)
    length = movie.duration 
    print(length)
    background = mpe.AudioFileClip(backing_audio)
    while background.duration < length:
        background = mpe.AudioFileClip(backing_audio)
        background = mpe.concatenate_audioclips([background]*2)
    
    background_duration = background.duration
    background = background.cutout(0, background_duration - length)
    print(background.duration)
    
    final_audio = mpe.CompositeAudioClip([movie.audio.volumex(1),
            background.volumex(0.2).audio_fadein(10).audio_fadeout(10)])

    final_audio.fps = 44100
    movie = movie.set_audio(final_audio)
    return movie



# probably keep these as is as quite good

