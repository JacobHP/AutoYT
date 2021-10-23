'''
Author: Jacob Howard-Parker
Functions for writing on images. Text args should be layed out as 
specified in data/templates/image_configuration.json
'''

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import re
import pandas as pd

def create_base_image(background=(26,26,27), size=(1920, 1080)):
    '''
    Create plain image of given size and background color
    '''

    img = Image.new('RGB', size, background)
    return img
    

def write_on_image(image, text_args, body):
    '''
    Write the text in the style and position specified in the text_args 
    on a given image.
    Input: image - PIL image, text_args - nested dictionary, body - string
    Ouput: image with string written based on specs in text_args
    '''

    color = text_args['color']
    margin, offset = text_args['position']
    font = ImageFont.truetype(text_args['font_loc'], text_args['font_size'])
    width = text_args['width']
    draw = ImageDraw.Draw(image)
    for line in textwrap.wrap(body, width=width):
            draw.text((margin, offset), line, color, font=font)
            offset += font.getsize(line)[1]
    return image

def open_and_write(base, text_args, text):
    '''
    Open and write on an image.
    Input: base - path to image, 
    '''
    
    img = Image.open(base)
    img = write_on_image(img, text_args, text)
    return img


def write_body_image(image, text_args, text):
    '''
    Write text onto an image
    '''

    color = text_args['color']
    margin, offset = text_args['position']
    font = ImageFont.truetype(text_args['font_loc'], text_args['font_size'])
    width = text_args['width']
    draw = ImageDraw.Draw(image)
    lines=0
    text_split = re.split('[\n][\n]+', text)
    for text in text_split:
        for line in textwrap.wrap(text, width=width):
            draw.text((margin, offset), line, color, font=font)
            offset += font.getsize(line)[1]
            lines+=1
        lines+=2 # for new paragraph
        offset+=font.getsize(line)[1]
    return image, lines 


def long_reddit_image(text_args_dict, paragraph_list, author, points, 
                    background, size):
    '''
    List of images by punctuation split
    '''

    image_list = []
    lines=0
    text=''
    second = False

    author_font = ImageFont.truetype(text_args_dict['author']['font_loc'],
                                text_args_dict['author']['font_size'])
    points_position = (text_args_dict['points']['position'][0]\
                                    +author_font.getsize(author)[0],
                                    text_args_dict['points']['position'][1])
    points_args = text_args_dict['points'].copy()
    points_args['position'] = points_position
    # points depends on author + we want to format it nicely
    dot = u"\u00B7"
    if points >= 1000:
        points = f' {dot} {round(points/1000, 1)}k points'
    else:
        points = f' {dot} {points} points'
    
    for paragraph in paragraph_list:
        for idx in range(len(paragraph)):
            # need to add if more than 40 lines etc.
            if lines <= 20:
                current_text = ' '.join(paragraph[:idx+1])
                base_img = create_base_image(background, size)
                image = write_on_image(base_img, text_args_dict['author'],
                                    author)
                
                image = write_on_image(image, points_args, points) 
                image, lines = write_body_image(image, text_args_dict['body'], 
                                                text+current_text)

                image_list.append(image)
                first_idx = idx
            
            elif lines>20:
                # start new image with secondary layout
                if second==False:
                    text='' 
                    first_idx = idx
                    second=True # only want once
                
                current_text = ' '.join(paragraph[first_idx : idx+1])
                
                base_img = create_base_image(background, size)
                image, lines = write_body_image(base_img, 
                                                text_args_dict['body_second'],
                                                text+current_text)
                image_list.append(image)
                lines+=20
        first_idx=0 # track that its a new para now
        text += current_text + ' \n\n'
    return image_list

    
def create_intro_image(author, points, subreddit, body ,text_args_dict, 
                        template = False):
    '''
    Create intro image
    '''

    if template:
        intro = Image.open(template)
    else:
        intro = create_base_image()
    draw = ImageDraw.Draw(intro)
    # subreddit
    intro = write_on_image(intro, text_args_dict['intro_subreddit'], 
                            'r/'+subreddit)

    # author
    intro = write_on_image(intro, text_args_dict['intro_author'], 
                            ' '+ u"\u00B7" + ' u/'+author)

    # body
    intro = write_on_image(intro, text_args_dict['intro_body'], body)
    return intro

