import streamlit as st
import whisper
import os
import tempfile

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

    except Exception as e:
        st.error(f"Erro ao transcrever o áudio: {str(e)}")
else:
    st.info("Por favor, grave um áudio para transcrever.")