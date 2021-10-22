'''
Author: Jacob Howard-Parker

Simple preprocessing module before text gets converted into speech
'''

import re

def clean_text(text):
    '''
    Removes links and emojis
    Input:
    Output:
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
                                # stole this off github - might be better to make it 
                                # pull up to date list from http://www.unicode.org/Public/emoji/1.0//emoji-data.txt
    text = emoji_pattern.sub(r'', text)

    # non-unicode emojis
    other_emoji = r'[\:\;\<\=][\)\(OoPpSsDd3]'
    # this wont remove everything - can add more as we go
    text = re.sub(other_emoji, '', text)
    # remove zero width space
    text = re.sub('&#x200b', '', text)
    return text


def split_paragraphs(text):
    '''
    Splits text into paragraphs (with spacing)
    Input:
    Output:
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
    Input:
    Output: List of lists, each list represents a paragraph, split along punctuation
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

    # what about double punc? - we may want to join up puncs after e.g.
    # while punc in list:
        # split[split.index(punc)-1]+=split[split.index[punc]]
        # remove the punc index
        # re-evaluate the while 
        # wrap this as a function and iterate over.



if __name__ == '__main__':
    test = "This is a test sentence... \n\nWhen I was a young kid, I really wanted to become an astronaut. It was a lifelong dream. \n\nSafe to say I'm not"
    split = split_punctuation(test)
    print(split)

