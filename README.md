# AutoYT
*** **WORK IN PROGRESS** ***


AutoYT is an automated youtube TTS content creation pipeline.

The top comments are scraped from popular subreddit posts, processed through text-to-speech and an image creation pipeline, then collated into a video and pushed to youtube. 

The pipeline is built using Python, with particular libraries including PIL, MoviePy and the Youtube Data API on GCP.

#### Overview

AutoYT scrapes Reddit comments/posts, cleans these, converts them to speech, generates images of comments/posts with Reddit themes, generates a video of comments being read out and pushes this to youtube.

Scraper &rarr; Cleaner &rarr; Text-to-Speech &rarr; Images &rarr; Movies &rarr; Youtube

#### Example Output

https://www.youtube.com/watch?v=YRujNRZYsFA&t=22s


#### Modules
* scraper - This module is built on top of the PRAW Reddit API wrapper and contains 2 functions. The ```scrape_top_comments``` function gets a dataframe of the top comments (and optionally child comments of these) from a given reddit post. The ```scrape_top_posts``` function gets a dataframe of the top posts from a given subreddit. 

* cleaner - This module contains a text cleaning function ```clean_text``` to remove links and emojis, and functions ```split_paragraphs``` and ```split_punctuation``` to split text into list split by paragraphs or punctuation.

* tts - This module is built using pyttsx3 and provides functions ```read_comment``` and ```read_comment_list``` to convert text strings into .mp4 audio files.

* images - *todo docs*

* movies - *todo docs*

* youtube - *todo docs* 

#### Folder Structure and Templates
* Folder structure - todo

```
AutoYT
│   README.md
│   .gitignore
│   LICENSE
│   requirements.txt
│   main.py (example pipeline)
│
└───autoyt
│   │   __init__.py
│   │   scraper.py
│   │   cleaner.py
│   │   tts.py
│   │   images.py
│   │   movies.py
│   │   youtube.py
│   
└─── data
│   └───templates
│   └───audio
│   └───images
│   └───movies
│   └───music
│   └───fonts
│   └───credentials
│       │   client_secret.json
│       │   credentials.json
│   └───templates
│       │   description.yaml
│       │   image_configuration.json
│       │   intro_base.jpeg
│       │   outro.jpeg
│       │   static.mp4
│       │   thumbnail_template.jpeg
│       │   youtube_request.json
```


#### Additional Requirements
* Requirements - In addition to packages in requirements.txt the code also requires ffmpeg and imagemagick. These can be downloaded from homebrew as follows:
```
brew install ffmpeg
brew install imagemagick
```
