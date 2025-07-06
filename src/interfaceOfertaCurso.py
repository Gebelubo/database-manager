import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_ofertas,
    inserir_oferta,
    buscar_oferta_por_id,
    atualizar_oferta,
    remover_oferta,
    listar_cursos,
    listar_disciplinas,
    listar_professores
)

def iniciar_interface_oferta():
    janela = tk.Toplevel()
    janela.title("Gestão de Oferta de Cursos")
    janela.geometry("750x520")

    main_frame = tk.Frame(janela)
    main_frame.pack(pady=10)

    entry_id_oferta = tk.Entry(main_frame)
    label_id_oferta = tk.Label(main_frame, text="ID Oferta")
    def mostrar_id():
        label_id_oferta.grid(row=0, column=0, sticky="e")
        entry_id_oferta.grid(row=0, column=1)
    def ocultar_id():
        label_id_oferta.grid_remove()
        entry_id_oferta.grid_remove()

    entry_id_curso = tk.Entry(main_frame)
    entry_id_disc = tk.Entry(main_frame)
    entry_id_prof = tk.Entry(main_frame)
    entry_periodo = tk.Entry(main_frame)
    entry_sala = tk.Entry(main_frame)
    entry_turno = tk.Entry(main_frame)

    tk.Label(main_frame, text="ID Curso").grid(row=1, column=0, sticky="e")  # obrigatório
    entry_id_curso.grid(row=1, column=1)

    tk.Label(main_frame, text="ID Disciplina").grid(row=2, column=0, sticky="e")  # obrigatório
    entry_id_disc.grid(row=2, column=1)

    tk.Label(main_frame, text="ID Professor").grid(row=3, column=0, sticky="e")  # obrigatório
    entry_id_prof.grid(row=3, column=1)

    tk.Label(main_frame, text="Período (ex: 2023.1)").grid(row=4, column=0, sticky="e")  # obrigatório
    entry_periodo.grid(row=4, column=1)

    tk.Label(main_frame, text="Sala (opcional)").grid(row=5, column=0, sticky="e")
    entry_sala.grid(row=5, column=1)

    tk.Label(main_frame, text="Turno (opcional)").grid(row=6, column=0, sticky="e")
    entry_turno.grid(row=6, column=1)

    lista = tk.Listbox(janela, width=90, height=15)
    lista.pack(pady=10)

    def mostrar_ofertas():
        lista.delete(0, tk.END)
        for oferta in listar_ofertas():
            lista.insert(tk.END, 
                f"Oferta: {oferta[0]} | Curso: {oferta[1]} | Disciplina: {oferta[2]} | Professor: {oferta[3]} | Período: {oferta[4]}")

    def adicionar_oferta():
        id_curso = int(entry_id_curso.get())
        id_disc = int(entry_id_disc.get())
        id_prof = int(entry_id_prof.get())
        periodo = entry_periodo.get().strip()
        sala = entry_sala.get().strip()
        turno = entry_turno.get().strip()
        if not periodo:
            messagebox.showwarning("Atenção", "Período é obrigatório.")
            return
        inserir_oferta(id_curso, id_disc, id_prof, periodo, sala, turno)
        mostrar_ofertas()
        entry_id_oferta.delete(0, tk.END)
        entry_id_curso.delete(0, tk.END)
        entry_id_disc.delete(0, tk.END)
        entry_id_prof.delete(0, tk.END)
        entry_periodo.delete(0, tk.END)
        entry_sala.delete(0, tk.END)
        entry_turno.delete(0, tk.END)

    def atualizar_oferta_gui():
        try:
            id_oferta = int(entry_id_oferta.get())
            id_curso = int(entry_id_curso.get()) if entry_id_curso.get().strip() else None
            id_disc = int(entry_id_disc.get()) if entry_id_disc.get().strip() else None
            id_prof = int(entry_id_prof.get()) if entry_id_prof.get().strip() else None
            periodo = entry_periodo.get().strip() or None
            sala = entry_sala.get().strip() or None
            turno = entry_turno.get().strip() or None

            if periodo:
                periodo_parts = periodo.split('.')
                if len(periodo_parts) != 2 or not all(part.isdigit() for part in periodo_parts):
                    messagebox.showwarning("Atenção", "Período deve estar no formato ANO.SEMESTRE (ex: 2023.1)")
                    return

            if not any([id_curso, id_disc, id_prof, periodo, sala, turno]):
                messagebox.showwarning("Atenção", "Informe ao menos um campo para atualizar.")
                return

            sucesso = atualizar_oferta(id_oferta, id_curso=id_curso, id_disc=id_disc, id_prof=id_prof, periodo=periodo, sala=sala, turno=turno)
            if sucesso:
                mostrar_ofertas()
                messagebox.showinfo("Sucesso", "Oferta atualizada com sucesso!")
            else:
                messagebox.showwarning("Falha", "Não foi possível atualizar a oferta. Verifique se o ID existe.")
        except ValueError:
            messagebox.showerror("Erro", "IDs devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def remover_oferta_gui():
        try:
            id_oferta = int(entry_id_oferta.get())
            sucesso = remover_oferta(id_oferta)
            if sucesso:
                mostrar_ofertas()
                messagebox.showinfo("Sucesso", "Oferta removida com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao remover oferta. Verifique se o ID existe.")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def buscar_oferta_gui():
        try:
            id_str = entry_id_oferta.get().strip()
            if not id_str:
                messagebox.showwarning("Atenção", "Digite um ID Oferta para buscar.")
                return
            id_oferta = int(id_str)
            oferta = buscar_oferta_por_id(id_oferta)
            lista.delete(0, tk.END)
            if oferta:
                lista.insert(tk.END, f"Oferta: {oferta[0]} | Curso: {oferta[1]} | Disciplina: {oferta[2]} | Professor: {oferta[3]} | Período: {oferta[4]}")
            else:
                messagebox.showinfo("Resultado", "Oferta não encontrada.")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", width=12, command=lambda: [ocultar_id(), adicionar_oferta()])
    btn_adicionar.grid(row=0, column=0, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", width=12, command=lambda: [mostrar_id(), atualizar_oferta_gui()])
    btn_atualizar.grid(row=0, column=1, padx=5)

    btn_remover = tk.Button(frame_botoes, text="Remover", width=12, command=lambda: [mostrar_id(), remover_oferta_gui()])
    btn_remover.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botoes, text="Buscar por ID", width=12, command=lambda: [mostrar_id(), buscar_oferta_gui()])
    btn_buscar.grid(row=1, column=0, padx=5, pady=5)

    btn_listar = tk.Button(frame_botoes, text="Listar Todos", width=12, command=mostrar_ofertas)
    btn_listar.grid(row=1, column=1, padx=5, pady=5)

    mostrar_ofertas()

if __name__ == "__main__":
    iniciar_interface_oferta()
    tk.mainloop()