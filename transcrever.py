import streamlit as st
import os
import tempfile
import google.generativeai as genai
import asyncio
import speech_recognition as sr
import io
import soundfile as sf
import numpy as np

#from text_to_speech import _text_to_speech
from app44 import text_to_speech

# Configuração da página do Streamlit
st.title("Agente I.A. para pesquisa via Áudio")
st.write("Grave um áudio usando o microfone.")

# Caixa para entrada de Gravação

# Inicializa o reconhecedor
recognizer = sr.Recognizer()

# Estado da sessão para controlar a transcrição
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

# Função para converter áudio do st.audio_input para formato compatível com speech_recognition
def process_audio(audio_data):
    try:
        # Lê o áudio do BytesIO
        audio_file = io.BytesIO(audio_data)
        with sf.SoundFile(audio_file, 'r') as f:
            audio_array = f.read(dtype='int16')
            sample_rate = f.samplerate
        
        # Converte o áudio para o formato WAV exigido por speech_recognition
        wav_io = io.BytesIO()
        sf.write(wav_io, audio_array, sample_rate, format='WAV')
        wav_io.seek(0)
        
        # Cria um AudioFile para speech_recognition
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)
        
        # Transcreve o áudio usando Google Speech Recognition
        text = recognizer.recognize_google(audio, language="en-HK")
        st.session_state.transcribed_text = text
        st.success(f"Texto transcrito: {text}")
    except sr.UnknownValueError:
        st.error("Não foi possível entender o áudio.")
        st.session_state.transcribed_text = ""
    except sr.RequestError as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        st.session_state.transcribed_text = ""
    except Exception as e:
        st.error(f"Erro ao processar o áudio: {str(e)}")
        st.session_state.transcribed_text = ""

# Interface do Streamlit

# Widget de entrada de áudio
audio_value = st.audio_input("Grave ou envie um áudio", key="audio_input")

# Processa o áudio quando um arquivo é carregado
if audio_value:
    st.info("Processando o áudio...")
    process_audio(audio_value.getvalue())

# Exibe o texto transcrito
if st.session_state.transcribed_text:
    st.write("**Texto Transcrito:**")
    st.write(st.session_state.transcribed_text)

#----------
# Configurar a chave de API
#gemini_key = user.secrets.get_secret("AIzaSyCDsvN4QtsDE2Bi1grncPEwDIAY96e4sCE")
genai.configure(api_key="AIzaSyCDsvN4QtsDE2Bi1grncPEwDIAY96e4sCE")

# Configurar o modelo com instruções do Gem
model1 = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="-comporte-se como um assistente para pesquisar o que for perguntado.A linguagem usada é ingles,responda em ingles.Caso a pessoa diga seu nome, cumprimente-a pelo nome , se ela disser o nome;em seguida pergunte em que pode ajudar mas somente a primeira vez.A saudação é só uma vez, somente se a pessoa disser o nome.Após dar a resposta : pergunte se a pessoa tem mais alguma pergunta.Caso não entenda a pergunta : peça para a pessoa reformular a pergunta. -Não gere asterisco na resposta em forma de lista nem  nenhum outro caractere tipo hifen, separe os itens com ponto-e-virgula ao final.Preferencia: os itens ficam numa mesma linha. "
)

# Captura de áudio
#audio_value = st.audio_input("Clique e envie uma pergunta via áudio")

if audio_value:
    try:
        
        transcription = st.session_state.transcribed_text

        # Exibir a transcrição
        st.subheader("Transcrição:")
        st.write(transcription)

        # Remover o arquivo temporário
        #os.unlink(temp_audio_path)
        
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
