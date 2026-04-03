---------Consultas
SELECT * FROM usuario;

SELECT * FROM evento ORDER BY fecha_hora DESC;

SELECT COUNT(*) AS total_eventos FROM evento;

SELECT * FROM transaccion ORDER BY fecha_hora DESC;

SELECT COUNT(*) AS transacciones_completadas
FROM transaccion
WHERE estado = 'completada';

SELECT * FROM nodo ORDER BY id_nodo;

SELECT * FROM replica;

SELECT 
    e.id_evento,
    u.nombre,
    e.tipo_evento,
    e.descripcion,
    e.prioridad,
    e.fecha_hora
FROM evento e
JOIN usuario u ON e.id_usuario = u.id_usuario
ORDER BY e.fecha_hora DESC;


SELECT
    t.id_transaccion,
    u.nombre,
    t.tipo_transaccion,
    t.monto,
    t.estado,
    t.fecha_hora
FROM transaccion t
JOIN usuario u ON t.id_usuario = u.id_usuario
ORDER BY t.fecha_hora DESC;



SELECT * FROM nodo ORDER BY id_nodo;

SELECT * FROM evento_replicado ORDER BY fecha_hora DESC LIMIT 5;