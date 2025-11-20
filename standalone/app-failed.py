# import chainlit as cl
# import json

# @cl.on_chat_start
# async def on_chat_start():
#     print("Chat session started.")
#     """Initialize the chat session"""
#     await cl.Message(
#         content="🚀 Chat session started. Listening for window messages..."
#     ).send()

# @cl.on_window_message
# async def handle_window_message(message: str):
#     print(f"Received window message: {message} ")
#     """
#     Handles window messages from the React host, including the READY_PING and 
#     application context updates.
#     """

#     try:
#         data = json.loads(message)

#         message_type = data.get("type")

#         if message_type == "READY_PING":
#             pong_payload = {
#                 "type": "READY_PONG",
#                 "status": "active",
#                 "session_id": cl.get_session().get("id")
#             }

#             await cl.send_window_message(content=json.dumps(pong_payload))
#             await cl.Message(
#                 content=f"PING received from host - sent PONG with session ID: {pong_payload['session_id']}",
#                 author="System Integration"
#             ).send()
#             print("Backend: Dispatched READY_PONG and established session.")

#         elif message_type == "CONTEXT_UPDATE":
#             context_data = data.get("payload", {})
#             user_id = context_data.get("userId", "N/A")

#             cl.user_session.set("user_id", user_id)

#             await cl.Message(
#                 content=f"Context received for User ID: {user_id}",
#                 author="System Integration"
#             ).send()

#     except json.JSONDecodeError:
#         print(f"Error: Received non-JSON string: {message}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


import chainlit as cl


@cl.on_window_message
async def window_message(message: str):
  if message.startswith("Client: "):
    await cl.Message(content=f"Window message received: {message}").send()


@cl.on_message
async def message():
  await cl.send_window_message("Server: Hello from Chainlit")



# import chainlit as cl
# from datetime import datetime
# import json

# @cl.on_chat_start
# async def on_chat_start():
#     """Initialize the embedded viewer session"""
#     cl.user_session.set("context", {
#         "projectId": None,
#         "token": None,
#         "timestamp": None,
#     })

#     await cl.Message(
#         content="🚀 Embedded viewer ready. Listening for context from parent window..."
#     ).send()

# @cl.on_window_message
# async def on_window_message(message: str):
#     """Handle messages from parent window via postMessage API"""
#     await cl.Message(
#         content=f"Window message received: `{message}`"
#     ).send()

#     try:
#         data = json.loads(message)

#         if data.get("type") == "VIEW_CONTEXT":
#             context = {
#                 "projectId": data.get("projectId"),
#                 "token": data.get("token"),
#                 "timestamp": data.get("timestamp", datetime.now().isoformat()),
#             }

#             cl.user_session.set("context", context)

#             await cl.Message(
#                 content=f"✅ Context received!\n\n📋 **AOI ID**: `{context['projectId']}`\n\n🔑 **Token**: `{context['token'][:40]}...`\n\n🕐 **Updated**: {datetime.fromisoformat(context['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"
#             ).send()

#             await cl.send_window_message(json.dumps({
#                 "type": "EMBEDDED_RESPONSE",
#                 "status": "received",
#                 "projectId": context["projectId"],
#                 "timestamp": datetime.now().isoformat(),
#             }))

#         else:
#             await cl.Message(
#                 content=f"⚠️ Unknown message type: `{data.get('type')}`"
#             ).send()

#     except json.JSONDecodeError as e:
#         await cl.Message(
#             content=f"❌ JSON parse error: {str(e)}\nReceived: {message}"
#         ).send()
#     except Exception as e:
#         await cl.Message(
#             content=f"❌ Error: {str(e)}"
#         ).send()

# @cl.on_message
# async def on_message(msg: cl.Message):
#     """Handle user messages"""
#     context = cl.user_session.get("context", {})

#     if context.get("projectId"):
#         await cl.Message(
#             content=f"📨 Message received with active context for: `{context['projectId']}`"
#         ).send()
#     else:
#         await cl.Message(
#             content="⏳ No context available yet. Waiting for parent window..."
#         ).send()





# import chainlit as cl
# from typing import Dict


# @cl.on_chat_start
# async def start():
#     """Chat session starts"""
#     await cl.Message(
#         content="🚀 Connected. Ready for authenticated chat."
#     ).send()


# @cl.on_window_message
# async def window_message(message: Dict[str, str] = {
#     "type": "VIEW_CONTEXT",
#     "projectId": str,
#     "token": str,
#     "timestamp": str,
# }):
#     if message.type == 'VIEW_CONTEXT':
#         await cl.Message(content=f"Window message received: {message}").send()
#         await cl.send_window_message(f"Server: Window message received: {message}")


# @cl.on_message
# async def on_message(msg: cl.Message):
#     await cl.Message(content=f"Normal message received: {msg.content}").send()
#     await cl.send_window_message(f"Server: Normal message received: {msg.content}")




# import os
# from typing import Optional
# import chainlit as cl
# from chainlit.logger import logger


# current_token: Optional[str] = None


# def setup():
#     """Setup Chainlit - disable default auth"""
#     os.environ["CHAINLIT_AUTH_DISABLED"] = "true"
#     os.environ["CHAINLIT_ENABLE_TELEMETRY"] = "false"


# @cl.on_chat_start
# async def start():
#     """Chat session starts"""
#     await cl.Message(
#         content="🚀 Connected. Ready for authenticated chat."
#     ).send()


# @cl.on_window_message
# async def handle_window_message(message: str):
#     """
#     Receive context data from parent React app
#     Example: { userId, sessionId, metadata }
#     """
#     await cl.Message(content=f"Received window message: {message}").send()
#     # try:
#     #     data = json.loads(message)
#     #     cl.user_session.set("user_context", data)

#     #     await cl.send_window_message(
#     #         json.dumps({"status": "received", "context": data})
#     #     )
#     # except json.JSONDecodeError:
#     #     await cl.send_window_message(
#     #         json.dumps({"status": "error", "message": "Invalid JSON"})
#     #     )


# @cl.on_message
# async def main(message: cl.Message):
#     """Process message with token authorization"""

#     if not current_token:
#         await cl.Message(
#             content="❌ No authorization token. Please refresh the page."
#         ).send()
#         return

#     await cl.Message(
#         content=f"✅ Authorized\n\nMessage: {message.content}\n\nToken: {current_token[:20]}..."
#     ).send()



# # Disable default auth
# setup()

# # import chainlit as cl
# # import json

# # @cl.set_starters
# # async def set_starters():
# #     return [
# #         cl.Starter(
# #             label="Hello",
# #             message="Hello there!",
# #             icon="/public/icon.svg",
# #         ),
# #     ]

# # @cl.on_message
# # async def main(message: cl.Message):
# #     await cl.Message(content=f"You said: {message.content}").send()

# # @cl.on_window_message
# # async def handle_window_message(message: str):
# #     print("Received window message:", message)
# #     """
# #     Receive context data from parent React app
# #     Example: { userId, sessionId, metadata }
# #     """
# #     try:
# #         data = json.loads(message)
# #         cl.user_session.set("user_context", data)

# #         await cl.send_window_message(
# #             json.dumps({"status": "received", "context": data})
# #         )
# #     except json.JSONDecodeError:
# #         await cl.send_window_message(
# #             json.dumps({"status": "error", "message": "Invalid JSON"})
# #         )
