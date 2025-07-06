-- Sistema de Gerenciamento de Cursos - Esquema do Banco de Dados
-- Versão: 2.2 (sem constraints de formato)
-- Data: 06/07/2025

-- Configurações iniciais
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

-- =====================================
-- REMOÇÃO DE TABELAS EXISTENTES (CASO NECESSÁRIO)
-- =====================================
DROP TABLE IF EXISTS Matricula;
DROP TABLE IF EXISTS OfertaCurso;
DROP TABLE IF EXISTS Disciplina;
DROP TABLE IF EXISTS Professor;
DROP TABLE IF EXISTS Curso;
DROP TABLE IF EXISTS Aluno;
DROP TABLE IF EXISTS LogAlunoInsert;
DROP TABLE IF EXISTS Perfil;

-- =====================================
-- CRIAÇÃO DAS TABELAS PRINCIPAIS
-- =====================================

-- Tabela de Alunos
CREATE TABLE Aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT,
    endereco TEXT,
    status TEXT,
    data_nascimento DATE
);

-- Tabela de Cursos
CREATE TABLE Curso (
    id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    carga_horaria INTEGER NOT NULL,
    descricao TEXT,
    modalidade TEXT
);

-- Tabela de Professores
CREATE TABLE Professor (
    id_prof INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    area_especializacao TEXT NOT NULL,
    telefone TEXT,
    email TEXT
);

-- Tabela de Disciplinas
CREATE TABLE Disciplina (
    id_disc INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    codigo TEXT NOT NULL,
    ementa TEXT,
    bibliografia TEXT,
    id_prof INTEGER,
    FOREIGN KEY (id_prof) REFERENCES Professor(id_prof) ON DELETE SET NULL
);

-- Tabela de Matrículas
CREATE TABLE Matricula (
    id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER NOT NULL,
    id_disc INTEGER NOT NULL,
    semestre TEXT NOT NULL,
    nota REAL,
    status TEXT,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno) ON DELETE CASCADE,
    FOREIGN KEY (id_disc) REFERENCES Disciplina(id_disc) ON DELETE CASCADE
);

-- Tabela de Ofertas de Curso
CREATE TABLE OfertaCurso (
    id_oferta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_curso INTEGER NOT NULL,
    id_disc INTEGER NOT NULL,
    id_prof INTEGER NOT NULL,
    periodo TEXT NOT NULL,
    sala TEXT,
    turno TEXT,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso) ON DELETE CASCADE,
    FOREIGN KEY (id_disc) REFERENCES Disciplina(id_disc) ON DELETE CASCADE,
    FOREIGN KEY (id_prof) REFERENCES Professor(id_prof) ON DELETE SET NULL
);

-- Tabela de Perfis
CREATE TABLE Perfil (
    id_perfil INTEGER PRIMARY KEY AUTOINCREMENT,
    id_prof INTEGER UNIQUE, -- UNIQUE garante 1:1
    bio TEXT,
    linkedin TEXT,
    FOREIGN KEY (id_prof) REFERENCES Professor(id_prof) ON DELETE CASCADE
);

-- =====================================
-- TABELAS DE LOG E AUDITORIA
-- =====================================

CREATE TABLE LogAlunoInsert (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER NOT NULL,
    nome TEXT NOT NULL,
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acao TEXT DEFAULT 'INSERT'
);

-- =====================================
-- TRIGGERS
-- =====================================

CREATE TRIGGER trg_log_insert_aluno
AFTER INSERT ON Aluno
BEGIN
    INSERT INTO LogAlunoInsert (id_aluno, nome) 
    VALUES (NEW.id_aluno, NEW.nome);
END;

CREATE TRIGGER trg_log_update_aluno
AFTER UPDATE ON Aluno
BEGIN
    INSERT INTO LogAlunoInsert (id_aluno, nome, acao) 
    VALUES (NEW.id_aluno, NEW.nome, 'UPDATE');
END;

-- =====================================
-- DADOS INICIAIS
-- =====================================

INSERT INTO Aluno (nome, email, telefone, endereco, status, data_nascimento) VALUES 
('Ana Lima', 'ana@email.com', '85999990000', 'Rua A, 123', 'ativo', '2000-01-01'),
('Carlos Mendes', 'carlos@email.com', NULL, NULL, 'ativo', '1999-05-15');

INSERT INTO Curso (nome, carga_horaria, descricao, modalidade) VALUES 
('Ciência da Computação', 3200, 'Curso voltado para algoritmos e estruturas de dados', 'Presencial'),
('Engenharia de Software', 3000, 'Curso focado em desenvolvimento de sistemas', 'EAD');

INSERT INTO Professor (nome, area_especializacao, telefone, email) VALUES 
('Marcos Silva', 'Banco de Dados', '85988887777', 'marcos@uni.edu'),
('Juliana Santos', 'Engenharia de Software', '85977776666', 'juliana@uni.edu');

INSERT INTO Disciplina (nome, codigo, ementa, bibliografia, id_prof) VALUES 
('Banco de Dados I', 'BD101', 'Fundamentos de bancos de dados relacionais', 'Elmasri & Navathe', 1),
('Programação Orientada a Objetos', 'POO201', 'Conceitos avançados de OO', 'Deitel & Deitel', 2);

INSERT INTO Matricula (id_aluno, id_disc, semestre, nota, status) VALUES 
(1, 1, '2024.2', 8.5, 'aprovado'),
(1, 2, '2024.2', 9.0, 'aprovado'),
(2, 1, '2024.2', 7.5, 'aprovado');

INSERT INTO OfertaCurso (id_curso, id_disc, id_prof, periodo, sala, turno) VALUES 
(1, 1, 1, '2024.2', 'A101', 'Manhã'),
(1, 2, 2, '2024.2', 'B202', 'Noite');

INSERT INTO Perfil (id_prof, bio, linkedin) VALUES
(1, 'Especialista em Banco de Dados com 10 anos de experiência.', 'https://linkedin.com/in/marcossilva'),
(2, 'Professora de Engenharia de Software e entusiasta de metodologias ágeis.', 'https://linkedin.com/in/julianasantos');

-- =====================================
-- ÍNDICES PARA MELHOR PERFORMANCE
-- =====================================

CREATE INDEX idx_aluno_nome ON Aluno(nome);
CREATE INDEX idx_disciplina_nome ON Disciplina(nome);
CREATE INDEX idx_matricula_aluno ON Matricula(id_aluno);
CREATE INDEX idx_matricula_disciplina ON Matricula(id_disc);

-- =====================================
-- CONSULTAS ÚTEIS (EXEMPLOS)
-- =====================================

SELECT id_aluno, nome, email FROM Aluno WHERE status = 'ativo';

SELECT d.nome AS disciplina, p.nome AS professor 
FROM Disciplina d
JOIN Professor p ON d.id_prof = p.id_prof;

SELECT d.nome AS disciplina, AVG(m.nota) AS media_nota
FROM Matricula m
JOIN Disciplina d ON m.id_disc = d.id_disc
GROUP BY m.id_disc;

SELECT a.nome, AVG(m.nota) AS media_geral
FROM Aluno a
JOIN Matricula m ON a.id_aluno = m.id_aluno
GROUP BY a.id_aluno
HAVING media_geral >= 8.0
ORDER BY media_geral DESC;
