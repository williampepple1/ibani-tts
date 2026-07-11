# Ibani Text-to-Speech: Kaggle Guide

This guide will walk you through exactly how to run the data preparation script and start training the AI in Kaggle.

## Step 1: Prepare the Dataset

Create a new Kaggle Notebook. Make sure **Internet is ON** in your Kaggle Notebook settings.

### Cell 1: Download code and install tools
```bash
!git clone https://github.com/williampepple1/ibani-tts.git
!apt-get update && apt-get install -y ffmpeg
```

### Cell 2: Setup Python 3.10 Environment & Install libraries
Since Kaggle sometimes updates its default Python version, we will create a dedicated Python 3.10 environment to ensure compatibility with TTS.
```bash
%cd /kaggle/working/ibani-tts
!conda create -n tts_env python=3.10 -y
!conda run -n tts_env pip install -r requirements.txt
```

### Cell 3: Run the Auto-Tuning Slicer
This script will download your Ibani JSON and the MP3s from Cloudflare, and slice them into verses.
```bash
!conda run -n tts_env python kaggle_prep_script.py
```
*(If it skips a chapter, that's completely normal! It just means the audio pauses were too messy, and skipping it keeps the training data clean.)*

### Cell 4: Verify the output (Optional)
```bash
print("Total audio files generated:")
!ls -1 wavs | wc -l
```

## Step 2: Train the AI Voice (Coqui TTS)

Now that you have your `wavs` folder and `metadata.csv` ready, you can start training the AI!

### Cell 5: Install Coqui TTS
This takes a minute to download the deep learning packages.
```bash
!conda run -n tts_env pip install TTS
```

### Cell 6: Start Training!
Run the training script we prepared. 
```bash
!conda run -n tts_env python train_tts.py
```

### What happens next?
- The script will run for several hours.
- It will periodically save checkpoints of your AI in the `tts_train_dir` folder.
- You can listen to sample outputs in the `tts_train_dir/eval` folder as it learns!
