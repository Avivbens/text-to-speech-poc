# OS imports
import certifi
import os

# Env
from dotenv import find_dotenv, load_dotenv

# AI
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

# Data manipulation
import soundfile as sf

# Set the REQUESTS_CA_BUNDLE environment variable to use the certifi bundle
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# load environment variables
load_dotenv(find_dotenv())

TARGET_FILE = "dist/output-rich.wav"
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


def query_model(text, description):
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        "parler-tts/parler_tts_mini_v0.1"
    ).to(DEVICE)

    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(DEVICE)
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(DEVICE)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    prepare_dist_folder()
    save_audio_from_speech(audio_arr, model.config.sampling_rate)


def prepare_dist_folder():
    dir_name = os.path.dirname(TARGET_FILE)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def save_audio_from_speech(audio_arr, samplerate):
    sf.write(TARGET_FILE, audio_arr, samplerate=samplerate)


def main():
    query_model(
        "Aviv Ben Shahar is a great guy!",
        "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast.",
    )


if __name__ == "__main__":
    main()
