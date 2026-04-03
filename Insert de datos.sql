-- Usuarios
INSERT INTO usuario (nombre, correo, estado) VALUES
('Ana Pérez', 'ana@example.com', 'activo'),
('Luis Gómez', 'luis@example.com', 'activo'),
('María Rodríguez', 'maria@example.com', 'activo'),
('Carlos Díaz', 'carlos@example.com', 'activo');

-- Eventos
INSERT INTO evento (id_usuario, tipo_evento, descripcion, prioridad) VALUES
(1, 'login', 'Inicio de sesión del usuario', 'alta'),
(2, 'consulta', 'Consulta de datos en tiempo real', 'media'),
(3, 'actualizacion', 'Actualización de registro', 'alta'),
(1, 'logout', 'Cierre de sesión', 'baja');

-- Transacciones
INSERT INTO transaccion (id_usuario, tipo_transaccion, monto, estado) VALUES
(1, 'compra', 2500.00, 'completada'),
(2, 'pago', 1200.50, 'pendiente'),
(3, 'transferencia', 350.75, 'completada'),
(4, 'compra', 999.99, 'pendiente');

-- Nodos
INSERT INTO nodo (nombre_nodo, tipo_nodo, estado) VALUES
('Nodo_Principal_1', 'principal', 'activo'),
('Nodo_Secundario_1', 'secundario', 'activo'),
('Nodo_Secundario_2', 'secundario', 'activo');

-- Réplicas
INSERT INTO replica (id_nodo_principal, id_nodo_secundario, estado_replicacion) VALUES
(1, 2, 'sincronizada'),
(1, 3, 'sincronizada');