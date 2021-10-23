'''
Author: Jacob Howard-Parker

Simple preprocessing module before text gets converted into speech
'''

import re

def clean_text(text):
    '''
    Removes links and emojis
    Input: text string
    Output: cleaned text string
    '''
    # Remove links
    text = re.sub(r'http[s]?://\S+', '', text)
    # Remove unicode emojis
    emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)
                                
    text = emoji_pattern.sub(r'', text)

    # non-unicode emojis
    other_emoji = r'[\:\;\<\=][\)\(OoPpSsDd3]'
    # this may not remove everything
    text = re.sub(other_emoji, '', text)
    # remove zero width space
    text = re.sub('&#x200b', '', text)
    return text


def split_paragraphs(text):
    '''
    Splits text into paragraphs (with spacing)
    Input: text string
    Output: list of paragraphs from text string
    '''
    return re.split('[\n][\n]+', text)


def _join_punc(punc, split_text):
    while punc in split_text:
        punc_idx = split_text.index(punc)
        split_text[punc_idx - 1]+=punc  
        split_text.pop(punc_idx)
    return split_text



def split_punctuation(text): 
    '''
    Splits text along full stops, commas, colons, semicolons and newlines
    Input: text string
    Output: List of lists, each list represents a paragraph, 
            split along punctuation
    '''
    # split paras then do this - would want to return a list of splits
    final_split = []
    split_para = split_paragraphs(text)
    for para in split_para:
        punc_re = r'(?<=[\.\,\:\;\!\?])\s*' # look behind then split on spaces
        split = re.split(punc_re, para)
        # remove empty strings
        while '' in split:
            split.remove('')
        for punc in ['.',',',':',';', '!', '?',"'", '"']:
            split = _join_punc(punc, split)
        final_split.append(split)
    return final_split


