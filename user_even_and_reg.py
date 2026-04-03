import threading
import time
import random
import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "bd_tiempo_real",
    "user": "postgres",
    "password": "smartcomx123"
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insertar_evento(usuario_id, numero_evento):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO evento (id_usuario, tipo_evento, descripcion, prioridad)
                    VALUES (%s, %s, %s, %s)
                """, (
                    usuario_id,
                    "evento_concurrente",
                    f"Evento de prueba #{numero_evento}",
                    random.choice(["alta", "media", "baja"])
                ))
                conn.commit()
                print(f"[OK] Evento #{numero_evento} insertado para usuario {usuario_id}")
    except Exception as e:
        print(f"[ERROR] Evento #{numero_evento}: {e}")

def insertar_transaccion(usuario_id, numero_transaccion):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO transaccion (id_usuario, tipo_transaccion, monto, estado)
                    VALUES (%s, %s, %s, %s)
                """, (
                    usuario_id,
                    random.choice(["compra", "pago", "transferencia"]),
                    round(random.uniform(100, 5000), 2),
                    "pendiente"
                ))
                conn.commit()
                print(f"[OK] Transacción #{numero_transaccion} insertada para usuario {usuario_id}")
    except Exception as e:
        print(f"[ERROR] Transacción #{numero_transaccion}: {e}")

def actualizar_transaccion(id_transaccion):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE transaccion
                    SET estado = 'completada',
                        fecha_hora = CURRENT_TIMESTAMP
                    WHERE id_transaccion = %s
                """, (id_transaccion,))
                conn.commit()
                print(f"[OK] Transacción {id_transaccion} actualizada a completada")
    except Exception as e:
        print(f"[ERROR] Actualizando transacción {id_transaccion}: {e}")

def lectura_tiempo_real():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.id_evento, u.nombre, e.tipo_evento, e.fecha_hora
                    FROM evento e
                    JOIN usuario u ON e.id_usuario = u.id_usuario
                    ORDER BY e.fecha_hora DESC
                    LIMIT 5
                """)
                resultados = cur.fetchall()
                print("\n=== Últimos 5 eventos ===")
                for fila in resultados:
                    print(fila)
    except Exception as e:
        print(f"[ERROR] Lectura en tiempo real: {e}")

def simular_fallo_nodo_principal():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE nodo
                    SET estado = 'fallo'
                    WHERE tipo_nodo = 'principal'
                """)
                conn.commit()
                print("[OK] Nodo principal marcado como fallo")
    except Exception as e:
        print(f"[ERROR] Simulando fallo: {e}")

def activar_nodo_secundario():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE nodo
                    SET estado = 'activo'
                    WHERE nombre_nodo = 'Nodo_Secundario_1'
                """)
                conn.commit()
                print("[OK] Nodo secundario activado como respaldo")
    except Exception as e:
        print(f"[ERROR] Activando nodo secundario: {e}")

def verificar_nodos():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM nodo ORDER BY id_nodo")
                resultados = cur.fetchall()
                print("\n=== Estado de nodos ===")
                for fila in resultados:
                    print(fila)
    except Exception as e:
        print(f"[ERROR] Verificando nodos: {e}")

def replicar_eventos_a_nodo_secundario():
    """
    Lógica real de replicación de eventos desde la tabla evento
    hacia la tabla evento_replicado.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO evento_replicado (
                        id_evento_original,
                        id_usuario,
                        tipo_evento,
                        descripcion,
                        fecha_hora,
                        prioridad
                    )
                    SELECT
                        e.id_evento,
                        e.id_usuario,
                        e.tipo_evento,
                        e.descripcion,
                        e.fecha_hora,
                        e.prioridad
                    FROM evento e
                    LEFT JOIN evento_replicado er
                        ON er.id_evento_original = e.id_evento
                    WHERE er.id_evento_original IS NULL
                """)

                cur.execute("""
                    UPDATE replica
                    SET estado_replicacion = 'sincronizada',
                        fecha_ultima_actualizacion = CURRENT_TIMESTAMP
                    WHERE id_nodo_principal = 1
                      AND id_nodo_secundario = 2
                """)

                conn.commit()
                print("[OK] Replicación de eventos completada hacia el nodo secundario")
    except Exception as e:
        print(f"[ERROR] Replicación entre nodos: {e}")

