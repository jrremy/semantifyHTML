import { useState } from "react";
import "./Navbar.css";

export default function Navbar({ tabs, activeTab, onSwitch }) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">SemantifyHTML</div>
      <ul className="navbar-links">
        {tabs.map((button) => (
          <li
            key={button}
            className={`navbar-link ${activeTab === button ? "selected" : ""}`}
            onClick={() => onSwitch(button)}
          >
            {button}
          </li>
        ))}
      </ul>
    </nav>
  );
}
