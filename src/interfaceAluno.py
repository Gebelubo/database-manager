import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_alunos,
    inserir_aluno,
    buscar_aluno_por_id,
    atualizar_aluno,
    remover_aluno,
    buscar_alunos_por_substring,
    buscar_aluno_por_id
)

def iniciar_interface():
    janela = tk.Tk()
    janela.title("Sistema de Cursos")
    janela.geometry("600x500")

    main_frame = tk.Frame(janela)
    main_frame.pack(pady=10)

    # Campo de ID (inicialmente oculto)
    entry_id = tk.Entry(main_frame)
    label_id = tk.Label(main_frame, text="ID")
    def mostrar_id():
        label_id.grid(row=0, column=0, sticky="e")
        entry_id.grid(row=0, column=1)
    def ocultar_id():
        label_id.grid_remove()
        entry_id.grid_remove()

    # Campos de entrada restantes (ajuste as linhas conforme o ID)
    tk.Label(main_frame, text="Nome").grid(row=1, column=0, sticky="e")  # obrigatório
    entry_nome = tk.Entry(main_frame)
    entry_nome.grid(row=1, column=1)

    tk.Label(main_frame, text="Email").grid(row=2, column=0, sticky="e")  # obrigatório
    entry_email = tk.Entry(main_frame)
    entry_email.grid(row=2, column=1)

    tk.Label(main_frame, text="Data Nascimento (opcional)").grid(row=3, column=0, sticky="e")
    entry_data_nascimento = tk.Entry(main_frame)
    entry_data_nascimento.grid(row=3, column=1)

    tk.Label(main_frame, text="Telefone (opcional)").grid(row=4, column=0, sticky="e")
    entry_telefone = tk.Entry(main_frame)
    entry_telefone.grid(row=4, column=1)

    tk.Label(main_frame, text="Endereço (opcional)").grid(row=5, column=0, sticky="e")
    entry_endereco = tk.Entry(main_frame)
    entry_endereco.grid(row=5, column=1)

    tk.Label(main_frame, text="Status (opcional)").grid(row=6, column=0, sticky="e")
    entry_status = tk.Entry(main_frame)
    entry_status.grid(row=6, column=1)

    # Listbox
    lista = tk.Listbox(janela, width=80, height=15)
    lista.pack(pady=10)

    # Funções
    def mostrar_alunos():
        lista.delete(0, tk.END)
        for aluno in listar_alunos():
            lista.insert(tk.END, f"ID: {aluno[0]} --- Nome: {aluno[1]} --- Email: {aluno[2]}")

    def adicionar_aluno():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        data_nascimento = entry_data_nascimento.get().strip()
        telefone = entry_telefone.get().strip()
        endereco = entry_endereco.get().strip()
        status = entry_status.get().strip() or "ativo"

        if not nome or not email:
            messagebox.showwarning("Atenção", "Nome e Email são obrigatórios.")
            return

        try:
            inserir_aluno(nome, email, telefone, endereco, status, data_nascimento)
            mostrar_alunos()
            messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def atualizar_aluno_gui():
        id_str = entry_id.get().strip()
        try:
            id_aluno = int(id_str)
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
            return

        nome = entry_nome.get().strip()
        email = entry_email.get().strip()

        if not nome and not email:
            messagebox.showwarning("Atenção", "Informe ao menos Nome ou Email para atualizar.")
            return

        try:
            if not buscar_aluno_por_id(id_aluno):
                messagebox.showerror("Erro", "Aluno com esse ID não existe.")
                return

            atualizar_aluno(id_aluno, nome=nome if nome else None, email=email if email else None)
            mostrar_alunos()
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_aluno_gui():
        id_str = entry_id.get().strip()
        try:
            id_aluno = int(id_str)
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
            return

        try:
            if not buscar_aluno_por_id(id_aluno):
                messagebox.showwarning("Atenção", "Aluno com esse ID não existe.")
                return

            remover_aluno(id_aluno)
            mostrar_alunos()
            messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def buscar_aluno():
        id_str = entry_id.get().strip()
        if not id_str:
            messagebox.showwarning("Atenção", "Digite um ID para buscar.")
            return
        try:
            id_aluno = int(id_str)
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
            return
        try:
            aluno = buscar_aluno_por_id(id_aluno)
            lista.delete(0, tk.END)
            if aluno:
                lista.insert(tk.END, f"ID Aluno: {aluno[0]}")
                lista.insert(tk.END, f"Nome: {aluno[1]}")
                lista.insert(tk.END, f"Email: {aluno[2]}")
                lista.insert(tk.END, f"Telefone: {aluno[3] if aluno[3] else 'Não informado'}")
                lista.insert(tk.END, f"Endereço: {aluno[4] if aluno[4] else 'Não informado'}")
                lista.insert(tk.END, f"Status: {aluno[5] if aluno[5] else 'Não informado'}")
                lista.insert(tk.END, f"Data Nascimento: {aluno[6] if aluno[6] else 'Não informado'}")
            else:
                messagebox.showinfo("Resultado", "Aluno não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def buscar_por_substring():
        substring = entry_nome.get().strip()
        if not substring:
            messagebox.showwarning("Atenção", "Digite uma substring no campo Nome para buscar.")
            return
        try:
            resultados = buscar_alunos_por_substring(substring)
            lista.delete(0, tk.END)
            for aluno in resultados:
                lista.insert(tk.END, f"ID: {aluno[0]} - Nome: {aluno[1]} - Email: {aluno[2]}")
            if not resultados:
                messagebox.showinfo("Resultado", "Nenhum aluno encontrado com essa substring.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    # Frame dos botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Botões
    tk.Button(frame_botoes, text="Adicionar", width=12, command=lambda: [ocultar_id(), adicionar_aluno()]).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Atualizar", width=12, command=lambda: [mostrar_id(), atualizar_aluno_gui()]).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Remover", width=12, command=lambda: [mostrar_id(), remover_aluno_gui()]).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="Buscar por ID", width=12, command=lambda: [mostrar_id(), buscar_aluno()]).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(frame_botoes, text="Buscar por Nome", width=12, command=buscar_por_substring).grid(row=1, column=1, padx=5, pady=5)

    # Ao iniciar, oculte o campo ID
    ocultar_id()
    # Mostrar alunos ao iniciar
    mostrar_alunos()
    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()
