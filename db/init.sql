-- Crear tabla: persona
CREATE TABLE persona (
    id_persona INTEGER PRIMARY KEY,
    primer_nombre VARCHAR(30) NOT NULL,
    segundo_nombre VARCHAR(30),
    apellidos VARCHAR(60) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(20) NOT NULL CHECK (genero IN ('Masculino', 'Femenino', 'No binario', 'Prefiero no reportar')),
    correo VARCHAR(100) NOT NULL CHECK (correo ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
    celular VARCHAR(10) NOT NULL CHECK (celular ~ '^[0-9]{10}$'),
    tipo_documento VARCHAR(25) NOT NULL CHECK (tipo_documento IN ('Tarjeta de identidad', 'Cédula')),
    foto VARCHAR(255),
    
    -- Validaciones adicionales
    CONSTRAINT chk_nombre1 CHECK (primer_nombre !~ '^[0-9]+$'),
    CONSTRAINT chk_nombre2 CHECK (segundo_nombre IS NULL OR segundo_nombre !~ '^[0-9]+$'),
    CONSTRAINT chk_apellidos CHECK (apellidos !~ '^[0-9]+$')
);

-- Crear tabla: log
CREATE TABLE log (
    id_log SERIAL PRIMARY KEY,
    accion VARCHAR(50) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_persona INTEGER
);

-- Insertar datos en persona
INSERT INTO persona (
    id_persona,primer_nombre, segundo_nombre, apellidos,
    fecha_nacimiento, genero, correo, celular,
    tipo_documento, foto
) VALUES
(1000123456,'Pedro', 'Luis', 'Pérez Gómez', '1995-04-12', 'Masculino', 'pedro.perez@example.com', '3014567890', 'Cédula', 'fotos/pedro.jpg'),
(1023456789,'Ana', NULL, 'Martínez Ríos', '2002-11-23', 'Femenino', 'ana.martinez@example.com', '3201234567', 'Tarjeta de identidad', 'fotos/ana.jpg'),
(1034567890,'Carlos', 'Eduardo', 'Ramírez López', '1990-06-05', 'Masculino', 'carlos.r@example.com', '3119876543', 'Cédula', 'fotos/carlos.jpg'),
(1045678901,'Laura', NULL, 'Zapata Mejía', '2001-09-15', 'No binario', 'laura.zapata@example.com', '3123456789', 'Cédula', 'fotos/laura.jpg'),
(1056789012,'Sofía', 'Elena', 'Morales Díaz', '1998-01-30', 'Prefiero no reportar', 'sofia.m@example.com', '3134567890', 'Tarjeta de identidad', 'fotos/sofia.jpg');

-- Insertar logs
INSERT INTO log (accion, id_persona) VALUES
('crear',1000123456),
('crear',1023456789),
('crear', 1034567890),
('crear', 1056789012),
('crear', 1045678901);

