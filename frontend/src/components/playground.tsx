import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import {
  useChatInteract,
  useChatMessages,
  IStep,
} from "@chainlit/react-client";
import { useMemo, useState } from "react";
import { cn } from "@/lib/utils";

function flattenMessages(
  messages: IStep[],
  condition: (node: IStep) => boolean
): IStep[] {
  return messages.reduce((acc: IStep[], node) => {
    if (condition(node)) {
      acc.push(node);
    }

    if (node.steps?.length) {
      acc.push(...flattenMessages(node.steps, condition));
    }

    return acc;
  }, []);
}

export function Playground() {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const { sendMessage } = useChatInteract();
  const { messages } = useChatMessages();

  const flatMessages = useMemo(() => {
    return flattenMessages(messages, (m) => m.type.includes("message"));
  }, [messages]);

  const handleSendMessage = () => {
    const content = inputValue.trim();
    if (content) {
      const message = {
        name: "user",
        type: "user_message" as const,
        output: content,
      };
      sendMessage(message, []);
      setInputValue("");
    }
  };

  const renderMessage = (message: IStep) => {
    const dateOptions: Intl.DateTimeFormatOptions = {
      hour: "2-digit",
      minute: "2-digit",
    };
    const date = new Date(message.createdAt).toLocaleTimeString(
      undefined,
      dateOptions
    );
    return (
      <div key={message.id} className="flex items-start space-x-2">
        <div className="w-20 text-sm text-green-500">{message.name}</div>
        <div className="flex-1 border rounded-lg p-2">
          <p className="text-black dark:text-white">{message.output}</p>
          <small className="text-xs text-gray-500">{date}</small>
        </div>
      </div>
    );
  };

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
            : "absolute right-4 bottom-20 max-w-lg bg-white dark:bg-gray-800 shadow-lg rounded-lg flex flex-col h-[60vh]"
        )}
      >
        <h1 className="text-2xl font-bold px-4 py-2 dark:text-blue-200 dark:bg-blue-950 rounded-t-lg flex items-center justify-between">
          Chainlit POC
          {isFullscreen && <button onClick={() => setIsFullscreen(false)}>X</button>}
        </h1>
        <div className="flex-1 overflow-auto p-6">
          <div className="space-y-4">
            {flatMessages.map((message) => renderMessage(message))}
          </div>
        </div>
        <div className="border-t p-4 bg-white dark:bg-gray-800">
          <div className="flex items-center space-x-2">
            <Input
              autoFocus
              className="flex-1"
              id="message-input"
              placeholder="Type a message"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyUp={(e) => {
                if (e.key === "Enter") {
                  handleSendMessage();
                }
              }}
            />
            <Button onClick={handleSendMessage} type="submit">
              Send
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
