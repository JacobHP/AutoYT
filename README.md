# AutoYT

AutoYT is an automated youtube TTS content creation pipeline.

The top comments are scraped from popular subreddit posts, processed through text-to-speech and an image creation pipeline, then collated into a video and pushed to youtube. 

The pipeline is built using Python, with particular libraries including PIL, MoviePy and the Youtube Data API on GCP.

### Overview

AutoYT scrapes Reddit comments/posts, cleans these, converts them to speech, generates images of comments/posts with Reddit themes, generates a video of comments being read out and pushes this to youtube.

Scraper &rarr; Cleaner &rarr; Text-to-Speech &rarr; Images &rarr; Movies &rarr; Youtube

### Example Output

https://www.youtube.com/watch?v=YRujNRZYsFA&t=22s


### Modules
* **scraper** - This module is built on top of the PRAW Reddit API wrapper and contains 2 functions. The ```scrape_top_comments``` function gets a dataframe of the top comments (and optionally child comments of these) from a given reddit post. The ```scrape_top_posts``` function gets a dataframe of the top posts from a given subreddit. 

* **cleaner** - This module contains a text cleaning function ```clean_text``` to remove links and emojis, and functions ```split_paragraphs``` and ```split_punctuation``` to split text into list split by paragraphs or punctuation.

* **tts** - This module is built using pyttsx3 and provides functions ```read_comment``` and ```read_comment_list``` to convert text strings into .mp4 audio files.

* **images** - Rather than screenshots, images of comments are created in the Reddiit style. This allows for a lot more functionality in presenting the comments (e.g. splitting on punctuation etc.). The images module is built using PIL and contains the ```long_reddit_image``` function that will return a list of images (based on split along paragraphs or punctuation), as well as additional helper functions to write on images.
 
* **movies** - This module is built on MoviePy and contains functions ```create_slide``` which combines images and audio into a video clip, and the  ```create_slide_movie``` which combines a list of slide clips into a movie with backing audio.

* **youtube** - This module provides functions to interact with the Youtube Data API. ```build_authenticated_service``` uses client credentials to build an authenticated connection to the API. ```upload_video``` uploads a youtube video with metadata given in the *request_body* argument. ```amend_thumbnail``` amends the thumbnail of a given video_id. See [Youtube Data API documentation](https://developers.google.com/youtube/v3/getting-started) for more details. Also, see **Additional Requirements** section of this documentation for details on additional requirements.

### Folder Structure and Templates
* Folder structure 
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


### Additional Requirements
* Requirements - In addition to packages in requirements.txt the code also requires ffmpeg and imagemagick. These can be downloaded from homebrew as follows:
```
brew install ffmpeg
brew install imagemagick
```
* Youtube Data API - To use the Youtube Data API and get credentials you will need to set up a GCP project with the Youtube Data API enabled. You will need to enable access for the google account that you wish to upload the video with. In addition, the youtube account you are uploading to must be verified (this is a simple procedure) and to upload public videos, the account must go through the youtube audit procedure by filling out [this form](https://support.google.com/youtube/contact/yt_api_form?hl=en) (slightly less simple).
