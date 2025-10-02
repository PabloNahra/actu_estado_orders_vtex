# funciones
import pyodbc
import config
import datetime
import requests


# Inserto registro de proceso actualizado
def log_grabar(texto, dir_log):
    fecha_actual = datetime.datetime.today()
    log = f'{fecha_actual} - Operación: {texto}\n'
    archivo = open(dir_log, 'a')
    archivo.write(log)
    archivo.close()
    return 0


def recuperar_entornos(server: str, database: str, user: str, password: str, table: str):
    """
    Recupera todos los registros de una tabla SQL Server en forma de lista de diccionarios.

    Parámetros:
        server (str): nombre o dirección del servidor SQL Server
        database (str): nombre de la base de datos
        user (str): usuario de SQL Server
        password (str): contraseña del usuario
        table (str): nombre de la tabla a consultar

    Retorna:
        list[dict]: lista de diccionarios con los registros
    """
    conn = None
    resultados = []

    try:
        # Conexión a SQL Server
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password}"
        )
        cursor = conn.cursor()

        # Ejecutar consulta
        query = f"SELECT * FROM {table} WHERE Activo = '1'"
        cursor.execute(query)

        # Obtener nombres de columnas
        columns = [col[0] for col in cursor.description]

        # Transformar a lista de diccionarios
        for row in cursor.fetchall():
            resultados.append(dict(zip(columns, row)))

    except Exception as e:
        print(f"Error al recuperar entornos: {e}")
    finally:
        if conn:
            conn.close()

    return resultados



def recuperar_parametro(sql_instancia, sql_db, sql_user, sql_pass, param_key: str):
	"""
	Recupera el valor (Param_Value) de la tabla tblParametros según el param_key indicado.

	Parámetros:
		sql_instancia (str): nombre o IP del servidor SQL Server
		sql_db (str): nombre de la base de datos
		sql_user (str): usuario de SQL Server
		sql_pass (str): contraseña
		param_key (str): clave del parámetro a recuperar

	Retorna:
		str: valor del parámetro (Param_Value), o None si no se encuentra
	"""

	conexion = None
	try:
		# Conectar a SQL Server
		conexion = pyodbc.connect(
			f"DRIVER={{ODBC Driver 17 for SQL Server}};"
			f"SERVER={sql_instancia};"
			f"DATABASE={sql_db};"
			f"UID={sql_user};"
			f"PWD={sql_pass}"
		)
		cursor = conexion.cursor()

		# Consulta del parámetro
		cursor.execute(
			"SELECT Param_Value FROM tblParametros WHERE Param_Key = ?",
			(param_key,)
		)
		row = cursor.fetchone()
		return row[0] if row else None

	except Exception as e:
		print(f"Error al recuperar parámetro '{param_key}': {e}")
		return None

	finally:
		if conexion:
			conexion.close()

def recuperar_facturas(sql_instancia, sql_db, sql_user, sql_pass):
	'''
	Función para recuperar las ordenes facturadas del ERP; apuntamos a una vista para que sea más rápida
	la configuración de nuevos circuitos de facturación
	:param sql:
	:param sql_db:
	:param sql_user:
	:param sql_pass:
	:return:
	Lista de diccionarios con datos de ordenes facturadas
	'''

	# Conecto con SQL
	conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}'
	                          ';SERVER=' + sql_instancia + ';DATABASE=' + sql_db + ';UID=' + sql_user + ';PWD=' + sql_pass)

	# Consulto los nuevos comprobantes
	ordenes_facturadas = []
	consulta = conexion.cursor()

	sql = "SELECT [cve_id],[Fecha_Emision_FC] " \
	      ",[Order_id],[Invoice_id]," \
	      "[Invoice_Value] " \
	      f"FROM {config.VTEX_Order_Pend_v} " \
	      "WHERE " \
	      f"convert(varchar(8),Fecha_Emision_FC,112) >= " \
	      f"CONVERT(VARCHAR(8), DATEADD(dd, -{config.dias_facturacion}, getdate()), 112)"

	# select para pruebas con StyleStore.com
	'''
	sql = "SELECT TOP 1 99999 as cve_id, getdate() as Fecha_Emision_FC, " \
	      "'1275491282396-01' as Order_id,'9999-00000001' as Invoice_id, " \
	      " 4995 as Invoice_Value " \
	      "FROM apertura " \
	'''

	cursor = conexion.cursor().execute(sql)
	columns = [column[0] for column in cursor.description]
	for row in cursor.fetchall():
		ordenes_facturadas.append(dict(zip(columns, row)))

	return ordenes_facturadas

