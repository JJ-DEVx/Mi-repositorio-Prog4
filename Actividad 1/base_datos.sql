CREATE TABLE heroes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    clase TEXT NOT NULL,
    nivel_experiencia INTEGER CHECK(nivel_experiencia >= 1)
);

CREATE TABLE misiones (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    dificultad TEXT CHECK(dificultad IN ('Fácil', 'Media', 'Difícil', 'Épica')),
    localizacion TEXT,
    recompensa INTEGER CHECK(recompensa >= 0)
);

CREATE TABLE monstruos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    nivel_amenaza INTEGER CHECK(nivel_amenaza BETWEEN 1 AND 10)
);

CREATE TABLE misiones_heroes (
    id INTEGER PRIMARY KEY,
    id_heroe INTEGER,
    id_mision INTEGER,
    FOREIGN KEY (id_heroe) REFERENCES heroes(id),
    FOREIGN KEY (id_mision) REFERENCES misiones(id),
    UNIQUE(id_heroe, id_mision)
);

CREATE TABLE misiones_monstruos (
    id INTEGER PRIMARY KEY,
    id_mision INTEGER,
    id_monstruo INTEGER,
    FOREIGN KEY (id_mision) REFERENCES misiones(id),
    FOREIGN KEY (id_monstruo) REFERENCES monstruos(id),
    UNIQUE(id_mision, id_monstruo)
);

INSERT INTO heroes (nombre, clase, nivel_experiencia)
VALUES 
    ('Kratos', 'Guerrero', 10),
    ('Gerald', 'Mago', 12),
    ('Legolas', 'Arquero', 15);

INSERT INTO misiones (nombre, dificultad, localizacion, recompensa)
VALUES 
    ('Rescate en el bosque', 'Media', 'Bosque oscuro', 300),
    ('Cueva del dragón', 'Difícil', 'Montañas rojas', 800);

INSERT INTO monstruos (nombre, tipo, nivel_amenaza)
VALUES 
    ('Dragón rojo', 'Dragón', 10),
    ('Goblin', 'Criatura', 3),
    ('Reanimado', 'No-muerto', 5);

INSERT INTO misiones_heroes (id_heroe, id_mision)
VALUES 
    (1,1),
    (1,2),
    (2,2),
    (3,2);

INSERT INTO misiones_monstruos (id_mision, id_monstruo)
VALUES 
    (1,2),
    (1,3),
    (2,1),
    (2,3);

SELECT 
    heroes.nombre AS heroe,
    misiones.nombre AS mision,
    monstruos.nombre AS monstruo
FROM misiones_heroes
JOIN heroes ON misiones_heroes.id_heroe = heroes.id
JOIN misiones ON misiones_heroes.id_mision = misiones.id
JOIN misiones_monstruos ON misiones.id = misiones_monstruos.id_mision
JOIN monstruos ON misiones_monstruos.id_monstruo = monstruos.id
ORDER BY heroe, mision;
