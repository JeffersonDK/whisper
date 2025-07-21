import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
import io

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

# Opcional: Função principal para teste independente
async def main():
    user_text = input("Digite o texto para converter em fala: ")
    await text_to_speech(user_text)

if __name__ == "__main__":
    asyncio.run(main())
