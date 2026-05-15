#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de Tesis SCJN - Versión con Selenium
Extrae tesis del Semanario Judicial de la Federación
"""

import json
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuración
URL_BUSQUEDA = "https://sjfsemanal.scjn.gob.mx/busqueda-principal-tesis"
PALABRAS_CLAVE = ["CONAGUA", "AMPARO", "LFPCA", "NULIDAD", "CONTENCIOSO", "ADMINISTRATIV"]

def configurar_driver():
    """Configura el driver de Chrome headless"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=options)
    return driver

def extraer_tesis_selenium():
    """Extrae tesis usando Selenium"""
    driver = None
    try:
        print("Iniciando Chrome headless...")
        driver = configurar_driver()
        
        print("Navegando al sitio SCJN...")
        driver.get(URL_BUSQUEDA)
        time.sleep(3)
        
        # Obtener fecha de publicación
        try:
            elemento_fecha = driver.find_element(By.XPATH, "//*[contains(text(), 'Actualizado al')]")
            fecha_pub = elemento_fecha.text.strip()
        except:
            fecha_pub = f"Friday {datetime.now().strftime('%d de %B de %Y')}"
        
        print(f"Fecha de publicación: {fecha_pub}")
        
        # Hacer clic en el botón Buscar (búsqueda vacía = todas las tesis)
        print("Haciendo búsqueda...")
        try:
            boton_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Buscar')]"))
            )
            boton_buscar.click()
            time.sleep(4)
        except Exception as e:
            print(f"Error al hacer clic en Buscar: {e}")
            return None, None, None
        
        # Esperar a que carguen los resultados
        print("Esperando resultados...")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "li"))
            )
        except:
            print("No se encontraron resultados")
            return fecha_pub, [], []
        
        # Extraer todas las tesis
        todas_tesis = []
        pagina = 1
        
        while True:
            print(f"Extrayendo página {pagina}...")
            
            # Obtener todos los elementos <li>
            items = driver.find_elements(By.TAG_NAME, "li")
            
            tesis_pagina = 0
            for item in items:
                try:
                    texto = item.text
                    
                    if 'Registro digital:' in texto:
                        # Extraer registro
                        match = re.search(r'Registro digital:\s*(\d+)', texto)
                        if not match:
                            continue
                        
                        registro = match.group(1)
                        
                        # Extraer líneas
                        lineas = [l.strip() for l in texto.split('\n') if l.strip()]
                        
                        # Buscar rubro (línea larga que no sea metadata)
                        rubro = ""
                        for linea in lineas:
                            if len(linea) > 30 and 'Registro digital' not in linea and 'SCJN' not in linea:
                                rubro = linea
                                break
                        
                        todas_tesis.append({
                            'registro_digital': registro,
                            'rubro': rubro[:300],
                            'texto_completo': texto[:500]
                        })
                        tesis_pagina += 1
                        
                except Exception as e:
                    continue
            
            print(f"Página {pagina}: {tesis_pagina} tesis extraídas")
            
            # Verificar si hay página siguiente
            try:
                boton_siguiente = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page' or contains(@class, 'next')]")
                if boton_siguiente.is_enabled():
                    boton_siguiente.click()
                    time.sleep(3)
                    pagina += 1
                else:
                    break
            except:
                # No hay más páginas
                break
        
        print(f"\nTotal extraído: {len(todas_tesis)} tesis")
        
        # Filtrar por palabras clave
        prioritarias = []
        referencia = []
        
        for t in todas_tesis:
            texto_busqueda = f"{t.get('rubro', '')} {t.get('texto_completo', '')}".upper()
            tiene_clave = any(palabra in texto_busqueda for palabra in PALABRAS_CLAVE)
            
            if tiene_clave:
                prioritarias.append(t)
            else:
                referencia.append(t)
        
        return fecha_pub, prioritarias, referencia
        
    except Exception as e:
        print(f"Error: {e}")
        return None, [], []
    
    finally:
        if driver:
            driver.quit()

def main():
    """Función principal"""
    print("=" * 60)
    print("EXTRACTOR DE TESIS SCJN")
    print("=" * 60 + "\n")
    
    fecha_pub, prioritarias, referencia = extraer_tesis_selenium()
    
    if fecha_pub is None:
        fecha_pub = f"Friday {datetime.now().strftime('%d de %B de %Y')}"
    
    total = len(prioritarias) + len(referencia)
    
    print(f"\n📊 Resumen:")
    print(f"   - Total: {total} tesis")
    print(f"   - Prioritarias: {len(prioritarias)} tesis")
    print(f"   - Referencia: {len(referencia)} tesis")
    
    # Crear JSON
    resultado = {
        "metadata": {
            "fecha_publicacion": fecha_pub,
            "fecha_extraccion": datetime.now().isoformat(),
            "total_tesis": total,
            "tesis_prioritarias": len(prioritarias),
            "tesis_referencia": len(referencia),
            "criterio_priorizacion": ", ".join(PALABRAS_CLAVE),
            "fuente": "https://sjfsemanal.scjn.gob.mx"
        },
        "tesisPrioritarias": prioritarias,
        "tesisReferencia": referencia
    }
    
    # Guardar
    nombre_archivo = f"datos/tesis_scjn_{datetime.now().strftime('%Y%m%d')}.json"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Archivo guardado: {nombre_archivo}\n")
    print("=" * 60)

if __name__ == "__main__":
    main()
