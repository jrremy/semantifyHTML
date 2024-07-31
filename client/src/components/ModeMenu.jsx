import "./ModeMenu.css"

export default function ModeMenu({buttons}) {
  return (
    <>
      <div className="menu-container">
        <menu>
          {buttons}
        </menu>
      </div>
    </>
  );
}
