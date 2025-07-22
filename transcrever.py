import streamlit as st
import whisper
import os
import tempfile
import google.generativeai as genai
import asyncio
#from text_to_speech import _text_to_speech
from app44 import text_to_speech

# Configuração da página do Streamlit
st.title("Agente I.A. para pesquisa via Áudio")
st.write("Grave um áudio usando o microfone.")

# Caixa de seleção para idioma
language_options = {"Português": "pt", "Inglês": "en"}
#selected_language = st.selectbox("Selecione o idioma da transcrição:", list(language_options.keys()))
#language_code = language_options[selected_language]
language_code = "pt"
# Inicializar o modelo Whisper (base)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# Configurar a chave de API
#gemini_key = user.secrets.get_secret("AIzaSyCDsvN4QtsDE2Bi1grncPEwDIAY96e4sCE")
genai.configure(api_key="AIzaSyCDsvN4QtsDE2Bi1grncPEwDIAY96e4sCE")

# Configurar o modelo com instruções do Gem
model1 = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="-comporte-se como um assistente para pesquisar o que for perguntado.cumprimente a pessoa  pelo nome , se ela disser o nome e pergunte em que pode ajudar mas somente na apresentação inicial ou se não entender a pergunta. -Não gere asterisco na resposta em forma de lista nem  nenhum outro caractere, separe os itens com ponto-e-virgula ao final.Preferencia: os itens ficam numa mesma linha. "
)

# Captura de áudio
audio_value = st.audio_input("Grave um áudio para transcrever")

if audio_value:
    try:
        # Criar um arquivo temporário para salvar o áudio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_value.getvalue())
            temp_audio_path = temp_audio.name

        # Exibir mensagem de processamento
        st.write("Processando o áudio...")

        # Transcrever o áudio com o idioma selecionado
        result = model.transcribe(temp_audio_path, language=language_code)
        transcription = result["text"]

        # Exibir a transcrição
        st.subheader("Transcrição:")
        st.write(transcription)

        # Remover o arquivo temporário
        os.unlink(temp_audio_path)
        
        # Iniciar uma sessão de chat
        chat = model1.start_chat(history=[])

        # Enviar uma mensagem
        envio =""
        response = chat.send_message(transcription)
        envio = response.text
        st.write(response.text)

        # Envia msg p/ converter em som
        # Text input area
        user_text = envio

        # Button to submit text from text_area
        #if st.button("Convert to Speech", key="convert_button"):
        if envio:
            if user_text.strip():
                # Call the async text_to_speech function
                audio_buffer = asyncio.run(text_to_speech(user_text))
                if audio_buffer:
                    # Display the audio widget
                    st.audio(audio_buffer, format="audio/mp3")
                    st.success("Audio generated successfully!")
            else:
                st.warning("Please enter valid text.")


    except Exception as e:
        st.error(f"Erro ao transcrever o áudio: {str(e)}")
else:
    st.info("Por favor, grave um áudio para transcrever.")
