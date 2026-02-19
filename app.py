import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ---------------- CONFIGURAÇÃO ----------------

PESSOAS = [
    "Pai", "Mãe",
    "Avô Paterno", "Avó Paterna",
    "Avô Materno", "Avó Materna"
]

DOENCAS = [
    "Diabetes",
    "Hipertensão",
    "Câncer",
    "Doença Cardíaca",
    "Alzheimer",
    "Depressão",
    "Asma",
    "Colesterol Alto",
    "Não possui nenhuma das doenças listadas",
    "Não sei",
]

OLHOS_OPCOES = ["Castanho", "Azul", "Verde", "Não sei"]
PELE_OPCOES = ["Clara", "Morena", "Escura", "Não sei"]
CABELO_OPCOES = ["Preto", "Castanho", "Loiro", "Ruivo", "Não sei"]


# ---------------- UTILIDADES ----------------

def converter_altura(valor: str | None):
    """
    Aceita:
    - "1.75" / "1,75" -> 1.75
    - "175" -> 1.75
    - "155" -> 1.55
    """
    if valor is None:
        return None

    valor = str(valor).strip()
    if not valor:
        return None

    valor = valor.replace(",", ".")

    # Caso "1.75"
    if "." in valor:
        try:
            v = float(valor)
            # validações básicas
            if 0.5 <= v <= 2.5:
                return v
            return v
        except ValueError:
            return None

    # Caso "175"/"155"
    if valor.isdigit() and len(valor) in (3, 4):
        try:
            cm = int(valor)
            return cm / 100.0
        except ValueError:
            return None

    # Última tentativa
    try:
        return float(valor)
    except ValueError:
        return None


def probabilidades_duas_fontes(valor_pai: str, valor_mae: str):
    """
    Modelo simplificado:
    - mesmo valor -> 100%
    - diferentes -> 50%/50%
    - 'Não sei' ou vazio -> None
    """
    if (not valor_pai) or (not valor_mae):
        return None
    if valor_pai == "Não sei" or valor_mae == "Não sei":
        return None

    if valor_pai == valor_mae:
        return {valor_pai: 100}
    return {valor_pai: 50, valor_mae: 50}


def formatar_probabilidades(titulo: str, probs: dict | None):
    """
    Retorna texto em linhas, no estilo:
    Olhos:
      Castanho: 50%
      Azul: 50%
    """
    if probs is None:
        return f"{titulo}: informação insuficiente"

    itens = sorted(probs.items(), key=lambda x: (-x[1], x[0]))
    linhas = [f"{titulo}:"]
    for nome, pct in itens:
        linhas.append(f"  {nome}: {pct}%")
    return "\n".join(linhas)


# ---------------- AÇÕES ----------------

def resetar_campos():
    for pessoa in PESSOAS:
        olhos_vars[pessoa].set("")
        pele_vars[pessoa].set("")
        cabelo_vars[pessoa].set("")
        altura_vars[pessoa].set("")
        for d in DOENCAS:
            doencas_vars[pessoa][d].set(False)


def mostrar_resultado(texto: str):
    """
    Janela de resultado com layout clean (como seu print),
    com botões Fechar e Resetar.
    """
    janela = tk.Toplevel(root)
    janela.title("Resultado")
    janela.geometry("560x380")
    janela.resizable(False, False)

    tk.Label(
        janela,
        text="Resultado da Simulação",
        font=("Arial", 14, "bold")
    ).pack(pady=(14, 10))

    # Conteúdo central com alinhamento à esquerda (sem Text grande, pra ficar clean)
    lbl = tk.Label(
        janela,
        text=texto,
        justify="left",
        anchor="w",
        font=("Arial", 10)
    )
    lbl.pack(padx=28, pady=8)

    tk.Button(janela, text="Fechar", width=10, command=janela.destroy).pack(pady=(10, 6))
    tk.Button(
        janela,
        text="Resetar",
        width=10,
        command=lambda: (resetar_campos(), janela.destroy())
    ).pack(pady=(0, 10))


