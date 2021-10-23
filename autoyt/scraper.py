'''
Author: Jacob Howard-Parker

This module provides functions for scraping comments from Reddit posts. 
The module uses the praw Reddit API and requires Reddit application 
credentials to use.

'''

import praw
import pandas as pd
import json


def scrape_top_comments(post_url, credentials, top_limit=10, child_limit=0):
    '''
    Scrapes top comments and metadata from the given Reddit post
    specified in the post_url argument.

    Inputs: 
        - post_url: url of reddit post
        - credentials: reddit application credentials json
        - top_limit: integer limit of top-level comments
        - child_limit: integer limit of child comments 
            (for each top-level comment)

    Outputs:
        - pandas DataFrame of post comments
    '''

    reddit = praw.Reddit(client_id=credentials['client_id'], 
                        client_secret=credentials['client_secret'],
                        user_agent=credentials['user_agent'])
    comments_list = []
    submission = reddit.submission(url=post_url)
    submission.comment_sort = 'top'
    submission.comments.replace_more(top_limit/5) # makes faster scrape 
    for top_level_comment in submission.comments:
        if top_level_comment.author: 
            comments_list.append([top_level_comment.id, None, 
                                top_level_comment.body,
                                top_level_comment.author.name, 
                                top_level_comment.ups, top_level_comment.downs]) 
            if child_limit > 0:
                for second_level_comment in top_level_comment.replies:
                    if second_level_comment.author:
                        comments_list.append([second_level_comment.id, 
                                            second_level_comment.parent_id[3:],
                                            second_level_comment.body, 
                                            second_level_comment.author.name, 
                                            second_level_comment.ups, 
                                            second_level_comment.downs])
            
    comments_df = pd.DataFrame(comments_list, 
            columns=['id', 'parent_id','body', 'author', 'upvotes', 'downvotes']) # issue with 0 downvotes 

    comments_df['net_votes'] = comments_df['upvotes'] - comments_df['downvotes']

    final_df = comments_df[comments_df['parent_id'].isnull()].sort_values(
            by='net_votes', ascending=False).reset_index().iloc[:top_limit , :]

        
    if child_limit > 0:
        child_df = comments_df[
            ~(comments_df['parent_id'].isnull()) & 
            (comments_df['parent_id'].isin(final_df['id'].unique()))]\
            .sort_values(by='net_votes', ascending=False).reset_index()\
                .iloc[:child_limit, :] # check this works
        final_df = final_df.append(child_df)
    return final_df

def scrape_top_posts(subreddit, credentials, post_limit=1):
    '''
    Scrapes top post metadata from given subreddit.
    Inputs: 
        - subreddit: string of subreddit name
        - credentials: reddit application credentials json
        - post_limit: integer number of posts
    Outputs:
        - pandas DataFrame of reddit posts
    '''
    reddit = praw.Reddit(client_id=credentials['client_id'], 
                        client_secret=credentials['client_secret'],
                        user_agent=credentials['user_agent'])

    top_posts = reddit.subreddit(subreddit).top('day', limit=post_limit)
    post_list = []
    for post in top_posts:
        if not post.author:
            post_list.append([post.url, post.title, post.selftext, '[deleted]'])
        else:
            post_list.append([post.url, post.title, post.selftext, 
                            str(post.author)])
    post_df = pd.DataFrame(post_list, columns=['url', 'title', 'body', 'author'])
    return post_df



