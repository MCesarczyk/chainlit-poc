import chainlit as cl
import json

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Hello",
            message="Hello there!",
            icon="/public/icon.svg",
        ),
    ]

@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content=f"You said: {message.content}").send()

@cl.on_window_message
async def handle_window_message(message: str):
    """
    Receive context data from parent React app
    Example: { userId, sessionId, metadata }
    """
    try:
        data = json.loads(message)
        cl.user_session.set("user_context", data)

        await cl.send_window_message(
            json.dumps({"status": "received", "context": data})
        )
    except json.JSONDecodeError:
        await cl.send_window_message(
            json.dumps({"status": "error", "message": "Invalid JSON"})
        )
