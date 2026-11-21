# 💰 Control de Gastos (Flask + SQLite)

Aplicación web para registrar gastos personales (fecha, descripción y monto) y generar reportes. Protegida con login.

**Stack:** Python · Flask · SQLite

## Credenciales de acceso
- **Usuario:** `admin`
- **Clave:** `123`

## Instalación y ejecución
```bash
git clone https://github.com/mariahuacho15-netizen/practica.calificada.git
cd practica.calificada
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Abrir http://127.0.0.1:5000

## Funcionamiento

### 1. Inicio de sesión
Al entrar se pide usuario y clave. Sin sesión activa, cualquier ruta redirige al login.

![Login](screenshots/01-login.png)

### 2. Registro de gastos
Se completa **fecha**, **descripción** y **monto**, y se pulsa *Guardar*. Debajo aparece la lista de gastos (del más reciente al más antiguo) con opción de eliminar.

![Gastos](screenshots/02-gastos.png)

### 3. Reporte
Muestra total, cantidad de gastos, promedio, total por mes y el detalle. Permite filtrar por rango de fechas e imprimir.

![Reporte](screenshots/03-reporte.png)

## Estructura
```
app.py            # rutas, login y base de datos
templates/        # login, gastos, reporte
static/style.css
gastos.db         # se crea automáticamente
```

> ⚠️ Proyecto de demostración: las credenciales están fijas en el código. No usar así en producción.
