import streamlit as st
import asyncio
import edge_tts
import io
import base64
from streamlit.components.v1 import html

async def text_to_speech(text):
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

# Streamlit app
#st.title("Text to Speech")
#st.write("Enter the text to convert to speech using the pt-BR-AntonioNeural voice, then click the button to generate and play the audio.")

# Text input
#user_text = st.text_area("Text to convert:", height=150)

# Explicitly render button
#convert_button = st.button("Convert and Play", key="convert_button")

# Debug: Confirm button is rendered
#st.write("Debug: Button should be visible above this line.")

# Handle button click
if user_text:
    if user_text.strip():
        audio_buffer = asyncio.run(text_to_speech(user_text))
        if audio_buffer:
            # Encode audio to base64 for HTML audio element
            audio_bytes = audio_buffer.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Inject HTML with autoplay audio element
            audio_html = f"""
            <audio id="audio" autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            <script>
                document.getElementById('audio').play().catch(function(error) {{
                    console.log("Autoplay failed: ", error);
                }});
            </script>
            """
            html(audio_html, height=50)
            st.success("Audio generated successfully!")
    else:
        st.warning("Please enter valid text.")
