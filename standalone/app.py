import chainlit as cl
from datetime import datetime
import json
from typing import Optional
import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    """Initialize the embedded viewer session"""
    cl.user_session.set("context", {
        "areaId": None,
        "token": None,
        "timestamp": None,
    })

    await cl.Message(
        content="🚀 Embedded viewer ready. Listening for context from parent window..."
    ).send()


@cl.on_window_message
async def on_window_message(message: str):
    """Handle messages from parent window via postMessage API"""

    try:
        data = json.loads(message)
        await cl.Message(
            content=f"Window message received: `{data}`"
        ).send()

        if data.get("type") == "VIEW_CONTEXT":
            context = {
                "areaId": data.get("areaId"),
                "token": data.get("token"),
                "timestamp": data.get("timestamp", datetime.now().isoformat()),
            }

            cl.user_session.set("context", context)

            await cl.Message(
                content=f"✅ Context received!\n\n📋 **AOI ID**: `{context['areaId']}`\n\n🔑 **Token**: `{context['token'][:40]}...`\n\n🕐 **Updated**: {datetime.fromisoformat(context['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"
            ).send()

            await cl.send_window_message(json.dumps({
                "type": "EMBEDDED_RESPONSE",
                "status": "received",
                "areaId": context["areaId"],
                "timestamp": datetime.now().isoformat(),
            }))

        else:
            await cl.Message(
                content=f"⚠️ Unknown message type: `{data.get('type')}`"
            ).send()

    except json.JSONDecodeError as e:
        await cl.Message(
            content=f"❌ JSON parse error: {str(e)}\nReceived: {message}"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Error: {str(e)}"
        ).send()

@cl.on_message
async def on_message(msg: cl.Message):
    """Handle user messages"""
    context = cl.user_session.get("context", {})

    if context.get("areaId"):
        await cl.Message(
            content=f"📨 Message received with active context for: `{context['areaId']}`"
        ).send()
    else:
        await cl.Message(
            content="⏳ No context available yet. Waiting for parent window..."
        ).send()

