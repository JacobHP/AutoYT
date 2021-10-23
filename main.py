'''
Author: Jacob Howard-Parker
# TODO
'''
from autoyt.scraper import scrape_top_comments, scrape_top_posts
from autoyt.cleaner import clean_text, split_punctuation
from autoyt.tts import read_comment, read_comment_list
from autoyt.images import *
from autoyt.movies import create_slide, create_slide_movie, read_video
from autoyt.youtube import *

import os
from shutil import rmtree
import pandas as pd
import json

with open('data/credentials/credentials.json') as credentials_file:
        credentials = json.load(credentials_file)

def run_pipeline(subreddit, thumbnail_color=(252,124,0), upload=False, 
                delete_files=False):
    '''
    Main reddit yt pipeline
    '''

    print('Scraping reddit data...')
    posts = scrape_top_posts(subreddit, credentials, post_limit=1)
    post_url = posts.iloc[0].url
    post_title = posts.iloc[0].title
    post_author = posts.iloc[0].author
    comments_df = scrape_top_comments(post_url, credentials, 
                                    top_limit = 5, child_limit=0)
    print('...Reddit scrape complete.')

    print('Cleaning data..')
    comments_df['body'] = comments_df['body'].apply(clean_text)
    comments_df['body'] = comments_df['body'].apply(split_punctuation)
    print(comments_df['body'].head())

    if not os.path.exists(f'data/images/{post_title}'):
        os.mkdir(f'data/images/{post_title}')
    if not os.path.exists(f'data/audio/{post_title}'):
        os.mkdir(f'data/audio/{post_title}')

    print('Creating audio and images..')
    format_dict = {'author': {'color':(79,188,255), 'position':(240,270), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':24,'width':100},
                'points': {'color':(129,131,132), 'position':(240, 270), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':24,'width':100}, # to add
                'body': {'color':(215, 218, 220), 'position':(240, 315), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':28,'width':100},
                'body_second': {'color':(215, 218, 220), 'position':(240, 270), 'font_loc':'data/fonts/noto-sans/NotoSans-Light.ttf', 'font_size':28,'width':100},
                "intro_subreddit" : {"color" : (215,218,220), "position":(240,280), "font_loc": "data/fonts/noto-sans/NotoSans-Bold.ttf", "font_size": 32, "width":100},
    "intro_points" : {"color" : (129,131,132), "position":(440,280), "font_loc": "data/fonts/noto-sans/NotoSans-Regular.ttf", "font_size": 32, "width":100},
    "intro_author" : {"color" : (129,131,132), "position":(440,280), "font_loc": "data/fonts/noto-sans/NotoSans-Regular.ttf", "font_size": 32, "width":100},
    "intro_body" : {"color" : (215,218,220), "position":(180,380), "font_loc": "data/fonts/noto-sans/NotoSans-Regular.ttf", "font_size": 58, "width":60},
    "thumbnail" : {"color" : (252,124,0), "position" : (800, 100), "font_loc": "data/fonts/noto-sans/impact/impact.ttf", "font_size":100, "width": 20}
               
               
                } # put this into json
    
    intro_img = create_intro_image(post_author, 1, subreddit, body=post_title, 
                                text_args_dict = format_dict, 
                                template='data/templates/intro_base.jpeg')

    intro_img.save(f'data/images/{post_title}/intro.png')
    read_comment(post_title, f'data/audio/{post_title}/intro')
    for author, comment, points in zip(comments_df.author, comments_df.body, 
                                    comments_df.net_votes):
        print(author)
        print(points)
        img_list = long_reddit_image(format_dict, comment, author, points, 
                                    background=(26,26,27), size=(1920, 1080))

        for idx in range(len(img_list)):
            img_list[idx].save(f'data/images/{post_title}/{author}_{idx}.png')
        comment_list = [x for para in comment for x in para]  
        read_comment_list(comment_list, 
                        output_dir = f'data/audio/{post_title}/{author}')
    
    # create thumbnail
    thumbnail = open_and_write('data/templates/thumbnail_template.jpeg', 
                                format_dict['thumbnail'], post_title)
                                
    thumbnail.save(f'data/images/{post_title}/thumbnail.png')

    # movie creation
    slide_list = []
    intro_slide = create_slide(f'data/images/{post_title}/intro.png', 
                            f'data/audio/{post_title}/intro.mp3')
    slide_list.append(intro_slide)
    intermission = read_video('data/templates/static.mp4').cutout(0,0.5).volumex(0.5)
    for author, comment in zip(comments_df.author, comments_df.body):
        slide_list.append(intermission)
        comment_list = [x for para in comment for x in para]
        for idx in range(len(comment_list)): 

            slide = create_slide(f'data/images/{post_title}/{author}_{idx}.png', 
                                f'data/audio/{post_title}/{author}_{idx}.mp3', 
                                lag=0.1)

            slide_list.append(slide)
    outro_slide = create_slide('data/templates/outro.jpeg', audio=None, 
                                duration=5)

    slide_list.append(outro_slide)
    movie = create_slide_movie(slide_list, 'data/music/Distant.mp3')
    movie.write_videofile(f'data/movies/{post_title}.mp4', fps=24, codec='libx264', 
                        audio_codec='aac')
    
    if upload:
        # upload to youtube
        # set thumbnail
        print(post_title)
        print(len(post_title))
        request_body = {
            "snippet": {
                "categoryId": 19,
        "title": post_title,
        "description": 
            f'''
            AutoReddit collates the best comments from the hottest posts on Reddit. Make sure to like and subscribe for more! 
             
            Full credit goes to post/comment authors: {post_url}

            \n\nTrack Name: DISTANT
            \nMusic By: LAKEY INSPIRED @ https://soundcloud.com/lakeyinspired
            \nOfficial 'LAKEY INSPIRED' YouTube Channel HERE - https://www.youtube.com/channel/UCOmy"
            ''',            
        "tags": ["askreddit", "reddit", "tts", "text-to-speech", "text2speech", "funny", "comments"]
            },
            "status": {
        "privacyStatus": "private",#"private",
        "selfDeclaredMadeForKids": False
             },
            "notifySubscribers": True,
            "onBehalfOfContentOwnerChannel": "AutoReddit"
        }

        service = build_authenticated_service('data/credentials/client_secret.json', 
                                            api_service_name='youtube',
                                            api_version='v3', 
                                            scopes=['https://www.googleapis.com/auth/youtube.upload'])

        response_id = upload_video(service, f'data/movies/{post_title}.mp4', request_body)
    
        amend_thumbnail(service, f'data/images/{post_title}/thumbnail.png', response_id)


        

    if delete_files:
        # remove saved files
        print('Removing files...')
        rmtree(f'data/images/{post_title}')
        rmtree(f'data/audio/{post_title}')

if __name__ == '__main__':


    run_pipeline('AskReddit', upload=False, delete_files=True)

    # todo
    # Create jsons for slide, intro, outro
    