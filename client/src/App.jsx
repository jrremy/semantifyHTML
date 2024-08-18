import { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Input from "./components/Input.jsx";
import Output from "./components/Output.jsx";

function App() {
  const [outputHTML, setOutputHTML] = useState("");
  const [loadingConvert, setLoadingConvert] = useState(false);

  const fetchSemanticHTML = async (inputHTML) => {
    setLoadingConvert(true);
    try {
      const response = await axios.post("http://localhost:8080/convert", {
        html: inputHTML,
      });
      setOutputHTML(response.data.semantic); // Set the converted HTML
    } catch (error) {
      console.error("Error fetching semantic HTML:", error);
      alert("Error fetching semantic HTML.");
    } finally {
      setLoadingConvert(false); // Hide the loader once conversion is complete
    }
  };

  return (
    <>
      <div className="input-output-container">
        <Input onConvert={fetchSemanticHTML} loadingConvert={loadingConvert} />
        <Output output={outputHTML} />
      </div>
    </>
  );
}

export default App;
