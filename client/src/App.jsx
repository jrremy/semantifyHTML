import { useState, useRef, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Navbar from "./components/Navbar.jsx";
import Input from "./components/Input.jsx";
import Output from "./components/Output.jsx";
import Changes from "./components/Changes.jsx";
import About from "./components/About.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("Convert");
  const [outputHTML, setOutputHTML] = useState("");
  const [loadingConvert, setLoadingConvert] = useState(false);
  const [changes, setChanges] = useState([]);
  const [showChanges, setShowChanges] = useState(false);
  const [noChanges, setNoChanges] = useState(false);

  const changesSectionRef = useRef(null);
  const outputSectionRef = useRef(null);

  useEffect(() => {
    if (outputHTML.length > 0 && outputSectionRef.current) {
      outputSectionRef.current.scrollIntoView({ behavior: "smooth" });
    }
    if (showChanges && changesSectionRef.current) {
      changesSectionRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [outputHTML.length > 0, showChanges]);

  const fetchSemanticHTML = async (inputHTML) => {
    if (inputHTML.length > 0) {
      setNoChanges(false);
      setLoadingConvert(true);
      try {
        const response = await axios.post("http://localhost:8080/convert", {
          html: inputHTML,
        });
        if (response.data.changes.length > 0) {
          setOutputHTML(response.data.semantic);
          setShowChanges(false);
          setChanges(response.data.changes);
        } else {
          setNoChanges(true);
          setTimeout(() => setNoChanges(false), 2000);
        }
      } catch (error) {
        console.error("Error fetching semantic HTML:", error);
        alert("Error fetching semantic HTML.");
      } finally {
        setLoadingConvert(false); // Hide the loader once conversion is complete
      }
    } else {
      setNoChanges(true);
      setTimeout(() => setNoChanges(false), 2000);
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
        <div className="page-content">
          {activeTab === "Convert" && (
            <>
              <h2 id="slogan">Make your markup code more accessible!</h2>

              <div className="page-section">
                <Input
                  onConvert={fetchSemanticHTML}
                  loadingConvert={loadingConvert}
                  noChanges={noChanges}
                />
              </div>
              {changes.length > 0 && (
                <div className="page-section" ref={outputSectionRef}>
                  <Output output={outputHTML} setShowChanges={setShowChanges} />
                </div>
              )}
              {showChanges && (
                <div className="page-section" ref={changesSectionRef}>
                  <Changes changes={changes} />
                </div>
              )}
            </>
          )}
          {activeTab === "About" && (
            <div className="page-section">
              <About />
            </div>
          )}
        </div>
      </main>
    </>
  );
}

export default App;
