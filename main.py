from flask import Flask
import random

frases: list[str] = [
    "A maioria das pessoas que sofre de dependência tecnológica sente um forte estresse quando fica fora da área de cobertura de rede ou não pode usar seus dispositivos",
    "De acordo com um estudo realizado em 2018, mais de 50% das pessoas entre 18 e 34 anos se consideram dependentes de seus smartphones."
]

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Página Inicial</h1>"

@app.route("/random_fact")
def random_fact():
    return f"<p>{random.choice(frases)}</p>"

@app.route("/about")
def sobre():
    return "<p>Vanima fez essa página</p>"

@app.route("/secret")
def gen_pass(pass_length=10):
    elements = "qwertyuiopasdfghjklzxcvbnm-+/*!?$%#@"
    password = ""
    
   
    for i in range(pass_length):
        password += random.choice(elements)
        
    return f"<p>Sua senha gerada é: {password}</p>"

app.run(debug=True)