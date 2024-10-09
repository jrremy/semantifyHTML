import { useState } from "react";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

import "./Output.css";

export default function Output({ output, setShowChanges }) {
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
        <div className="output-header">
          <h2>Converted Semantic HTML</h2>
          <button id="copy-button" onClick={copyToClipboard}>
            <ContentCopyIcon fontSize="small" />
          </button>
          {copySuccess && <span className="copy-success">{copySuccess}</span>}
        </div>
        <textarea className="input-output" value={output} readOnly></textarea>
        <button className="view-changes" onClick={setShowChanges}>
          View Changes
        </button>
      </div>
    </>
  );
}
