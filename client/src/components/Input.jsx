import { useState, useRef } from "react";
import axios from "axios";
import PulseLoader from "react-spinners/PulseLoader";

import "./Input.css";
import ModeMenu from "./ModeMenu.jsx";

export default function Input({ onConvert, loadingConvert }) {
  const [inputMode, setinputMode] = useState("Paste HTML");
  const [inputURL, setInputURL] = useState("");
  const [loadingURL, setLoadingURL] = useState(false);
  const [inputHTML, setInputHTML] = useState("");

  const fileInputRef = useRef(null);

  const loadHTMLfromURL = async () => {
    setLoadingURL(true);
    try {
      const response = await axios.post("http://localhost:8080/load", {
        url: inputURL,
      });
      setInputHTML((await response).data.content);
    } catch (error) {
      console.error("Error fetching HTML from URL:", error);
      alert("Please enter a valid URL.");
    } finally {
      setLoadingURL(false);
    }
  };

  function handleLoadButtonClick() {
    loadHTMLfromURL();
  }

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file && file.type === "text/html") {
      const reader = new FileReader();
      reader.onload = () => {
        setInputHTML(reader.result); // Set the file content to state
      };
      reader.readAsText(file);
    } else {
      alert("Please upload a valid HTML file.");
    }
  }

  function handleFileButton() {
    fileInputRef.current.click();
  }

  function handleConvertButtonClick() {
    onConvert(inputHTML);
  }

  function handleModeButtonClick(mode) {
    setinputMode(mode);
  }

  function handleURLInputChange(event) {
    setInputURL(event.target.value);
  }

  function handleHTMLInputChange(event) {
    setInputHTML(event.target.value);
  }

  const inputModes = ["Paste HTML", "Paste URL", "Import File"];

  return (
    <>
      <div className="input-box">
        <ModeMenu
          modes={inputModes}
          activeMode={inputMode}
          onSwitch={handleModeButtonClick}
        ></ModeMenu>
        {inputMode === "Paste URL" && (
          <>
            <div className="url-container">
              <div className="url-enter">
                <input
                  placeholder="Enter a URL to extract HTML from"
                  value={inputURL}
                  onChange={handleURLInputChange}
                ></input>
                <button onClick={handleLoadButtonClick}>Load</button>
              </div>
              <PulseLoader
                id="url-pulse-loader"
                size={10}
                color="white"
                speedMultiplier={1.5}
                loading={loadingURL}
              />
            </div>
          </>
        )}
        {inputMode === "Import File" && (
          <>
            <div className="import-file">
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: "none" }}
                onChange={handleFileChange}
              ></input>
              <button onClick={handleFileButton}>Choose File</button>
            </div>
          </>
        )}
        <h3>Input HTML</h3>
        <textarea
          className="input-output"
          value={inputHTML}
          onChange={handleHTMLInputChange}
          placeholder="Enter Your HTML"
        ></textarea>

        <div className="convert-container">
          <button onClick={handleConvertButtonClick}>Convert</button>
          <PulseLoader
            id="convert-pulse-loader"
            size={10}
            color="white"
            speedMultiplier={1.5}
            loading={loadingConvert}
          />
        </div>
      </div>
    </>
  );
}
