# configuraciones
from pathlib import Path
import json

# Levanto las configuraciones del archivo .json
with open('config_vtex_orders_facturado.json', 'r') as file:
    # Lee el contenido del archivo JSON
    json_data = json.load(file)

# Directorio de Log
dir_log = Path(json_data['generales']['dir_log'])


# Defino las credenciales del Server SQL de la Integracion
sql_server_int = json_data['cred_SQL_Integracion']['sql_server_int']
sql_db_int = json_data['cred_SQL_Integracion']['sql_db_int']
sql_user_int = json_data['cred_SQL_Integracion']['sql_user_int']
sql_pass_int = json_data['cred_SQL_Integracion']['sql_pass_int']


# Objetos SQL
## defino la tabla de entornos
entornos = json_data['Objetos_SQL']['entornos']
## defino la tabla de parametros
parametros = json_data['Objetos_SQL']['parametros']
## Defino la vista de donde tomamos las facturas que faltan impactar desde Bejerman
##VTEX_Order_Pend_v = json_data['Objetos_SQL']['VTEX_Order_Pend_v'] # StyleStore
## Defino la vista de donde tomamos las facturas que faltan impactar desde Dragon
##VTEX_Order_Pend_v_Dragon = json_data['Objetos_SQL']['VTEX_Order_Pend_v_Dragon']
## defino la tabla de log
VTEX_Orders_Table_Log = json_data['Objetos_SQL']['VTEX_Orders_Table_Log']


# parametros de funcionamiento
dias_facturacion = json_data['generales']['dias_facturacion']

# Defino los datos de configuración para tomar los datos del excel
excel_nombre_patron = json_data['Parametros_Excel']['excel_nombre_patron']
excel_directorio = json_data['Parametros_Excel']['excel_directorio']
excel_directorio_procesado = json_data['Parametros_Excel']['excel_directorio_procesado']

# Defino las credenciales del Server SQL de Bejerman
sql_instancia_sb = json_data['cred_SQL_Bejerman']['sql_server_sb']
sql_db_sb = json_data['cred_SQL_Bejerman']['sql_db_sb']
sql_user_sb = json_data['cred_SQL_Bejerman']['sql_user_sb']
sql_pass_sb = json_data['cred_SQL_Bejerman']['sql_pass_sb']
