import { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";

function App() {
  const [outputHTML, setOutputHTML] = useState("");
  const [inputHTML, setInputHTML] = useState("");

  const fetchSemanticHTML = async () => {
    const response = await axios.post("http://localhost:8080/convert", {
      html: inputHTML,
    });
    setOutputHTML((await response).data.semantic);
  };

  function handleClick() {
    fetchSemanticHTML();
  }

  function handleInputChange(event) {
    setInputHTML(event.target.value);
  }

  /*useEffect(() => {
    
  }, []);*/

  return (
    <>
      <div class="input-area">
        <h3>Input HTML code here:</h3>
        <textarea class="input-output-boxes" value={inputHTML} onChange={handleInputChange}></textarea>
      </div>
      <button onClick={handleClick}>Convert</button>
      <div class="output-area">
        <h3>Converted Semantic HTML:</h3>
        <textarea class="input-output-boxes" value={outputHTML}></textarea>
      </div>
    </>
  );
}

export default App;
