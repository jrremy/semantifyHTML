import { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Navbar from "./components/Navbar.jsx";
import Input from "./components/Input.jsx";
import Output from "./components/Output.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("Convert");
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

  const tabs = ["Convert", "About"];

  return (
    <>
      <Navbar tabs={tabs} onSwitch={setActiveTab}></Navbar>
      <div class="body">
        <div>
          <h1>SemantifyHTML</h1>
          <h2>Make your markup code more accesible!</h2>
        </div>
        {activeTab === "Convert" && (
          <div className="input-output-container">
            <Input
              onConvert={fetchSemanticHTML}
              loadingConvert={loadingConvert}
            />
            <Output output={outputHTML} />
          </div>
        )}
        {activeTab === "About" && <p>About section text</p>}
      </div>
    </>
  );
}

export default App;
