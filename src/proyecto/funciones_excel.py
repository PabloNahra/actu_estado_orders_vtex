import config
import glob
import pandas as pd
import funciones
import shutil
import datetime
import os
import pyodbc
def mover_archivo_xlsx(ruta_origen, arch_origen, ruta_dest, arch_dest, inf_datetime):
    '''
    Mover un archivo de una ubicación determinada a otra con detalle de
    fecha y hora del traspaso o no
    :param ruta_origen: ruta de origen
    :param arch_origen: nombre del archivo xlsx origen
    :param ruta_dest: ruta de destino
    :param arch_dest: nombre del archivo xlsx destino
    :param inf_datetime: si informa fecha y hora al pasar el archivo o no
    (si no la informa reemplaza el existente)
    :return:
    '''

    origen = ruta_origen + arch_origen + ".xlsx"

    if inf_datetime == 1:
        now = datetime.datetime.today()
        date_time = now.strftime("%Y%m%d_%H%M%S")
        destino = ruta_dest + arch_dest + "_" + date_time + ".xlsx"
    else:
        destino = ruta_dest + arch_dest + ".xlsx"

    shutil.move(origen, destino)

    return

def lectura_excels():
	'''
	Función para leer los datos de los excels que respondan al formato establecido
	y a partir de estos datos retornor una lista de diccionarios con el contenido de los excel
	:return:
	Lista de diccionarios con datos de los excels que se depositan en un directorio
	'''

	# Define el patrón de búsqueda para archivos que comiencen con "orders_" y tengan extensión .xlsx
	patron = f'{config.excel_directorio}\\{config.excel_nombre_patron}*.xlsx'

	# Usa glob para encontrar los archivos que coincidan con el patrón
	xlsx_files = glob.glob(patron)

	if xlsx_files:
		# Inicializa una lista para almacenar los diccionarios por fila
	    dicts_por_fila = []
	    # Recorre los archivos importados
	    for file in xlsx_files:
	        # Lee el archivo Excel
	        df = pd.read_excel(file)

	        # Obtiene la primera fila del DataFrame como claves
	        columnas = df.columns.tolist()

	        # Verifica que la lista contenga exactamente dos valores: "Order-id" e "Invoice_id"
	        if set(columnas) == set(["Order_id", "Invoice_id"]):
		        # Itera a través de las filas del DataFrame
		        for _, fila in df.iterrows():
			        # Crea un diccionario para la fila actual
			        fila_dict = dict(zip(columnas, fila))
			        # Agrega el diccionario a la lista
			        dicts_por_fila.append(fila_dict)

			    # mover el archivo a procesado
		        # Obtiene el nombre base del archivo
		        nombre_base = os.path.basename(file)

		        # Encuentra la posición de "orders_" y ".xlsx"
		        indice_xlsx = nombre_base.find(".xlsx")

		        # Extrae la parte antes de "orders_" y hasta la extensión ".xlsx"
		        nombre_archivo = nombre_base[:indice_xlsx]

		        mover_archivo_xlsx(config.excel_directorio, nombre_archivo,
		                           config.excel_directorio_procesado, nombre_archivo, 1)

	        else:
		        funciones.log_grabar(f'El excel no contiene exactamente las columnas requeridas: {file}', config.dir_log)

	return dicts_por_fila
def tabla_log_put_vtas_excel(sql_instancia, sql_db, sql_user, sql_pass, nuevas_fc_excel):
	'''
	A partir de una lista de diccionarios con los datos de los comprobantes facturados
	registrados en un Excel	grabar las mismas realizando un insert en una tabla de datos SQL
	'''
	# Conecto con SQL
	conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
	                          'SERVER=' + sql_instancia + ';DATABASE=' + sql_db + ';UID=' + sql_user + ';PWD=' + sql_pass)

	consulta = conexion.cursor()

	for comprobante in nuevas_fc_excel:
		# si la lista viene de Bejerman
		sql = f"INSERT INTO {config.VTEX_Orders_Table} " \
		      "(cve_id, Fecha_Emision_FC, " \
		      "Order_id, Invoice_id, " \
		      "Invoice_Value, " \
		      "Fecha_Informado, Leido) " \
		      "VALUES " \
		      f"((SELECT ISNULL(MAX(cve_id), 90000000)+1 FROM tblVTEX_Orders_Facturas_API_Log_Style " \
		      f"WHERE cve_id >= 90000000), " \
		      f"getdate(), " \
		      f"'{comprobante['Order_id']}', '{comprobante['Invoice_id']}'," \
		      f"0," \
		      f"getdate(), 0)"

		consulta.execute(sql)
		conexion.commit()


	# Cierro conexión
	consulta.close()
	conexion.close()

	return 0


