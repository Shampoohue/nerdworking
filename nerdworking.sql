CREATE TABLE IF NOT EXISTS usuario(
    matricula INTEGER UNIQUE NOT NULL,
    nombres TEXT NOT NULL, 
    apepaterno TEXT NOT NULL,
    apematerno TEXT DEFAULT '',
    semestre INTEGER DEFAULT 1,
    carrera TEXT NOT NULL CHECK(carrera IN ('Arquitectura', 'Ing. Agrónomo', 'Ing. Biomédica', 'Ing. Civil', 'Ing. en Ciencias Ambientales', 'Ing. en Energías Renovables', 'Ing. en Materiales', 'Ing. en Semiconductores', 'Ing. en Sistemas de Información', 'Ing. en Tecnología Electrónica', 'Ing. Industrial y de Sistemas', 'Ing. Mecatrónica', 'Ing. Metalúrgica', 'Ing. Minero', 'Ing. Químico', 'Lic. de Químico en Alimentos', 'Lic. en Administración', 'Lic. en Administración Pública', 'Lic. en Antropología', 'Lic. en Artes Escénicas', 'Lic. en Artes Plásticas', 'Lic. en Biología', 'Lic. en Ciencias de la Computación', 'Lic. en Ciencias de la Comunicación', 'Lic. en Ciencias Genómicas', 'Lic. en Ciencias Nutricionales', 'Lic. en Contaduría Pública', 'Lic. en Cultura Física y Deporte', 'Lic. en Derecho', 'Lic. en Diseño Gráfico', 'Lic. en Economía', 'Lic. en Educación', 'Lic. en Enfermería', 'Lic. en Enseñanza del Inglés', 'Lic. en Finanzas', 'Lic. en Física', 'Lic. en Física Médica', 'Lic. en Fisioterapia', 'Lic. en Geología', 'Lic. en Historia', 'Lic. en Lingüística', 'Lic. en Literaturas Hispánicas', 'Lic. en Logística', 'Lic. en Matemáticas', 'Lic. en Mercadotecnia', 'Lic. en Música', 'Lic. en Negocios y Comercio Internacionales', 'Lic. en Odontología', 'Lic. en Psicología', 'Lic. en Química', 'Lic. en Seguridad Pública', 'Lic. en Sociología', 'Lic. en Sustentabilidad', 'Lic. en Trabajo Social', 'Lic. en Turismo', 'Medicina', 'Médico Veterinario Zootecnista', 'Químico Biólogo Clínico')),
    correo TEXT AS (CONCAT('a', matricula, '@unison.mx')) STORED,
    psswrd TEXT NOT NULL,
    adminuser INTEGER CHECK(adminuser IN (0, 1)) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS everyman(
    id INTEGER PRIMARY KEY,
    tipo TEXT CHECK(tipo IN ('Post', 'Anuncio', 'Perfil', 'Respuesta')) NOT NULL,
    titulo TEXT NOT NULL, 
    body TEXT NOT NULL,
    creator INTEGER DEFAULT NULL,
    imgfile TEXT DEFAULT NULL,
    edited INTEGER CHECK(edited IN (0, 1)) DEFAULT 0, 
    aceptable INTEGER CHECK(aceptable IN (0, 1)) DEFAULT 0,
    FOREIGN KEY (creator) REFERENCES usuario(matricula) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tiempo(
    año INTEGER NOT NULL CHECK(año > 1900),
    mes INTEGER NOT NULL CHECK(mes > 0 AND mes <= 12),
    dia INTEGER NOT NULL CHECK(dia > 0 AND dia <= 31),
    hora INTEGER NOT NULL CHECK(hora >= 0 AND hora <= 23),
    min INTEGER NOT NULL CHECK(min >= 0 AND min <= 59),
    seg INTEGER NOT NULL CHECK(seg >= 0 AND seg <= 59),
    everyman INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (everyman) REFERENCES everyman(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tags(
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,
    tsuku INTEGER NOT NULL,
    FOREIGN KEY (tsuku) REFERENCES everyman(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interes (
    post INTEGER NOT NULL,
    user INTEGER NOT NULL,
    interesado INTEGER DEFAULT 1,
    PRIMARY KEY (post, user),
    FOREIGN KEY (post) REFERENCES everyman(id) ON DELETE CASCADE,
    FOREIGN KEY (user) REFERENCES usuario(matricula) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS frommetoyou (
    id INTEGER PRIMARY KEY,
    mywords TEXT NOT NULL,
    talker INTEGER NOT NULL,
    listener INTEGER NOT NULL,
    FOREIGN KEY (talker) REFERENCES user(matricula) ON DELETE CASCADE,
    FOREIGN KEY (listener) REFERENCES user(matricula) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notif (
    post INTEGER NOT NULL,
    user INTEGER NOT NULL,
    descr TEXT NOT NULL,
    checked INTEGER CHECK(checked IN (0, 1)) DEFAULT 0, 
    FOREIGN KEY (post) REFERENCES everyman(id) ON DELETE CASCADE,
    FOREIGN KEY (user) REFERENCES usuario(matricula) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS respuesta (
    response INTEGER NOT NULL,
    responded INTEGER NOT NULL,
    FOREIGN KEY (response) REFERENCES everyman(id) ON DELETE CASCADE,
    FOREIGN KEY (responded) REFERENCES everyman(id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS deleteresponses
AFTER DELETE ON respuesta
BEGIN
    DELETE FROM everyman WHERE tipo = 'Respuesta' AND id = OLD.id;
END;

INSERT INTO usuario (matricula, nombres, apepaterno, apematerno, semestre, carrera, psswrd, adminuser) VALUES
(224204735, 'Leonardo', 'Montaño', 'Lares', 5, 'Ing. en Sistemas de Información', 'wagooguspassword', 1),
(224211540, 'Gerardo', 'Tapia', 'Fimbres', 5, 'Ing. en Sistemas de Información', 'shampoopassword', 1),
(224205962, 'Andrea Guadalupe', 'López', 'González', 5, 'Ing. en Sistemas de Información', 'geraldog', 1);

INSERT INTO everyman (tipo, titulo, body, creator, aceptable) VALUES
('Post', 'Ayudenme con mi proyecto', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 224211540, 1),
('Perfil', 'Gerardo Tapia Fimbres', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 224211540, 1),
('Perfil', 'Leonardo Montaño Lares', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 224204735, 1),
('Respuesta', '', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 224204735, 1);

INSERT INTO everyman (tipo, titulo, body, creator, imgfile, aceptable) VALUES
('Post', 'Proyecto de estadisticas de diabetes', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 224204735, 'uploads/icon.png', 1);

INSERT INTO everyman (tipo, titulo, body, aceptable) VALUES
('Anuncio', '2026 NASA Space Apps Challenge', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1);

INSERT INTO everyman (tipo, titulo, body, creator, aceptable) VALUES
('Perfil', 'Andy', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 224205962, 1);

INSERT INTO tags (term, tsuku) VALUES
('Python', 1), ('Flask', 1), ('JavaScript', 1), ('SQLite', 1), ('CSS', 1), ('HTML', 1),
('HTML', 2), ('CSS', 2), ('PostgreSQL', 2), ('MySQL', 2), ('Ubuntu', 2), ('VirtualBox', 2),
('Java', 3), ('Python', 3), ('HTML', 3), ('CSS', 3), ('JavaScript', 3), ('C', 3), ('GDscript/Godot', 3),
('PHP', 5), ('HTML', 5), ('CSS', 5), ('JavaScript', 5), ('MySQL', 5), ('Python', 5), ('Panda Python', 5),
('JavaScript', 6), ('HTML', 6), ('Python', 6);

INSERT INTO tiempo (año, mes, dia, hora, min, seg, everyman) VALUES
(2026, 11, 13, 16, 43, 20, 1),
(2026, 11, 14, 10, 5, 50, 4),
(2026, 11, 15, 13, 12, 25, 5),
(2026, 9, 2, 12, 30, 30, 6);

INSERT INTO respuesta (response, responded) VALUES (4, 1);

INSERT INTO interes (post, user) VALUES (5, 224211540);
INSERT INTO interes (post, user) VALUES (1, 224204735);