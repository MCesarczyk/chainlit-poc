import reactLogo from "./assets/react.svg";
import chainlitLogo from "./assets/chainlit.png";
import "./App.css";

function App() {
  return (
    <>
      <div>
        <a href="https://docs.chainlit.io" target="_blank">
          <img src={chainlitLogo} className="logo" alt="Chainlit logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Chainlit in React POC</h1>
      <div className="card">
        <iframe
          src={import.meta.env.VITE_CHAINLIT_URL || "http://localhost:8077"}
          width="100%"
          height="100%"
          style={{ border: "none" }}
          sandbox="allow-scripts allow-same-origin"
          title="External App"
        />
      </div>
    </>
  );
}

export default App;
