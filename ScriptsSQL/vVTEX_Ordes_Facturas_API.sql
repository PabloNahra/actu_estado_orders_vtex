USE [SBDASAT]
GO

/****** Object:  View [dbo].[vVTEX_Ordes_Facturas_API]    Script Date: 10/11/2022 16:29:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO







--ALTER view [dbo].[vVTEX_Ordes_Facturas_API] as
/*

-- =============================================
-- Author:		Pablo Nahra
-- Create date: 2022/11/10
-- Description: Vista que usamos en un proceso de Python
que impacta la actualización de las ordenes en VTEX
-- =============================================

*/

	select 
--	convert(varchar(8),cve.cve_FEmision,112), CONVERT(VARCHAR(8), DATEADD(dd, -30, getdate()), 112),
	cve.cve_id,
	cve.cve_FEmision as Fecha_Emision_FC,
	dscv.Dscv_IdWeb as Order_id,
	cve.cve_CodPvt+'-'+cve.cve_nro as Invoice_id,
	cve.cve_ImpMonEmis as Invoice_Value
	
	--FROM segcabv AS scv WITH(nolock) 
	--Join 
	from 
	cabventa as cve WITH(nolock) 
	--	on scv.scv_id = cve.cvescv_id
	Join TipComp AS tco WITH(nolock) 
		on tco.tco_cod = cve.cvetco_Cod
	Join DtsSegCabV as dscv WITH(nolock) 
		on dscv.scv_id = cve.cvescv_id
	left Join tblVTEX_Ordes_Facturas_API_Log as lg WITH(nolock) 
		on lg.cve_id = cve.cve_id
	where 
	cve.cve_CodPvt in ('0085', '0186') and isnull(cve.cve_NroCAITal ,'') <> ''
	and tco.tco_TipoFijo = 'FC' and tco.tco_Circuito = 'V'
	and isnull(lg.cve_id,'') = '' 
	and convert(varchar(10),cve.cve_FEmision,112) >= '20221101' 
	and isnull(ltrim(rtrim(dscv.Dscv_IdWeb)), '') <> '' 
	and ISNULL(ltrim(rtrim(cve.cve_NroCAITal)), '') <> ''
	and 
	(
	--PEDIDOS VTEX
		(
		LEN(ltrim(rtrim(dscv.Dscv_IdWeb))) = 16
		and isnumeric(ltrim(rtrim(REPLACE(dscv.Dscv_IdWeb, '-', '')))) = 1
		)
	or
	--PEDIDOS ML
		(
		LEFT(ltrim(rtrim(dscv.Dscv_IdWeb)), 3) = 'ML-'
		AND
		isnumeric(ltrim(rtrim(REPLACE(dscv.Dscv_IdWeb, 'ML-', '')))) = 1
		)
	or
	--PEDIDOS ICBC
		(
		LEFT(ltrim(rtrim(dscv.Dscv_IdWeb)), 4) = 'ICB-'
		AND
		isnumeric(ltrim(rtrim(REPLACE(dscv.Dscv_IdWeb, 'ICB-', '')))) = 1
		)
	or
	--PEDIDOS BNA
		(
		LEFT(ltrim(rtrim(dscv.Dscv_IdWeb)), 4) = 'BNA-'
		AND
		isnumeric(ltrim(rtrim(REPLACE(dscv.Dscv_IdWeb, 'BNA-', '')))) = 1
		)
		
	)
	

--order by invoice_id desc




GO


