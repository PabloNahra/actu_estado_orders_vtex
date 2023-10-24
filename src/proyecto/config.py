# configuraciones
from pathlib import Path
import json

# Levanto las configuraciones del archivo .json
with open('config_vtex_orders_facturado.json', 'r') as file:
    # Lee el contenido del archivo JSON
    json_data = json.load(file)

# Directorio de Log
dir_log = Path(json_data['generales']['dir_log'])

# Configuración de modalidad: "Bejerman - Leer de Bejerman las facturas" // "Excel - Leer de Planilla Excel"
modalidad = json_data['generales']['modalidad'] # 'Bejerman' // 'Excel'

# Defino las credenciales del Server SQL de Bejerman
sql_instancia_sb = json_data['cred_SQL_Bejerman']['sql_server_sb']
sql_db_sb = json_data['cred_SQL_Bejerman']['sql_db_sb']
sql_user_sb = json_data['cred_SQL_Bejerman']['sql_user_sb']
sql_pass_sb = json_data['cred_SQL_Bejerman']['sql_pass_sb']

# Definino las credenciales de la API VTEX STYLE STORE
VTEX_API_AppKey = json_data['VTEX_API']['VTEX_API_AppKey']
VTEX_API_AppToken = json_data['VTEX_API']['VTEX_API_AppToken']
VTEX_accountName = json_data['VTEX_API']['VTEX_accountName']
VTEX_enviroment = json_data['VTEX_API']['VTEX_enviroment']

# Definino las credenciales de la API VTEX CARMIN WEB
#VTEX_API_AppKey = 'vtexappkey-carminar-NKUENZ'
#VTEX_API_AppToken = 'FXRUTJSPGEDOGPTPZKIOOMGAFMBJUVNZVHAJLWTNIJLJGXKFRWTODCUKVCUBADGLMSHLCESCUDFRYFGDNOJCGPHJJPQMAFNUXYOMQBOLIZRMEMPZVYXUUEYUUXFEZVFX'
#VTEX_accountName = 'carminar'
#VTEX_enviroment = 'vtexcommercestable'

# Defino la vista de donde tomamos las facturas que faltan impactar desde Bejerman
VTEX_Order_Pend_v = json_data['Objetos_SQL']['VTEX_Order_Pend_v'] # StyleStore
# VTEX_Order_Pend_v = 'vVTEX_Orders_Facturas_API_Carmin' # Carmin Store

# Defino los datos de configuración para tomar los datos del excel
excel_nombre_patron = json_data['Parametros_Excel']['excel_nombre_patron']
excel_directorio = json_data['Parametros_Excel']['excel_directorio']
excel_directorio_procesado = json_data['Parametros_Excel']['excel_directorio_procesado']

# defino la tabla de log
VTEX_Orders_Table = json_data['Objetos_SQL']['VTEX_Orders_Table'] #'tblVTEX_Orders_Facturas_API_Log_Style' # StyleStore
# VTEX_Orders_Table = 'tblVTEX_Orders_Facturas_API_Log_Carmin' # Carmin Store

# parametros de funcionamiento
dias_facturacion = json_data['generales']['dias_facturacion']