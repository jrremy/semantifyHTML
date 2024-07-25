import { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";

function App() {
  const [selectedModeButtonIndex, setSelectedModeButtonIndex] = useState(0);
  const [outputHTML, setOutputHTML] = useState("");
  const [inputHTML, setInputHTML] = useState("");

  const fetchSemanticHTML = async () => {
    const response = await axios.post("http://localhost:8080/convert", {
      html: inputHTML,
    });
    setOutputHTML((await response).data.semantic);
  };

  function handleConvertButtonClick() {
    fetchSemanticHTML();
  }

  function handleModeButtonClick(index) {
    setSelectedModeButtonIndex(index);
  }

  function handleInputChange(event) {
    setInputHTML(event.target.value);
  }

  const inputModes = ["Paste HTML", "Paste URL"];

  return (
    <>
      <div className="menu-container">
        <menu>
          {inputModes.map((button, index) => (
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
        </menu>
      </div>
      <div class="input-area">
        <h3>Input HTML code here:</h3>
        <textarea
          class="input-output-boxes"
          value={inputHTML}
          onChange={handleInputChange}
        ></textarea>
      </div>
      <button onClick={handleConvertButtonClick}>Convert</button>
      <div class="output-area">
        <h3>Converted Semantic HTML:</h3>
        <textarea class="input-output-boxes" value={outputHTML}></textarea>
      </div>
    </>
  );
}

export default App;
