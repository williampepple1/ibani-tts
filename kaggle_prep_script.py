import requests
import json
import os
import csv
from pydub import AudioSegment
from pydub.silence import split_on_silence

# --- CONFIGURATION ---
BASE_URL = "https://ibani.online"
JSON_URL = "https://raw.githubusercontent.com/williampepple1/ibani-translator/main/ibani_eng.json"

RAW_DIR = "raw_audio_chapters"
WAV_DIR = "wavs"
METADATA_FILE = "metadata.csv"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(WAV_DIR, exist_ok=True)

book_index_map = {
    "MAT": 40, "MRK": 41, "LUK": 42, "JHN": 43,
    "ACT": 44, "ROM": 45, "1CO": 46, "2CO": 47,
    "GAL": 48, "EPH": 49, "PHP": 50, "COL": 51,
    "1TH": 52, "2TH": 53, "1TI": 54, "2TI": 55,
    "TIT": 56, "PHM": 57, "HEB": 58, "JAS": 59,
    "1PE": 60, "2PE": 61, "1JN": 62, "2JN": 63,
    "3JN": 64, "JUD": 65, "REV": 66
}

# 1. Download JSON
print("Downloading Ibani JSON Text...")
response = requests.get(JSON_URL)
verses_data = response.json()

# Group verses by chapter
chapters_data = {}
for verse in verses_data:
    book = verse.get("book")
    chapter = int(verse.get("chapter", 0))
    if book not in chapters_data:
        chapters_data[book] = {}
    if chapter not in chapters_data[book]:
        chapters_data[book][chapter] = []
    
    chapters_data[book][chapter].append(verse)

metadata_records = []

# 2. Process Each Chapter
print("Starting Download and Audio Slicing...")

for book_code, chapters in chapters_data.items():
    if book_code not in book_index_map:
        continue
        
    b_num = str(book_index_map[book_code]).zfill(2)
    
    for ch_num, verses in chapters.items():
        c_num = str(ch_num).zfill(3)
        file_name = f"IBYLSTN2DA_B{b_num}_{book_code}_{c_num}.mp3"
        audio_url = f"{BASE_URL}/{file_name}"
        save_path = os.path.join(RAW_DIR, file_name)
        
        # Download if we don't have it yet
        if not os.path.exists(save_path):
            print(f"Downloading {file_name}...")
            r = requests.get(audio_url)
            if r.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(r.content)
            else:
                print(f"  -> Failed to download. Skipping {book_code} Ch {ch_num}")
                continue
                
        # 3. Slice Audio on Silence
        print(f"Slicing {file_name} into verses...")
        try:
            audio = AudioSegment.from_mp3(save_path)
            # You might need to tweak min_silence_len (in ms) and silence_thresh (in dBFS)
            # based on how the narrator speaks. 
            audio_chunks = split_on_silence(
                audio, 
                min_silence_len=1000, # 1 second of silence triggers a split
                silence_thresh=-40    # Silence is anything quieter than -40dB
            )
            
            # Check if chunks roughly match verse count
            if len(audio_chunks) == len(verses):
                print(f"  -> Perfect match! {len(audio_chunks)} audio chunks for {len(verses)} verses.")
            else:
                print(f"  -> WARNING: Found {len(audio_chunks)} audio chunks but expected {len(verses)} verses. You may need to manually review this chapter.")
            
            # 4. Save individual WAVs and build Metadata
            # We map up to whichever is smaller (chunks or verses) to avoid errors
            limit = min(len(audio_chunks), len(verses))
            
            for i in range(limit):
                verse_obj = verses[i]
                chunk = audio_chunks[i]
                
                v_num = verse_obj.get("verse")
                ibani_text = verse_obj.get("ibani_text", "").strip()
                
                # Format: MAT_1_8.wav
                wav_filename = f"{book_code}_{ch_num}_{v_num}.wav"
                wav_filepath = os.path.join(WAV_DIR, wav_filename)
                
                # Export chunk as standard TTS format (Mono, 22050Hz)
                chunk = chunk.set_frame_rate(22050).set_channels(1)
                chunk.export(wav_filepath, format="wav")
                
                # Add to metadata: filename|text
                metadata_records.append([wav_filename, ibani_text])
                
        except Exception as e:
            print(f"  -> Error slicing {file_name}: {e}")

# 5. Write metadata.csv (LJSpeech standard format)
print("\nWriting metadata.csv...")
with open(METADATA_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="|")
    for record in metadata_records:
        writer.writerow(record)
        
print("🎉 ALL DONE! Your dataset is ready in the 'wavs' folder with 'metadata.csv'.")
