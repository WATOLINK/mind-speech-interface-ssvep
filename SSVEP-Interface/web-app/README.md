### Setup

1. Make sure you have node installed https://nodejs.org/en/download/
2. Make sure the following python packages are installed\
    `pip install websockets`\
    `pip install asyncio`
3. Install the required node modules using npm\
    `cd SSVEP-Interface/web-app/`\
    `npm install`

### Running the Web App

Note: The python app and web app are completely separate, they should both run simultaneously on the same device in different terminal windows

1. Make sure that all devices are on the same network (hotspot preferred, eduroam is funky)
3. Start the python app
3. Start the web app\
    `cd SSVEP-Interface/web-app/`\
    `npm start`
4. The web app terminal window provides an `ip:port` address, open it using any browser on a device that's on the same network
5. To connect to the python app, enter the same ip as the url and use port 8765
