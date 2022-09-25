from watolink_TTS import *

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    # TTS_synthesizer.train_glowTTS(name="LJSpeech", meta_file_train="metadata.csv",
    #                   output_path = path,
    #                   input_path= os.path.join(path, "LJSpeech-1.1/"))
    # jj = TTS_synthesizer(model_name = "tts_models/en/ljspeech/tacotron2-DDC")
    newest_model_path = TTS_synthesizer.get_newest_model(path)
    jj = TTS_synthesizer(config_path = newest_model_path + "config.json", model_path = newest_model_path + "best_model.pth")
    jj.synthesize(text = "omae wa mo shindeiru")
    jj.synthesize(text = "dame dane")
    jj.synthesize(text = "hi my name is jeff", out_path = "jeff.wav")
    jj.synthesize(text = "pee pee poo poo girl", out_path = "watolink_meme.wav")
    jj.synthesize(text = "omae wa mo shindeiru", out_path = "watolink_meme.wav")