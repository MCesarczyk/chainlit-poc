import reactLogo from "./assets/react.svg";
import chainlitLogo from "./assets/chainlit.png";
import "./App.css";
import { ChainlitEmbed } from "./ChainlitEmbed";

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
        <ChainlitEmbed />
      </div>
    </>
  );
}

export default App;
