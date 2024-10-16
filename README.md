# pt-audio-splitter
## Installation
```sh
pip install -r requirements.txt
```

## How to use the script
1. put the source audio as wav file in ./source folder
2. in process.py modify the source file name
```python
audio = AudioSegment.from_wav(f"{project_folder}/source/raw_audio_1.wav")
```
3. run the script
```sh
./process.py
```

## Output files
the recoginzed mp3 files will be located at ./output_words folder

the unrecogized wav files will be located at ./output_segment folder
