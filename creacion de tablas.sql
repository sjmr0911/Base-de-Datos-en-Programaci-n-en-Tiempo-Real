-- =========================================
-- BASE DE DATOS EN TIEMPO REAL
-- PostgreSQL
-- =========================================

-- Tabla de usuarios
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de eventos
CREATE TABLE evento (
    id_evento SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    prioridad VARCHAR(20) NOT NULL DEFAULT 'media',
    CONSTRAINT fk_evento_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

-- Tabla de transacciones
CREATE TABLE transaccion (
    id_transaccion SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_transaccion VARCHAR(50) NOT NULL,
    monto NUMERIC(12,2) NOT NULL CHECK (monto >= 0),
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaccion_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

-- Tabla de nodos
CREATE TABLE nodo (
    id_nodo SERIAL PRIMARY KEY,
    nombre_nodo VARCHAR(100) NOT NULL UNIQUE,
    tipo_nodo VARCHAR(20) NOT NULL CHECK (tipo_nodo IN ('principal', 'secundario')),
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('activo', 'inactivo', 'fallo')),
    fecha_ultimo_ping TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de replicación
CREATE TABLE replica (
    id_replica SERIAL PRIMARY KEY,
    id_nodo_principal INT NOT NULL,
    id_nodo_secundario INT NOT NULL,
    estado_replicacion VARCHAR(20) NOT NULL CHECK (estado_replicacion IN ('sincronizada', 'pendiente', 'error')),
    fecha_ultima_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_replica_nodo_principal
        FOREIGN KEY (id_nodo_principal)
        REFERENCES nodo(id_nodo)
        ON DELETE CASCADE,
    CONSTRAINT fk_replica_nodo_secundario
        FOREIGN KEY (id_nodo_secundario)
        REFERENCES nodo(id_nodo)
        ON DELETE CASCADE,
    CONSTRAINT chk_nodos_diferentes
        CHECK (id_nodo_principal <> id_nodo_secundario)
);

--Tabla de eventos replicados
CREATE TABLE evento_replicado (
    id_evento_replicado SERIAL PRIMARY KEY,
    id_evento_original INT NOT NULL,
    id_usuario INT NOT NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_hora TIMESTAMP NOT NULL,
    prioridad VARCHAR(20) NOT NULL,
    replicado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_evento_replicado UNIQUE (id_evento_original)
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_evento_usuario ON evento(id_usuario);
CREATE INDEX idx_evento_fecha_hora ON evento(fecha_hora);
CREATE INDEX idx_transaccion_usuario ON transaccion(id_usuario);
CREATE INDEX idx_transaccion_fecha_hora ON transaccion(fecha_hora);
CREATE INDEX idx_nodo_estado ON nodo(estado);
CREATE INDEX idx_replica_estado ON replica(estado_replicacion);


