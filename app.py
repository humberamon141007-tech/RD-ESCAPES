import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Importaciones para generar PDFs profesionales
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Configuración de la página con diseño ancho
st.set_page_config(
    page_title="RD-ESCAPES - Software de Gestión Profesional",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ESTILO VISUAL PROFESIONAL: CARBONO & NEÓN PREMIUM ---
st.markdown(
    """
    <style>
    /* Estilos generales de la aplicación */
    .stApp {
        background-color: #0b0e14;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Contenedores de métricas con efecto profesional */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-left: 4px solid #ff6600;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #ff6600;
    }

    /* Encabezados elegantes */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Botones principales con degradado de competición */
    .stButton>button {
        background: linear-gradient(135deg, #ff6600 0%, #e65c00 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 14px rgba(255, 102, 0, 0.35);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff8533 0%, #ff6600 100%);
        box-shadow: 0 6px 20px rgba(255, 102, 0, 0.5);
        transform: translateY(-1px);
    }

    /* Botones de la barra lateral desplegada */
    section[data-testid="stSidebar"] .stButton>button {
        width: 100%;
        text-align: left;
        margin-bottom: 4px;
        background: #161b22;
        border: 1px solid #30363d;
        color: #c9d1d9;
        font-weight: 500;
        box-shadow: none;
        border-radius: 6px;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background: #ff6600;
        border: 1px solid #ff6600;
        color: white;
    }

    /* Barra lateral estilizada */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #21262d;
    }

    /* Tarjetas y formularios */
    div.stForm {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicializar bases de datos y configuraciones en la sesión
if "clientes" not in st.session_state:
  st.session_state.clientes = pd.DataFrame(
      columns=[
          "ID",
          "Nombre",
          "Teléfono",
          "Dirección",
          "Marca",
          "Modelo",
          "Año",
          "Patente",
      ]
  )
if "stock" not in st.session_state:
  st.session_state.stock = pd.DataFrame(
      columns=[
          "ID",
          "Código",
          "Producto",
          "Categoría",
          "Stock Actual",
          "Stock Mínimo",
          "Precio Venta",
      ]
  )
if "compras" not in st.session_state:
  st.session_state.compras = pd.DataFrame(
      columns=[
          "Fecha",
          "Distribuidor",
          "Producto",
          "Cantidad",
          "Costo Unitario",
      ]
  )
if "ventas" not in st.session_state:
  st.session_state.ventas = pd.DataFrame(
      columns=[
          "ID",
          "Fecha",
          "Cliente",
          "Vehículo",
          "Producto/Servicio",
          "Total",
      ]
  )
if "turnos" not in st.session_state:
  st.session_state.turnos = pd.DataFrame(
      columns=[
          "ID",
          "Fecha",
          "Hora",
          "Cliente",
          "Vehículo",
          "Trabajo a Realizar",
      ]
  )
if "distribuidores" not in st.session_state:
  st.session_state.distribuidores = pd.DataFrame(
      columns=[
          "ID",
          "Nombre Empresa",
          "CUIT",
          "Teléfono",
          "Dirección",
          "Email",
          "Insumos / Repuestos",
      ]
  )
if "agenda" not in st.session_state:
  st.session_state.agenda = pd.DataFrame(
      columns=[
          "ID",
          "Nombre / Contacto",
          "Teléfono",
          "Categoría",
          "Dirección / Detalle",
      ]
  )
if "compromisos" not in st.session_state:
  st.session_state.compromisos = pd.DataFrame(
      columns=[
          "ID",
          "Tipo",
          "N° Documento",
          "Proveedor/Destinatario",
          "Monto",
          "Emisión",
          "Vencimiento",
          "Estado",
      ]
  )
if "presupuestos" not in st.session_state:
  st.session_state.presupuestos = []

if "caja" not in st.session_state:
  st.session_state.caja = pd.DataFrame(
      columns=["Fecha", "Tipo", "Concepto", "Monto"]
  )

if "gastos_fijos" not in st.session_state:
  st.session_state.gastos_fijos = pd.DataFrame(
      columns=["ID", "Fecha", "Concepto", "Categoría", "Monto"]
  )

if "categorias_stock" not in st.session_state:
  st.session_state.categorias_stock = [
      "Silenciadores",
      "Coples / Abrazaderas",
      "Flexibles",
      "Punteras",
      "Deportivos",
      "Accesorios",
  ]

# Orden predeterminado del menú (incluyendo Gastos Fijos)
if "orden_menu" not in st.session_state:
  st.session_state.orden_menu = [
      "📊 Panel Principal",
      "📈 Reportes y Gráficos de Caja",
      "💡 Control de Gastos Fijos",
      "👥 Clientes",
      "📝 Presupuestos",
      "💰 Ventas",
      "📦 Control de Stock",
      "🛒 Compras",
      "💳 Cheques y Compromisos",
      "💵 Caja Diaria",
      "📅 Calendario de Turnos",
      "📖 Agenda y Contactos",
      "🏭 Distribuidores y Proveedores",
      "⚙️ Configuración",
  ]

if "menu_activo" not in st.session_state:
  st.session_state.menu_activo = "📊 Panel Principal"


# Función para generar el PDF de presupuestos con Marca de Agua
def generar_pdf_presupuesto(
    nro_presupuesto,
    fecha,
    cliente_info,
    vehiculo_info,
    items,
    total_general,
):
  filename = f"Presupuesto_{nro_presupuesto.replace('/', '-')}.pdf"
  c = canvas.Canvas(filename, pagesize=letter)
  width, height = letter

  logo_path = "logo.jpg"
  if os.path.exists(logo_path):
    try:
      c.saveState()
      c.setFillAlpha(0.12)
      c.setStrokeAlpha(0.12)
      c.drawImage(
          logo_path,
          width / 2 - 150,
          height / 2 - 150,
          width=300,
          height=300,
          preserveAspectRatio=True,
          mask="auto",
      )
      c.restoreState()
    except Exception:
      pass

  c.setFont("Helvetica-Bold", 14)
  c.drawString(200, height - 40, "PRESUPUESTO / COTIZACIÓN COMERCIAL")

  c.setFont("Helvetica-Bold", 10)
  c.drawString(50, height - 80, "PROVEEDOR")
  c.setFont("Helvetica", 9)
  c.drawString(50, height - 95, "RD Escapes")
  c.drawString(50, height - 110, "Responsable: Ramon Chavez")
  c.drawString(50, height - 125, "Teléfono: 297-4050219")
  c.drawString(50, height - 140, "Email: humbertomch@hotmail.com")
  c.drawString(50, height - 155, "Dirección: 1 de Mayo 127 B Ciudadela")
  c.drawString(50, height - 170, "Localidad: COMODORO RIVADAVIA")

  c.setFont("Helvetica", 9)
  c.drawString(350, height - 95, f"Presupuesto N°: {nro_presupuesto}")
  c.drawString(350, height - 110, f"Fecha de emisión: {fecha}")
  c.drawString(350, height - 125, "Plazo de entrega: A COORDINAR")
  c.drawString(350, height - 140, "Plazo de pago: 60 Días")

  c.setFont("Helvetica-Bold", 10)
  c.drawString(50, height - 205, "CLIENTES")
  c.setFont("Helvetica", 9)
  c.drawString(50, height - 220, f"Empresa / Cliente: {cliente_info}")
  c.drawString(50, height - 235, f"Vehículo / Patente: {vehiculo_info}")

  c.line(50, height - 250, width - 50, height - 250)

  y = height - 270
  c.setFont("Helvetica-Bold", 9)
  c.drawString(50, y, "DESCRIPCIÓN")
  c.drawString(380, y, "CANT")
  c.drawString(430, y, "PRECIO UN.")
  c.drawString(510, y, "TOTAL")
  c.line(50, y - 5, width - 50, y - 5)

  y -= 20
  c.setFont("Helvetica", 9)
  for item in items:
    desc, cant, p_unit, p_total = item
    c.drawString(50, y, str(desc)[:60])
    c.drawString(380, y, str(cant))
    c.drawString(430, y, f"${p_unit:,.2f}")
    c.drawString(510, y, f"${p_total:,.2f}")
    y -= 18

  c.line(50, y - 5, width - 50, y - 5)
  y -= 25
  c.setFont("Helvetica-Bold", 10)
  c.drawString(380, y, "TOTAL:")
  c.drawString(510, y, f"${total_general:,.2f}")

  y -= 50
  c.setFont("Helvetica-Bold", 9)
  c.drawString(50, y, "Condiciones comerciales")
  y -= 15
  c.setFont("Helvetica", 8)
  c.drawString(50, y, "• Presupuesto válido por 5 días desde su emisión.")
  y -= 12
  c.drawString(
      50, y, "• Plazo de pago con depósito en cuenta corriente: 60 días fecha factura."
  )
  y -= 12
  c.drawString(
      50,
      y,
      "• Los valores indicados se mantienen vigentes siempre que se respeten"
      " los plazos de pago establecidos.",
  )
  y -= 12
  c.drawString(
      50,
      y,
      "• La ejecución de los trabajos, entrega de materiales quedaran sujetas a"
      " la recepcion previa de la orden de compra correspondiente.",
  )
  y -= 12
  c.drawString(50, y, "• Entrega a coordinar.")

  c.save()
  return filename


# --- BARRA LATERAL CON EL LOGO DEL TALLER ---
logo_app = "logo.jpg"
if os.path.exists(logo_app):
  st.sidebar.image(logo_app, width=200)

st.sidebar.markdown("### 📂 Navegación Principal")

for opcion in st.session_state.orden_menu:
  if st.sidebar.button(opcion, key=f"btn_{opcion}"):
    st.session_state.menu_activo = opcion

menu = st.session_state.menu_activo

# ----------------- PANEL PRINCIPAL -----------------
if menu == "📊 Panel Principal":
  st.title("📊 Panel de Control - RD-ESCAPES")
  st.markdown(
      "Resumen general del estado operativo y financiero de tu taller."
  )
  st.markdown("")

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Clientes", len(st.session_state.clientes))
  col2.metric("Productos", len(st.session_state.stock))
  col3.metric("Turnos", len(st.session_state.turnos))
  col4.metric(
      "Cheques Pendientes",
      len(
          st.session_state.compromisos[
              st.session_state.compromisos["Estado"] == "Pendiente"
          ]
      )
      if not st.session_state.compromisos.empty
      else 0,
  )

  st.markdown("")
  if not st.session_state.compromisos.empty:
    hoy = datetime.date.today()
    pendientes = st.session_state.compromisos[
        st.session_state.compromisos["Estado"] == "Pendiente"
    ].copy()
    if not pendientes.empty:
      pendientes["Vencimiento_dt"] = pd.to_datetime(
          pendientes["Vencimiento"]
      ).dt.date
      por_vencer = pendientes[
          (pendientes["Vencimiento_dt"] - hoy).apply(lambda x: x.days) <= 5
      ]
      if not por_vencer.empty:
        st.error(
            "⚠️ ¡ATENCIÓN! Hay cheques o compromisos próximos a vencer o"
            " vencidos:"
        )
        st.dataframe(
            por_vencer[
                [
                    "ID",
                    "Tipo",
                    "N° Documento",
                    "Proveedor/Destinatario",
                    "Monto",
                    "Vencimiento",
                ]
            ],
            use_container_width=True,
        )

  st.markdown("### 🚨 Alertas de Stock Bajo")
  if not st.session_state.stock.empty:
    stock_df = st.session_state.stock
    alertas = stock_df[stock_df["Stock Actual"] <= stock_df["Stock Mínimo"]]
    if not alertas.empty:
      st.error("¡Atención! Productos con stock bajo en inventario:")
      st.dataframe(alertas, use_container_width=True)
    else:
      st.success("¡Todo en orden! No hay productos con faltante de stock.")
  else:
    st.info("Aún no hay productos cargados en el inventario.")

# ----------------- REPORTES Y GRÁFICOS DE CAJA -----------------
elif menu == "📈 Reportes y Gráficos de Caja":
  st.title("📈 Reportes Financieros y Gráficos de Caja")
  st.markdown(
      "Análisis en tiempo real de ingresos, egresos y porcentajes de rentabilidad."
  )
  st.markdown("")

  if not st.session_state.caja.empty:
    df_caja = st.session_state.caja
    ingresos_total = df_caja[df_caja["Tipo"].str.contains("Ingreso")][
        "Monto"
    ].sum()
    egresos_total = df_caja[df_caja["Tipo"].str.contains("Egreso")][
        "Monto"
    ].sum()
    balance_neto = ingresos_total - egresos_total

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ingresos", f"${ingresos_total:,.2f}")
    col2.metric("Total Egresos", f"${egresos_total:,.2f}")
    col3.metric("Balance Neto en Caja", f"${balance_neto:,.2f}", delta=balance_neto)

    st.markdown("---")

    if ingresos_total > 0 or egresos_total > 0:
      st.subheader("📊 Distribución Porcentual (Ingresos vs Egresos)")

      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

      etiquetas = ["Ingresos", "Egresos"]
      valores = [ingresos_total, egresos_total]
      colores = ["#2ecc71", "#e74c3c"]

      ax1.pie(
          valores,
          labels=etiquetas,
          autopct="%1.1f%%",
          startangle=90,
          colors=colores,
          textprops={"color": "white", "weight": "bold"},
      )
      ax1.set_title(
          "Proporción General (%)", color="white", fontsize=14, weight="bold"
      )

      ax2.bar(
          etiquetas,
          valores,
          color=colores,
          width=0.5,
          edgecolor="white",
          linewidth=1,
      )
      ax2.set_ylabel("Monto en ($)", color="white", weight="bold")
      ax2.set_title(
          "Comparativa en Pesos ($)", color="white", fontsize=14, weight="bold"
      )
      ax2.tick_params(colors="white")
      ax2.grid(axis="y", linestyle="--", alpha=0.3)

      fig.patch.set_facecolor("#0b0e14")
      ax1.set_facecolor("#0b0e14")
      ax2.set_facecolor("#0b0e14")

      st.pyplot(fig)
    else:
      st.info(
          "Los montos totales son cero, registra ingresos o egresos para"
          " visualizar los gráficos."
      )

    st.markdown("### 📋 Detalle Completo de Movimientos")
    st.dataframe(df_caja, use_container_width=True)
  else:
    st.info(
        "Aún no hay movimientos de caja registrados para generar reportes."
    )

# ----------------- CONTROL DE GASTOS FIJOS -----------------
elif menu == "💡 Control de Gastos Fijos":
  st.title("💡 Control de Gastos Fijos del Taller")
  st.markdown(
      "Registra los servicios básicos (Luz, Gas, Internet, Alquiler, etc.) y"
      " mantén el control contable."
  )

  with st.form("form_gasto_fijo", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      fecha_g = st.date_input("Fecha de Pago / Registro", datetime.date.today())
      concepto_g = st.text_input(
          "Concepto (ej. Factura de Luz SCPL, Internet, Alquiler)"
      )
    with col2:
      categoria_g = st.selectbox(
          "Categoría de Gasto", ["Luz", "Gas", "Internet / Teléfono", "Alquiler", "Impuestos / Tasas", "Otro"]
      )
      monto_g = st.number_input("Monto ($)", min_value=0.0, value=0.0)

    submit_gasto = st.form_submit_button("Registrar Gasto Fijo")
    if submit_gasto:
      if concepto_g and monto_g > 0:
        nuevo_id_g = (
            int(st.session_state.gastos_fijos["ID"].max()) + 1
            if not st.session_state.gastos_fijos.empty
            else 1
        )
        nuevo_reg_g = pd.DataFrame({
            "ID": [nuevo_id_g],
            "Fecha": [str(fecha_g)],
            "Concepto": [concepto_g],
            "Categoría": [categoria_g],
            "Monto": [monto_g],
        })
        # Guardar en gastos fijos
        st.session_state.gastos_fijos = pd.concat(
            [st.session_state.gastos_fijos, nuevo_reg_g], ignore_index=True
        )
        # Sincronizar automáticamente como Egreso en la Caja Diaria
        nuevo_egreso_caja = pd.DataFrame({
            "Fecha": [str(fecha_g)],
            "Tipo": ["Egreso (Gasto Fijo)"],
            "Concepto": [f"Gasto Fijo [{categoria_g}]: {concepto_g}"],
            "Monto": [monto_g],
        })
        st.session_state.caja = pd.concat(
            [st.session_state.caja, nuevo_egreso_caja], ignore_index=True
        )
        st.success(
            "¡Gasto fijo registrado con éxito y descontado de caja automáticamente!"
        )
      else:
        st.warning("Completa el concepto y un monto mayor a 0.")

  st.markdown("### 📋 Historial de Gastos Fijos")
  if not st.session_state.gastos_fijos.empty:
    total_gf = st.session_state.gastos_fijos["Monto"].sum()
    st.metric("Total Acumulado en Gastos Fijos", f"${total_gf:,.2f}")
    st.markdown("---")
    st.dataframe(st.session_state.gastos_fijos, use_container_width=True)

    id_del_g = st.number_input(
        "ID de Gasto Fijo a eliminar por error", min_value=0, step=1, key="del_gf"
    )
    if st.button("Eliminar Gasto Fijo"):
      if id_del_g in st.session_state.gastos_fijos["ID"].values:
        st.session_state.gastos_fijos = st.session_state.gastos_fijos[
            st.session_state.gastos_fijos["ID"] != id_del_g
        ]
        st.success("Gasto fijo eliminado correctamente.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")
  else:
    st.info("Aún no hay gastos fijos registrados.")

# ----------------- CLIENTES -----------------
elif menu == "👥 Clientes":
  st.title("👥 Gestión de Clientes y Vehículos")
  st.markdown("Registra y administra la base de datos de clientes y unidades.")

  with st.form("form_cliente", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      nombre = st.text_input("Nombre / Empresa")
      telefono = st.text_input("Teléfono / Celular")
      direccion = st.text_input("Dirección")
    with col2:
      marca = st.text_input("Marca del Vehículo (ej. Toyota)")
      modelo = st.text_input("Modelo (ej. Etios)")
      anio = st.text_input("Año (ej. 2022)")
      patente = st.text_input("Patente / Dominio")

    submit_cliente = st.form_submit_button("Guardar Cliente y Vehículo")
    if submit_cliente:
      if nombre and patente:
        nuevo_id = (
            int(st.session_state.clientes["ID"].max()) + 1
            if not st.session_state.clientes.empty
            else 1
        )
        nuevo_reg = pd.DataFrame({
            "ID": [nuevo_id],
            "Nombre": [nombre],
            "Teléfono": [telefono],
            "Dirección": [direccion],
            "Marca": [marca],
            "Modelo": [modelo],
            "Año": [anio],
            "Patente": [patente],
        })
        st.session_state.clientes = pd.concat(
            [st.session_state.clientes, nuevo_reg], ignore_index=True
        )
        st.success(f"Cliente {nombre} registrado exitosamente.")
      else:
        st.warning("Nombre y Patente son obligatorios.")

  st.markdown("### Listado de Clientes y Vehículos")
  if not st.session_state.clientes.empty:
    st.dataframe(st.session_state.clientes, use_container_width=True)
    id_del_c = st.number_input(
        "ID de Cliente a eliminar por error", min_value=0, step=1, key="del_c"
    )
    if st.button("Eliminar Cliente"):
      if id_del_c in st.session_state.clientes["ID"].values:
        st.session_state.clientes = st.session_state.clientes[
            st.session_state.clientes["ID"] != id_del_c
        ]
        st.success("Cliente eliminado correctamente.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")
  else:
    st.info("No hay clientes cargados.")

# ----------------- AGENDA Y CONTACTOS -----------------
elif menu == "📖 Agenda y Contactos":
  st.title("📖 Libreta de Contactos y Agenda")
  st.markdown("Directorio rápido de contactos institucionales y talleres.")

  with st.form("form_agenda", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      contacto_nombre = st.text_input("Nombre / Empresa del Contacto")
      contacto_tel = st.text_input("Teléfono / Celular")
    with col2:
      contacto_cat = st.selectbox(
          "Categoría", ["Cliente", "Proveedor", "Taller Amigo", "Otro"]
      )
      contacto_dir = st.text_input("Dirección o Nota adicional")

    submit_agenda = st.form_submit_button("Guardar Contacto")
    if submit_agenda:
      if contacto_nombre and contacto_tel:
        nuevo_id_ag = (
            int(st.session_state.agenda["ID"].max()) + 1
            if not st.session_state.agenda.empty
            else 1
        )
        nuevo_cont = pd.DataFrame({
            "ID": [nuevo_id_ag],
            "Nombre / Contacto": [contacto_nombre],
            "Teléfono": [contacto_tel],
            "Categoría": [contacto_cat],
            "Dirección / Detalle": [contacto_dir],
        })
        st.session_state.agenda = pd.concat(
            [st.session_state.agenda, nuevo_cont], ignore_index=True
        )
        st.success(f"Contacto '{contacto_nombre}' guardado en la agenda.")
      else:
        st.warning("Nombre y Teléfono son obligatorios.")

  st.markdown("### 📋 Directorio de Contactos")
  if not st.session_state.agenda.empty:
    st.dataframe(st.session_state.agenda, use_container_width=True)

    id_del_ag = st.number_input(
        "ID de Contacto a eliminar", min_value=0, step=1, key="del_agenda"
    )
    if st.button("Eliminar Contacto"):
      if id_del_ag in st.session_state.agenda["ID"].values:
        st.session_state.agenda = st.session_state.agenda[
            st.session_state.agenda["ID"] != id_del_ag
        ]
        st.success("Contacto eliminado.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")
  else:
    st.info("Aún no hay contactos guardados en la agenda.")

# ----------------- CONTROL DE STOCK -----------------
elif menu == "📦 Control de Stock":
  st.title("📦 Control de Stock y Alertas")
  st.markdown("Gestión de inventario de escapes, repuestos y accesorios.")

  with st.form("form_stock", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
      codigo = st.text_input("Código de Producto")
      producto = st.text_input("Nombre del Escape / Repuesto")
    with col2:
      categoria = st.selectbox(
          "Categoría", st.session_state.categorias_stock
      )
      stock_actual = st.number_input("Stock Actual", min_value=0, value=10)
    with col3:
      stock_minimo = st.number_input(
          "Stock Mínimo (Alerta)", min_value=0, value=3
      )
      precio_venta = st.number_input("Precio de Venta ($)", min_value=0.0, value=0.0)

    submit_stock = st.form_submit_button("Registrar Producto")
    if submit_stock:
      if codigo and producto:
        nuevo_id = (
            int(st.session_state.stock["ID"].max()) + 1
            if not st.session_state.stock.empty
            else 1
        )
        nuevo_prod = pd.DataFrame({
            "ID": [nuevo_id],
            "Código": [codigo],
            "Producto": [producto],
            "Categoría": [categoria],
            "Stock Actual": [stock_actual],
            "Stock Mínimo": [stock_minimo],
            "Precio Venta": [precio_venta],
        })
        st.session_state.stock = pd.concat(
            [st.session_state.stock, nuevo_prod], ignore_index=True
        )
        st.success("Producto registrado correctamente.")
      else:
        st.warning("Código y Nombre son obligatorios.")

  st.markdown("### Inventario Actual")
  if not st.session_state.stock.empty:
    st.dataframe(st.session_state.stock, use_container_width=True)

    id_del_s = st.number_input(
        "ID de Producto a eliminar por error", min_value=0, step=1, key="del_s"
    )
    if st.button("Eliminar Producto del Stock"):
      if id_del_s in st.session_state.stock["ID"].values:
        st.session_state.stock = st.session_state.stock[
            st.session_state.stock["ID"] != id_del_s
        ]
        st.success("Producto eliminado del stock.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")

    csv = st.session_state.stock.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descargar Stock en CSV",
        csv,
        "stock_rd_escapes.csv",
        "text/csv",
        key="download-stock",
    )
  else:
    st.info("No hay productos cargados.")

# ----------------- COMPRAS -----------------
elif menu == "🛒 Compras":
  st.title("🛒 Registro de Compras a Proveedores")
  st.markdown("Control de insumos adquiridos y descuento automático en caja.")

  with st.form("form_compras", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      fecha = st.date_input("Fecha de Compra", datetime.date.today())
      distribuidor = st.text_input("Distribuidor / Proveedor")
    with col2:
      producto_compra = st.text_input("Producto Adquirido")
      cantidad = st.number_input("Cantidad", min_value=1, value=1)
      costo = st.number_input("Costo Unitario ($)", min_value=0.0, value=0.0)

    submit_compra = st.form_submit_button("Registrar Compra")
    if submit_compra:
      nueva_compra = pd.DataFrame({
          "Fecha": [str(fecha)],
          "Distribuidor": [distribuidor],
          "Producto": [producto_compra],
          "Cantidad": [cantidad],
          "Costo Unitario": [costo],
      })
      st.session_state.compras = pd.concat(
          [st.session_state.compras, nueva_compra], ignore_index=True
      )
      total_compra = cantidad * costo
      nuevo_egreso = pd.DataFrame({
          "Fecha": [str(fecha)],
          "Tipo": ["Egreso (Compra)"],
          "Concepto": [f"Compra a {distribuidor}: {producto_compra}"],
          "Monto": [total_compra],
      })
      st.session_state.caja = pd.concat(
          [st.session_state.caja, nuevo_egreso], ignore_index=True
      )
      st.success("Compra registrada y descontada de caja con éxito.")

  st.markdown("### Historial de Compras")
  st.dataframe(st.session_state.compras, use_container_width=True)

# ----------------- VENTAS -----------------
elif menu == "💰 Ventas":
  st.title("💰 Registro de Ventas y Servicios")
  st.markdown("Control de ventas de productos y servicios de instalación.")

  with st.form("form_ventas", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      fecha_v = st.date_input("Fecha de Venta", datetime.date.today())
      cliente_v = st.text_input("Cliente")
      vehiculo_v = st.text_input("Vehículo / Patente")
    with col2:
      detalle_v = st.text_input("Producto o Servicio")
      total_v = st.number_input("Total Cobrado ($)", min_value=0.0, value=0.0)

    submit_venta = st.form_submit_button("Registrar Venta")
    if submit_venta:
      nuevo_id = (
          int(st.session_state.ventas["ID"].max()) + 1
          if not st.session_state.ventas.empty
          else 1
      )
      nueva_venta = pd.DataFrame({
          "ID": [nuevo_id],
          "Fecha": [str(fecha_v)],
          "Cliente": [cliente_v],
          "Vehículo": [vehiculo_v],
          "Producto/Servicio": [detalle_v],
          "Total": [total_v],
      })
      st.session_state.ventas = pd.concat(
          [st.session_state.ventas, nueva_venta], ignore_index=True
      )
      nuevo_ingreso = pd.DataFrame({
          "Fecha": [str(fecha_v)],
          "Tipo": ["Ingreso (Venta)"],
          "Concepto": [f"Venta a {cliente_v} ({detalle_v})"],
          "Monto": [total_v],
      })
      st.session_state.caja = pd.concat(
          [st.session_state.caja, nuevo_ingreso], ignore_index=True
      )
      st.success("Venta registrada y sumada a caja con éxito.")

  st.markdown("### Historial de Ventas")
  if not st.session_state.ventas.empty:
    st.dataframe(st.session_state.ventas, use_container_width=True)

    id_del_v = st.number_input(
        "ID de Venta a eliminar por error", min_value=0, step=1, key="del_v"
    )
    if st.button("Eliminar Venta"):
      if id_del_v in st.session_state.ventas["ID"].values:
        st.session_state.ventas = st.session_state.ventas[
            st.session_state.ventas["ID"] != id_del_v
        ]
        st.success("Venta eliminada correctamente.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")

    csv_v = st.session_state.ventas.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descargar Ventas en CSV",
        csv_v,
        "ventas_rd_escapes.csv",
        "text/csv",
        key="download-ventas",
    )
  else:
    st.info("No hay ventas registradas aún.")

# ----------------- PRESUPUESTOS (PDF CON MARCA DE AGUA) -----------------
elif menu == "📝 Presupuestos":
  st.title("📝 Generador de Presupuestos Profesionales (Formato PDF)")
  st.markdown(
      "Elabora cotizaciones comerciales formales con marca de agua y diseño"
      " institucional."
  )

  col_1, col_2 = st.columns(2)
  with col_1:
    cliente_pres = st.text_input(
        "Cliente / Empresa (ej. CLEAR PETROLEUM S.A.)"
    )
  with col_2:
    vehiculo_pres = st.text_input(
        "Vehículo y Patente (ej. TOYOTA ETIOS - AB988AI)"
    )

  st.markdown("### 🛒 Agregar Ítems al Presupuesto")
  with st.form("form_item_presupuesto", clear_on_submit=True):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
      desc_item = st.text_input(
          "Descripción (ej. Fabricación de salida de escape)"
      )
    with col_b:
      cant_item = st.number_input("Cantidad", min_value=1, value=1)
    with col_c:
      precio_unit_item = st.number_input(
          "Precio Unitario ($)", min_value=0.0, value=0.0
      )

    add_item_btn = st.form_submit_button("Añadir Ítems al Detalle")
    if add_item_btn:
      if desc_item and precio_unit_item > 0:
        total_item = cant_item * precio_unit_item
        if "temp_items" not in st.session_state:
          st.session_state.temp_items = []
        st.session_state.temp_items.append(
            (desc_item, cant_item, precio_unit_item, total_item)
        )
        st.success("Ítem agregado al presupuesto.")
      else:
        st.warning("Completa la descripción y un precio mayor a 0.")

  if "temp_items" in st.session_state and st.session_state.temp_items:
    st.markdown("#### Detalle actual del Presupuesto:")
    df_temp = pd.DataFrame(
        st.session_state.temp_items,
        columns=["Descripción", "Cantidad", "Precio Unitario", "Total"],
    )
    st.dataframe(df_temp, use_container_width=True)

    total_presupuesto = df_temp["Total"].sum()
    st.markdown(f"### **Total General: ${total_presupuesto:,.2f}**")

    if st.button("📄 Generar y Descargar Presupuesto en PDF"):
      nro_p = len(st.session_state.presupuestos) + 256
      nro_str = f"{nro_p}/ARBAIT"
      fecha_actual = datetime.date.today().strftime("%d/%m/%Y")

      pdf_path = generar_pdf_presupuesto(
          nro_str,
          fecha_actual,
          cliente_pres,
          vehiculo_pres,
          st.session_state.temp_items,
          total_presupuesto,
      )

      st.session_state.presupuestos.append({
          "N°": nro_str,
          "Fecha": fecha_actual,
          "Cliente": cliente_pres,
          "Vehículo": vehiculo_pres,
          "Total": total_presupuesto,
      })

      st.success("¡Presupuesto generado con éxito!")

      with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Descargar PDF con Marca de Agua (Imprimir / WhatsApp)",
            data=f,
            file_name=pdf_path,
            mime="application/pdf",
        )

    if st.button("🗑️ Limpiar / Reiniciar Presupuesto"):
      st.session_state.temp_items = []
      st.rerun()
  else:
    st.info("Agrega ítems arriba para armar el presupuesto en PDF.")

# ----------------- CHEQUES Y COMPROMISOS DE PAGO -----------------
elif menu == "💳 Cheques y Compromisos":
  st.title("💳 Control de Cheques, E-Cheqs y Compromisos de Pago")
  st.markdown("Seguimiento de documentos financieros y alertas de vencimiento.")

  lista_proveedores = (
      st.session_state.distribuidores["Nombre Empresa"].tolist()
      if not st.session_state.distribuidores.empty
      else ["Sin proveedores cargados"]
  )

  with st.form("form_compromiso", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      tipo_comp = st.selectbox(
          "Tipo de Documento",
          ["E-Cheq", "Cheque Físico", "Pagaré", "Cuenta Corriente / Otro"],
      )
      nro_doc = st.text_input("N° de Documento / Cheque")
      proveedor_comp = st.selectbox(
          "Proveedor / Destinatario", lista_proveedores
      )
    with col2:
      monto_comp = st.number_input("Monto ($)", min_value=0.0, value=0.0)
      fecha_emision = st.date_input(
          "Fecha de Emisión", datetime.date.today()
      )
      fecha_pago = st.date_input(
          "Fecha de Pago / Vencimiento",
          datetime.date.today() + datetime.timedelta(days=30),
      )

    submit_comp = st.form_submit_button("Registrar Compromiso de Pago")
    if submit_comp:
      if (
          nro_doc
          and proveedor_comp != "Sin proveedores cargados"
          and monto_comp > 0
      ):
        nuevo_id = (
            int(st.session_state.compromisos["ID"].max()) + 1
            if not st.session_state.compromisos.empty
            else 1
        )
        nuevo_reg_c = pd.DataFrame({
            "ID": [nuevo_id],
            "Tipo": [tipo_comp],
            "N° Documento": [nro_doc],
            "Proveedor/Destinatario": [proveedor_comp],
            "Monto": [monto_comp],
            "Emisión": [str(fecha_emision)],
            "Vencimiento": [str(fecha_pago)],
            "Estado": ["Pendiente"],
        })
        st.session_state.compromisos = pd.concat(
            [st.session_state.compromisos, nuevo_reg_c], ignore_index=True
        )
        st.success("Compromiso de pago registrado con éxito.")
      else:
        st.warning(
            "Completa el N° de documento, selecciona un proveedor válido y un"
            " monto mayor a 0."
        )

  st.markdown("### 📋 Listado de Compromisos Registrados")
  if not st.session_state.compromisos.empty:
    st.dataframe(st.session_state.compromisos, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
      id_pagado = st.number_input(
          "ID de Compromiso a marcar como Pagado",
          min_value=0,
          step=1,
          key="pag_comp",
      )
      if st.button("Marcar como Pagado"):
        if id_pagado in st.session_state.compromisos["ID"].values:
          st.session_state.compromisos.loc[
              st.session_state.compromisos["ID"] == id_pagado, "Estado"
          ] = "Pagado"
          st.success("Compromiso marcado como Pagado.")
          st.rerun()
        else:
          st.warning("ID no encontrado.")
    with col_b:
      id_elim = st.number_input(
          "ID de Compromiso a eliminar", min_value=0, step=1, key="del_comp"
      )
      if st.button("Eliminar Registro"):
        if id_elim in st.session_state.compromisos["ID"].values:
          st.session_state.compromisos = st.session_state.compromisos[
              st.session_state.compromisos["ID"] != id_elim
          ]
          st.success("Compromiso eliminado.")
          st.rerun()
        else:
          st.warning("ID no encontrado.")
  else:
    st.info("No hay cheques o compromisos de pago cargados aún.")

# ----------------- CAJA DIARIA -----------------
elif menu == "💵 Caja Diaria":
  st.title("💵 Control de Caja Diaria (Ingresos y Egresos)")
  st.markdown("Registro y balance de entradas y salidas de efectivo.")

  with st.form("form_caja_extra", clear_on_submit=True):
    st.subheader("Registrar Movimiento Extra en Caja")
    col1, col2, col3 = st.columns(3)
    with col1:
      fecha_c = st.date_input("Fecha", datetime.date.today())
      tipo_c = st.selectbox(
          "Tipo de Movimiento", ["Ingreso Extra", "Egreso / Gasto Extra"]
      )
    with col2:
      concepto_c = st.text_input("Concepto")
    with col3:
      monto_c = st.number_input("Monto ($)", min_value=0.0, value=0.0)

    submit_caja = st.form_submit_button("Registrar Movimiento")
    if submit_caja:
      if concepto_c and monto_c > 0:
        mov = pd.DataFrame({
            "Fecha": [str(fecha_c)],
            "Tipo": [tipo_c],
            "Concepto": [concepto_c],
            "Monto": [monto_c],
        })
        st.session_state.caja = pd.concat(
            [st.session_state.caja, mov], ignore_index=True
        )
        st.success("Movimiento registrado en caja.")
      else:
        st.warning("Completa el concepto y un monto válido.")

  st.markdown("### Resumen y Movimientos de Caja")
  if not st.session_state.caja.empty:
    ingresos = st.session_state.caja[
        st.session_state.caja["Tipo"].str.contains("Ingreso")
    ]["Monto"].sum()
    egresos = st.session_state.caja[
        st.session_state.caja["Tipo"].str.contains("Egreso")
    ]["Monto"].sum()
    balance = ingresos - egresos

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Ingresos", f"${ingresos:,.2f}")
    c2.metric("Total Egresos", f"${egresos:,.2f}")
    c3.metric("Balance en Caja", f"${balance:,.2f}", delta=balance)

    st.markdown("---")
    st.dataframe(st.session_state.caja, use_container_width=True)
  else:
    st.info("Aún no hay movimientos registrados en caja.")

# ----------------- CALENDARIO DE TURNOS -----------------
elif menu == "📅 Calendario de Turnos":
  st.title("📅 Agenda de Turnos de Vehículos")
  st.markdown("Planificación y organización de los trabajos en el taller.")

  with st.form("form_turnos", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      fecha_turno = st.date_input("Fecha del Turno", datetime.date.today())
      hora_turno = st.time_input("Hora del Turno")
      cliente_t = st.text_input("Nombre del Cliente")
    with col2:
      vehiculo_t = st.text_input("Vehículo y Patente")
      trabajo = st.text_area("Trabajo a Realizar")

    submit_turno = st.form_submit_button("Agendar Turno")
    if submit_turno:
      nuevo_id = (
          int(st.session_state.turnos["ID"].max()) + 1
          if not st.session_state.turnos.empty
          else 1
      )
      nuevo_turno = pd.DataFrame({
          "ID": [nuevo_id],
          "Fecha": [str(fecha_turno)],
          "Hora": [str(hora_turno)],
          "Cliente": [cliente_t],
          "Vehículo": [vehiculo_t],
          "Trabajo a Realizar": [trabajo],
      })
      st.session_state.turnos = pd.concat(
          [st.session_state.turnos, nuevo_turno], ignore_index=True
      )
      st.success("¡Turno agendado con éxito!")

  st.markdown("### Próximos Turnos Registrados")
  if not st.session_state.turnos.empty:
    st.dataframe(st.session_state.turnos, use_container_width=True)

    id_del_t = st.number_input(
        "ID de Turno a eliminar por error", min_value=0, step=1, key="del_t"
    )
    if st.button("Eliminar Turno"):
      if id_del_t in st.session_state.turnos["ID"].values:
        st.session_state.turnos = st.session_state.turnos[
            st.session_state.turnos["ID"] != id_del_t
        ]
        st.success("Turno eliminado correctamente.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")
  else:
    st.info("No hay turnos agendados por el momento.")

# ----------------- DISTRIBUIDORES Y PROVEEDORES (COMPLETO) -----------------
elif menu == "🏭 Distribuidores y Proveedores":
  st.title("🏭 Gestión de Distribuidores y Proveedores")
  st.markdown("Directorio de proveedores, CUIT y repuestos habituales.")

  with st.form("form_distribuidor", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      nombre_emp = st.text_input("Nombre de la Empresa / Proveedor")
      cuit_emp = st.text_input("CUIT (ej. 30-12345678-9)")
      tel_dist = st.text_input("Teléfono de Contacto")
    with col2:
      dir_dist = st.text_input("Dirección")
      email_dist = st.text_input("Correo Electrónico (Email)")
      insumos = st.text_input("Insumos / Repuestos que provee")

    submit_dist = st.form_submit_button("Guardar Proveedor / Distribuidor")
    if submit_dist:
      if nombre_emp:
        nuevo_id_d = (
            int(st.session_state.distribuidores["ID"].max()) + 1
            if not st.session_state.distribuidores.empty
            else 1
        )
        nuevo_dist = pd.DataFrame({
            "ID": [nuevo_id_d],
            "Nombre Empresa": [nombre_emp],
            "CUIT": [cuit_emp],
            "Teléfono": [tel_dist],
            "Dirección": [dir_dist],
            "Email": [email_dist],
            "Insumos / Repuestos": [insumos],
        })
        st.session_state.distribuidores = pd.concat(
            [st.session_state.distribuidores, nuevo_dist], ignore_index=True
        )
        st.success("¡Proveedor registrado correctamente!")
      else:
        st.warning("El nombre de la empresa es obligatorio.")

  st.markdown("### Directorio Completo de Proveedores")
  if not st.session_state.distribuidores.empty:
    st.dataframe(st.session_state.distribuidores, use_container_width=True)

    id_del_d = st.number_input(
        "ID de Proveedor a eliminar por error", min_value=0, step=1, key="del_dist"
    )
    if st.button("Eliminar Proveedor"):
      if id_del_d in st.session_state.distribuidores["ID"].values:
        st.session_state.distribuidores = st.session_state.distribuidores[
            st.session_state.distribuidores["ID"] != id_del_d
        ]
        st.success("Proveedor eliminado correctamente.")
        st.rerun()
      else:
        st.warning("ID no encontrado.")
  else:
    st.info("No hay proveedores cargados todavía.")

# ----------------- CONFIGURACIÓN -----------------
elif menu == "⚙️ Configuración":
  st.title("⚙️ Configuración del Sistema")
  st.markdown("Personalización de parámetros y orden del menú.")

  st.subheader("🔀 Personalizar el Orden del Menú")
  st.write("Mueve las opciones asignándoles una posición numérica (1 al 14):")

  with st.form("form_orden_menu"):
    nuevo_orden = []
    for op in st.session_state.orden_menu:
      idx_actual = st.session_state.orden_menu.index(op) + 1
      pos = st.number_input(
          f"Posición para: {op}", min_value=1, max_value=14, value=idx_actual
      )
      nuevo_orden.append((pos, op))

    submit_orden = st.form_submit_button("Guardar Nuevo Orden del Menú")
    if submit_orden:
      nuevo_orden.sort(key=lambda x: x[0])
      st.session_state.orden_menu = [item[1] for item in nuevo_orden]
      st.success("¡Orden del menú actualizado con éxito!")
      st.rerun()

  st.markdown("---")
  st.subheader("📦 Categorías de Stock")
  st.write("Categorías actuales:", ", ".join(st.session_state.categorias_stock))

  with st.form("form_nueva_categoria"):
    nueva_cat = st.text_input("Nombre de la nueva categoría")
    submit_cat = st.form_submit_button("Añadir Categoría")
    if submit_cat:
      if nueva_cat and nueva_cat not in st.session_state.categorias_stock:
        st.session_state.categorias_stock.append(nueva_cat)
        st.success(f"¡Categoría '{nueva_cat}' agregada con éxito!")
      elif not nueva_cat:
        st.warning("Escribe un nombre válido.")
      else:
        st.info("Esa categoría ya existe.")