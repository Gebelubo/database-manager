import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_matriculas,
    inserir_matricula,
    buscar_matricula,
    atualizar_matricula,
    remover_matricula,
    listar_alunos,
    listar_disciplinas
)

def iniciar_interface_matricula():
    janela = tk.Toplevel()
    janela.title("Gestão de Matrículas")
    janela.geometry("700x520")

    # Frame principal
    main_frame = tk.Frame(janela)
    main_frame.pack(pady=10)

    # Campos de entrada
    entry_semestre = tk.Entry(main_frame)
    entry_nota = tk.Entry(main_frame)
    entry_status = tk.Entry(main_frame)

    # Layout dos campos
    tk.Label(main_frame, text="Semestre").grid(row=2, column=0, sticky="e")  # obrigatório
    entry_semestre.grid(row=2, column=1)

    tk.Label(main_frame, text="Nota (opcional)").grid(row=3, column=0, sticky="e")
    entry_nota.grid(row=3, column=1)

    tk.Label(main_frame, text="Status (opcional)").grid(row=4, column=0, sticky="e")
    entry_status.grid(row=4, column=1)
    lista = tk.Listbox(janela, width=90, height=15)
    lista.pack(pady=10)

    # Labels e entries SEMPRE visíveis para ID Aluno e ID Disciplina
    label_id_aluno = tk.Label(main_frame, text="ID Aluno")
    entry_id_aluno = tk.Entry(main_frame)
    label_id_aluno.grid(row=0, column=0, sticky="e")
    entry_id_aluno.grid(row=0, column=1)

    label_id_disc = tk.Label(main_frame, text="ID Disciplina")
    entry_id_disc = tk.Entry(main_frame)
    label_id_disc.grid(row=1, column=0, sticky="e")
    entry_id_disc.grid(row=1, column=1)

    # Não use ocultar_ids() ou mostrar_ids() para esses campos!
    # Eles devem estar sempre visíveis para todas as operações.

    # Funções de operação
    def mostrar_matriculas():
        lista.delete(0, tk.END)
        for mat in listar_matriculas():
            nota = mat[4] if mat[4] is not None else "N/A"
            lista.insert(tk.END, f"ID Matrícula: {mat[0]} --- Aluno: {mat[1]} --- Disciplina: {mat[2]} --- Semestre: {mat[3]} --- Nota: {nota} --- Status: {mat[5] if mat[5] else 'N/A'}")

    def adicionar_matricula():
        try:
            id_aluno = int(entry_id_aluno.get())
            id_disc = int(entry_id_disc.get())
            semestre = entry_semestre.get().strip()
            if not semestre:
                messagebox.showwarning("Atenção", "Semestre é obrigatório.")
                return
            nota_str = entry_nota.get().strip()
            nota = float(nota_str) if nota_str else None
            status = entry_status.get().strip() or None  # Pega o status ou None se vazio

            inserir_matricula(id_aluno, id_disc, semestre, nota, status)
            mostrar_matriculas()
            messagebox.showinfo("Sucesso", "Matrícula adicionada com sucesso!")

            # Limpa os campos após adição
            entry_id_aluno.delete(0, tk.END)
            entry_id_disc.delete(0, tk.END)
            entry_semestre.delete(0, tk.END)
            entry_nota.delete(0, tk.END)
            entry_status.delete(0, tk.END)  # Limpa o campo de status também
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros e nota deve ser número decimal válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def atualizar_matricula_gui():
        try:
            id_aluno = int(entry_id_aluno.get())
            id_disc = int(entry_id_disc.get())
            semestre = entry_semestre.get().strip() or None
            nota_str = entry_nota.get().strip()
            nota = float(nota_str) if nota_str else None
            status = entry_status.get().strip() or None  # Pega o status ou None se vazio

            if semestre is None and nota is None and status is None:
                messagebox.showwarning("Atenção", "Informe ao menos semestre, nota ou status para atualizar.")
                return

            atualizar_matricula(id_aluno, id_disc, semestre=semestre, nota=nota, status=status)
            mostrar_matriculas()
            messagebox.showinfo("Sucesso", "Matrícula atualizada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros e nota deve ser um número decimal.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def remover_matricula_gui():
        try:
            id_aluno = int(entry_id_aluno.get())
            id_disc = int(entry_id_disc.get())
            remover_matricula(id_aluno, id_disc)
            mostrar_matriculas()
            messagebox.showinfo("Sucesso", "Matrícula removida com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def buscar_matricula_gui():
        try:
            id_aluno_str = entry_id_aluno.get().strip()
            id_disc_str = entry_id_disc.get().strip()

            if not id_aluno_str or not id_disc_str:
                messagebox.showwarning("Atenção", "Digite ambos IDs (Aluno e Disciplina) para buscar.")
                return

            id_aluno = int(id_aluno_str)
            id_disc = int(id_disc_str)

            mat = buscar_matricula(id_aluno, id_disc)
            lista.delete(0, tk.END)
            if mat:
                nota = mat[4] if mat[4] is not None else "N/A"
                lista.insert(tk.END, f"ID Matricula: {mat[0]}")
                lista.insert(tk.END, f"Aluno: {mat[1]}")
                lista.insert(tk.END, f"Disciplina: {mat[2]}")
                lista.insert(tk.END, f"Semestre: {mat[3]}")
                lista.insert(tk.END, f"Nota: {nota}")
                lista.insert(tk.END, f"Status: {mat[5] if mat[5] else 'N/A'}")
            else:
                messagebox.showinfo("Resultado", "Matrícula não encontrada.")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    # Frame de botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Botões de ação
    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", width=12, command=adicionar_matricula)
    btn_adicionar.grid(row=0, column=0, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", width=12, command=atualizar_matricula_gui)
    btn_atualizar.grid(row=0, column=1, padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", width=12, command=remover_matricula_gui)
    btn_remover.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botoes, text="Buscar", width=12, command=buscar_matricula_gui)
    btn_buscar.grid(row=1, column=0, padx=5, pady=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Todos", width=12, command=mostrar_matriculas)
    btn_listar.grid(row=1, column=1, padx=5, pady=5)

    # Mostra as matrículas ao iniciar
    mostrar_matriculas()

if __name__ == "__main__":
    iniciar_interface_matricula()
    tk.mainloop()