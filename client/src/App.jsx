import { useState, useRef, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Navbar from "./components/Navbar.jsx";
import Input from "./components/Input.jsx";
import Output from "./components/Output.jsx";
import Changes from "./components/Changes.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("Convert");
  const [outputHTML, setOutputHTML] = useState("");
  const [loadingConvert, setLoadingConvert] = useState(false);
  const [changes, setChanges] = useState([]);
  const [showChanges, setShowChanges] = useState(false);
  const [noChanges, setNoChanges] = useState(false);

  const changesSectionRef = useRef(null);
  const outputSectionRef = useRef(null);

  // useEffect(() => {
  //   if (showChanges && changesSectionRef.current) {
  //     changesSectionRef.current.scrollIntoView({ behavior: "smooth" });
  //   }
  // }, [showChanges]);

  const fetchSemanticHTML = async (inputHTML) => {
    if (inputHTML.length > 0) {
      setNoChanges(false);
      setLoadingConvert(true);
      try {
        const response = await axios.post("http://localhost:8080/convert", {
          html: inputHTML,
        });
        setShowChanges(false);
        if (response.data.changes.length > 0) {
          setOutputHTML(response.data.semantic);
          setChanges(response.data.changes);
        } else {
          setNoChanges(true);
        }
      } catch (error) {
        console.error("Error fetching semantic HTML:", error);
        alert("Error fetching semantic HTML.");
      } finally {
        setLoadingConvert(false); // Hide the loader once conversion is complete
      }
    } else {
      setNoChanges(true);
    }
  };

  const tabs = ["Convert", "About"];

  return (
    <>
      <header>
        <Navbar
          tabs={tabs}
          activeTab={activeTab}
          onSwitch={setActiveTab}
        ></Navbar>
      </header>
      <main>
        {activeTab === "Convert" && (
          <div className="convert-page">
            <h2 id="slogan">Make your markup code more accessible!</h2>

            <div className="convert-section">
              <Input
                onConvert={fetchSemanticHTML}
                loadingConvert={loadingConvert}
                noChanges={noChanges}
              />
            </div>
            {changes.length > 0 && !noChanges && (
              <div className="convert-section">
                <Output output={outputHTML} setShowChanges={setShowChanges} />
              </div>
            )}
            {showChanges && (
              <div className="convert-section" ref={changesSectionRef}>
                <Changes changes={changes} />
              </div>
            )}
          </div>
        )}
        {activeTab === "About" && <p>About section text</p>}
      </main>
    </>
  );
}

export default App;