# insert de nuevos comprobantes
def tabla_log_put_vtas(sql_instancia, sql_db, sql_user, sql_pass, nuevas_fc):
	'''
	A partir de una lista de diccionarios con los datos de los comprobantes facturados
	grabar las mismas realizando un insert en una tabla de datos SQL
	'''
	# Conecto con SQL
	conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
	                          'SERVER=' + sql_instancia + ';DATABASE=' + sql_db + ';UID=' + sql_user + ';PWD=' + sql_pass)

	consulta = conexion.cursor()

	for comprobante in nuevas_fc:

		# Convertir la fecha al formato SQL Server
		if isinstance(comprobante['Fecha_Emision_FC'], str):
			# Si es string, asumir que ya está en formato correcto o convertirlo
			Fecha_Emision_FC_formateada = comprobante['Fecha_Emision_FC']
		else:
			# Si es datetime object
			Fecha_Emision_FC_formateada = comprobante['Fecha_Emision_FC'].strftime('%Y-%m-%d %H:%M:%S')

		sql = (f"INSERT INTO {config.VTEX_Orders_Table_Log} " \
		      "(entorno_id, Razon_Social, "
		       "BDD, id, "
		       "Fecha_Emision_FC, "
		       "Order_id, "
		       "Invoice_id, Invoice_Value, "
		       "Fecha_Informado, Leido) " \
		      "VALUES " \
		      f"('{comprobante['entorno_id']}', '{comprobante['Razon_Social']}', "
		       f"'{comprobante['BDD_Dragon']}', '{comprobante['ID']}', "
		       f"'{Fecha_Emision_FC_formateada}', " \
		      f"'{comprobante['Order_ID']}', "
		       f"'{comprobante['Invoice_ID']}'," \
		      f"{comprobante['Invoice_Value']}," \
		      f"getdate(), 0)"
		       )

		consulta.execute(sql)
		conexion.commit()

	# Cierro conexión
	consulta.close()
	conexion.close()

	return 0


# tomar comprobantes que todavía no impactaron
def comprob_a_impactar(sql_instancia, sql_db, sql_user, sql_pass, entorno_id):
	'''
	Recuperar los datos de comprobantes a impactar en VTEX
	'''
	# Conecto con SQL
	conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
	                          'SERVER=' + sql_instancia + ';DATABASE=' + sql_db + ';UID=' + sql_user + ';PWD=' + sql_pass)

	# Consulto los nuevos comprobantes
	nuevos_comprobantes = []

	sql = "SELECT Order_id, Invoice_Id, Fecha_Emision_FC, ROUND(Invoice_Value, 2) AS Invoice_Value " \
	      f"FROM {config.VTEX_Orders_Table_Log} " \
	      f"WHERE entorno_id = {entorno_id} and " \
	      f"leido = 0 and Fecha_Emision_FC >= DATEADD(day, -{config.dias_facturacion}, GETDATE())"

	cursor = conexion.cursor().execute(sql)
	columns = [column[0] for column in cursor.description]
	for row in cursor.fetchall():
		nuevos_comprobantes.append(dict(zip(columns, row)))

	return nuevos_comprobantes

def vtex_api_get_order_valores(order_id, api_key, api_token, vtex_account_name, vtex_enviroment):
	'''
	Obtener valores de una Order

	Utilizamos este servicio API según nos recomendó M3
	https://developers.vtex.com/vtex-rest-api/reference/getorder
	:param order_facturadas:
	:return:
	'''

	# Datos generales del header
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"X-VTEX-API-AppKey": api_key,
		"X-VTEX-API-AppToken": api_token
	}

	# url de api vtex
	url = f"https://{vtex_account_name}.{vtex_enviroment}.com.br/api/oms/pvt/orders/{str(order_id)}"

	response = requests.get(url, headers=headers)

	# grabar log capturando respuestas del servicio
	resultado = response.json()
	# order_valores = {'orderId': resultado['orderId'], 'status': resultado['status'], 'value': resultado['value']}
	if 'error' not in resultado:
		order_valores = {'orderId': str(order_id), 'status': resultado['status'], 'value': resultado['value']}
	else:
		order_valores = {'orderId': str(order_id)}

	return order_valores


def vtex_api_actualizar_estado_order_preparando(order_id, api_key, api_token, vtex_account_name, vtex_enviroment):
	'''
	Modificamos el estado de la Order a Preparando (Handling)
	Doc VTEX
	https://developers.vtex.com/vtex-rest-api/reference/starthandling
	:param order_id: Id de la Order en VTEX
	:return:
	'''

	# Datos generales del header
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"X-VTEX-API-AppKey": api_key,
		"X-VTEX-API-AppToken": api_token
	}

	# url de api vtex
	url = f"https://{vtex_account_name}.{vtex_enviroment}.com.br/api/oms/pvt/orders/{order_id}/start-handling"

	response = requests.post(url, headers=headers)

	return 0

