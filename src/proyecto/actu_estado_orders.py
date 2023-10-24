# actualizar estado de order en Vtex
import funciones
import config
import funciones_excel

# Control de errores
try:
	funciones.log_grabar('Prog - actualizar estado de order - Inicio', config.dir_log)

	# capturo las nuevas facturas de Bejerman o de Excel según corresponda
	if config.modalidad == 'Bejerman':
		# capturo las nuevas facturas emitidas en el ERP Bejerman
		facturas_pend = funciones.recuperar_facturas(config.sql_instancia_sb, config.sql_db_sb, config.sql_user_sb,
		                                             config.sql_pass_sb)

		# grabo las nuevas facturas en la tabla de log
		funciones.tabla_log_put_vtas(config.sql_instancia_sb, config.sql_db_sb, config.sql_user_sb,
		                             config.sql_pass_sb, facturas_pend)
	elif config.modalidad == 'Excel':
		facturas_pend_excel = funciones_excel.lectura_excels()

		funciones_excel.tabla_log_put_vtas_excel(config.sql_instancia_sb, config.sql_db_sb,
		                                         config.sql_user_sb, config.sql_pass_sb,
		                                         facturas_pend_excel)

	# capturo las facturas pendientes de impactar en VTEX
	fc_impactar = funciones.comprob_a_impactar(config.sql_instancia_sb, config.sql_db_sb, config.sql_user_sb,
	                                           config.sql_pass_sb)

	# impacto en VTEX
	funciones.vtex_api_actualizar_estado_orders_facturado(fc_impactar, config.VTEX_API_AppKey,
	                                                      config.VTEX_API_AppToken,config.VTEX_accountName,
	                                                      config.VTEX_enviroment)
except Exception as e:
	funciones.log_grabar(f'ERROR - Termino programa - Exception: {e}', config.dir_log)
	if hasattr(e, 'message'):
		funciones.log_grabar(f'ERROR - Termino programa - Message: {e.message}', config.dir_log)
except PermissionError as e:
	funciones.log_grabar(f'ERROR - Termino programa: {e}', config.dir_log)
	funciones.log_grabar('ERROR - Termino programa: Error de acceso a directorio', config.dir_log)
	if hasattr(e, 'message'):
		funciones.log_grabar(f'ERROR - Termino programa - Message: {e.message}', config.dir_log)

finally:
	funciones.log_grabar('Prog - actualizar estado de order - Fin', config.dir_log)