def calcular():
    # --------- Características (Pais) ---------
    pai_olhos = olhos_vars["Pai"].get()
    mae_olhos = olhos_vars["Mãe"].get()

    pai_pele = pele_vars["Pai"].get()
    mae_pele = pele_vars["Mãe"].get()

    pai_cabelo = cabelo_vars["Pai"].get()
    mae_cabelo = cabelo_vars["Mãe"].get()

    probs_olhos = probabilidades_duas_fontes(pai_olhos, mae_olhos)
    probs_pele = probabilidades_duas_fontes(pai_pele, mae_pele)
    probs_cabelo = probabilidades_duas_fontes(pai_cabelo, mae_cabelo)

    # --------- Altura (média dos pais) ---------
    alt_pai = converter_altura(altura_vars["Pai"].get())
    alt_mae = converter_altura(altura_vars["Mãe"].get())

    if alt_pai is not None and alt_mae is not None:
        altura_est = (alt_pai + alt_mae) / 2
        altura_txt = f"Altura estimada: {altura_est:.2f} m"
    else:
        altura_txt = "Altura estimada: informação insuficiente"

    # --------- Doenças (percentual por doença) ---------
    total = len(PESSOAS)
    nao_sabe_count = 0

    # doenças "reais" (sem os controles)
    doencas_reais = [d for d in DOENCAS if d not in ("Não sei", "Não possui nenhuma das doenças listadas")]

    contagem = {d: 0 for d in doencas_reais}

    for pessoa in PESSOAS:
        if doencas_vars[pessoa]["Não sei"].get():
            nao_sabe_count += 1

        if doencas_vars[pessoa]["Não possui nenhuma das doenças listadas"].get():
            # ignora outras seleções dessa pessoa
            continue

        for d in doencas_reais:
            if doencas_vars[pessoa][d].get():
                contagem[d] += 1

    linhas_doencas = []
    for d in doencas_reais:
        if contagem[d] > 0:
            pct = round((contagem[d] / total) * 100, 1)
            linhas_doencas.append(f"{d}: {pct}%")

    if not linhas_doencas:
        doencas_txt = "Risco hereditário:\n  Nenhuma doença relevante informada."
    else:
        doencas_txt = "Risco hereditário:\n  " + "\n  ".join(linhas_doencas)

    if nao_sabe_count > 0:
        doencas_txt += f"\n\nObs.: {nao_sabe_count} familiares marcados como 'Não sei'."

    # --------- Monta texto final (estilo clean) ---------
    texto_final = (
        f"{formatar_probabilidades('Olhos', probs_olhos)}\n\n"
        f"{formatar_probabilidades('Pele', probs_pele)}\n\n"
        f"{formatar_probabilidades('Cabelo', probs_cabelo)}\n\n"
        f"{altura_txt}\n\n"
        f"{doencas_txt}\n\n"
        "Aviso: simulação educacional. Não substitui avaliação médica."
    )

    mostrar_resultado(texto_final)


# ---------------- UI PRINCIPAL ----------------

root = tk.Tk()
root.title("Simulador Genético Familiar")
root.geometry("920x640")

# Canvas + Scroll
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Scroll com mouse: não rola a página se estiver em Combobox
def _on_mousewheel(event):
    widget_focado = root.focus_get()
    if isinstance(widget_focado, ttk.Combobox):
        return
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


root.bind_all("<MouseWheel>", _on_mousewheel)

# Variáveis
olhos_vars = {}
pele_vars = {}
cabelo_vars = {}
altura_vars = {}
doencas_vars = {}

# Formulário
for pessoa in PESSOAS:
    frame = tk.LabelFrame(scrollable_frame, text=pessoa, padx=10, pady=10)
    frame.pack(fill="x", padx=10, pady=6)

    olhos_vars[pessoa] = tk.StringVar()
    pele_vars[pessoa] = tk.StringVar()
    cabelo_vars[pessoa] = tk.StringVar()
    altura_vars[pessoa] = tk.StringVar()
    doencas_vars[pessoa] = {}

    ttk.Label(frame, text="Cor dos olhos").grid(row=0, column=0, sticky="w")
    ttk.Combobox(
        frame,
        textvariable=olhos_vars[pessoa],
        values=OLHOS_OPCOES,
        state="readonly",
        width=18
    ).grid(row=0, column=1, sticky="w", padx=(6, 0))

    ttk.Label(frame, text="Cor da pele").grid(row=1, column=0, sticky="w")
    ttk.Combobox(
        frame,
        textvariable=pele_vars[pessoa],
        values=PELE_OPCOES,
        state="readonly",
        width=18
    ).grid(row=1, column=1, sticky="w", padx=(6, 0))

    ttk.Label(frame, text="Cor do cabelo").grid(row=2, column=0, sticky="w")
    ttk.Combobox(
        frame,
        textvariable=cabelo_vars[pessoa],
        values=CABELO_OPCOES,
        state="readonly",
        width=18
    ).grid(row=2, column=1, sticky="w", padx=(6, 0))

    ttk.Label(frame, text="Altura (ex: 1.75 ou 175)").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=altura_vars[pessoa], width=20).grid(row=3, column=1, sticky="w", padx=(6, 0))

    ttk.Label(frame, text="Doenças").grid(row=4, column=0, sticky="nw")

    col = 1
    for d in DOENCAS:
        var = tk.BooleanVar()
        doencas_vars[pessoa][d] = var
        ttk.Checkbutton(frame, text=d, variable=var).grid(row=4, column=col, sticky="w", padx=4)
        col += 1

# Botão calcular
tk.Button(
    scrollable_frame,
    text="Calcular",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12),
    command=calcular
).pack(pady=18)

# Rodapé (fixo, fora do canvas)
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

root.mainloop()
