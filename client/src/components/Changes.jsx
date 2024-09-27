import { useState } from "react";

import "./Changes.css";

export default function Changes({ changes }) {
  const [currentChangeIndex, setCurrentChangeIndex] = useState(0);

  const fetchExplanation = async (change) => {
    const response = await axios.post("http://localhost:8080/convert", {
      change: change,
    });
  };

  function decrementChangeIndex() {
    setCurrentChangeIndex((currentChangeIndex) => currentChangeIndex - 1);
  }

  function incrementChangeIndex() {
    setCurrentChangeIndex((currentChangeIndex) => currentChangeIndex + 1);
  }

  return (
    <div className="changes">
      <h3>Changes</h3>
      {/* <div className="change-boxes">
          {changes.map((change) => (
            <div key={change} className="change-box">
              <p>Original Tag: {change.original_tag}</p>
              <p>New Tag: {change.new_tag}</p>
              <p>Content: {change.content}</p>
            </div>
          ))}
        </div> */}

      <div className="change-box">
        {changes.length === 0 && <p>No changes found</p>}
        {changes.length > 0 && (
          <>
            <p>Original Tag: {changes[currentChangeIndex].original_tag}</p>
            <p>New Tag: {changes[currentChangeIndex].new_tag}</p>
            <p>Content: {changes[currentChangeIndex].content}</p>
          </>
        )}
      </div>

      <div>
        <button
          onClick={decrementChangeIndex}
          disabled={currentChangeIndex === 0}
        >
          Previous Change
        </button>
        <button
          onClick={incrementChangeIndex}
          disabled={
            (currentChangeIndex === changes.length - 1) | (changes.length === 0)
          }
        >
          Next Change
        </button>
      </div>
    </div>
  );
}