def prueba_1_insercion_concurrente_eventos():
    print("\n--- PRUEBA 1: Inserción concurrente de eventos ---")
    hilos = []
    inicio = time.time()

    for i in range(20):
        usuario_id = random.randint(1, 4)
        hilo = threading.Thread(target=insertar_evento, args=(usuario_id, i + 1))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    fin = time.time()
    print(f"Tiempo total de la prueba 1: {fin - inicio:.2f} segundos")

def prueba_2_insercion_concurrente_transacciones():
    print("\n--- PRUEBA 2: Inserción concurrente de transacciones ---")
    hilos = []
    inicio = time.time()

    for i in range(10):
        usuario_id = random.randint(1, 4)
        hilo = threading.Thread(target=insertar_transaccion, args=(usuario_id, i + 1))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    fin = time.time()
    print(f"Tiempo total de la prueba 2: {fin - inicio:.2f} segundos")

def prueba_3_actualizacion_simultanea():
    print("\n--- PRUEBA 3: Actualización simultánea de transacciones ---")
    ids = []

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO transaccion (id_usuario, tipo_transaccion, monto, estado)
                    VALUES
                    (1, 'pago', 500, 'pendiente'),
                    (2, 'pago', 700, 'pendiente'),
                    (3, 'pago', 900, 'pendiente')
                    RETURNING id_transaccion
                """)
                ids = [fila[0] for fila in cur.fetchall()]
                conn.commit()
    except Exception as e:
        print(f"[ERROR] Preparando prueba 3: {e}")
        return

    hilos = []
    for id_tx in ids:
        hilo = threading.Thread(target=actualizar_transaccion, args=(id_tx,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

def prueba_4_lectura_tiempo_real():
    print("\n--- PRUEBA 4: Lectura en tiempo real ---")
    lectura_tiempo_real()

def prueba_5_fallo_y_respaldo():
    print("\n--- PRUEBA 5: Simulación de fallo del nodo principal ---")
    simular_fallo_nodo_principal()
    activar_nodo_secundario()
    verificar_nodos()

def prueba_6_replicar_eventos_a_nodo_secundario():
    print("\n--- PRUEBA 6: Replicación de eventos hacia nodo secundario ---")
    replicar_eventos_a_nodo_secundario()

def prueba_7_replicacion_entre_nodos():
    print("\n--- PRUEBA 7: Verificación de replicación entre nodos ---")

    # Se asegura que la réplica esté actualizada antes de validar
    replicar_eventos_a_nodo_secundario()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM evento")
                total_original = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM evento_replicado")
                total_replicado = cur.fetchone()[0]

                cur.execute("""
                    SELECT id_replica, estado_replicacion, fecha_ultima_actualizacion
                    FROM replica
                    WHERE id_nodo_principal = 1
                      AND id_nodo_secundario = 2
                """)
                estado_replica = cur.fetchone()

                print(f"Total eventos en nodo principal: {total_original}")
                print(f"Total eventos en nodo secundario: {total_replicado}")
                print(f"Estado de la réplica: {estado_replica}")

                if total_original == total_replicado:
                    print("[OK] Replicación consistente entre nodos")
                else:
                    print("[WARNING] La cantidad de eventos no coincide entre nodos")

    except Exception as e:
        print(f"[ERROR] Verificando replicación: {e}")

def main():
    print("=== SISTEMA DE PRUEBAS DE BASE DE DATOS EN TIEMPO REAL ===")
    prueba_1_insercion_concurrente_eventos()
    prueba_2_insercion_concurrente_transacciones()
    prueba_3_actualizacion_simultanea()
    prueba_4_lectura_tiempo_real()
    prueba_5_fallo_y_respaldo()
    prueba_6_replicar_eventos_a_nodo_secundario()
    prueba_7_replicacion_entre_nodos()

    print("\n=== TODAS LAS PRUEBAS FUERON EJECUTADAS ===")

if __name__ == "__main__":
    main()