# 🤖 EXTRACTOR AUTOMÁTICO SCJN - GitHub Actions

**Sistema 100% automatizado, gratis y en la nube para extraer tesis semanales del SCJN.**

## ✅ CARACTERÍSTICAS

- ✅ **100% Gratis** - GitHub Actions (2000 minutos/mes gratuitos)
- ✅ **Totalmente Automático** - Se ejecuta cada viernes a las 11:00 AM
- ✅ **Sin instalación local** - Todo corre en la nube
- ✅ **Repositorio externo** - Tus datos en GitHub
- ✅ **Notificaciones por email** - Recibes aviso cuando se extraen tesis
- ✅ **Sin Selenium** - Más rápido y confiable

## 🚀 INSTALACIÓN (5 PASOS - 10 MINUTOS)

### PASO 1: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `scjn-tesis-automatico`
3. Descripción: `Extractor automático de tesis SCJN`
4. Marca como **Público** (o Privado si prefieres)
5. ✅ Marca "Add a README file"
6. Click **"Create repository"**

### PASO 2: Subir archivos al repositorio

**Opción A - Usando la interfaz web (más fácil):**

1. En tu repositorio, click **"Add file"** → **"Upload files"**
2. Arrastra estos archivos:
   - `extractor_simple.py`
   - `.github/workflows/extraer_tesis.yml`
3. Escribe mensaje: `Initial commit - Sistema automatizado`
4. Click **"Commit changes"**

**Opción B - Usando Git (si lo conoces):**

```bash
git clone https://github.com/TU_USUARIO/scjn-tesis-automatico.git
cd scjn-tesis-automatico
mkdir -p .github/workflows datos

# Copiar archivos aquí
# extractor_simple.py → raíz
# extraer_tesis.yml → .github/workflows/

git add .
git commit -m "Sistema automatizado SCJN"
git push
```

### PASO 3: Configurar Secrets (Email)

Para recibir notificaciones por email:

1. En tu repositorio, ve a **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Crea 3 secrets:

**Secret 1:**
- Name: `EMAIL_USERNAME`
- Value: `tu_email@gmail.com`

**Secret 2:**
- Name: `EMAIL_PASSWORD`
- Value: `tu_contraseña_de_aplicación` (ver abajo cómo obtenerla)
- 
**Secret 3:**
- Name: `EMAIL_DESTINATARIO`
- Value: `email_donde_recibes@gmail.com`

### PASO 4: Obtener contraseña de aplicación Gmail

1. Ve a https://myaccount.google.com/security
2. Busca **"Contraseñas de aplicaciones"** (o "App passwords")
3. Genera una nueva contraseña para "Mail"
4. Copia la contraseña de 16 caracteres
5. Úsala como `EMAIL_PASSWORD` en el Secret

### PASO 5: Habilitar GitHub Actions

1. En tu repositorio, ve a la pestaña **Actions**
2. Si ves un botón verde **"I understand my workflows, go ahead and enable them"**, haz clic
3. Ya está listo ✅

## 🎯 PROBARLO AHORA (Ejecución manual)

No esperes al viernes, pruébalo ahora:

1. Ve a **Actions** → **"Extracción Semanal SCJN"**
2. Click **"Run workflow"** → **"Run workflow"**
3. Espera 2-3 minutos
4. Revisa:
   - ✅ El workflow debe mostrar ✓ verde
   - ✅ Debes recibir un email
   - ✅ Debe aparecer un archivo en `datos/tesis_scjn_YYYYMMDD.json`

## 📊 VERIFICAR RESULTADOS

### Ver archivos extraídos:

1. En tu repositorio, abre la carpeta `datos/`
2. Verás archivos como: `tesis_scjn_20260514.json`
3. Click para ver el contenido

### Ver historial de ejecuciones:

1. Pestaña **Actions**
2. Click en cualquier ejecución para ver los logs

## ⏰ PROGRAMACIÓN AUTOMÁTICA

El sistema se ejecuta automáticamente:
- **Cada viernes a las 11:00 AM** (hora México)
- **Sin hacer nada** - Solo revisa tu email o el repositorio

## 🔧 PERSONALIZACIÓN

### Cambiar hora de ejecución:

Edita `.github/workflows/extraer_tesis.yml`:

```yaml
schedule:
  # Cambiar horario aquí (formato UTC)
  - cron: '0 17 * * 5'  # Viernes 11:00 AM México
```

### Cambiar palabras clave prioritarias:

Edita `extractor_simple.py` línea 122:

```python
palabras_clave = ['CONAGUA', 'AMPARO', 'LFPCA', 'NULIDAD', 'CONTENCIOSO', 'ADMINISTRATIV']
```

## ❓ SOLUCIÓN DE PROBLEMAS

### ❌ El workflow falla

1. Ve a **Actions** → Click en la ejecución fallida
2. Revisa el error en los logs
3. Usualmente es un problema de Secrets mal configurados

### ❌ No recibo emails

1. Verifica que los 3 Secrets estén configurados correctamente
2. Verifica que la contraseña de aplicación Gmail sea válida
3. Revisa tu carpeta de SPAM

### ❌ No se guardan archivos

1. Verifica que el repositorio tenga permisos de escritura
2. Ve a **Settings** → **Actions** → **General**
3. En "Workflow permissions", selecciona **"Read and write permissions"**

## 📈 COSTOS

- **GitHub Actions:** GRATIS (2000 minutos/mes)
- **Este workflow usa:** ~2 minutos/semana
- **Total al mes:** ~8 minutos de 2000 disponibles
- **Costo real:** $0.00

## 🎓 SIGUIENTES PASOS

Una vez funcionando:

1. ✅ Revisa los datos cada semana
2. ✅ Puedes descargar los JSONs para análisis
3. ✅ Puedes crear dashboards con los datos
4. ✅ Puedes integrar con Google Sheets, etc.

---

**¿Problemas?** Abre un Issue en este repositorio.
