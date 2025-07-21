import streamlit as st
import asyncio
import edge_tts
import io

async def _text_to_speech(text):
    """Converts text to speech using edge_tts and returns audio bytes."""
    try:
        tts = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
        audio_buffer = io.BytesIO()
        async for chunk in tts.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

def play_text_to_speech(text):
    """Receives text, generates speech, and displays st.audio widget."""
    if not text or not text.strip():
        st.warning("Please provide valid text.")
        return
    
    # Run async text-to-speech conversion
    audio_buffer = asyncio.run(_text_to_speech(text))
    if audio_buffer:
        # Display the audio widget with the generated audio
        st.audio(audio_buffer, format="audio/mp3")
        st.success("Audio generated successfully!")