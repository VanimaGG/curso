import random
import time
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
import speech_recognition as sr
from deep_translator import MyMemoryTranslator

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
        "saudade", "telemóvel", "espelho", "história", "natureza"
    ],
    "difícil": [
        "tecnologia", "universidade", "informação", "pronúncia", "imaginação",
        "característica", "desenvolvimento", "conscientização", "inconstitucional", "responsabilidade",
        "paralelepípedo", "significado", "infraestrutura", "perspectiva", "biodiversidade"
    ],
    "impossível": [
        "hipopotomonstrosesquipedaliofobia", "anticonstitucionalissimamente", "otorrinolaringologista", "pneumoultramicroscopicossilicovulcanoconiose", "inefável",
        "idiossincrasia", "obnubilado", "verossimilhança", "recondito", "pueril",
        "vicissitude", "empirismo", "anacronismo", "locupletar", "pusilânime"
    ]
}

translator = MyMemoryTranslator(source="en-GB", target="pt-BR")
recognizer = sr.Recognizer()

def gravar_audio(filename="output.wav"):
    print("\n🎙️ Fale a tradução em INGLÊS...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav_write(filename, sample_rate, recording)
    print("⏳ Processando...")

def reconhecer_e_traduzir(filename="output.wav"):
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        # Reconhece o áudio capturado em INGLÊS
        texto_ingles = recognizer.recognize_google(audio, language="en-US").lower().strip()
        # Traduz a fala em inglês para PORTUGUÊS
        traducao_portugues = translator.translate(texto_ingles).lower().strip()
        return texto_ingles, traducao_portugues
    except sr.UnknownValueError:
        return None, "Não foi possível entender a fala em inglês."
    except sr.RequestError as e:
        return None, f"Erro de conexão: {e}"

def jogar():
    print("--- JOGO DE TRADUÇÃO POR FALA ---")
    nivel = input("Escolha o nível (fácil, médio, difícil, impossível): ").lower().strip()

    if nivel not in words_by_level:
        print("Nível inválido!")
        return

    
    print(f"🎯 Nível selecionado: {nivel.capitalize()}")
    time.sleep(1)
    print("📜 Regras: Veja a palavra em Português e fale a tradução em INGLÊS.")
    time.sleep(1)
    print("   O sistema entenderá seu inglês, traduzirá para o Português e comparará.")
    time.sleep(1)
    print(f"   Se cometer {max_errors} erros, o jogo termina!")
    time.sleep(1)
   

    pontos = 0
    erros = 0
    palavras = words_by_level[nivel].copy()

    while erros < max_errors and palavras:
        palavra_alvo = random.choice(palavras)
        palavras.remove(palavra_alvo)

        print("\n----------------------------------------")
        print(f"Pontos: {pontos} | Erros: {erros}/{max_errors}")
        print(f"Palavra em Português: >>> {palavra_alvo.upper()} <<<")

        input("Pressione ENTER e diga a palavra em INGLÊS...")
        gravar_audio()
        
        fala_en, traducao_pt = reconhecer_e_traduzir()

        if fala_en is None:
            erros += 1
            print(f"❌ {traducao_pt}")
            continue

        print(f"Você disse em inglês: '{fala_en}'")
        print(f"Tradução de volta para PT: '{traducao_pt}'")

        # Compara a tradução da fala ou a própria palavra falada diretamente
        if traducao_pt == palavra_alvo or fala_en == palavra_alvo:
            pontos += 10
            print("✅ Acertou!")
        else:
            erros += 1
            print(f"❌ Errou! O correto era a tradução de: {palavra_alvo}")

    print("\n----------------------------------------")
    if erros >= max_errors:
        print("☠️ Fim de jogo! Você atingiu 3 erros.")
    else:
        print("🏆 Parabéns! Você concluiu todas as palavras.")
    print(f"Pontuação final: {pontos}")

if __name__ == "__main__":
    jogar()