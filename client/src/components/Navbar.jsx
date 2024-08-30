import { useState } from "react";
import "./Navbar.css";

export default function Navbar({ tabs, activeTab, onSwitch }) {
  return (
    <nav className="navbar">
      <h1 className="navbar-logo">SemantifyHTML</h1>
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
