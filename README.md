# mind-speech-interface-ssvep
Mind-Speech Interface for NeuroTechX Student Clubs Competition 2022

## Requirements

To install requirements, make sure you have Python 3.8 or older installed, then run

    pip install -r requirements.txt

Make sure to run the command from the base directory (mind-speech-interface-ssvep) of the Git repo

## CCAKNN Model Training

## Online SSVEP Interface

    cd mind-speech-interface-ssvep

for synthetic board:

    python EEG-DATA-Pipeline/Data_Streamer.py --board-id=-1 --model-path=eeg-ai-layer\modelname.model

for non synthetic board:

    python EEG-DATA-Pipeline/Data_Streamer.py --model-path=eeg-ai-layer\modelname.model

## Offline SSVEP Data Collection 

To run the offline data-collection demo, copy and paste the following command.

    cd mind-speech-interface-ssvep
    
for openBCI

    python ODC-DEMO/4_stim_demo.py --board-id=0 --serial-port=deviceserialport
    
for gTec

    python ODC-DEMO/4_stim_demo.py --board-id=8 --serial-port=deviceserialport
    
## Offline SSVEP Data Analysis 
To visualize the csv created from data collection, in your terminal run:
    jupyter notebook

Then in the browser window navigate to the notebook under EEG-Data-Visualization:

<img width="408" alt="Screen Shot 2022-07-05 at 5 00 37 PM" src="https://user-images.githubusercontent.com/34819737/177415768-4630ae1e-c9fb-4b94-b82f-02cc252556d5.png">

Insert the csv name of the recording you want to visualize in this section:

<img width="715" alt="Screen Shot 2022-07-05 at 5 26 53 PM" src="https://user-images.githubusercontent.com/34819737/177419300-542e8df2-8f5a-4344-a61d-9f73770efc00.png">

Then click:

<img width="423" alt="Screen Shot 2022-07-05 at 4 55 10 PM" src="https://user-images.githubusercontent.com/34819737/177414726-94eec197-3778-4231-90ac-487477b04ebf.png">

And averaged FFT plots of every stimuli response for each electrode will appear at the bottom and look like this:

<img width="654" alt="Screen Shot 2022-07-05 at 4 58 29 PM" src="https://user-images.githubusercontent.com/34819737/177415446-e1ec3b81-8d0d-49e0-97e5-822074659387.png">


