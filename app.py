import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

# ---------------- CONFIGURAÇÃO ----------------

pessoas = [
    "Pai", "Mãe",
    "Avô Paterno", "Avó Paterna",
    "Avô Materno", "Avó Materna"
]

doencas_lista = [
    "Diabetes",
    "Hipertensão",
    "Câncer",
    "Doença Cardíaca",
    "Alzheimer",
    "Depressão",
    "Asma",
    "Colesterol Alto",
    "Não possui nenhuma das doenças listadas",
    "Não sei"
]

olhos_opcoes = ["Castanho", "Azul", "Verde", "Não sei"]
pele_opcoes = ["Clara", "Morena", "Escura", "Não sei"]
cabelo_opcoes = ["Preto", "Castanho", "Loiro", "Ruivo", "Não sei"]

# ---------------- FUNÇÕES ----------------

def converter_altura(valor):
    if not valor:
        return None

    valor = valor.replace(",", ".")
    if "." in valor:
        return float(valor)

    if len(valor) == 3:
        return float(valor) / 100

    return float(valor)


def resetar_campos():
    for pessoa in pessoas:
        olhos_vars[pessoa].set("")
        pele_vars[pessoa].set("")
        cabelo_vars[pessoa].set("")
        altura_vars[pessoa].set("")

        for doenca in doencas_lista:
            doencas_vars[pessoa][doenca].set(False)


def calcular():
    resultado = ""

    # ---------------- HERANÇA MENDELIANA SIMPLIFICADA ----------------

    pai_olhos = olhos_vars["Pai"].get()
    mae_olhos = olhos_vars["Mãe"].get()

    if pai_olhos and mae_olhos and pai_olhos != "Não sei" and mae_olhos != "Não sei":
        if pai_olhos == mae_olhos:
            prob_olhos = f"Alta chance de olhos {pai_olhos}"
        else:
            prob_olhos = f"Chance distribuída entre {pai_olhos} e {mae_olhos}"
    else:
        prob_olhos = "Informação insuficiente sobre olhos"

    resultado += f"👁 Olhos: {prob_olhos}\n\n"

    # ---------------- ALTURA (média simples) ----------------

    alturas = []
    for pessoa in pessoas:
        alt = converter_altura(altura_vars[pessoa].get())
        if alt:
            alturas.append(alt)

    if alturas:
        media = sum(alturas) / len(alturas)
        resultado += f"📏 Altura estimada: {round(media, 2)} m\n\n"
    else:
        resultado += "📏 Altura: dados insuficientes\n\n"

    # ---------------- DOENÇAS (estatística simples) ----------------

    risco_texto = ""
    for doenca in doencas_lista:
        if doenca in ["Não possui nenhuma das doenças listadas", "Não sei"]:
            continue

        contagem = 0
        for pessoa in pessoas:
            if doencas_vars[pessoa][doenca].get():
                contagem += 1

        if contagem > 0:
            risco = min(contagem * 15, 90)
            risco_texto += f"{doenca}: risco estimado de {risco}%\n"

    if risco_texto == "":
        risco_texto = "Sem riscos significativos informados"

    resultado += f"🧬 Risco hereditário:\n{risco_texto}"

    mostrar_resultado(resultado)
    resetar_campos()


def mostrar_resultado(texto):
    janela = tk.Toplevel(root)
    janela.title("Resultado")
    janela.geometry("500x400")

    tk.Label(janela, text="Resultado da Simulação",
             font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(janela, text=texto,
             justify="left",
             wraplength=450).pack(padx=20)

    tk.Button(janela, text="Fechar",
              command=janela.destroy).pack(pady=5)

    tk.Button(janela, text="Resetar",
              command=lambda: [resetar_campos(), janela.destroy()]).pack(pady=5)


# ---------------- JANELA PRINCIPAL ----------------

root = tk.Tk()
root.title("Simulador Genético Familiar")
root.geometry("800x600")

# ---------------- CANVAS COM SCROLL ----------------

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Scroll só funciona fora de combobox
def _on_mousewheel(event):
    if root.focus_get().__class__.__name__ != "TCombobox":
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)

# ---------------- VARIÁVEIS ----------------

olhos_vars = {}
pele_vars = {}
cabelo_vars = {}
altura_vars = {}
doencas_vars = {}

# ---------------- FORMULÁRIO ----------------

for pessoa in pessoas:
    frame = tk

    frame = tk.LabelFrame(scrollable_frame, text=pessoa, padx=10, pady=10)
    frame.pack(fill="x", padx=10, pady=5)

    olhos_vars[pessoa] = tk.StringVar()
    pele_vars[pessoa] = tk.StringVar()
    cabelo_vars[pessoa] = tk.StringVar()
    altura_vars[pessoa] = tk.StringVar()
    doencas_vars[pessoa] = {}

    ttk.Label(frame, text="Cor dos Olhos").grid(row=0, column=0)
    ttk.Combobox(frame, textvariable=olhos_vars[pessoa],
                 values=olhos_opcoes).grid(row=0, column=1)

    ttk.Label(frame, text="Cor da Pele").grid(row=1, column=0)
    ttk.Combobox(frame, textvariable=pele_vars[pessoa],
                 values=pele_opcoes).grid(row=1, column=1)

    ttk.Label(frame, text="Cor do Cabelo").grid(row=2, column=0)
    ttk.Combobox(frame, textvariable=cabelo_vars[pessoa],
                 values=cabelo_opcoes).grid(row=2, column=1)

    ttk.Label(frame, text="Altura (ex: 1.75 ou 175)").grid(row=3, column=0)
    ttk.Entry(frame, textvariable=altura_vars[pessoa]).grid(row=3, column=1)

    ttk.Label(frame, text="Doenças").grid(row=4, column=0)

    col = 1
    for doenca in doencas_lista:
        var = tk.BooleanVar()
        doencas_vars[pessoa][doenca] = var
        ttk.Checkbutton(frame, text=doenca, variable=var)\
            .grid(row=4, column=col, sticky="w")
        col += 1

# ---------------- BOTÃO CALCULAR ----------------

tk.Button(scrollable_frame, text="Calcular",
          bg="#4CAF50",
          fg="white",
          font=("Arial", 12),
          command=calcular).pack(pady=20)

# ---------------- RODAPÉ PROFISSIONAL ----------------

footer = tk.Frame(root, bg="#EAEAEA", height=30)
footer.pack(side="bottom", fill="x")

ano_atual = datetime.now().year

tk.Label(
    footer,
    text=f"Simulador Genético Familiar v1.0  |  Desenvolvido por Fernando Amorim © {ano_atual}",
    bg="#EAEAEA",
    fg="#555555",
    font=("Arial", 8)
).pack(pady=5)

# ---------------- INICIAR ----------------

root.mainloop()


