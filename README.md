# AutoYT
*** **WORK IN PROGRESS** ***


AutoYT is an automated youtube TTS content creation pipeline.

The top comments are scraped from popular subreddit posts, processed through text-to-speech and an image creation pipeline, then collated into a video and pushed to youtube. 

The pipeline is built using Python, and in particular, PIL, MoviePy and the Youtube Data API on GCP.s

#### Overview

AutoYT scrapes Reddit comments/posts, cleans these, converts them to speech, generates images of comments/posts with Reddit themes, generates a video of comments being read out and pushes this to youtube.

Scraper &rarr; Cleaner &rarr; Text-to-Speech &rarr; Images &rarr; Movies &rarr; Youtube

#### Example Output

https://www.youtube.com/watch?v=YRujNRZYsFA&t=22s


#### Modules
* scraper - *todo*

* cleaner - *todo*

* tts - *todo*

* images - *todo*

* movies - *todo*

* youtube - *todo*

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
* Requirements - In addition to packages in requirements.txt *TODO*
