import { useState } from "react";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import CheckIcon from "@mui/icons-material/Check";

import "./Output.css";

export default function Output({ output, setShowChanges }) {
  // State to show copy success message
  const [copySuccess, setCopySuccess] = useState(false);
  const [copyIcon, setCopyIcon] = useState(
    <ContentCopyIcon fontSize="small" />
  );

  // Function to copy text to clipboard
  const copyToClipboard = () => {
    navigator.clipboard.writeText(output).then(
      () => {
        setCopySuccess(true);
        setCopyIcon(<CheckIcon fontSize="small" />);
        // Reset the success message after a short delay
        setTimeout(() => setCopySuccess(false), 2000);
        setTimeout(
          () => setCopyIcon(<ContentCopyIcon fontSize="small" />),
          2000
        );
      },
      (err) => {
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
            {copyIcon}
          </button>
          {copySuccess && <span id="copy-success">Copied!</span>}
        </div>
        <textarea className="input-output" value={output} readOnly></textarea>
        <button className="view-changes" onClick={setShowChanges}>
          View Changes
        </button>
      </div>
    </>
  );
}
