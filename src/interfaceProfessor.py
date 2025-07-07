import tkinter as tk
from tkinter import messagebox
from banco import (
    listar_professores,
    inserir_professor,
    buscar_professor_por_id,
    atualizar_professor,
    remover_professor
)

def iniciar_interface_professor():
    """
    Inicia a interface gráfica para gestão de professores,
    permitindo adicionar, atualizar, remover, buscar e listar professores.
    """
    janela = tk.Tk()
    janela.title("Gestão de Professores")
    janela.geometry("650x500")  # Tamanho ajustado

    # Frame principal
    main_frame = tk.Frame(janela)
    main_frame.pack(pady=10)

    # Campos de entrada
    entry_id = tk.Entry(main_frame)
    label_id = tk.Label(main_frame, text="ID")
    def mostrar_id():
        label_id.grid(row=0, column=0, sticky="e")
        entry_id.grid(row=0, column=1)
    def ocultar_id():
        label_id.grid_remove()
        entry_id.grid_remove()

    entry_nome = tk.Entry(main_frame)
    entry_area = tk.Entry(main_frame)
    entry_telefone = tk.Entry(main_frame)
    entry_email = tk.Entry(main_frame)

    # Layout dos campos
    label_id.grid(row=0, column=0, sticky="e")
    entry_id.grid(row=0, column=1)

    tk.Label(main_frame, text="Nome*").grid(row=1, column=0, sticky="e")  # obrigatório
    entry_nome.grid(row=1, column=1)

    tk.Label(main_frame, text="Área de Especialização*").grid(row=2, column=0, sticky="e")  # obrigatório
    entry_area.grid(row=2, column=1)

    tk.Label(main_frame, text="Telefone (opcional)").grid(row=3, column=0, sticky="e")
    entry_telefone.grid(row=3, column=1)

    tk.Label(main_frame, text="Email (opcional)").grid(row=4, column=0, sticky="e")
    entry_email.grid(row=4, column=1)

    # Listbox para mostrar professores
    lista = tk.Listbox(janela, width=85, height=15)
    lista.pack(pady=10)

    # Funções
    def mostrar_professores():
        lista.delete(0, tk.END)
        for prof in listar_professores():
            telefone = prof[3] if prof[3] else "Não informado"
            email = prof[4] if prof[4] else "Não informado"
            lista.insert(tk.END,
                         f"ID Professor: {prof[0]} --- Nome: {prof[1]} --- Área: {prof[2]}")

    def adicionar_professor():
        nome = entry_nome.get().strip()
        area = entry_area.get().strip()
        telefone = entry_telefone.get().strip() or None
        email = entry_email.get().strip() or None

        if not nome or not area:
            messagebox.showwarning("Atenção", "Nome e área são obrigatórios.")
            return

        inserir_professor(nome, area, telefone, email)
        mostrar_professores()

        # Limpa os campos
        entry_id.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_area.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    def atualizar_professor_gui():
        try:
            id_prof = int(entry_id.get())
            nome = entry_nome.get().strip()
            area = entry_area.get().strip()
            telefone = entry_telefone.get().strip()
            email = entry_email.get().strip()

            update_fields = {}
            if nome:
                update_fields['nome'] = nome
            if area:
                update_fields['area_especializacao'] = area
            if telefone:
                update_fields['telefone'] = telefone
            if email:
                update_fields['email'] = email

            if not update_fields:
                messagebox.showwarning("Atenção", "Informe ao menos um campo para atualizar.")
                return

            atualizar_professor(id_prof, **update_fields)
            mostrar_professores()
            messagebox.showinfo("Sucesso", "Professor atualizado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def remover_professor_gui():
        try:
            id_prof = int(entry_id.get())
            remover_professor(id_prof)
            mostrar_professores()
            messagebox.showinfo("Sucesso", "Professor removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def buscar_professor():
        try:
            id_str = entry_id.get().strip()
            if not id_str:
                messagebox.showwarning("Atenção", "Digite um ID para buscar.")
                return

            id_prof = int(id_str)
            prof = buscar_professor_por_id(id_prof)
            lista.delete(0, tk.END)
            if prof:
                telefone = prof[3] if prof[3] else "Não informado"
                email = prof[4] if prof[4] else "Não informado"
                lista.insert(tk.END,f"ID: {prof[0]} | Nome: {prof[1]} - Área: {prof[2]}")
                lista.insert(tk.END, f"Nome: {prof[1]}")
                lista.insert(tk.END, f"Área: {prof[2]}")
                lista.insert(tk.END, f"Telefone: {telefone}")
                lista.insert(tk.END, f"Email: {email}")
            else:
                messagebox.showinfo("Resultado", "Professor não encontrado.")
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    # Frame de botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Botões
    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", width=12, command=lambda: [ocultar_id(), adicionar_professor()])
    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", width=12, command=lambda: [mostrar_id(), atualizar_professor_gui()])
    btn_remover = tk.Button(frame_botoes, text="Remover", width=12, command=lambda: [mostrar_id(), remover_professor_gui()])
    btn_buscar = tk.Button(frame_botoes, text="Buscar por ID", width=12, command=lambda: [mostrar_id(), buscar_professor()])

    btn_adicionar.grid(row=0, column=0, padx=5)
    btn_atualizar.grid(row=0, column=1, padx=5)
    btn_remover.grid(row=0, column=2, padx=5)
    btn_buscar.grid(row=1, column=0, padx=5, pady=5)
    tk.Button(frame_botoes, text="Listar Todos", width=12, command=mostrar_professores).grid(row=1, column=1, padx=5, pady=5)

    # Informação de campos obrigatórios
    tk.Label(janela, text="* Campos obrigatórios", font=("Arial", 8)).pack()

    # Mostrar os professores ao iniciar
    mostrar_professores()

    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface_professor()
