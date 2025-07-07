import sqlite3
import os
from typing import List, Tuple, Optional

class BancoDados:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance

    def _inicializar(self):
        self._criar_tabelas()

    def _conectar(self) -> sqlite3.Connection:
        conn = sqlite3.connect("sistema.db")
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _criar_tabelas(self):
        criar_tabelas = False
        if not os.path.exists("sistema.db"):
            criar_tabelas = True
        else:
            with self._conectar() as conn:
                tabelas_necessarias = ["Aluno", "Curso", "Professor", "Disciplina", "Matricula", "OfertaCurso"]
                tabelas_existentes = [row[0] for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';"
                ).fetchall()]
                for tabela in tabelas_necessarias:
                    if tabela not in tabelas_existentes:
                        criar_tabelas = True
                        break
        if criar_tabelas:
            if not os.path.exists("modelo.sql"):
                raise FileNotFoundError("O arquivo 'modelo.sql' não foi encontrado na pasta do projeto.")
            with self._conectar() as conn:
                with open("modelo.sql", "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
                conn.commit()

    # --- ALUNO ---
    def listar_alunos(self) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Aluno").fetchall()

    def inserir_aluno(self, nome: str, email: str, telefone: Optional[str] = None,
                      endereco: Optional[str] = None, status: Optional[str] = "ativo",
                      data_nascimento: Optional[str] = None) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute(
                    "INSERT INTO Aluno (nome, email, telefone, endereco, status, data_nascimento) VALUES (?, ?, ?, ?, ?, ?)",
                    (nome, email, telefone, endereco, status, data_nascimento)
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise Exception(f"Erro de integridade: {e}")
            return False

    def buscar_aluno_por_id(self, id_aluno: int):
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Aluno WHERE id_aluno = ?", (id_aluno,)).fetchone()

    def atualizar_aluno(self, id_aluno: int, nome: Optional[str] = None, data_nascimento: Optional[str] = None,
                        telefone: Optional[str] = None, email: Optional[str] = None) -> bool:
        try:
            with self._conectar() as conn:
                campos, valores = [], []
                if nome: campos.append("nome = ?"); valores.append(nome)
                if data_nascimento: campos.append("data_nascimento = ?"); valores.append(data_nascimento)
                if telefone: campos.append("telefone = ?"); valores.append(telefone)
                if email: campos.append("email = ?"); valores.append(email)
                if not campos:
                    print("Nenhum campo para atualizar.")
                    return False
                valores.append(id_aluno)
                sql = f"UPDATE Aluno SET {', '.join(campos)} WHERE id_aluno = ?"
                conn.execute(sql, valores)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar aluno: {e}")
            return False

    def remover_aluno(self, id_aluno: int) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM Aluno WHERE id_aluno = ?", (id_aluno,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover aluno: {e}")
            return False

    def buscar_alunos_por_substring(self, substring: str) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Aluno WHERE nome LIKE ?", (f"%{substring}%",)).fetchall()

    # --- CURSO ---
    def listar_cursos(self) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Curso").fetchall()

    def inserir_curso(self, nome, carga_horaria, descricao=None, modalidade=None):
        try:
            with self._conectar() as conn:
                conn.execute("INSERT INTO Curso (nome, carga_horaria, descricao, modalidade) VALUES (?, ?, ?, ?)", (nome, carga_horaria, descricao, modalidade))
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise Exception(f"Erro de integridade: {e}")
            return False

    def buscar_curso_por_id(self, id_curso: int) -> Optional[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Curso WHERE id_curso = ?", (id_curso,)).fetchone()

    def atualizar_curso(self, id_curso: int, nome: Optional[str] = None, descricao: Optional[str] = None) -> bool:
        try:
            with self._conectar() as conn:
                campos, valores = [], []
                if nome: campos.append("nome = ?"); valores.append(nome)
                if descricao: campos.append("descricao = ?"); valores.append(descricao)
                if not campos:
                    print("Nenhum campo para atualizar.")
                    return False
                valores.append(id_curso)
                sql = f"UPDATE Curso SET {', '.join(campos)} WHERE id_curso = ?"
                conn.execute(sql, valores)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar curso: {e}")
            return False

    def remover_curso(self, id_curso: int) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM Curso WHERE id_curso = ?", (id_curso,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover curso: {e}")
            return False

    # --- PROFESSOR ---
    def listar_professores(self) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Professor").fetchall()

    def buscar_professor_por_id(self, id_prof: int) -> Optional[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Professor WHERE id_prof = ?", (id_prof,)).fetchone()

    def inserir_professor(self, nome, area_especializacao, telefone=None, email=None):
        try:
            with self._conectar() as conn:
                conn.execute("INSERT INTO Professor (nome, area_especializacao, telefone, email) VALUES (?, ?, ?, ?)",
                             (nome, area_especializacao, telefone, email))
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise Exception(f"Erro de integridade: {e}")
            return False

    def atualizar_professor(self, id_prof: int, nome: Optional[str] = None, area_especializacao: Optional[str] = None,
                            telefone: Optional[str] = None, email: Optional[str] = None) -> bool:
        try:
            with self._conectar() as conn:
                campos, valores = [], []
                if nome: campos.append("nome = ?"); valores.append(nome)
                if area_especializacao: campos.append("area_especializacao = ?"); valores.append(area_especializacao)
                if telefone: campos.append("telefone = ?"); valores.append(telefone)
                if email: campos.append("email = ?"); valores.append(email)
                if not campos:
                    print("Nenhum campo para atualizar.")
                    return False
                valores.append(id_prof)
                sql = f"UPDATE Professor SET {', '.join(campos)} WHERE id_prof = ?"
                conn.execute(sql, valores)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar professor: {e}")
            return False

    def remover_professor(self, id_prof: int) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM Professor WHERE id_prof = ?", (id_prof,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover professor: {e}")
            return False

    # --- DISCIPLINA ---
    def listar_disciplinas(self) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Disciplina").fetchall()

    def buscar_disciplina_por_id(self, id_disc: int) -> Optional[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Disciplina WHERE id_disc = ?", (id_disc,)).fetchone()

    def inserir_disciplina(self, nome, codigo, ementa=None, bibliografia=None, id_prof=None):
        try:
            with self._conectar() as conn:
                conn.execute("INSERT INTO Disciplina (nome, codigo, ementa, bibliografia, id_prof) VALUES (?, ?, ?, ?, ?)",
                             (nome, codigo, ementa, bibliografia, id_prof))
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise Exception(f"Erro de integridade: {e}")
            return False

    def atualizar_disciplina(self, id_disc: int, nome: Optional[str] = None,
                             ementa: Optional[str] = None, id_prof: Optional[int] = None) -> bool:
        try:
            with self._conectar() as conn:
                campos, valores = [], []
                if nome: campos.append("nome = ?"); valores.append(nome)
                if ementa: campos.append("ementa = ?"); valores.append(ementa)
                if id_prof is not None: campos.append("id_prof = ?"); valores.append(id_prof)
                if not campos:
                    print("Nenhum campo para atualizar.")
                    return False
                valores.append(id_disc)
                sql = f"UPDATE Disciplina SET {', '.join(campos)} WHERE id_disc = ?"
                conn.execute(sql, valores)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar disciplina: {e}")
            return False

    def remover_disciplina(self, id_disc: int) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM Disciplina WHERE id_disc = ?", (id_disc,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover disciplina: {e}")
            return False

    # --- MATRICULA ---
    def listar_matriculas(self) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Matricula").fetchall()

    def buscar_matricula(self, id_aluno: int, id_disc: int) -> Optional[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM Matricula WHERE id_aluno = ? AND id_disc = ?",
                                (id_aluno, id_disc)).fetchone()

    def inserir_matricula(self, id_aluno: int, id_disc: int, semestre: str,
                          nota: Optional[float] = None, status: Optional[str] = None) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("INSERT INTO Matricula (id_aluno, id_disc, semestre, nota, status) VALUES (?, ?, ?, ?, ?)",
                             (id_aluno, id_disc, semestre, nota, status))
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise Exception(f"Erro de integridade: {e}")
            return False

    def atualizar_matricula(self, id_aluno: int, id_disc: int,
                            semestre: Optional[str] = None, nota: Optional[float] = None) -> bool:
        try:
            with self._conectar() as conn:
                campos, valores = [], []
                if semestre: campos.append("semestre = ?"); valores.append(semestre)
                if nota is not None: campos.append("nota = ?"); valores.append(nota)
                if not campos:
                    print("Nenhum campo para atualizar matrícula.")
                    return False
                valores += [id_aluno, id_disc]
                sql = f"UPDATE Matricula SET {', '.join(campos)} WHERE id_aluno = ? AND id_disc = ?"
                conn.execute(sql, valores)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar matrícula: {e}")
            return False

    def remover_matricula(self, id_aluno: int, id_disc: int) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM Matricula WHERE id_aluno = ? AND id_disc = ?", (id_aluno, id_disc))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover matrícula: {e}")
            return False

    # --- OFERTA CURSO ---
    def listar_ofertas(self) -> List[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM OfertaCurso").fetchall()

    def buscar_oferta_por_id(self, id_oferta: int) -> Optional[Tuple]:
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM OfertaCurso WHERE id_oferta = ?", (id_oferta,)).fetchone()

    def inserir_oferta(self, id_curso, id_disc, id_prof, periodo, sala=None, turno=None):
        try:
            with self._conectar() as conn:
                conn.execute("INSERT INTO OfertaCurso (id_curso, id_disc, id_prof, periodo, sala, turno) VALUES (?, ?, ?, ?, ?, ?)",
                             (id_curso, id_disc, id_prof, periodo, sala, turno))
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise Exception(f"Erro de integridade: {e}")
            return False

    def atualizar_oferta(self, id_oferta: int, id_curso: Optional[int] = None,
                         id_disc: Optional[int] = None, id_prof: Optional[int] = None,
                         periodo: Optional[str] = None) -> bool:
        try:
            with self._conectar() as conn:
                campos, valores = [], []
                if id_curso is not None: campos.append("id_curso = ?"); valores.append(id_curso)
                if id_disc: campos.append("id_disc = ?"); valores.append(id_disc)
                if id_prof is not None: campos.append("id_prof = ?"); valores.append(id_prof)
                if periodo: campos.append("periodo = ?"); valores.append(periodo)
                if not campos:
                    print("Nenhum campo para atualizar oferta.")
                    return False
                valores.append(id_oferta)
                sql = f"UPDATE OfertaCurso SET {', '.join(campos)} WHERE id_oferta = ?"
                conn.execute(sql, valores)
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar oferta: {e}")
            return False

    def remover_oferta(self, id_oferta: int) -> bool:
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM OfertaCurso WHERE id_oferta = ?", (id_oferta,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover oferta: {e}")
            return False

    # --- PERFIL ---
    def inserir_perfil(self, id_prof, bio=None, linkedin=None):
        try:
            with self._conectar() as conn:
                conn.execute(
                    "INSERT INTO Perfil (id_prof, bio, linkedin) VALUES (?, ?, ?)",
                    (id_prof, bio, linkedin)
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir perfil: {e}")
            return False

    def buscar_perfil_por_professor(self, id_prof):
        with self._conectar() as conn:
            return conn.execute(
                "SELECT * FROM Perfil WHERE id_prof = ?", (id_prof,)
            ).fetchone()

    def atualizar_perfil(self, id_prof, bio=None, linkedin=None):
        try:
            with self._conectar() as conn:
                conn.execute(
                    "UPDATE Perfil SET bio = ?, linkedin = ? WHERE id_prof = ?",
                    (bio, linkedin, id_prof)
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")
            return False

    def remover_perfil(self, id_prof):
        try:
            with self._conectar() as conn:
                conn.execute("DELETE FROM Perfil WHERE id_prof = ?", (id_prof,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover perfil: {e}")
            return False

# Singleton Access
_banco_instance = None

def get_banco():
    global _banco_instance
    if _banco_instance is None:
        _banco_instance = BancoDados()
    return _banco_instance

# Funções utilitárias
listar_alunos = lambda: get_banco().listar_alunos()
inserir_aluno = lambda *args, **kwargs: get_banco().inserir_aluno(*args, **kwargs)
buscar_aluno_por_id = lambda *args, **kwargs: get_banco().buscar_aluno_por_id(*args, **kwargs)
atualizar_aluno = lambda *args, **kwargs: get_banco().atualizar_aluno(*args, **kwargs)
remover_aluno = lambda *args, **kwargs: get_banco().remover_aluno(*args, **kwargs)
buscar_alunos_por_substring = lambda *args, **kwargs: get_banco().buscar_alunos_por_substring(*args, **kwargs)

listar_cursos = lambda: get_banco().listar_cursos()
inserir_curso = lambda *args, **kwargs: get_banco().inserir_curso(*args, **kwargs)
buscar_curso_por_id = lambda *args, **kwargs: get_banco().buscar_curso_por_id(*args, **kwargs)
atualizar_curso = lambda *args, **kwargs: get_banco().atualizar_curso(*args, **kwargs)
remover_curso = lambda *args, **kwargs: get_banco().remover_curso(*args, **kwargs)
listar_professores = lambda: get_banco().listar_professores()
buscar_professor_por_id = lambda *args, **kwargs: get_banco().buscar_professor_por_id(*args, **kwargs)
inserir_professor = lambda *args, **kwargs: get_banco().inserir_professor(*args, **kwargs)
atualizar_professor = lambda *args, **kwargs: get_banco().atualizar_professor(*args, **kwargs)
remover_professor = lambda *args, **kwargs: get_banco().remover_professor(*args, **kwargs)
listar_disciplinas = lambda: get_banco().listar_disciplinas()
buscar_disciplina_por_id = lambda *args, **kwargs: get_banco().buscar_disciplina_por_id(*args, **kwargs)
inserir_disciplina = lambda *args, **kwargs: get_banco().inserir_disciplina(*args, **kwargs)
atualizar_disciplina = lambda *args, **kwargs: get_banco().atualizar_disciplina(*args, **kwargs)
remover_disciplina = lambda *args, **kwargs: get_banco().remover_disciplina(*args, **kwargs)
listar_matriculas = lambda: get_banco().listar_matriculas()
buscar_matricula = lambda *args, **kwargs: get_banco().buscar_matricula(*args, **kwargs)
inserir_matricula = lambda *args, **kwargs: get_banco().inserir_matricula(*args, **kwargs)
atualizar_matricula = lambda *args, **kwargs: get_banco().atualizar_matricula(*args, **kwargs)
remover_matricula = lambda *args, **kwargs: get_banco().remover_matricula(*args, **kwargs)
listar_ofertas = lambda: get_banco().listar_ofertas()
buscar_oferta_por_id = lambda *args, **kwargs: get_banco().buscar_oferta_por_id(*args, **kwargs)
inserir_oferta = lambda *args, **kwargs: get_banco().inserir_oferta(*args, **kwargs)
atualizar_oferta = lambda *args, **kwargs: get_banco().atualizar_oferta(*args, **kwargs)
remover_oferta = lambda *args, **kwargs: get_banco().remover_oferta(*args, **kwargs)
