import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_disciplinas,
    inserir_disciplina,
    buscar_disciplina_por_id,
    atualizar_disciplina,
    remover_disciplina,
    buscar_professor_por_id
)

def iniciar_interface_disciplina():
    janela = tk.Toplevel()
    janela.title("Gestão de Disciplinas")
    janela.geometry("650x480")

    main_frame = tk.Frame(janela)
    main_frame.pack(pady=10)

    entry_id = tk.Entry(main_frame)
    label_id = tk.Label(main_frame, text="ID")
    def mostrar_id():
        label_id.grid(row=0, column=0, sticky="e")
        entry_id.grid(row=0, column=1)
    def ocultar_id():
        label_id.grid_remove()
        entry_id.grid_remove()

    entry_nome = tk.Entry(main_frame)
    entry_codigo = tk.Entry(main_frame)
    entry_ementa = tk.Entry(main_frame)
    entry_bibliografia = tk.Entry(main_frame)
    entry_prof_id = tk.Entry(main_frame)

    tk.Label(main_frame, text="Nome").grid(row=1, column=0, sticky="e")  # obrigatório
    entry_nome.grid(row=1, column=1)

    tk.Label(main_frame, text="Código").grid(row=2, column=0, sticky="e")  # obrigatório
    entry_codigo.grid(row=2, column=1)

    tk.Label(main_frame, text="Ementa (opcional)").grid(row=3, column=0, sticky="e")
    entry_ementa.grid(row=3, column=1)

    tk.Label(main_frame, text="Bibliografia (opcional)").grid(row=4, column=0, sticky="e")
    entry_bibliografia.grid(row=4, column=1)

    tk.Label(main_frame, text="Professor (ID) (opcional)").grid(row=5, column=0, sticky="e")
    entry_prof_id.grid(row=5, column=1)

    lista = tk.Listbox(janela, width=80, height=15)
    lista.pack(pady=10)

    def mostrar_disciplinas():
        lista.delete(0, tk.END)
        for disc in listar_disciplinas():
            prof_id = disc[5] if disc[5] else "N/A"
            lista.insert(tk.END, f"ID: {disc[0]} --- Nome: {disc[1]} --- Prof ID: {prof_id}")

    def adicionar_disciplina():
        nome = entry_nome.get().strip()
        codigo = entry_codigo.get().strip()
        ementa = entry_ementa.get().strip()
        bibliografia = entry_bibliografia.get().strip()
        prof_id_str = entry_prof_id.get().strip()
        prof_id = int(prof_id_str) if prof_id_str else None

        if not nome or not codigo:
            messagebox.showwarning("Atenção", "Nome e código são obrigatórios.")
            return

        inserir_disciplina(nome, codigo, ementa, bibliografia, prof_id)
        mostrar_disciplinas()
        messagebox.showinfo("Sucesso", "Disciplina adicionada com sucesso!")
        entry_id.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_codigo.delete(0, tk.END)
        entry_ementa.delete(0, tk.END)
        entry_bibliografia.delete(0, tk.END)
        entry_prof_id.delete(0, tk.END)

    def atualizar_disciplina_gui():
        try:
            id_disc = int(entry_id.get().strip())
            nome = entry_nome.get().strip()
            ementa = entry_ementa.get().strip()
            prof_id_str = entry_prof_id.get().strip()

            campos_para_atualizar = {}
            if nome:
                campos_para_atualizar['nome'] = nome
            if ementa:
                campos_para_atualizar['ementa'] = ementa
            if prof_id_str:
                try:
                    campos_para_atualizar['id_prof'] = int(prof_id_str)
                except ValueError:
                    messagebox.showerror("Erro", "ID Professor deve ser um número inteiro.")
                    return

            if not campos_para_atualizar:
                messagebox.showwarning("Atenção", "Informe ao menos um campo para atualizar.")
                return

            atualizar_disciplina(id_disc, **campos_para_atualizar)
            mostrar_disciplinas()
            messagebox.showinfo("Sucesso", "Disciplina atualizada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_disciplina_gui():
        try:
            id_disc = int(entry_id.get())
            if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover esta disciplina?"):
                remover_disciplina(id_disc)
                mostrar_disciplinas()
                messagebox.showinfo("Sucesso", "Disciplina removida com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def buscar_disciplina():
        try:
            id_str = entry_id.get().strip()
            if not id_str:
                messagebox.showwarning("Atenção", "Digite um ID para buscar.")
                return
            id_disc = int(id_str)
            disc = buscar_disciplina_por_id(id_disc)
            lista.delete(0, tk.END)
            if disc:
                lista.insert(tk.END, f"ID Disciplina: {disc[0]}")
                lista.insert(tk.END, f"Nome: {disc[1]}")
                lista.insert(tk.END, f"Código: {disc[2]}")
                lista.insert(tk.END, f"Ementa: {disc[3] if disc[3] else 'N/A'}")
                lista.insert(tk.END, f"Bibliografia: {disc[4] if disc[4] else 'N/A'}")
                lista.insert(tk.END, f"Professor: {disc[5] if disc[5] else 'N/A'}")
            else:
                messagebox.showinfo("Resultado", "Disciplina não encontrada.")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", width=12, command=lambda: [ocultar_id(), adicionar_disciplina()])
    btn_adicionar.grid(row=0, column=0, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", width=12, command=lambda: [mostrar_id(), atualizar_disciplina_gui()])
    btn_atualizar.grid(row=0, column=1, padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", width=12, command=lambda: [mostrar_id(), remover_disciplina_gui()])
    btn_remover.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botoes, text="Buscar por ID", width=12, command=lambda: [mostrar_id(), buscar_disciplina()])
    btn_buscar.grid(row=1, column=0, padx=5, pady=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Todos", width=12, command=mostrar_disciplinas)
    btn_listar.grid(row=1, column=1, padx=5, pady=5)

    mostrar_disciplinas()
    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface_disciplina()