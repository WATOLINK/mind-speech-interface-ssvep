# mind-speech-interface-ssvep
Mind-Speech Interface for NeuroTechX Student Clubs Competition 2022

To install requirements, make sure you have Python 3.8 or older installed, then run

    pip install -r requirements.txt

Make sure to run the command from the base directory (mind-speech-interface-ssvep) of the Git repo

## Offline SSVEP Data Collection 
To run the offline data-collection demo, copy and paste the following command.

    cd mind-speech-interface-ssvep
    python ODC-DEMO/demo.py --board-id=0 --serial-port=COM3
    
## Offline SSVEP Data Analysis 
To visualize the csv created from data collection, in your terminal run:
    jupyter notebook

Then in the browser window navigate to the notebook under EEG-Data-Visualization 
<img width="477" alt="Screen Shot 2022-07-05 at 4 53 51 PM" src="https://user-images.githubusercontent.com/34819737/177414540-edf62736-326a-48ba-95f2-836d0600ce0f.png">
Insert the csv name of the one you want to visualize in that section ^

Then click:
<img width="423" alt="Screen Shot 2022-07-05 at 4 55 10 PM" src="https://user-images.githubusercontent.com/34819737/177414726-94eec197-3778-4231-90ac-487477b04ebf.png">

And averaged FFT plots of every stimuli response for each electrode will appear at the bottom and look like this:
<img width="654" alt="Screen Shot 2022-07-05 at 4 58 29 PM" src="https://user-images.githubusercontent.com/34819737/177415446-e1ec3b81-8d0d-49e0-97e5-822074659387.png">


