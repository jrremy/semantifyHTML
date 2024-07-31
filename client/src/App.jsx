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
      <Input onConvert={fetchSemanticHTML}/>
      <div class="output-area">
        <h3>Converted Semantic HTML:</h3>
        <textarea class="input-output-boxes" value={outputHTML}></textarea>
      </div>
    </>
  );
}

export default App;
