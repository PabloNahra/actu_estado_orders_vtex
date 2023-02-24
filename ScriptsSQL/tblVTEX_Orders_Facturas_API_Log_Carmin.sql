USE [SBDASAT]
GO

/****** Object:  Table [dbo].[tblVTEX_Orders_Facturas_API_Log]    Script Date: 17/11/2022 11:02:47 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tblVTEX_Orders_Facturas_API_Log_Carmin](
	[IdRegistro] [int] IDENTITY(1,1) NOT NULL,
	[cve_id] [int] NOT NULL,
	[Fecha_Emision_FC] [datetime] NOT NULL,
	[Order_id] [varchar](25) NOT NULL,
	[Invoice_id] [varchar](25) NOT NULL,
	[Invoice_Value] [decimal](16, 2) NULL,
	[Fecha_Informado] [datetime] NULL,
	[Leido] [int] NULL,
	[Leido_Fecha] [datetime] NULL,
	[Leido_Log] [varchar](250) NULL,
	[Observacion] [varchar](250) NULL,
 CONSTRAINT [PK_tblVTEX_Ordes_Facturas_API_Log_Carmin] PRIMARY KEY NONCLUSTERED 
(
	[cve_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]
GO


