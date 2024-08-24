import { useState } from "react";
import "./Output.css";

export default function Output({ output }) {
  // State to show copy success message
  const [copySuccess, setCopySuccess] = useState("");

  // Function to copy text to clipboard
  const copyToClipboard = () => {
    navigator.clipboard.writeText(output).then(
      () => {
        setCopySuccess("Copied!");
        // Reset the success message after a short delay
        setTimeout(() => setCopySuccess(""), 2000);
      },
      (err) => {
        setCopySuccess("Failed to copy!");
        console.error("Failed to copy text: ", err);
      }
    );
  };

  return (
    <>
      <div className="output-box">
        <h3>Converted Semantic HTML</h3>
        <textarea
          className="input-output-boxes"
          value={output}
          readOnly
        ></textarea>
        <button onClick={copyToClipboard}>Copy to Clipboard</button>
        {copySuccess && <span className="copy-success">{copySuccess}</span>}
      </div>
    </>
  );
}