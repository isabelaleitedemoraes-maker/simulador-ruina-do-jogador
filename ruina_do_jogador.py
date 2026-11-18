import os
import random
import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def recurso(nome):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)


velocidade = 10
max_rodada = 100_000


def prob_ruina_teorica(i, N, p):
    q = 1 - p
    if i <= 0:
        return 1.0
    if i >= N:
        return 0.0
    if abs(p - q) < 1e-12:
        return (N - i) / N
    r = q / p
    if r > 1:
        return (r ** (i - N) - 1) / (r ** (-N) - 1)
    return (r ** i - r ** N) / (1 - r ** N)


def duracao_teorica(i, N, p):
    q = 1 - p
    if i <= 0 or i >= N:
        return 0.0
    if abs(p - q) < 1e-12:
        return i * (N - i)
    r = q / p
    if r > 1:
        razao = (r ** (-N) - r ** (i - N)) / (r ** (-N) - 1)
    else:
        razao = (1 - r ** i) / (1 - r ** N)
    return i / (q - p) - (N / (q - p)) * razao


def simular_partida(i, N, p):
    fortuna, rodadas = i, 0
    while 0 < fortuna < N and rodadas < max_rodada:
        fortuna += 1 if random.random() < p else -1
        rodadas += 1
    return (fortuna <= 0), rodadas


def monte_carlo(i, N, p, K):
    ruinas = 0
    total_rodadas = 0
    for _ in range(K):
        ruina, rodadas = simular_partida(i, N, p)
        ruinas += 1 if ruina else 0
        total_rodadas += rodadas
    return ruinas / K, total_rodadas / K


root = Tk()
root.title("Ruína do jogador")
larg_tela = root.winfo_screenwidth()
alt_tela = root.winfo_screenheight()
largura = min(1080, larg_tela - 40)
altura = min(1000, alt_tela - 80)
root.geometry(f"{largura}x{altura}+20+10")
root.minsize(700, 520)

painel = Frame(root)
painel.pack(pady=10)


def campo(linha, coluna, rotulo, valor_inicial=""):
    Label(painel, text=rotulo).grid(row=linha, column=coluna, sticky="e", pady=3, padx=(12, 0))
    caixa = Entry(painel, width=12)
    caixa.grid(row=linha, column=coluna + 1, padx=6, pady=3)
    caixa.insert(0, valor_inicial)
    return caixa


Label(painel, text="Configuração da simulação:",
      font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 4))

Label(painel, text="Quantidade de jogadores (1 a 10)").grid(row=1, column=0, sticky="e", pady=3, padx=(12, 0))
spin_qtd = Spinbox(painel, from_=1, to=10, width=10)
spin_qtd.grid(row=1, column=1, padx=6, pady=3)
spin_qtd.delete(0, "end")
spin_qtd.insert(0, "3")

entry_inicial = campo(1, 2, "Capital inicial (R$)", "5")
entry_meta = campo(2, 0, "Meta R$", "10")
entry_chance = campo(2, 2, "Chance de Ganhar (%)", "50")
entry_sims = campo(3, 0, "Nº de apostadores (estatísticas)", "1000")

rodape = Frame(root)
rodape.pack(side="bottom", fill="x")

fig = Figure(figsize=(6, 4), dpi=100, constrained_layout=True)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="top", pady=6, fill="both", expand=True)

linhas = []
anotacoes = []
jogadores = []
max_len = 0
ani = None
stats_visivel = False


def init():
    for linha in linhas:
        linha.set_data([], [])
    for ann in anotacoes:
        ann.set_visible(False)
    return linhas


def resumo_final():
    partes = []
    for jogador in jogadores:
        er = jogador["fim_rodada"]
        if jogador["faliu"]:
            partes.append(f"{jogador['nome']}: faliu na rodada {er}")
        elif jogador["venceu"]:
            partes.append(f"{jogador['nome']}: chegou à meta na rodada {er}")
        else:
            partes.append(f"{jogador['nome']}: não terminou em {er} rodadas")
    return "   |   ".join(partes)


def animate(k):
    for linha, jogador, ann in zip(linhas, jogadores, anotacoes):
        y = jogador["historico"][:k]
        x = range(len(y))
        linha.set_data(x, y)
        if k - 1 >= jogador["fim_rodada"]:
            ann.set_visible(True)
    if k >= max_len:
        painel_final.config(text=resumo_final())
    return linhas


def ler_parametros():
    try:
        qtd = int(spin_qtd.get())
        fortuna_inicial = int(entry_inicial.get())
        meta = int(entry_meta.get())
        chance = int(entry_chance.get())
        n_sims = int(entry_sims.get())
    except ValueError:
        status.config(text="Todos os campos devem ser números inteiros.", fg="red")
        return None

    if not (1 <= qtd <= 10):
        status.config(text="A quantidade de jogadores deve ficar entre 1 e 10.", fg="red")
        return None
    if fortuna_inicial < 1:
        status.config(text="A fortuna inicial precisa ser pelo menos 1.", fg="red")
        return None
    if meta <= fortuna_inicial:
        status.config(text="A meta precisa ser maior que a fortuna inicial.", fg="red")
        return None
    if not (1 <= chance <= 99):
        status.config(text="A chance precisa ficar entre 1 e 99.", fg="red")
        return None
    if n_sims < 1:
        status.config(text="O nº de apostadores precisa ser pelo menos 1.", fg="red")
        return None

    return qtd, fortuna_inicial, meta, chance, n_sims, chance / 100


