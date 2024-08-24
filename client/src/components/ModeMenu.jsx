import "./ModeMenu.css";

export default function ModeMenu({ modes, activeMode, onSwitch }) {
  return (
    <>
      <div className="menu-container">
        <menu>
          {modes.map((button) => (
            <button
              key={button}
              className={`menu-button ${
                activeMode === button ? "selected" : ""
              }`}
              onClick={() => onSwitch(button)}
            >
              {button}
            </button>
          ))}
        </menu>
      </div>
    </>
  );
}
