from dotenv import load_dotenv
import os
import asyncio
from typing import Annotated
from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli, tokenize, tts
from livekit.agents.llm import ChatContext, ChatImage, ChatMessage
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero

# Load environment variables from a .env file
load_dotenv()

# List of required environment variables
required_vars = [
    "LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET",
    "DEEPGRAM_API_KEY", "OPENAI_API_KEY"
]

# Check for missing environment variables and raise an error if any are missing
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

class AssistantFunction(agents.llm.FunctionContext):
    """Defines functions that can be called by the assistant."""

    @agents.llm.ai_callable(
        description=(
            "Called when asked to evaluate something that requires vision capabilities, "
            "such as an image, video, or the webcam feed."
        )
    )
    async def image(
        self,
        user_msg: Annotated[str, agents.llm.TypeInfo(description="The user message that triggered this function")],
    ):
        """Handles user messages related to vision capabilities."""
        print(f"Message triggering vision capabilities: {user_msg}")
        return None

async def get_video_track(room: rtc.Room) -> rtc.RemoteVideoTrack:
    """Retrieve the first video track from the room.

    Args:
        room (rtc.Room): The LiveKit room object.

    Returns:
        rtc.RemoteVideoTrack: The first video track found in the room.

    Raises:
        ValueError: If no video tracks are found.
    """
    video_track = asyncio.Future[rtc.RemoteVideoTrack]()
    for _, participant in room.remote_participants.items():
        for _, track_publication in participant.track_publications.items():
            if track_publication.track is not None and isinstance(track_publication.track, rtc.RemoteVideoTrack):
                video_track.set_result(track_publication.track)
                print(f"Using video track {track_publication.track.sid}")
                return await video_track

    raise ValueError("No video track found in the room.")

async def entrypoint(ctx: JobContext):
    """Main entry point for the assistant's functionality."""
    await ctx.connect()
    print(f"Connected to room: {ctx.room.name}")

    # Define the chat context for the assistant
    chat_context = ChatContext(
        messages=[
            ChatMessage(
                role="system",
                content=(
                    "Your name is Alloy. You are a funny, witty bot. Your interface with users will be voice and vision."
                    " Respond with short and concise answers. Avoid using unpronouncable punctuation or emojis."
                ),
            )
        ]
    )

    # Initialize OpenAI LLM and TTS systems
    gpt = openai.LLM(model="gpt-4o")
    openai_tts = tts.StreamAdapter(
        tts=openai.TTS(voice="alloy"),
        sentence_tokenizer=tokenize.basic.SentenceTokenizer(),
    )

    latest_image: rtc.VideoFrame | None = None

    # Create the voice assistant with required components
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=gpt,
        tts=openai_tts,
        fnc_ctx=AssistantFunction(),
        chat_ctx=chat_context,
    )

    chat = rtc.ChatManager(ctx.room)

    async def _answer(text: str, use_image: bool = False):
        """Responds to the user's message with text and optionally the latest image."""
        content: list[str | ChatImage] = [text]
        if use_image and latest_image:
            content.append(ChatImage(image=latest_image))

        chat_context.messages.append(ChatMessage(role="user", content=content))

        # Stream the chat response from GPT
        stream = gpt.chat(chat_ctx=chat_context)
        await assistant.say(stream, allow_interruptions=True)

    @chat.on("message_received")
    def on_message_received(msg: rtc.ChatMessage):
        """Handles incoming messages from the user."""
        if msg.message:
            asyncio.create_task(_answer(msg.message, use_image=False))

    @assistant.on("function_calls_finished")
    def on_function_calls_finished(called_functions: list[agents.llm.CalledFunction]):
        """Triggered when an assistant's function call completes."""
        if len(called_functions) == 0:
            return

        user_msg = called_functions[0].call_info.arguments.get("user_msg")
        if user_msg:
            asyncio.create_task(_answer(user_msg, use_image=True))

    # Start the assistant in the room
    assistant.start(ctx.room)

    await asyncio.sleep(1)  # Allow some time for initialization
    await assistant.say("Hi there! How can I help?", allow_interruptions=True)

    # Main loop for processing video input
    while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
        video_track = await get_video_track(ctx.room)
        async for event in rtc.VideoStream(video_track):
            latest_image = event.frame

if __name__ == "__main__":
    # Run the application with the specified entry point
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
