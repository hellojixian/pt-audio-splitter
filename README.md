# pt-audio-splitter
## Installation
```sh
pip install -r requirements.txt
```

## How to use the script
1. put the source audio as wav file in ./source folder
2. run the script
```sh
./process.py [audio_file_name.wav]
```

## Usage help
```sh
$ ./process.py -h
usage: process.py [-h] [--model MODEL] source

Audio Splitter tool

positional arguments:
  source         source audio file, in ./source folder eg: raw_audio.wav

options:
  -h, --help     show this help message and exit
  --model MODEL  specify the AI model to use

```
## Advanced usage
in case if you want to try different models, you can do as below
```sh
./process.py raw_audio_1.wav --model=base
```
available models are below
- tiny.en
- tiny
- base.en
- base
- small.en
- small
- medium.en  [default]
- medium
- large-v1
- large-v2
- large-v3
- large
- large-v3-turbo
- turbo

## Output files
the recoginzed mp3 files will be located at ./output_words folder

the unrecogized wav files will be located at ./output_segment folder
