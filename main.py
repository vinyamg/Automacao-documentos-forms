import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from modulos.automatizadorXI import automata2
from modulos.automatizadorXII import automata
from modulos.automata_dca import dca
from modulos.automatizadorIII import automata3
import re

def abrir_nova_janela(option, tipo):
    opcao_tipo = opcao.get()
    pdf = caminho_arquivo.get()
    nova_janela = tk.Toplevel(janela)
    nova_janela.resizable(False, False)
    nova_janela.title("Configuração")
    nova_janela.geometry("300x290")
    if option == "DCA":
        def executar():
            microbiano = var1.get()  # 1 se marcado, 0 se não
            termolabeis = var2.get()
            retnoicas = var3.get()
            crf_num = crf.get()
            crt_validacao = re.search(r'[a-zA-Z]', crf_num)
            if crt_validacao:
                messagebox.showwarning("Aviso", "O CRF é somente numeros!")
                return

            horario_num = horario.get()
            nova_janela.destroy()
            dca(pdf, microbiano, termolabeis, crf_num, horario_num, retnoicas)

        instrucao = tk.Label(nova_janela, text='Digite o CRF')
        instrucao.pack()
        crf = tk.Entry(nova_janela, width=30)
        crf.pack(pady=10)
        instrucao = tk.Label(nova_janela, text='Digite o Horario')
        instrucao.pack()
        horario = tk.Entry(nova_janela, width=42)
        horario.pack(pady=10)
        horario.insert(0, "De segunda a sexta, das 00h as 00h, de sábado, 00h as 00h")
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        var3 = tk.IntVar()

        cb1 = tk.Checkbutton(nova_janela, text="Microbiano", variable=var1)
        cb2 = tk.Checkbutton(nova_janela, text="Termolábeis", variable=var2)
        cb3 = tk.Checkbutton(nova_janela, text="Retnóicas", variable=var3)

        cb1.pack(pady=5)
        cb2.pack(pady=5)
        cb3.pack(pady=5)

        tk.Button(nova_janela, text="Enviar", command=lambda: executar()).pack(pady=10)
    elif option == "Anexo":
        nova_janela.geometry("300x390")
        def executar_anexo():

            vre_coleta = vre.get()
            decisao = opcao_selecionada.get()
            nova_janela.destroy()
            if tipo == "anexoXI":
                automata2(pdf, opcao_tipo, decisao, vre_coleta)
            elif tipo == "anexoXII":
                automata(pdf, opcao_tipo, vre_coleta)
            elif tipo == "anexoIII":
                automata3(pdf, opcao_tipo, decisao)
        instrucao = tk.Label(nova_janela, text='Digite o VRE(se aplicável)')
        instrucao.pack()
        vre = tk.Entry(nova_janela, width=30)
        vre.pack(pady=10)

        instrucao = tk.Label(nova_janela, text='Caso seja alteração:')
        instrucao.pack()
        opcao_selecionada = tk.StringVar(value="Nenhum")
        frame_opcoes = tk.LabelFrame(nova_janela, text="Selecione UMA opção")
        frame_opcoes.pack(pady=15)

        escolhas = ['Nenhum', 'Assunção(Tecnico)', 'Baixa(Tecnico)', 'Responsavel legal', 'Razão Social', 'Endereço', 'Nome Fantasia']
        for i in escolhas:
            tk.Radiobutton(
                frame_opcoes,
                text=i,
                variable=opcao_selecionada,
                value=i
            ).pack(anchor="w")

        tk.Button(nova_janela, text="Enviar", command=lambda: executar_anexo()).pack(pady=10)


def escolher_arquivo():
    arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("arquivos pdf", "*.pdf")]
    )
    if arquivo:
        caminho_arquivo.set(arquivo)


def confirmar():
    opcao_tipo = opcao.get()
    if not caminho_arquivo.get():
        messagebox.showwarning("Aviso", "Selecione um pdf!")
        return

    if not opcao_selecionada.get():
        messagebox.showwarning("Aviso", "Selecione uma opção de formulário!")
        return
    if opcao_tipo == 'Selecione a opção':
        messagebox.showwarning("Aviso", "Selecione uma opção!")
        return

    messagebox.showinfo(
        "Resumo",
        f"Arquivo:\n{caminho_arquivo.get()}\n\n"
        f"Opção escolhida: {opcao_selecionada.get()}\n"
        f"Aperte 'Ok' para confirmar"
    )

    if opcao_selecionada.get() == 'DCA':
        abrir_nova_janela('DCA', 't')
    elif opcao_selecionada.get() == 'AnexoXI':
        abrir_nova_janela("Anexo", "anexoXI")
    elif opcao_selecionada.get() == 'AnexoXII':
        abrir_nova_janela("Anexo", "anexoXII")
    elif opcao_selecionada.get() == 'AnexoIII':
        abrir_nova_janela("Anexo", "anexoIII")

# Janela principal
janela = tk.Tk()
janela.resizable(False, False)
janela.title("Selecionar pdf e formulário")
janela.geometry("450x300")

caminho_arquivo = tk.StringVar()
opcao_selecionada = tk.StringVar(value="")

tk.Button(janela, text="Selecionar Pdf", command=escolher_arquivo).pack(pady=10)
tk.Label(janela, textvariable=caminho_arquivo, wraplength=400).pack()

frame_opcoes = tk.LabelFrame(janela, text="Selecione UMA opção")
frame_opcoes.pack(pady=15)

formularios = ['DCA', 'AnexoXI', 'AnexoXII', 'AnexoIII']
for i in formularios:
    tk.Radiobutton(
        frame_opcoes,
        text=i,
        variable=opcao_selecionada,
        value=i
    ).pack(anchor="w")

opcao = tk.StringVar(value="Selecione a opção")

combo = ttk.Combobox(
    janela,
    textvariable=opcao,
    values=["Inicial", "Renovação", "Alteração", "Cancelamento"],
    state="readonly"
)

combo.pack()

tk.Button(janela, text="Confirmar", command=confirmar).pack(pady=10)

janela.mainloop()