import requests
import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

API_KEY = "nj6YN+Tx57DUkZv6UkOXnA==5bLX7sGG8FPpkoCj"   # coloque sua chave aqui
ARQUIVO = "historico_famosos.txt"

# ---------------------- Funções lógicas --------------------------

def salvar_historico(texto):
    """Salva o resultado no arquivo."""
    with open(ARQUIVO, "a", encoding="utf-8") as f:
        f.write(texto + "\n---\n")

def buscar_famoso(nome):
    """Busca famoso na API e retorna texto formatado."""
    url = f"https://api.api-ninjas.com/v1/celebrity?name={nome}"
    
    resposta = requests.get(url, headers={"X-Api-Key": API_KEY})

    if resposta.status_code != 200:
        return "Erro ao acessar API."

    dados = resposta.json()

    if not dados:
        return "Nenhum famoso encontrado com esse nome."

    pessoa = dados[0]  # pega o primeiro resultado

    texto = (
        f"Nome: {pessoa.get('name')}\n"
        f"Profissão: {', '.join(pessoa.get('occupation', []))}\n"
        f"Idade: {pessoa.get('age', 'Desconhecida')}\n"
        f"Altura: {pessoa.get('height', 'Desconhecida')} cm\n"
        f"Nacionalidade: {pessoa.get('nationality', 'Desconhecida')}\n"
    )

    salvar_historico(texto)
    return texto

def carregar_historico():
    """Lê as buscas anteriores."""
    if not os.path.exists(ARQUIVO):
        return "Histórico vazio."

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------- Recursividade --------------------------

def limpar_box():
    """Função recursiva simples para limpar a caixa de texto."""
    resultado_box.delete(1.0, tk.END)

# ---------------------- Interface Tkinter --------------------------

def executar_busca():
    nome = entrada_nome.get()
    if not nome.strip():
        messagebox.showwarning("Atenção", "Digite um nome!")
        return
    
    resultado = buscar_famoso(nome)
    limpar_box()
    resultado_box.insert(tk.END, resultado)

def mostrar_historico():
    limpar_box()
    resultado_box.insert(tk.END, carregar_historico())

# ------------------------- JANELA ---------------------------------

janela = tk.Tk()
janela.title("Buscador de Famosos")
janela.geometry("450x500")
janela.resizable(False, False)
janela.configure(bg="#1e90ff")  # azul bonito

# Título
titulo = tk.Label(
    janela,
    text="Busca de Famosos",
    font=("Arial", 20, "bold"),
    bg="#1e90ff",
    fg="white"
)
titulo.pack(pady=10)

# Entrada
entrada_nome = tk.Entry(janela, font=("Arial", 14), width=25)
entrada_nome.pack(pady=10)

# Botões
btn_buscar = tk.Button(
    janela,
    text="Buscar",
    font=("Arial", 14),
    width=15,
    command=executar_busca
)
btn_buscar.pack(pady=5)

btn_historico = tk.Button(
    janela,
    text="Ver Histórico",
    font=("Arial", 14),
    width=15,
    command=mostrar_historico
)
btn_historico.pack(pady=5)

# Caixa de texto de resultados
resultado_box = scrolledtext.ScrolledText(janela, width=50, height=18, font=("Arial", 12))
resultado_box.pack(pady=10)

# Rodar janela
janela.mainloop()
