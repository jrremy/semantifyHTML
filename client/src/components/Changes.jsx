import { useState } from "react";
import axios from "axios";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

import "./Changes.css";

export default function Changes({ changes }) {
  const [currentChangeIndex, setCurrentChangeIndex] = useState(0);
  const [explanations, setExplanations] = useState(
    Array(changes.length).fill("")
  );

  const fetchExplanationStream = async (changeIndex) => {
    const change = changes[changeIndex];

    try {
      const response = await fetch("http://localhost:8080/explanation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          original_tag: change.original_tag,
          new_tag: change.new_tag,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      // Stream the data and update explanations as it comes in
      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        const chunk = decoder.decode(value, { stream: true });
        setExplanations((prevExplanations) => {
          const updatedExplanations = [...prevExplanations];
          updatedExplanations[changeIndex] += chunk;
          return updatedExplanations;
        });
      }
    } catch (error) {
      console.error("Error generating explanation:", error);
      alert("Error generating explanation.");
    }
  };

  function decrementChangeIndex() {
    setCurrentChangeIndex((currentChangeIndex) => currentChangeIndex - 1);
  }

  function incrementChangeIndex() {
    setCurrentChangeIndex((currentChangeIndex) => currentChangeIndex + 1);
  }

  return (
    <div className="changes">
      <h2>Changes</h2>
      <div className="changes-container">
        <div className="change-box">
          {changes.length === 0 && <p>No changes found</p>}
          {changes.length > 0 && (
            <>
              <h3>Original Tag</h3>
              <pre>{changes[currentChangeIndex].original_tag}</pre>
              <h3>New Tag</h3>
              <pre>{changes[currentChangeIndex].new_tag}</pre>
              <div className="frequency">
                <h3>Frequency: </h3>
                <p>{changes[currentChangeIndex].frequency}</p>
              </div>

              {/* <p>New Tag: {changes[currentChangeIndex].new_tag}</p> */}
              {/* <p>Content: {changes[currentChangeIndex].content}</p> */}
            </>
          )}
        </div>
        <div className="explanation-box">
          {explanations[currentChangeIndex] ? (
            <p>{explanations[currentChangeIndex]}</p>
          ) : (
            <button onClick={() => fetchExplanationStream(currentChangeIndex)}>
              Generate Explanation
            </button>
          )}
        </div>
      </div>

      <nav class="changes-nav">
        <button
          id="changes-prev"
          onClick={decrementChangeIndex}
          disabled={currentChangeIndex === 0}
        >
          <ArrowBackIosIcon></ArrowBackIosIcon>
          Previous
        </button>
        <button
          id="changes-next"
          onClick={incrementChangeIndex}
          disabled={
            (currentChangeIndex === changes.length - 1) | (changes.length === 0)
          }
        >
          Next
          <ArrowForwardIosIcon></ArrowForwardIosIcon>
        </button>
      </nav>
    </div>
  );
}
