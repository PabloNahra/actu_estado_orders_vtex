# configuraciones
from pathlib import Path

# Directorio de Log
dir_log = Path('actu_estado_orders_log.txt')

# Defino las credenciales del Server SQL de Bejerman
sql_instancia_sb = '10.10.29.159'
sql_db_sb = 'SBDASAT'
sql_user_sb = 'sa'
sql_pass_sb = 'Tetraedro2020%'

# Definino las credenciales de la API VTEX STYLE STORE
# VTEX_API_AppKey = 'vtexappkey-stylewatch-GQVYIK'
# VTEX_API_AppToken = 'VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF'
# VTEX_accountName = 'stylewatch'
# VTEX_enviroment = 'vtexcommercestable'


# Definino las credenciales de la API VTEX CARMIN WEB
VTEX_API_AppKey = 'vtexappkey-carminar-NKUENZ'
VTEX_API_AppToken = 'FXRUTJSPGEDOGPTPZKIOOMGAFMBJUVNZVHAJLWTNIJLJGXKFRWTODCUKVCUBADGLMSHLCESCUDFRYFGDNOJCGPHJJPQMAFNUXYOMQBOLIZRMEMPZVYXUUEYUUXFEZVFX'
VTEX_accountName = 'carminar'
VTEX_enviroment = 'vtexcommercestable'

# defino la vista de donde tomamos las facturas que faltan impactar
# VTEX_Order_Pend_v = 'vVTEX_Orders_Facturas_API' # StyleStore
VTEX_Order_Pend_v = 'vVTEX_Orders_Facturas_API_Carmin' # Carmin Store

# defino la tabla de log
VTEX_Orders_Table = 'tblVTEX_Orders_Facturas_API_Log_Carmin'

# parametros de funcionamiento
dias_facturacion = 30