import streamlit as st
import whisper
import os
import tempfile
import google.generativeai as genai
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import io
import edge_tts

async def text_to_speech(text):
    """Converte texto em fala e reproduz em memória usando edge_tts e pydub."""
    tts = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
    
    # Coleta os fragmentos de áudio em um buffer na memória
    audio_buffer = io.BytesIO()
    async for chunk in tts.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    
    # Reposiciona o cursor do buffer para o início
    audio_buffer.seek(0)
    
    # Carrega os dados de áudio no AudioSegment do pydub
    audio = AudioSegment.from_file(audio_buffer, format="mp3")
    
    # Reproduz o áudio
    play(audio)

# Configuração da página do Streamlit
st.title("Transcrição de Áudio com Whisper")
st.write("Grave um áudio usando o microfone e veja a transcrição em tempo real.")

# Caixa de seleção para idioma
language_options = {"Português": "pt", "Inglês": "en"}
selected_language = st.selectbox("Selecione o idioma da transcrição:", list(language_options.keys()))
language_code = language_options[selected_language]

# Inicializar o modelo Whisper (base)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# Configurar a chave de API
genai.configure(api_key="AIzaSyCDsvN4QtsDE2Bi1grncPEwDIAY96e4sCE")

# Configurar o modelo com instruções do Gemini
model1 = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="Você é um professor de inglês. Inicie perguntando: 'Em que eu poderia ajudar?' - caso a pessoa diga seu próprio nome, repita o nome dela ao final da frase inicial."
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

        # Enviar a transcrição para o modelo Gemini
        response = chat.send_message(transcription)
        st.write(response.text)
        resposta = response.text

        # Chamar a função text_to_speech do módulo geek
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(text_to_speech(resposta))
        #await text_to_speech(resposta)
        loop.run_until_complete(text_to_speech(resposta)

    except Exception as e:
        st.error(f"Erro ao processar o áudio ou reproduzir a fala: {str(e)}")
else:
    st.info("Por favor, grave um áudio para transcrever.")
