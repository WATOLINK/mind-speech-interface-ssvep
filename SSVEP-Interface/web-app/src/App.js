import "./App.css";
import { useState } from "react";
import { TextField, Button } from "@mui/material";

function App() {
  const [location, setLocation] = useState("");
  const [socket, setSocket] = useState(null);

  const connectClicked = () => {
    if (location === "") {
      var ip = document.getElementById("text-ip").value;
      var port = document.getElementById("text-port").value;
      try {
        var newSocket = new WebSocket(`ws://${ip}:${port}/`);
      } catch (err) {
        alert(`Connection Failed`);
      }

      newSocket.onopen = (e) => {
        setLocation(newSocket.url);
      };
      newSocket.onclose = (e) => {
        setLocation("");
        setSocket(null);
      };
      newSocket.onerror = (e) => {
        alert("Connection Failed");
      };

      setSocket(newSocket);
    } else {
      socket.send("disconnect");
      socket.close();
      setSocket(null);
    }
  };

  const promptClicked = () => {
    var prompt = document.getElementById("text-prompt").value;
    socket.send("prompt: " + prompt);
  };

  const micClicked = () => {
    var text = document.getElementById("text-prompt");
    // const texts = document.querySelector(".texts");

    // Focus the input field
    text.focus();

    var speech = true;
    window.SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new window.SpeechRecognition();
    recognition.interimResults = true;

    // let p = document.createElement("p");

    recognition.addEventListener("result", (e) => {
      const prompt = Array.from(e.results)
        .map((result) => result[0])
        .map((result) => result.transcript)
        .join("");

      //   p.innerText = prompt;
      text.value = prompt;

      console.log(prompt);
    });

    if (speech === true) {
      recognition.start();
    }
  };

  return (
    <div className="App">
      <div className="controls">
        <p className="status">Connected to: {location}</p>
        <div className="connection-location">
          <TextField id="text-ip" variant="standard" placeholder="IP" />
          <TextField id="text-port" placeholder="Port" variant="standard" />
        </div>
        <Button variant="outlined" onClick={connectClicked}>
          {location === "" ? "Connect" : "Disconnect"}
        </Button>

        <TextField
          id="text-prompt"
          // label="Prompt"
          placeholder="Prompt"
          variant="standard"
          fullWidth
          sx={{
            "& label.Mui-focused": {
              display: "none",
            },
          }}
        />

        <Button
          variant="outlined"
          onClick={promptClicked}
          disabled={location === "" ? true : undefined}
        >
          Send Prompt
        </Button>
        <Button variant="outlined" onClick={micClicked} id="mic-clicked">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 0 24 24"
            width="24"
            fill="#1976D2"
          >
            <path d="M0 0h24v24H0z" fill="none" />
            <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z" />
          </svg>
        </Button>
      </div>
    </div>
  );
}

export default App;
