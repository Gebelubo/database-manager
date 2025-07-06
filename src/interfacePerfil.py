import tkinter as tk
from tkinter import messagebox
from banco import BancoDados

def iniciar_interface():
    bd = BancoDados()
    janela = tk.Toplevel()
    janela.title("Gerenciar Perfil de Professor")
    janela.geometry("400x300")

    tk.Label(janela, text="ID Professor").grid(row=0, column=0, sticky="e")
    entry_id_prof = tk.Entry(janela)
    entry_id_prof.grid(row=0, column=1)

    tk.Label(janela, text="Bio (opcional)").grid(row=1, column=0, sticky="e")
    entry_bio = tk.Entry(janela)
    entry_bio.grid(row=1, column=1)

    tk.Label(janela, text="LinkedIn (opcional)").grid(row=2, column=0, sticky="e")
    entry_linkedin = tk.Entry(janela)
    entry_linkedin.grid(row=2, column=1)

    def adicionar_perfil():
        id_prof = entry_id_prof.get().strip()
        bio = entry_bio.get().strip() or None
        linkedin = entry_linkedin.get().strip() or None
        if not id_prof:
            messagebox.showwarning("Atenção", "Informe o ID do Professor.")
            return
        if bd.inserir_perfil(int(id_prof), bio, linkedin):
            messagebox.showinfo("Sucesso", "Perfil cadastrado!")
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar perfil.")

    def buscar_perfil():
        id_prof = entry_id_prof.get().strip()
        if not id_prof:
            messagebox.showwarning("Atenção", "Informe o ID do Professor.")
            return
        perfil = bd.buscar_perfil_por_professor(int(id_prof))
        if perfil:
            entry_bio.delete(0, tk.END)
            entry_linkedin.delete(0, tk.END)
            entry_bio.insert(0, perfil[2] or "")
            entry_linkedin.insert(0, perfil[3] or "")
        else:
            messagebox.showinfo("Info", "Perfil não encontrado.")

    tk.Button(janela, text="Adicionar/Atualizar", command=adicionar_perfil).grid(row=3, column=0, pady=10)
    tk.Button(janela, text="Buscar", command=buscar_perfil).grid(row=3, column=1, pady=10)