def vtex_api_actualizar_estado_orders_facturado(order_facturadas,
                                                api_key, api_token,
                                                vtex_account_name, vtex_enviroment):
    '''
    Desde una lista con las ordenes que se facturaron impactar en el ambiente de vtex
    para pasar el pedido a estado facturado

    Utilizamos este servicio API según nos recomendó M3
    https://developers.vtex.com/vtex-rest-api/reference/invoicenotification
    :param order_facturadas:
    :return:
    '''

    # Datos generales del header
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-VTEX-API-AppKey": api_key,
        "X-VTEX-API-AppToken": api_token
    }

    for order in order_facturadas:
        try:
            # primero pasamos la order a preparando ('handling')
            vtex_api_actualizar_estado_order_preparando(order['Order_id'],
                                                        api_key, api_token,
                                                        vtex_account_name, vtex_enviroment)

            # url de api vtex
            # ejemplo: url = "https://stylewatch.vtexcommercestable.com.br/api/oms/pvt/orders/1275291282121-01/invoice"
            url = f"https://{vtex_account_name}.{vtex_enviroment}.com.br/api/oms/pvt/orders/{order['Order_id']}/invoice"

            # consulto el valor de la Order (definición de ECO que es el valor a informar) - 2022-11-11
            valores_order = vtex_api_get_order_valores(order['Order_id'], api_key, api_token, vtex_account_name, vtex_enviroment)

            # configuro el json para Api vtex
            # configuro el json para Api vtex
            payload = {
	            # el valor a informar es con dos decimales pero no debe incluir ningun separador de decimales
	            "invoiceValue": f"{valores_order.get('value', '') if valores_order else ''}",
	            "dispatchedDate": None,
	            "type": "Output",
	            "issuanceDate": f"{order.get('Fecha_Emision_FC', '')}",
	            # "issuanceDate": "2022-11-10T07:25:43-05:00",
	            "invoiceNumber": f"{order.get('Invoice_Id', '')}",
	            "invoiceKey": None,
	            "courier": None,
	            "trackingNumber": None,
	            "trackingUrl": None
            }
            '''
            payload = {
                # el valor a informar es con dos decimales pero no debe incluir ningun separador de decimales
                # "invoiceValue": f"{str(order['Invoice_Value']).replace('.','')}",
                "invoiceValue": f"{valores_order['value']}",
                "dispatchedDate": None,
                "type": "Output",
                "issuanceDate": f"{order['Fecha_Emision_FC']}",
                # "issuanceDate": "2022-11-10T07:25:43-05:00",
                "invoiceNumber": f"{order['Invoice_Id']}",
                "invoiceKey": None,
                "courier": None,
                "trackingNumber": None,
                "trackingUrl": None
            }'''

            response = requests.post(url, json=payload, headers=headers)

            # grabar log capturando respuestas del servicio
            resultado = response.json()
            rta = response.status_code
            if rta == 200:
                tabla_log_resultado(config.sql_server_int, config.sql_db_int,
                                    config.sql_user_int, config.sql_pass_int,
                                    order['Order_id'], 1, 'Exitoso')
            else:
                tabla_log_resultado(config.sql_server_int, config.sql_db_int,
                                    config.sql_user_int, config.sql_pass_int,
                                    order['Order_id'], 2, f"Inconveniente al actualizar - {rta} "
                                                          f"- {resultado['error']['message']}")

        except requests.exceptions.RequestException as e:
            # Error de conexión, timeout, etc.
            error_msg = f"Error de conexión en order {order['Order_id']}: {str(e)}"
            tabla_log_resultado(config.sql_server_int, config.sql_db_int,
                                config.sql_user_int, config.sql_pass_int,
                                order['Order_id'], 2, error_msg)
            continue  # Continuar con la siguiente orden

        except KeyError as e:
            # Error cuando falta una clave en el diccionario
            error_msg = f"Falta clave en datos de order {order['Order_id']}: {str(e)}"
            tabla_log_resultado(config.sql_server_int, config.sql_db_int,
                                config.sql_user_int, config.sql_pass_int,
                                order['Order_id'], 2, error_msg)
            continue  # Continuar con la siguiente orden

        except ValueError as e:
            # Error en el formato de los datos (JSON, fechas, etc.)
            error_msg = f"Error en formato de datos en order {order['Order_id']}: {str(e)}"
            tabla_log_resultado(config.sql_server_int, config.sql_db_int,
                                config.sql_user_int, config.sql_pass_int,
                                order['Order_id'], 2, error_msg)
            continue  # Continuar con la siguiente orden

        except Exception as e:
            # Captura cualquier otro error inesperado
            error_msg = f"Error inesperado en order {order['Order_id']}: {str(e)}"
            tabla_log_resultado(config.sql_server_int, config.sql_db_int,
                                config.sql_user_int, config.sql_pass_int,
                                order['Order_id'], 2, error_msg)
            continue  # Continuar con la siguiente orden

    return 0
