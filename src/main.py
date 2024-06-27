# OS imports
import certifi
import os

# Env
from dotenv import find_dotenv, load_dotenv

# AI
from transformers import (
    SpeechT5Processor,
    SpeechT5ForTextToSpeech,
    SpeechT5HifiGan,
    set_seed,
)
import torch

# Data manipulation
import soundfile as sf
from datasets import load_dataset

# Set the REQUESTS_CA_BUNDLE environment variable to use the certifi bundle
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# load environment variables
load_dotenv(find_dotenv())


def query_model(text):
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    inputs = processor(text=text, return_tensors="pt")

    embeddings_dataset = load_dataset(
        "Matthijs/cmu-arctic-xvectors", split="validation"
    )
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    # embeddings_dataset = load_dataset(
    #     "blabble-io/libritts_r", "clean", split="train.clean.100"
    # )
    # speaker_embeddings = torch.tensor(embeddings_dataset["train.clean.100"]).unsqueeze(
    #     0
    # )

    set_seed(555)  # make deterministic

    # generate speech
    speech = model.generate(
        inputs["input_ids"], speaker_embeddings=speaker_embeddings, vocoder=vocoder
    )

    return speech


def save_audio(speech, filename):
    os.mkdir(os.path.dirname(filename))
    sf.write(filename, speech.numpy(), samplerate=16000)


def main():
    speech = query_model("Aviv Ben Shahar is a great guy!")
    save_audio(speech, "./dist/output.wav")


if __name__ == "__main__":
    main()
