'''
Author: Jacob Howard-Parker
#TODO

'''

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import re
import pandas as pd

def create_base_image(background=(26,26,27), size=(1920, 1080)):
    img = Image.new('RGB', size, background)
    return img
    

def write_on_image(image, text_args, body):
    '''
    Write the text in the style and position specified in the text_args 
    on a given image.
    Input: image - PIL image, text_args - nested dictionary
    Ouput:
    '''
    # try and make this as flexible as possible
    color = text_args['color']
    margin, offset = text_args['position']
    font = ImageFont.truetype(text_args['font_loc'], text_args['font_size'])
    width = text_args['width']
    draw = ImageDraw.Draw(image)
    for line in textwrap.wrap(body, width=width):
            draw.text((margin, offset), line, color, font=font)
            offset += font.getsize(line)[1]
    return image


def write_body_image(image, text_args, text):
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


def long_reddit_image(text_args_dict, paragraph_list, author, points, background, size):
    '''
    We want a list of images by punctuation split
    '''
    image_list = []
    lines=0
    text=''
    second = False

    author_font = ImageFont.truetype(text_args_dict['author']['font_loc'],
                                text_args_dict['author']['font_size'])
    points_position = (text_args_dict['points']['position'][0]+author_font.getsize(author)[0],
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
    
            if lines <= 20:
                current_text = ' '.join(paragraph[:idx+1])
                print(lines)
                base_img = create_base_image(background, size)
                image = write_on_image(base_img, text_args_dict['author'], author)
                
                image = write_on_image(image, points_args, points) # add the spacing
                image, lines = write_body_image(image, text_args_dict['body'], text+current_text)
                image_list.append(image)
                first_idx = idx
            
            elif lines>20:
                # start new image with secondary layout
                print(lines)
                if second==False:
                    text='' 
                    first_idx = idx
                    second=True# only want once
                print(first_idx, idx)
                current_text = ' '.join(paragraph[first_idx : idx+1])
                print(current_text)
                base_img = create_base_image(background, size)
                image, lines = write_body_image(base_img, text_args_dict['body_second'], text+current_text)
                image_list.append(image)
                lines+=20
        #lines+=2 # for new para
        first_idx=0
        text += current_text + ' \n\n'
    return image_list

    
def create_intro_image(author, points, subreddit, body ,text_args_dict, template = False):
    '''
    Create intro image
    '''
    if template:
        intro = Image.open(template)
    else:
        intro = create_base_image()
    draw = ImageDraw.Draw(intro)
    # subreddit
    intro = write_on_image(intro, text_args_dict['intro_subreddit'], 'r/'+subreddit)
    # author
    intro = write_on_image(intro, text_args_dict['intro_author'], ' '+ u"\u00B7" + ' u/'+author)
    # body
    intro = write_on_image(intro, text_args_dict['intro_body'], body)
    return intro

def open_and_write(base, body_dict, text):
    '''
    Create simple thumbnail
    '''
    
    img = Image.open(base)
    img = write_on_image(img, body_dict, text)
    return img





    


if __name__ == '__main__':
    text_dict = {'author': {'color':(79,188,255), 'position':(240,270), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':24,'width':100},
                'points': {'color':(129,131,132), 'position':(240, 270), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':24,'width':100}, # to add
                'body': {'color':(215, 218, 220), 'position':(240, 315), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':28,'width':100},
                'body_second': {'color':(215, 218, 220), 'position':(240, 270), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':28,'width':100},
                "intro_subreddit" : {"color" : (215,218,220), "position":(240,280), "font_loc": "data/fonts/noto-sans/NotoSans-Bold.ttf", "font_size": 32, "width":100},
    "intro_points" : {"color" : (129,131,132), "position":(440,280), "font_loc": "data/fonts/noto-sans/NotoSans-Regular.ttf", "font_size": 32, "width":100},
    "intro_author" : {"color" : (129,131,132), "position":(440,280), "font_loc": "data/fonts/noto-sans/NotoSans-Regular.ttf", "font_size": 32, "width":100},
    "intro_body" : {"color" : (215,218,220), "position":(180,380), "font_loc": "data/fonts/noto-sans/NotoSans-Regular.ttf", "font_size": 58, "width":60}
                }

    #img = create_base_image()
    #image, lines = write_body_image(img, text_dict['body'], 'The quick brown fox jumped over the lazy dog lmao so cool \n\n And then maybe we could go for icecream... or something else? :p')
    #image.save('temp.png')

    #paragraph_list = [['When we went to the park.'], ['My mom and I used to go the park together,', 'which was a rarity in those days.', 'Sometimes we would see birds;', 'or planes.'],
    #['Long story short,', 'fuckoff!']]*5
    #image_list = long_reddit_image(text_dict, paragraph_list, 'phwj97', '493', background=(26,26,27), size=(1920, 1080))

    #for idx in range(len(image_list)):
     #   image_list[idx].save(f'temp_{idx}.png')
    author='phwj97'
    points=2
    subreddit='AskReddit'
    body = "Dear people of Reddit, what is the weirdest animal you've ever seen?"
    text_args_dict=text_dict
    img = create_intro_image(author, points, subreddit, body ,text_args_dict, template='/Users/Jacob/autoyt2/data/templates/intro_base.jpeg')
    img.save('temp.png')
    # now test multi-image functionality 