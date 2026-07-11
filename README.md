# Ibani Text-to-Speech (TTS) Models

This repository is dedicated to preparing datasets and training Text-to-Speech (TTS) models for the Ibani language.
It is kept separate from the text translation models to prevent Python dependency conflicts between audio libraries and text libraries.

## Data Preparation on Kaggle

Since the Ibani audio dataset consists of chapter-level MP3s hosted on Cloudflare, the audio needs to be split into verse-level chunks to train a TTS model.

1. Create a Kaggle Notebook with a GPU (e.g., T4 x2) and Internet enabled.
2. Upload or copy the contents of `kaggle_prep_script.py` into a Kaggle cell.
3. Run the script to automatically:
   - Download the `ibani_eng.json` text data.
   - Download the Chapter MP3s from the Cloudflare bucket.
   - Slice the audio based on silent pauses between verses.
   - Generate the required `metadata.csv`.

## Requirements

The `requirements.txt` is specifically for local audio preparation if you choose to run it locally. For training, a completely different set of TTS libraries (like Coqui-TTS) will be required.
