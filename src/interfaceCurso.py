import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_cursos,
    inserir_curso,
    buscar_curso_por_id,
    atualizar_curso,
    remover_curso
)

def iniciar_interface_curso():
    janela = tk.Toplevel()
    janela.title("Gestão de Cursos")
    janela.geometry("600x450")

    # Frame principal
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

    # Campos de entrada
    entry_nome = tk.Entry(main_frame)
    entry_descricao = tk.Entry(main_frame)
    entry_carga = tk.Entry(main_frame)

    # Layout dos campos
    tk.Label(main_frame, text="Nome").grid(row=1, column=0, sticky="e")  # obrigatório
    entry_nome.grid(row=1, column=1)

    tk.Label(main_frame, text="Carga Horária").grid(row=3, column=0, sticky="e")  # obrigatório
    entry_carga.grid(row=3, column=1)

    tk.Label(main_frame, text="Descrição (opcional)").grid(row=2, column=0, sticky="e")
    entry_descricao.grid(row=2, column=1)

    tk.Label(main_frame, text="Modalidade (opcional)").grid(row=4, column=0, sticky="e")
    entry_modalidade = tk.Entry(main_frame)
    entry_modalidade.grid(row=4, column=1)

    # Frame dos botões usando grid (corrigido)
    frame_botoes = tk.Frame(main_frame)
    frame_botoes.grid(row=5, column=0, columnspan=2, pady=10)

    # Listbox para mostrar cursos
    lista = tk.Listbox(janela, width=80, height=15)
    lista.pack(pady=10)

    # Funções
    def mostrar_cursos():
        lista.delete(0, tk.END)
        for curso in listar_cursos():
            lista.insert(tk.END, f"ID Curso: {curso[0]} --- Nome: {curso[1]}")

    def adicionar_curso():
        nome = entry_nome.get().strip()
        descricao = entry_descricao.get().strip()
        carga_str = entry_carga.get().strip()
        modalidade = entry_modalidade.get().strip()
        if not nome or not carga_str:
            messagebox.showwarning("Atenção", "Nome e carga horária são obrigatórios.")
            return
        carga = int(carga_str)
        inserir_curso(nome, carga, descricao, modalidade)
        mostrar_cursos()
        messagebox.showinfo("Sucesso", "Curso adicionado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_carga.delete(0, tk.END)
        entry_modalidade.delete(0, tk.END)

    def atualizar_curso_gui():
        try:
            id_curso = int(entry_id.get())
            nome = entry_nome.get().strip() or None
            descricao = entry_descricao.get().strip() or None

            if nome is None and descricao is None:
                messagebox.showwarning("Atenção", "Informe ao menos um campo para atualizar.")
                return

            atualizar_curso(id_curso, nome=nome, descricao=descricao)
            mostrar_cursos()
            messagebox.showinfo("Sucesso", "Curso atualizado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_curso_gui():
        try:
            id_str = entry_id.get().strip()
            if not id_str:
                messagebox.showwarning("Atenção", "Digite um ID para remover.")
                return

            id_curso = int(id_str)
            remover_curso(id_curso)
            mostrar_cursos()
            messagebox.showinfo("Sucesso", "Curso removido com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar_curso():
        try:
            id_str = entry_id.get().strip()
            if not id_str:
                messagebox.showwarning("Atenção", "Digite um ID para buscar.")
                return

            id_curso = int(id_str)
            curso = buscar_curso_por_id(id_curso)
            lista.delete(0, tk.END)
            if curso:
                lista.insert(tk.END, f"ID Curso: {curso[0]}")
                lista.insert(tk.END, f"Nome: {curso[1]}")
                lista.insert(tk.END, f"Carga horária: {curso[2] if curso[2] else 'N/A'}")
                lista.insert(tk.END, f"Descrição: {curso[3] if curso[3] else 'N/A'}")
                lista.insert(tk.END, f"Modalidade: {curso[4] if curso[4] else 'N/A'}")
            else:
                messagebox.showinfo("Resultado", "Curso não encontrado.")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    # Botões de ação
    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", width=12, command=lambda: [ocultar_id(), adicionar_curso()])
    btn_adicionar.grid(row=0, column=0, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", width=12, command=lambda: [mostrar_id(), atualizar_curso_gui()])
    btn_atualizar.grid(row=0, column=1, padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", width=12, command=lambda: [mostrar_id(), remover_curso_gui()])
    btn_remover.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botoes, text="Buscar por ID", width=12, command=lambda: [mostrar_id(), buscar_curso()])
    btn_buscar.grid(row=1, column=0, padx=5, pady=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Todos", width=12, command=mostrar_cursos)
    btn_listar.grid(row=1, column=1, padx=5, pady=5)

    # Mostrar cursos ao abrir
    mostrar_cursos()

if __name__ == "__main__":
    iniciar_interface_curso()
