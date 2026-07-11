import os
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

output_path = "tts_train_dir"
os.makedirs(output_path, exist_ok=True)

dataset_config = BaseDatasetConfig(
    formatter="ljspeech", 
    meta_file_train="metadata.csv", 
    path=os.getcwd()
)

config = VitsConfig(
    audio=dict(sample_rate=22050, resample=True),
    run_name="vits_ibani",
    batch_size=16,
    eval_batch_size=8,
    batch_group_size=4,
    num_loader_workers=2,
    num_eval_loader_workers=2,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    text_cleaner="basic_cleaners",
    use_phonemes=False, # No Ibani phoneme dict exists, use characters
    phoneme_language=None,
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    compute_input_seq_cache=True,
    print_step=25,
    print_eval=True,
    mixed_precision=True,
    output_path=output_path,
    datasets=[dataset_config],
)

# Initialize Audio Processor & Tokenizer
ap = AudioProcessor.init_from_config(config)
tokenizer, config = TTSTokenizer.init_from_config(config)

# Load data
train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
)

# Initialize Model
model = Vits(config, ap, tokenizer, speaker_manager=None)

# Initialize Trainer
trainer = Trainer(
    TrainerArgs(),
    config,
    output_path,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
)

# Start Training
trainer.fit()
