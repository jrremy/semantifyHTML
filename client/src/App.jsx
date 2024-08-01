import { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Input from "./components/Input.jsx";

function App() {
  const [outputHTML, setOutputHTML] = useState("");

  const fetchSemanticHTML = async (inputHTML) => {
    const response = await axios.post("http://localhost:8080/convert", {
      html: inputHTML,
    });
    setOutputHTML((await response).data.semantic);
  };

  return (
    <>
      <div className="input-output-container">
        <Input onConvert={fetchSemanticHTML} />
        <div className="output-area">
          <h3>Converted Semantic HTML:</h3>
          <textarea className="input-output-boxes" value={outputHTML}></textarea>
        </div>
      </div>
    </>
  );
}

export default App;
