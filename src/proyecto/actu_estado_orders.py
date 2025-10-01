# actualizar estado de order en Vtex
import funciones, funciones_excel, funciones_dragon
import config


# Control de errores
try:
	funciones.log_grabar('Prog - actualizar estado de order - Inicio', config.dir_log)

	# Recorrer cada entorno de la lista
	for entorno in config.entornos:
		try:
			funciones.log_grabar(f"Procesando entorno: {entorno['empresa']}", config.dir_log)

			# capturo las nuevas facturas de Bejerman o de Excel según corresponda
			if entorno['modalidad_fc'] == 'Bejerman':
				# capturo las nuevas facturas emitidas en el ERP Bejerman
				facturas_pend = funciones.recuperar_facturas(config.sql_instancia_sb, config.sql_db_sb,
				                                             config.sql_user_sb,
				                                             config.sql_pass_sb)

				# grabo las nuevas facturas en la tabla de log
				funciones.tabla_log_put_vtas(config.sql_instancia_sb, config.sql_db_sb, config.sql_user_sb,
				                             config.sql_pass_sb, facturas_pend)
			elif entorno['modalidad_fc'] == 'Excel':
				facturas_pend_excel = funciones_excel.lectura_excels()

				funciones_excel.tabla_log_put_vtas_excel(config.sql_instancia_sb, config.sql_db_sb,
				                                         config.sql_user_sb, config.sql_pass_sb,
				                                         facturas_pend_excel)
			elif entorno['modalidad_fc'] == 'Dragon':
				# capturo las nuevas facturas emitidas en la sucursal de Dragon
				facturas_pend = funciones_dragon.recuperar_facturas_dragon(config.sql_instancia_sb,
				                                                           config.sql_db_sb,
				                                                           config.sql_user_sb,
				                                                           config.sql_pass_sb,
				                                                           empresa_id=entorno['empresa'])

				# grabo las nuevas facturas en la tabla de log
				funciones.tabla_log_put_vtas(config.sql_instancia_sb, config.sql_db_sb, config.sql_user_sb,
				                             config.sql_pass_sb, facturas_pend)

			# capturo las facturas pendientes de impactar en VTEX
			fc_impactar = funciones.comprob_a_impactar(config.sql_instancia_sb,
			                                           config.sql_db_sb,
			                                           config.sql_user_sb,
			                                           config.sql_pass_sb)

			# impacto en VTEX
			'''
			funciones.vtex_api_actualizar_estado_orders_facturado(fc_impactar, config.VTEX_API_AppKey,
			                                                      config.VTEX_API_AppToken, config.VTEX_accountName,
			                                                      config.VTEX_enviroment)
			                                                      '''

			funciones.log_grabar(f'Entorno {entorno} procesado exitosamente', config.dir_log)

		except Exception as e:
			funciones.log_grabar(f'ERROR en entorno {entorno}: {e}', config.dir_log)
			if hasattr(e, 'message'):
				funciones.log_grabar(f'ERROR - Detalle entorno {entorno}: {e.message}', config.dir_log)
			# Continúa con el siguiente entorno
			continue

		except PermissionError as e:
			funciones.log_grabar(f'ERROR de permisos en entorno {entorno}: {e}', config.dir_log)
			if hasattr(e, 'message'):
				funciones.log_grabar(f'ERROR de permisos - Detalle entorno {entorno}: {e.message}', config.dir_log)
			# Continúa con el siguiente entorno
			continue

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