def vtex_api_actualizar_estado_orders_facturado_OLD(order_facturadas,
                                                api_key, api_token,
                                                vtex_account_name, vtex_enviroment):
	'''
	Desde una lista con las ordenes que se facturaron impactar en el ambiente de vtex
	para pasar el pedido a estado facturado

	Utilizamos este servicio API según nos recomendó M3
	https://developers.vtex.com/vtex-rest-api/reference/invoicenotification
	:param order_facturadas:
	:return:
	'''

	# Datos generales del header
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"X-VTEX-API-AppKey": api_key,
		"X-VTEX-API-AppToken": api_token
	}

	for order in order_facturadas:

		# primero pasamos la order a preparando ('handling')
		vtex_api_actualizar_estado_order_preparando(order['Order_id'],
		                                            api_key, api_token,
		                                            vtex_account_name, vtex_enviroment)

		# url de api vtex
		# ejemplo: url = "https://stylewatch.vtexcommercestable.com.br/api/oms/pvt/orders/1275291282121-01/invoice"
		url = f"https://{vtex_account_name}.{vtex_enviroment}.com.br/api/oms/pvt/orders/{order['Order_id']}/invoice"

		# consulto el valor de la Order (definición de ECO que es el valor a informar) - 2022-11-11
		valores_order = vtex_api_get_order_valores(order['Order_id'], api_key, api_token, vtex_account_name, vtex_enviroment)

		# configuro el json para Api vtex
		payload = {
			# el valor a informar es con dos decimales pero no debe incluir ningun separador de decimales
			# "invoiceValue": f"{str(order['Invoice_Value']).replace('.','')}",
			"invoiceValue": f"{valores_order['value']}",
			"dispatchedDate": None,
			"type": "Output",
			"issuanceDate": f"{order['Fecha_Emision_FC']}",
			# "issuanceDate": "2022-11-10T07:25:43-05:00",
			"invoiceNumber": f"{order['Invoice_Id']}",
			"invoiceKey": None,
			"courier": None,
			"trackingNumber": None,
			"trackingUrl": None
		}

		response = requests.post(url, json=payload, headers=headers)

		# grabar log capturando respuestas del servicio
		resultado = response.json()
		rta = response.status_code
		if rta == 200:
			tabla_log_resultado(config.sql_instancia_sb, config.sql_db_sb,
			                    config.sql_user_sb, config.sql_pass_sb,
			                    order['Order_id'], 1, 'Exitoso')
		else:
			tabla_log_resultado(config.sql_instancia_sb, config.sql_db_sb,
			                    config.sql_user_sb, config.sql_pass_sb,
			                    order['Order_id'], 2, f"Inconveniente al actualizar - {rta} "
			                                          f"- {resultado['error']['message']}")

	return 0



def tabla_log_resultado(sql_instancia, sql_db, sql_user, sql_pass, order_id, leido_id, leido_log):
	'''
	Graba en la tabla de log del proceso el resultado de cada actualizacion
	:param sql_instancia:
	:param sql_db:
	:param sql_user:
	:param sql_pass:
	:param order_id:
	:param leido_id:
	:param leido_log:
	:return:
	'''

	# Conecto con SQL
	conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
	                          'SERVER=' + sql_instancia + ';DATABASE=' + sql_db + ';UID=' + sql_user + ';PWD=' + sql_pass)

	consulta = conexion.cursor()

	sql = f"UPDATE {config.VTEX_Orders_Table_Log} " \
	      f"SET " \
	      f"Leido = {leido_id}, " \
	      f"Leido_Fecha = GETDATE(), " \
	      f"Leido_Log = '{leido_log}' " \
	      f"FROM {config.VTEX_Orders_Table_Log} " \
	      f"WHERE " \
	      f"Order_id = '{order_id}' and " \
	      f"leido = 0"

	consulta.execute(sql)
	conexion.commit()

	# Cierro conexión
	consulta.close()
	conexion.close()

	return 0