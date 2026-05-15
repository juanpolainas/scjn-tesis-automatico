# ⚡ GUÍA RÁPIDA - 5 PASOS

## 📋 LO QUE NECESITAS

- Cuenta de GitHub (gratis)
- Cuenta de Gmail (para recibir notificaciones)

---

## 🚀 PASO 1: CREAR REPOSITORIO

1. Ir a: https://github.com/new
2. Nombre: `scjn-tesis-automatico`
3. Marcar "Public" y "Add README"
4. Click **"Create repository"**

---

## 📁 PASO 2: SUBIR ARCHIVOS

1. Descargar el ZIP que te compartí
2. Extraer archivos
3. En GitHub, click **"Add file"** → **"Upload files"**
4. Arrastra:
   - `extractor_simple.py`
   - Carpeta `.github` completa
5. Click **"Commit changes"**

---

## 🔐 PASO 3: CONFIGURAR EMAIL

### 3.1 Obtener contraseña de aplicación Gmail:

1. Ir a: https://myaccount.google.com/apppasswords
2. Nombre: "SCJN Automatico"
3. Copiar contraseña de 16 caracteres (ej: `abcd efgh ijkl mnop`)

### 3.2 Agregar Secrets en GitHub:

1. En tu repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** 3 veces:

**Secret 1:**
```
Name: EMAIL_USERNAME
Value: tu_email@gmail.com
```

**Secret 2:**
```
Name: EMAIL_PASSWORD
Value: abcd efgh ijkl mnop  (la de 16 caracteres)
```

**Secret 3:**
```
Name: EMAIL_DESTINATARIO
Value: donde_recibes_notificaciones@gmail.com
```

---

## ⚙️ PASO 4: HABILITAR PERMISOS

1. **Settings** → **Actions** → **General**
2. En "Workflow permissions":
   - Seleccionar: ☑ **"Read and write permissions"**
3. Click **"Save"**

---

## ✅ PASO 5: PROBAR

1. Ir a **Actions**
2. Click **"Extracción Semanal SCJN"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Esperar 2-3 minutos
5. Debes recibir email ✉️
6. En `datos/` aparece archivo JSON 📄

---

## 🎯 ¡LISTO!

Ahora se ejecutará automáticamente cada **viernes a las 11:00 AM**.

### ¿Dónde ver los resultados?

- **Carpeta datos/:** `tesis_scjn_YYYYMMDD.json`
- **Email:** Recibirás notificación semanal
- **Actions:** Historial de ejecuciones

---

## ❓ ¿PROBLEMAS?

### No recibo emails:
- Verifica los 3 Secrets
- Revisa carpeta SPAM
- Verifica contraseña de aplicación Gmail

### No se guardan archivos:
- Verifica "Read and write permissions" (Paso 4)

### Workflow falla:
- Ve a **Actions** → Click en ejecución roja
- Lee el error en los logs

---

**Tiempo total:** ~10 minutos  
**Costo:** $0.00  
**Mantenimiento:** Ninguno  
