import { useState } from "react";

import "./Output.css";

export default function Output({output}) {
  return (
    <>
      <div className="input-container">
        <h3>Converted Semantic HTML</h3>
        <textarea className="input-output-boxes" value={output}></textarea>
      </div>
    </>
  );
}
