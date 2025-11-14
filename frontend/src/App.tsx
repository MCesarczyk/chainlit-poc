import { useEffect } from "react";
import { sessionState, useChatSession } from "@chainlit/react-client";
import { useRecoilValue } from "recoil";

import { Embedded } from "@/components/embedded";

const userEnv = {};

function App() {
  const { connect } = useChatSession();
  const session = useRecoilValue(sessionState);
  useEffect(() => {
    if (session?.socket.connected) {
      return;
    }
    fetch("http://localhost:8079/custom-auth", {credentials: "include"})
      .then(() => {
        connect({
          userEnv
        });
      });
  }, [connect]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <>
      <div>
        <Embedded />
      </div>
    </>
  );
}

export default App;
