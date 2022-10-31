# mind-speech-interface-ssvep
Mind-Speech Interface for NeuroTechX Student Clubs Competition 2022

This repository includes offline data collection and analysis tools for SSVEP, trainable models for SSVEP prediction, as well as an SSVEP text/speech interface.

Platform Support: Currently our tools support Windows 10 and up. MacOS is technically supported but is not recommended. For Mac devices with ARM SOCs (M1, M2 etc) you will need to run our tools in a Rosetta emulated terminal.

## Credit
Some of our models and signal processing methods were adapted from the following repositories: 
- https://github.com/aaravindravi/Brain-computer-interfaces
- https://github.com/eugeneALU/CECNL_RealTimeBCI

## Requirements

To install requirements, make sure you have Python 3.10+ installed, then run
```python
pip install -r requirements.txt
```
Make sure to run the command from the base directory (mind-speech-interface-ssvep) of the Git repo

## General Hardware Setup

Our software tools support the OpenBCI Cyton board as well as the gtec Unicorn Hybrid for EEG data capturing.   

When setting up the device please make sure the channel numbers correspond to the following 10-20 electrode locations.
Note that this image is viewed as if you were looking at the back of someone's head.

![image](https://user-images.githubusercontent.com/34819737/178824314-7b1296b8-cdd2-424b-86ef-b65fec7e2d6e.png)

# OFFLINE SSVEP BCI 

## Offline SSVEP Data Collection 

To run the offline data-collection demo, copy and paste the following commands:
```python
cd mind-speech-interface-ssvep
```

If you are using the OpenBCI with active electrodes you need to set the gain of the amplifier to work with them. To do this, follow the readme here:
```python
cd cyton-active-electrode-gain-set
```

Regardless of if you are or are not using active electrodes, continue here:
```python
cd SSVEP-Data-Collection
```

NOTE: SSVEP-Data-Collection/configs.py --> open this file in a text editor and ensure the NUM_STIMS value is set to your desired # of stimuli (4 or 6 or 8), then save and exit.

Now you should be able to run the data collection tool!

for openBCI 
```python
python run_demo.py --board-id=0 --serial-port=deviceserialport
```
for gTec
```python
python run_demo.py --board-id=8 
```
Note for using the OpenBCI: to find your device serial port, either look in you device settings (windows) or if using a mac type this in the terminal:

    ls /dev/cu.*


## Offline SSVEP Data Analysis 
To visualize the csv created from data collection, in your terminal run:
```python
jupyter notebook
```
Then in the browser window navigate to the notebook under EEG-Data-Visualization:

<img width="408" alt="Screen Shot 2022-07-05 at 5 00 37 PM" src="https://user-images.githubusercontent.com/34819737/177415768-4630ae1e-c9fb-4b94-b82f-02cc252556d5.png">

Insert the csv name of the recording you want to visualize in this section:

<img width="715" alt="Screen Shot 2022-07-05 at 5 26 53 PM" src="https://user-images.githubusercontent.com/34819737/177419300-542e8df2-8f5a-4344-a61d-9f73770efc00.png">

Then click:

<img width="423" alt="Screen Shot 2022-07-05 at 4 55 10 PM" src="https://user-images.githubusercontent.com/34819737/177414726-94eec197-3778-4231-90ac-487477b04ebf.png">

And averaged FFT plots of every stimuli response for each electrode will appear at the bottom and look like this:

<img width="654" alt="Screen Shot 2022-07-05 at 4 58 29 PM" src="https://user-images.githubusercontent.com/34819737/177415446-e1ec3b81-8d0d-49e0-97e5-822074659387.png">

## FBCCA-KNN Model Training/Testing

Training models is relatively simple using the training script! 

The only default parameters to pass would be:

- data: The path to your data. The data path can be a folder of folders of csvs or a path to the csv itself. Both should be fine.
- output-path: The directory where a model will be saved.
- output-name: The name of the saved model.
- model-type: Specify the type of model to train here.
- window-length: Window length of example taken from particular trial.
- shift-length: Shift between example windows.

The window and shift lengths exist to allow us to manufacture more unique examples the KNN can train on.

There are some handy flags:
- train: Whether to train a model
- eval: Whether to evaluate model using train/test split.
- verbose: Whether to output metrics information like accuracy and a confusion matrix to the terminal.

To train a FBCCA-KNN model, navigate to `mind-speech-interface-ssvep/` and run

```python
python -m eeg_ai_layer.models.train --data=<YOUR_DATA_PATH> --train --output-path=<YOUR_MODEL_OUTPUT_PATH> --output-name=<YOUR_MODEL_NAME> --model-type=fbcca_knn --shift-length=<SECONDS> --window-length=<SECONDS> --no-zero
```

If you'd like to see some metrics, pass the `--verbose` flag like so:

```python
python -m eeg_ai_layer.models.train --data=<YOUR_DATA_PATH> --train --output-path=<YOUR_MODEL_OUTPUT_PATH> --output-name=<YOUR_MODEL_NAME> --model-type=fbcca_knn --shift-length=<SECONDS> --window-length=<SECONDS> --no-zero --verbose 
```

# ONLINE SSVEP BCI 

## GPT-3 API Key Setup
In order to use GPT-3, create a ```.env``` file within the mind-speech-interface-ssvep folder. 

Within this document create a variable called ```OPENAI_KEY```, and set it to your OpenAI API key. Ensure that the key is in quotation marks.

Now, GPT-3 should work with the SSVEP GUI!

## Twitter API Key Setup
To use the twitter api refer to the readme in "mind-speech-interface-ssvep/SSVEP-Interface/server/".

## Text To Speech Setup
Please follow the readme in "mind-speech-interface-ssvep/SSVEP-Interface/_TTS/".

This feature allows you to train a voice model on samples of your own voice to use with the interface. It is not required for operation of the GUI.

## Speech To Text WebApp for Prompt Input 
Please follow the readme in "mind-speech-interface-ssvep/SSVEP-Interface/web-app/".

## Online SSVEP Interface
After ensuring GPT-3, Twitter, and TTS features are setup, you will be ready to run our fully integrated SSVEP interface, copy and paste the following commands:

```python
cd mind-speech-interface-ssvep
```
for synthetic board:
```python
python SSVEP-Interface/Data_Streamer.py --board-id=-1 --model-type=fbcca

# Alternatively
python SSVEP-Interface/Data_Streamer.py --board-id=-1 --model-type=fbcca_knn --model-path=eeg-ai-layer\models\savedmodels\modelname.model
```
for non synthetic board (our online system auto-detects board-id and serial-port):
```python
python SSVEP-Interface/Data_Streamer.py --model-type=fbcca

# Alternatively
python SSVEP-Interface/Data_Streamer.py  --model-type=fbcca_knn --model-path=eeg-ai-layer\models\savedmodels\modelname.model
```

Note: If you are using the OpenBCI with active electrodes with the online interface, please follow the steps to change the gain mentioned in the offline setup earlier before running the online interface.
