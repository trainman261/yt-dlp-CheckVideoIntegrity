## Check Video Integrity

This is a plugin to check if the video was downloaded successfully. It first checks a number of different fields to check if the length matches the metadata from the site (in my experience this is often a symptom of a download gone wrong). On Windows, it also checks the file duration metadata. Pull requests are welcome for other platforms.

When all the duration checks are complete, it uses ffmpeg to look through the video and search for any signs of corruption.

If there is a problem, it will abort, and yt-dlp will return an error code.


## Installation

Tested on `2023.11.16`.

You can install this package with pip:
```
python3 -m pip install -U https://github.com/trainman261/yt-dlp-CheckVideoIntegrity/archive/master.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.


## Development

Python is by far not my best language, don't expect great code - but feel free to improve it! Pull requests are welcome, as mentioned.
Also, feel free to open issues.
