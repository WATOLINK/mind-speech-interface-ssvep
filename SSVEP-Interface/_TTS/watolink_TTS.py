#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import TTS
from pathlib import Path

import simpleaudio as sa
import os
import io

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

# Trainer: Where the ✨️ happens.
# TrainingArgs: Defines the set of arguments of the Trainer.
from trainer import Trainer, TrainerArgs

# GlowTTSConfig: all model related values for training, validating and testing.
from TTS.tts.configs.glow_tts_config import GlowTTSConfig

# BaseDatasetConfig: defines name, formatter and path of the dataset.
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.glow_tts import GlowTTS
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

class TTS_synthesizer:

    def __init__(self, model_name = "tts_models/en/ljspeech/tacotron2-DDC", vocoder_name = None,
                    config_path = None, model_path = None, use_cuda = False, vocoder_path = None, vocoder_config_path = None, encoder_path = None, encoder_config_path = None,
                    speakers_file_path = None, language_ids_file_path = None):
        """
        __init__() initializes the TTS_synthesizer with a TTS model, either pre-built by coqui or custom trained
        
        """
        # load model manager
        self.path = Path(TTS.__file__).parent / ".models.json"
        self.manager = ModelManager(self.path)

        self.model_path = None
        self.config_path = None
        self.speakers_file_path = None
        self.language_ids_file_path = None
        self.vocoder_path = None
        self.vocoder_config_path = None
        self.encoder_path = None
        self.encoder_config_path = None

        # load pre-trained model paths
        if model_name is not None and not model_path:
            self.model_path, self.config_path, self.model_item = self.manager.download_model(model_name)
            self.vocoder_name = self.model_item["default_vocoder"] if vocoder_name is None else vocoder_name

        if vocoder_name is not None and not vocoder_path:
            self.vocoder_path, self.vocoder_config_path, _ = self.manager.download_model(vocoder_name)

        # CASE4: set custom model paths
        if model_path is not None:
            self.model_path = model_path
            self.config_path = config_path
            self.speakers_file_path = speakers_file_path
            self.language_ids_file_path = language_ids_file_path

        if vocoder_path is not None:
            self.vocoder_path = vocoder_path
            self.vocoder_config_path = vocoder_config_path

        if encoder_path is not None:
            self.encoder_path = encoder_path
            self.encoder_config_path = encoder_config_path

        # load models
        self.synthesizer = Synthesizer(
            self.model_path,
            self.config_path,
            self.speakers_file_path,
            self.language_ids_file_path,
            self.vocoder_path,
            self.vocoder_config_path,
            self.encoder_path,
            self.encoder_config_path,
            use_cuda,
        )
    
    def list_models(self):
        """
        list_models(self) list pre-trained TTS models
        """
        self.manager.list_models()

    def synthesize( self,text = "hi my name is jeff", out_path = None,
                    speaker_idx = None, language_idx = None, speaker_wav = None, gst_style = None, capacitron_style_wav = None, capacitron_style_text = None, list_speaker_idxs = False, list_language_idxs = False,
                    save_spectogram = False, reference_wav = None, reference_speaker_idx = None
                    ):
        """
        synthesize() generates audio output for a string of text using the TTS model given to the TTS_synthesizer instance       
        
        text: type=str, default=None, help="Text to generate speech."

        Args for running pre-trained TTS models.
        model_name: type=str default="tts_models/en/ljspeech/tacotron2-DDC" help="Name of one of the pre-trained TTS models in format <language>/<dataset>/<model_name>"
        vocoder_name: type=str default=None help="Name of one of the pre-trained  vocoder models in format <language>/<dataset>/<model_name>"

        Args for running custom models
        config_path: default=None, type=str, help="Path to model config file."
        model_path: type=str, default=None, help="Path to model file."
        out_path: type=str default=None help="Output wav file path." if None, use file stream and do not write to storage
        use_cuda: type=bool, help="Run model on CUDA.", default=False
        vocoder_path: type=str help="Path to vocoder model file. If it is not defined, model uses GL as vocoder. Please make sure that you installed vocoder library before (WaveRNN)." default=None
        vocoder_config_path: type=str, help="Path to vocoder model config file.", default=None
        encoder_path: type=str help="Path to speaker encoder model file." default=None
        encoder_config_path: type=str, help="Path to speaker encoder config file.", default=None

        args for multi-speaker synthesis
        speakers_file_path: type=str, help="JSON file for multi-speaker model.", default=None
        language_ids_file_path: type=str, help="JSON file for multi-lingual model.", default=None
        speaker_idx: type=str help="Target speaker ID for a multi-speaker TTS model." default=None
        language_idx: type=str help="Target language ID for a multi-lingual TTS model." default=None
        speaker_wav: help="wav file(s) to condition a multi-speaker TTS model with a Speaker Encoder. You can give multiple file paths. The d_vectors is computed as their average." default=None
        gst_style: help="Wav path file for GST style reference.", default=None
        capacitron_style_wav: type=str, help="Wav path file for Capacitron prosody reference.", default=None
        capacitron_style_text: type=str, help="Transcription of the reference.", default=None
        list_speaker_idxs: help="List available speaker ids for the defined multi-speaker model." type=str2bool default=False
        list_language_idxs: help="List available language ids for the defined multi-lingual model.", type=str2bool, default=False

        aux args
        save_spectogram: type=bool help="If true save raw spectogram for further (vocoder) processing in out_path." default=False
        reference_wav: type=str help="Reference wav file to convert in the voice of the speaker_idx or speaker_wav" default=None
        reference_speaker_idx: type=str help="speaker ID of the reference_wav speaker (If not provided the embedding will be computed using the Speaker Encoder)." default=None
        """

        # query speaker ids of a multi-speaker model.
        if list_speaker_idxs:
            print(
                " > Available speaker ids: (Set --speaker_idx flag to one of these values to use the multi-speaker model."
            )
            print(self.synthesizer.tts_model.speaker_manager.ids)
            return

        # query langauge ids of a multi-lingual model.
        if list_language_idxs:
            print(
                " > Available language ids: (Set --language_idx flag to one of these values to use the multi-lingual model."
            )
            print(self.synthesizer.tts_model.language_manager.ids)
            return

        # check the arguments against a multi-speaker model.
        if self.synthesizer.tts_speakers_file and (not speaker_idx and not speaker_wav):
            print(
                " [!] Looks like you use a multi-speaker model. Define `--speaker_idx` to "
                "select the target speaker. You can list the available speakers for this model by `--list_speaker_idxs`."
            )
            return

        # RUN THE SYNTHESIS
        if text:
            print(" > Text: {}".format(text))

        # kick it
        wav = self.synthesizer.tts(
            text,
            speaker_idx,
            language_idx,
            speaker_wav,
            reference_wav=reference_wav,
            style_wav=capacitron_style_wav,
            style_text=capacitron_style_text,
            reference_speaker_name=reference_speaker_idx,
        )

        if out_path == None:
            out_path = io.BytesIO()

        # save the results
        print(" > Saving output to {}".format(out_path))
        self.synthesizer.save_wav(wav, out_path)

        # play sound in realtime
        wave_obj = sa.WaveObject.from_wave_file(out_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

        # os.remove(out_path) # delete temp audio file
    
    @staticmethod
    def train_glowTTS(name="LJSpeech", meta_file_train="metadata.csv",
                      output_path = os.path.dirname(os.path.abspath(__file__)),
                      input_path= os.path.join(os.path.dirname(os.path.abspath(__file__)), "LJSpeech-1.1/")):
        """
        train_glowTTS(name, meta_file_train, output_path, input_path) trains and outputs a TTS model
        using the glowTTS model. *name specifies the name of the formatter they use, so it's important
        Requires: dataset must be present at input_path with a meta_file ready for training
        """

        # DEFINE DATASET CONFIG
        # Set LJSpeech as our target dataset and define its path.
        # You can also use a simple Dict to define the dataset and pass it to your custom formatter.
        dataset_config = BaseDatasetConfig(
            name=name, meta_file_train=meta_file_train, path=input_path
        )

        # INITIALIZE THE TRAINING CONFIGURATION
        # Configure the model. Every config class inherits the BaseTTSConfig.
        config = GlowTTSConfig(
            batch_size=32,
            eval_batch_size=16,
            num_loader_workers=4,
            num_eval_loader_workers=4,
            run_eval=True,
            test_delay_epochs=-1,
            epochs=2,
            text_cleaner="phoneme_cleaners",
            use_phonemes=True,
            phoneme_language="en-us",
            phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
            print_step=25,
            print_eval=False,
            mixed_precision=True,
            output_path=output_path,
            datasets=[dataset_config],
        )

        # INITIALIZE THE AUDIO PROCESSOR
        # Audio processor is used for feature extraction and audio I/O.
        # It mainly serves to the dataloader and the training loggers.
        ap = AudioProcessor.init_from_config(config)

        # INITIALIZE THE TOKENIZER
        # Tokenizer is used to convert text to sequences of token IDs.
        # If characters are not defined in the config, default characters are passed to the config
        tokenizer, config = TTSTokenizer.init_from_config(config)

        # LOAD DATA SAMPLES
        # Each sample is a list of ```[text, audio_file_path, speaker_name]```
        # You can define your custom sample loader returning the list of samples.
        # Or define your custom formatter and pass it to the `load_tts_samples`.
        # Check `TTS.tts.datasets.load_tts_samples` for more details.
        train_samples, eval_samples = load_tts_samples(
            dataset_config,
            eval_split=True,
            eval_split_max_size=config.eval_split_max_size,
            eval_split_size=config.eval_split_size
        )

        # INITIALIZE THE MODEL
        # Models take a config object and a speaker manager as input
        # Config defines the details of the model like the number of layers, the size of the embedding, etc.
        # Speaker manager is used by multi-speaker models.
        model = GlowTTS(config, ap, tokenizer, speaker_manager=None)

        # INITIALIZE THE TRAINER
        # Trainer provides a generic API to train all the 🐸TTS models with all its perks like mixed-precision training,
        # distributed training, etc.
        trainer = Trainer(
            TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples
        )

        # AND... 3,2,1... 🚀
        trainer.fit()
    
    @staticmethod
    def get_newest_model(model_output_path):
        """
        get_newest_model(model_output_path) produces path to folder of newest model, false
        if no model exists
        get_newest_model: Str -> Str or Bool
        Requires: model_output_path is a valid path
        """
        for root, dirs, files in os.walk(model_output_path):
            trained_dirs = [x for x in dirs if x.startswith("run-")]
            if len(trained_dirs) > 0:
                new_path = trained_dirs[0]
                for name in trained_dirs:
                    if os.path.exists(os.path.join(root, name + "/best_model.pth")) and os.path.getmtime(os.path.join(root, name + "/")) >= os.path.getmtime(new_path):
                        new_path = os.path.join(root, name + "/")
                return new_path
        return False