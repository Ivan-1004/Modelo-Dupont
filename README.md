# 💸 Modelo de Flujo de Efectivo Libre (FEL) – Streamlit App

Este proyecto implementa un modelo automatizado para calcular el **Flujo de Efectivo Libre (FEL)** a partir de una base de datos en Excel, utilizando **Python** y **Streamlit**.

## 📊 Objetivo

El modelo permite cargar un archivo Excel con información financiera histórica y calcula automáticamente los siguientes indicadores:

- **EBITDA**
- **Variación de cuentas por cobrar (Δ CxC)**
- **Variación de inventarios (Δ Inventarios)**
- **Variación de proveedores (Δ Proveedores)**
- **Variación de capital de trabajo (CT)**
- **FEL (antes de CapEx e impuestos)**

Todos los resultados se presentan en una tabla con:
- **Renglones = indicadores**
- **Columnas = años**
- **Valores absolutos con un decimal**

---

## 📁 Estructura del Proyecto

```
modelo-fel/
├── app.py               # Código principal de la app en Streamlit
├── README.md            # Este archivo
```

---

## 🚀 Cómo ejecutar localmente

### 1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/modelo-fel.git
cd modelo-fel
```

### 2. Crea un entorno virtual y actívalo:

```bash
python -m venv venv
source venv/bin/activate        # En Linux/macOS
venv\Scripts\activate           # En Windows
```

### 3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes un archivo `requirements.txt`, instala manualmente:

```bash
pip install streamlit pandas openpyxl
```

### 4. Ejecuta la aplicación:

```bash
streamlit run app.py
```

---

## 🌐 Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub.
2. Ve a: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecta tu cuenta de GitHub.
4. Selecciona el repositorio y el archivo `app.py`.
5. Haz clic en “Deploy”.

¡Listo! Tu modelo FEL estará disponible como una app web.

---

## 📷 Ejemplo de formato de entrada

El archivo Excel debe tener esta estructura:

| Indicador         | 1992 | 1993 | 1994 | ... |
|-------------------|------|------|------|-----|
| EBIT              | ...  | ...  | ...  |     |
| Depreciación      | ...  | ...  | ...  |     |
| Cuentas por cobrar| ...  | ...  | ...  |     |
| Inventarios       | ...  | ...  | ...  |     |
| Proveedores       | ...  | ...  | ...  |     |

> El campo **"Indicador"** debe estar en la primera columna y los años en la primera fila.

---

## 📩 Contacto

Desarrollado por [Tu Nombre o Equipo].  
Contacto: [tuemail@dominio.com]
