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

# Support for GPU (requires an Intel based MacOS)
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
TARGET_FILE = "dist/output-rich.wav"

SYSTEM_DETAILS = list(
    {
        "A male speaker with a strong low voice. He talks very clearly with a bit higher tone, with very clear audio quality. Try to sound like a radio host or a podcast host. The speaker should sound like a professional speaker, with a clear and strong voice. Make the speed of his words a bit faster than normal, but not too fast.",
        "A cool male speaker with a strong low voice, in a very confined sounding environment with very clear audio quality. Try to sound like a radio host or a podcast host. The speaker should sound like a professional speaker, with a clear and strong voice.",
    }
)


def query_model(text, description):
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        "parler-tts/parler_tts_mini_v0.1"
    ).to(DEVICE)

    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(DEVICE)
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(DEVICE)

    generation = model.generate(
        input_ids=input_ids,
        prompt_input_ids=prompt_input_ids,
    )
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
        "Hello everyone! I am your virtual host for today, We're about to talk about the latest trends in AI and machine learning, Let's dive in! The following is a brief of the article you've asked me to read for you.",
        SYSTEM_DETAILS[1],
    )


if __name__ == "__main__":
    main()
