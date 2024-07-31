import { useState } from "react";
import axios from "axios";

import "./Input.css";
import ModeMenu from "./ModeMenu.jsx";

export default function Input({ onConvert }) {
  const [selectedModeButtonIndex, setSelectedModeButtonIndex] = useState(0);
  const [inputURL, setInputURL] = useState("");
  const [inputHTML, setInputHTML] = useState("");

  const loadHTMLfromURL = async () => {
    const response = await axios.post("http://localhost:8080/load", {
      url: inputURL,
    });
    setInputHTML((await response).data.content);
  };

  function handleLoadButtonClick() {
    loadHTMLfromURL();
  }

  function handleConvertButtonClick() {
    onConvert(inputHTML);
  }

  function handleModeButtonClick(index) {
    setSelectedModeButtonIndex(index);
  }

  function handleURLInputChange(event) {
    setInputURL(event.target.value);
  }

  function handleHTMLInputChange(event) {
    setInputHTML(event.target.value);
  }

  const inputModes = ["Paste HTML", "Paste URL"];

  return (
    <>
      <ModeMenu
        buttons={inputModes.map((button, index) => (
          <button
            key={index}
            className={`menu-button ${
              selectedModeButtonIndex === index ? "selected" : ""
            }`}
            onClick={() => handleModeButtonClick(index)}
          >
            {button}
          </button>
        ))}
      ></ModeMenu>
      <div class="input">
        {selectedModeButtonIndex === 1 && (
          <>
            <input
              class="input-area"
              value={inputURL}
              onChange={handleURLInputChange}
            ></input>
            <button onClick={handleLoadButtonClick}>Load</button>
          </>
        )}
        <h3>Input HTML code here:</h3>
        <textarea
          class="input-output-boxes"
          value={inputHTML}
          onChange={handleHTMLInputChange}
        ></textarea>
      </div>
      <button onClick={handleConvertButtonClick}>Convert</button>
    </>
  );
}
