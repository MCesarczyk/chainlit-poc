import jwt
import chainlit as cl
from datetime import datetime
import json
from typing import Optional
import os


SECRET = os.getenv("JWT_SECRET_KEY")

if SECRET is None:
    raise ValueError("JWT_SECRET_KEY environment variable not set")


@cl.on_chat_start
async def on_chat_start():
    """Initialize session—NOT YET AUTHORIZED"""
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
            token: Optional[str] = data.get("token")
            try:
                payload = jwt.decode(token, SECRET, algorithms=["RS256"])

                context = cl.user_session.get("context", {})
                context["authorized"] = True
                context["token"] = token
                context["userId"] = payload.get("user_id")
                context["email"] = payload.get("email")
                context["timestamp"] = datetime.now().isoformat()
                context["expiry"] = payload.get("exp")
                context["areaId"] = data.get("areaId")

                print("Payload:", payload)
                print("Context:", context)

                cl.user_session.set("context", context)

                await cl.Message(
                    content=f"✅ **Authorized!**\n\n👤 User: `{payload.get('user_id')}`\n📧 Email: `{payload.get('email')}`"
                ).send()

            except jwt.InvalidTokenError as e:
                await cl.Message(
                    content=f"❌ **Authorization failed**: Invalid token {str(e)}"
                ).send()
                return

            context = cl.user_session.get("context", {})
            if not context.get("authorized"):
                await cl.Message(content="❌ Not authorized. Send AUTH_TOKEN first.").send()
                return

            await cl.Message(
                content=f"✅ Context received!\n\n📋 **AOI ID**: `{context['areaId']}`\n\n🔑 **Token**: `{context['token'][:40]}...`\n\n🕐 **Updated**: {datetime.fromisoformat(context['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n\n🕐 **Expires**: {datetime.fromtimestamp(context['expiry']).strftime('%Y-%m-%d %H:%M:%S')}"
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
    """Only process messages if authorized"""
    context = cl.user_session.get("context", {})

    if not context.get("authorized"):
        await cl.Message(
            content="❌ **Not authorized.** Please send AUTH_TOKEN via postMessage first."
        ).send()
        return

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

