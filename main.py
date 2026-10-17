import random
import time
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
import speech_recognition as sr
from deep_translator import MyMemoryTranslator, GoogleTranslator
# nova versão
# Configurações gerais
duration = 5
sample_rate = 44100
max_errors = 3

words_by_level = {
    "fácil": [
        "gato", "cachorro", "maçã", "leite", "sol",
        "água", "livro", "bola", "mesa", "porta",
        "flor", "peixe", "pão", "chuva", "amigo"
    ],
    "médio": [
        "casa", "escola", "amigo", "janela", "amarelo",
        "trabalho", "computador", "viagem", "caderno", "família",
        "saudade", "espelho", "história", "natureza"
    ],
    "difícil": [
        "tecnologia", "universidade", "informação", "pronúncia", "imaginação",
        "característica", "desenvolvimento", "responsabilidade",
        "significado", "infraestrutura", "perspectiva", "biodiversidade"
    ],
    "impossível": [
        "inefável", "idiossincrasia", "obnubilado", "verossimilhança", "recondito", 
        "pueril", "vicissitude", "empirismo", "anacronismo", "pusilânime"
    ]
}

# Usando o GoogleTranslator que costuma ser bastante estável para pares de línguas
translator = GoogleTranslator(source='pt', target='en')
recognizer = sr.Recognizer()

def gravar_audio(filename="output.wav"):
    print("\n🎙️ Fale a tradução em INGLÊS...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav_write(filename, sample_rate, recording)
    print("⏳ Processando...")

def reconhecer_fala(filename="output.wav"):
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        # Reconhece o áudio capturado em INGLÊS
        texto_ingles = recognizer.recognize_google(audio, language="en-US").lower().strip()
        return texto_ingles
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"⚠️ Erro de conexão com o serviço de reconhecimento: {e}")
        return None

def jogar():
    print("--- JOGO DE TRADUÇÃO POR FALA ---")
    nivel = input("Escolha o nível (fácil, médio, difícil, impossível): ").lower().strip()

    if nivel not in words_by_level:
        print("❌ Nível inválido!")
        return

    print(f"\n🎯 Nível selecionado: {nivel.capitalize()}")
    time.sleep(1)
    print("📜 Regras: Veja a palavra em Português e fale a tradução em INGLÊS.")
    time.sleep(1)
    print(f"   Se cometer {max_errors} erros, o jogo termina!\n")
    time.sleep(1)

    pontos = 0
    erros = 0
    palavras = words_by_level[nivel].copy()

    while erros < max_errors and palavras:
        palavra_pt = random.choice(palavras)
        palavras.remove(palavra_pt)

        # Traduz a palavra alvo do português para o inglês para servir de gabarito técnico
        try:
            palavra_en_esperada = translator.translate(palavra_pt).lower().strip()
        except Exception:
            palavra_en_esperada = ""

        print("\n----------------------------------------")
        print(f"Pontos: {pontos} | Erros: {erros}/{max_errors}")
        print(f"Palavra em Português: >>> {palavra_pt.upper()} <<<")

        input("Pressione ENTER e diga a palavra em INGLÊS...")
        gravar_audio()
        
        fala_en = reconhecer_fala()

        if fala_en is None:
            erros += 1
            print("❌ Não foi possível entender a fala em inglês. Tente falar mais claro próximo ao microfone.")
            continue

        print(f"🗣️ Você disse em inglês: '{fala_en}'")
        print(f"💡 Esperado em inglês (aproximado): '{palavra_en_esperada}'")

        # Compara o que o utilizador disse diretamente com a tradução esperada
        if fala_en == palavra_en_esperada or palavra_en_esperada in fala_en:
            pontos += 10
            print("✅ Acertou!")
        else:
            erros += 1
            print(f"❌ Errou! O termo correto em inglês seria algo como: '{palavra_en_esperada}'")

    print("\n----------------------------------------")
    if erros >= max_errors:
        print("☠️ Fim de jogo! Você atingiu o limite de erros.")
    else:
        print("🏆 Parabéns! Você concluiu todas as palavras.")
    print(f"Pontuação final: {pontos}")

if __name__ == "__main__":
    jogar()