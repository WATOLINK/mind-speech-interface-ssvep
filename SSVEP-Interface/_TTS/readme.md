# Watolink_TTS
Watolink_TTS is a class that provides methods to train and use a coqui AI TTS model
# Notes:
1. !!! run with python38 since coqui is only installed in python 3.8
2. relevant doc info: https://tts.readthedocs.io/en/latest/inference.html
3. adapted from synthesize.py: https://github.com/coqui-ai/TTS/blob/dev/TTS/bin/synthesize.py
4. a simpler implementation: https://github.com/coqui-ai/TTS/discussions/864
5. install pytorch with cuda if training is not using GPU

# Installation
1. install Visual Studio C++ build tools, select "Desktop development with C++"
2. pip install TTS
3. pip install simpleaudio
4. Download prebuilt TTS model for coqui AI in the CLI

    tts --text "Text for TTS" --model_name "tts_models/en/ljspeech/tacotron2-DDC"
5. if encountering install errors, such as "ERROR: Invalid requirement: 'simpleaudio\x83", try the following:

    pip install -U pip
    pip uninstall setuptools
    pip install 'setuptools<20.2'


# Example usage:
First, import everything from watolink_TTS

    from watolink_TTS import *
    path = os.path.dirname(os.path.abspath(__file__))

Then, optionally, you can train your custom TTS model to a specified path. Otherwise, you can use a pre-built model from coqui

    TTS_synthesizer.train_glowTTS(name="LJSpeech", meta_file_train="metadata.csv",
                        output_path = path,
                        input_path= os.path.join(path, "LJSpeech-1.1/"))

Then, initialize a TTS_synthesizer using a model

    # Use pre-built model:
    jj = TTS_synthesizer(model_name = "tts_models/en/ljspeech/tacotron2-DDC")

or...

    # Use custom trained model:
    newest_model_path = TTS_synthesizer.get_newest_model(path)
    jj = TTS_synthesizer(config_path = newest_model_path + "config.json", model_path = newest_model_path + "best_model.pth")

Lastly, you generate speech from text by simply calling the synthesize() method:

    # audio is generated and delete in realtime if not specify out_path
    jj.synthesize(text = "dame dane")
    
    # specify out_path to save audio to storage
    jj.synthesize(text = "hi my name is jeff", out_path = "jeff.wav")
    jj.synthesize(text = "pee pee poo poo girl", out_path = "watolink_meme.wav")
    jj.synthesize(text = "omae wa mo shindeiru", out_path = "watolink_meme.wav")
