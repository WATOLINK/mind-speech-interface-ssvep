import './App.css';
import { useState } from 'react';
import { TextField, Button } from '@mui/material';

function App() {
    const [ location, setLocation ] = useState('');
    const [ socket, setSocket ] = useState(null);

    const connectClicked = () => {
        if (location === "") {
            var ip = document.getElementById("text-ip").value;
            var port = document.getElementById("text-port").value;
            try {
                var newSocket = new WebSocket(`ws://${ip}:${port}/`);
            } catch (err) {
                alert(`Connection Failed`)
            }

            newSocket.onopen = e => {
                setLocation(newSocket.url);
            };
            newSocket.onclose = e => {
                setLocation("");
                setSocket(null);
            };
            newSocket.onerror = e => {
                alert("Connection Failed");
            };

            setSocket(newSocket);
        } else {
            socket.send("disconnect");
            socket.close();
            setSocket(null);
        }
    }

    const promptClicked = () => {
        var prompt = document.getElementById("text-prompt").value;
        socket.send("prompt: " + prompt);
    }

    return (
        <div className="App">
            <div className="controls">
                <p className='status'>Connected to: { location }</p>
                <div className="connection-location">
                    <TextField id="text-ip" label="IP" variant="standard" />
                    <TextField id="text-port" label="Port" variant="standard" />
                </div>
                <Button variant="outlined" onClick={ connectClicked }>{ location === '' ? 'Connect' : 'Disconnect' }</Button>
                <TextField id="text-prompt" label="Prompt" variant="standard" fullWidth />
                <Button variant="outlined" onClick={ promptClicked } disabled={ location === '' ? true : undefined }>Send Prompt</Button>
            </div>
        </div>
    );
}

export default App;
