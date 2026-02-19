import tkinter as tk
from tkinter import ttk
import random

# ---------------- FUNÇÕES ---------------- #

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

        for doenca in doencas_vars[pessoa]:
            doencas_vars[pessoa][doenca].set(False)


def mostrar_resultado(texto):
    janela = tk.Toplevel(root)
    janela.title("Resultado")
    janela.geometry("500x500")

    texto_widget = tk.Text(janela, wrap="word")
    texto_widget.insert("1.0", texto)
    texto_widget.config(state="disabled")
    texto_widget.pack(expand=True, fill="both")

    frame_botoes = ttk.Frame(janela)
    frame_botoes.pack(pady=10)

    ttk.Button(frame_botoes, text="Fechar", command=janela.destroy).pack(side="left", padx=10)
    ttk.Button(frame_botoes, text="Resetar Tudo", command=lambda: [resetar_campos(), janela.destroy()]).pack(side="left", padx=10)


def calcular():
    try:
        resultado = "\n=== RESULTADO ESTIMADO ===\n\n"

        # ---------------- OLHOS ---------------- #
        olhos_pai = olhos_vars["Pai"].get()
        olhos_mae = olhos_vars["Mãe"].get()

        if olhos_pai == olhos_mae:
            resultado += f"Cor dos olhos provável: {olhos_pai}\n"
        elif "Não sei" in [olhos_pai, olhos_mae]:
            resultado += "Cor dos olhos: informação insuficiente\n"
        else:
            resultado += f"Cor dos olhos provável: {random.choice([olhos_pai, olhos_mae])}\n"

        # ---------------- PELE ---------------- #
        pele_pai = pele_vars["Pai"].get()
        pele_mae = pele_vars["Mãe"].get()

        if pele_pai == pele_mae:
            resultado += f"Tom de pele provável: {pele_pai}\n"
        elif "Não sei" in [pele_pai, pele_mae]:
            resultado += "Tom de pele: informação insuficiente\n"
        else:
            resultado += f"Tom intermediário entre {pele_pai} e {pele_mae}\n"

        # ---------------- CABELO ---------------- #
        cabelo_pai = cabelo_vars["Pai"].get()
        cabelo_mae = cabelo_vars["Mãe"].get()

        if cabelo_pai == cabelo_mae:
            resultado += f"Cor do cabelo provável: {cabelo_pai}\n"
        elif "Não sei" in [cabelo_pai, cabelo_mae]:
            resultado += "Cor do cabelo: informação insuficiente\n"
        else:
            resultado += f"Possível mistura entre {cabelo_pai} e {cabelo_mae}\n"

        # ---------------- ALTURA ---------------- #
        altura_pai = converter_altura(altura_vars["Pai"].get())
        altura_mae = converter_altura(altura_vars["Mãe"].get())

        if altura_pai and altura_mae:
            altura_media = (altura_pai + altura_mae) / 2
            resultado += f"Altura estimada: {round(altura_media,2)} m\n"
        else:
            resultado += "Altura: informação insuficiente\n"

        # ---------------- DOENÇAS ---------------- #
        resultado += "\nRisco baseado no histórico familiar:\n"

        todas_doencas = {}

        for pessoa in doencas_vars:

            if doencas_vars[pessoa]["Não possui nenhuma das doenças listadas"].get():
                continue

            for doenca, var in doencas_vars[pessoa].items():
                if var.get() and doenca not in ["Não sei", "Não possui nenhuma das doenças listadas"]:
                    todas_doencas[doenca] = todas_doencas.get(doenca, 0) + 1

        if todas_doencas:
            for doenca, qtd in todas_doencas.items():
                risco = round((qtd / len(pessoas)) * 100, 1)
                resultado += f"- {doenca}: {qtd} familiares ({risco}%)\n"
        else:
            resultado += "Nenhuma doença relevante informada.\n"

        resultado += "\n⚠ Modelo educacional simplificado."

        mostrar_resultado(resultado)

    except:
        mostrar_resultado("Erro no preenchimento dos dados.")

# ---------------- JANELA PRINCIPAL ---------------- #

root = tk.Tk()
root.title("Analisador Genético Familiar")
root.geometry("750x650")

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = ttk.Frame(canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def _on_mousewheel(event):
    widget_focado = root.focus_get()

    # Se estiver focado em Combobox, não faz scroll da página
    if isinstance(widget_focado, ttk.Combobox):
        return

    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)


canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ---------------- DADOS ---------------- #

pessoas = [
    "Pai", "Mãe",
    "Avô Paterno", "Avó Paterna",
    "Avô Materno", "Avó Materna"
]

cores_olhos = ["Castanho", "Azul", "Verde", "Não sei"]
cores_pele = ["Clara", "Morena", "Escura", "Não sei"]
cores_cabelo = ["Preto", "Castanho", "Loiro", "Ruivo", "Não sei"]

lista_doencas = [
    "Diabetes Tipo 1",
    "Diabetes Tipo 2",
    "Hipertensão",
    "Câncer",
    "Cardiopatia",
    "AVC",
    "Alzheimer",
    "Parkinson",
    "Asma",
    "Depressão",
    "Ansiedade",
    "Colesterol Alto",
    "Obesidade",
    "Doença Autoimune",
    "Tireoidite",
    "Não sei",
    "Não possui nenhuma das doenças listadas"
]

olhos_vars = {}
pele_vars = {}
cabelo_vars = {}
altura_vars = {}
doencas_vars = {}

# ---------------- CAMPOS ---------------- #

for pessoa in pessoas:

    frame = ttk.LabelFrame(scroll_frame, text=pessoa)
    frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame, text="Olhos:").grid(row=0, column=0)
    olhos_vars[pessoa] = ttk.Combobox(frame, values=cores_olhos)
    olhos_vars[pessoa].grid(row=0, column=1)

    ttk.Label(frame, text="Pele:").grid(row=1, column=0)
    pele_vars[pessoa] = ttk.Combobox(frame, values=cores_pele)
    pele_vars[pessoa].grid(row=1, column=1)

    ttk.Label(frame, text="Cabelo:").grid(row=2, column=0)
    cabelo_vars[pessoa] = ttk.Combobox(frame, values=cores_cabelo)
    cabelo_vars[pessoa].grid(row=2, column=1)

    ttk.Label(frame, text="Altura (m):").grid(row=3, column=0)
    altura_vars[pessoa] = ttk.Combobox(
        frame,
        values=[round(x/100,2) for x in range(100, 211)]
    )
    altura_vars[pessoa].grid(row=3, column=1)

    ttk.Label(frame, text="Doenças:").grid(row=4, column=0)

    doencas_vars[pessoa] = {}
    col = 1
    for doenca in lista_doencas:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame, text=doenca, variable=var)
        chk.grid(row=4, column=col)
        doencas_vars[pessoa][doenca] = var
        col += 1

ttk.Button(scroll_frame, text="Calcular Probabilidades", command=calcular).pack(pady=20)

root.mainloop()