def iniciar():
    global ani, linhas, anotacoes, jogadores, max_len, stats_visivel

    dados = ler_parametros()
    if dados is None:
        return
    qtd, fortuna_inicial, meta, chance, n_sims, p = dados

    if ani is not None:
        try:
            ani.event_source.stop()
        except Exception:
            pass
        ani = None

    stats_visivel = False
    painel_stats.config(text="")
    btn_stats.config(text="Mostrar valores calculados")

    jogadores = []
    for k in range(qtd):
        jogadores.append({
            "nome": f"Jogador {k + 1}",
            "fortuna": fortuna_inicial,
            "historico": [fortuna_inicial],
            "jogando": True,
        })

    rodada = 0
    while any(j["jogando"] for j in jogadores) and rodada < max_rodada:
        rodada += 1
        for jogador in jogadores:
            if not jogador["jogando"]:
                continue
            if random.random() < p:
                jogador["fortuna"] += 1
            else:
                jogador["fortuna"] -= 1
            jogador["historico"].append(jogador["fortuna"])
            if jogador["fortuna"] <= 0 or jogador["fortuna"] >= meta:
                jogador["jogando"] = False

    max_len = max(len(j["historico"]) for j in jogadores)

    for jogador in jogadores:
        hist = jogador["historico"]
        jogador["fim_rodada"] = len(hist) - 1
        jogador["faliu"] = hist[-1] <= 0
        jogador["venceu"] = hist[-1] >= meta

    painel_final.config(text="")

    ax.clear()
    ax.set_xlim(0, max_len)
    ax.set_ylim(-meta * 0.05, meta * 1.08)
    ax.set_title("A ruína do jogador")
    ax.set_xlabel("rodada")
    ax.set_ylabel("fortuna (R$)")
    ax.axhline(meta, color="green", linestyle="--")
    ax.axhline(0, color="red", linestyle="--")

    linhas = []
    anotacoes = []
    for jogador in jogadores:
        (linha,) = ax.plot([], [], lw=2, label=jogador["nome"])
        linhas.append(linha)

        if jogador["faliu"]:
            cor, dy = "red", 10
        elif jogador["venceu"]:
            cor, dy = "green", -16
        else:
            cor, dy = "gray", 10
        ann = ax.annotate(
            f"rodada {jogador['fim_rodada']}",
            xy=(jogador["fim_rodada"], jogador["historico"][-1]),
            xytext=(0, dy), textcoords="offset points",
            ha="center", fontsize=8, fontweight="bold", color=cor,
            visible=False,
        )
        anotacoes.append(ann)

    if qtd <= 6:
        ax.legend(loc="upper right", fontsize=8)

    ani = FuncAnimation(fig, animate, init_func=init,
                        frames=max_len + 1, interval=velocidade,
                        blit=False, repeat=False, cache_frame_data=False)
    canvas.draw_idle()

    status.config(text="Pronto. Veja o gráfico. (Os valores só aparecem se você quiser.)",
                  fg="green")


def alternar_estatisticas():
    global stats_visivel

    if stats_visivel:
        painel_stats.config(text="")
        btn_stats.config(text="Mostrar valores calculados")
        stats_visivel = False
        status.config(text="Valores ocultados. Mostrando só o gráfico.", fg="green")
        return

    dados = ler_parametros()
    if dados is None:
        return
    _, fortuna_inicial, meta, chance, n_sims, p = dados

    status.config(text=f"Calculando com {n_sims} apostadores...", fg="green")
    root.update_idletasks()

    p_obs, dur_obs = monte_carlo(fortuna_inicial, meta, p, n_sims)
    p_teo = prob_ruina_teorica(fortuna_inicial, meta, p)
    dur_teo = duracao_teorica(fortuna_inicial, meta, p)

    texto = (
        f"Parâmetros:  capital inicial R$ {fortuna_inicial}   •   "
        f"meta R$ {meta}   •   chance de ganhar {chance}%\n"
        f"Estatísticas sobre {n_sims} apostadores\n"
        f"{'':22}{'Observado':>14}{'Teórico':>14}\n"
        f"{'Probabilidade de ruína':22}{p_obs*100:>13.1f}%{p_teo*100:>13.1f}%\n"
        f"{'Duração média (rodadas)':22}{dur_obs:>14.1f}{dur_teo:>14.1f}"
    )
    painel_stats.config(text=texto)
    btn_stats.config(text="Ocultar valores calculados")
    stats_visivel = True
    status.config(text="Compare o observado com o teórico.", fg="green")


barra = Frame(rodape)
barra.pack(pady=4)

try:
    play_btn = PhotoImage(file=recurso("play-button.png"))
    play_btn_menor = play_btn.subsample(15, 15)
    meu_botao = Button(barra, image=play_btn_menor, command=iniciar, borderwidth=0)
except Exception:
    meu_botao = Button(barra, text="▶ Jogar", command=iniciar,
                       font=("Helvetica", 16), borderwidth=0)
meu_botao.pack(side="left", padx=8)

btn_stats = Button(barra, text="Mostrar valores calculados",
                   command=alternar_estatisticas, font=("Helvetica", 11))
btn_stats.pack(side="left", padx=8)

status = Label(rodape, text="Preencha os campos e aperte play", fg="black")
status.pack(pady=2)

painel_final = Label(rodape, text="", font=("Arial", 10), fg="#333333",
                     wraplength=largura - 40, justify="center")
painel_final.pack(pady=2)

painel_stats = Label(rodape, text="", font=("Courier New", 11), justify="left")
painel_stats.pack(pady=(2, 8))


def ajustar_quebra(evento):
    if evento.widget is root:
        painel_final.config(wraplength=max(300, evento.width - 40))


root.bind("<Configure>", ajustar_quebra)

mainloop()
