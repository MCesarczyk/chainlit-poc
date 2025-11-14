import { useState } from "react";

import { cn } from "@/lib/utils";

export function Embedded() {
  const [isFullscreen, setIsFullscreen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 bg-hero-image bg-stretch bg-center">
      {!isFullscreen && (
        <button
          onClick={() => setIsFullscreen(true)}
          className="absolute right-4 bottom-4 rounded-full w-12 h-12 grid place-items-center text-3xl font-black dark:text-blue-200 bg-blue-600"
        >
          X
        </button>
      )}
      <div
        className={cn(
          isFullscreen
            ? "min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col"
            : "absolute right-4 bottom-20 max-w-lg min-w-[512px] bg-white dark:bg-gray-800 shadow-lg rounded-lg flex flex-col h-[60vh]"
        )}
      >
        <h1 className="text-2xl font-bold px-4 py-2 dark:text-blue-200 dark:bg-blue-950 rounded-t-lg flex items-center justify-between">
          Chainlit POC
          {isFullscreen && (
            <button onClick={() => setIsFullscreen(false)}>X</button>
          )}
        </h1>
        <iframe
          src="http://localhost:8077"
          className={cn(
            "w-full h-full",
            isFullscreen ? "min-h-screen" : "flex-1"
          )}
          width="100%"
          height="100%"
          frameBorder="0"
          sandbox="allow-scripts allow-same-origin"
          title="External App"
        />
      </div>
    </div>
  );
}
