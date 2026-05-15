#!/usr/bin/env python3
"""
Extractor Simple SCJN - Sin Selenium
Usa requests + BeautifulSoup para máxima simplicidad
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import re

def extraer_tesis_scjn():
    """Extrae tesis de la semana del SCJN"""
    
    print("🔍 Extrayendo tesis del SCJN...")
    
    # URL base
    url_base = "https://sjfsemanal.scjn.gob.mx"
    url_busqueda = f"{url_base}/busqueda-principal-tesis"
    
    # Hacer request a la página principal
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url_busqueda, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer fecha de publicación
        fecha_elem = soup.find(string=re.compile(r'Actualizado al viernes'))
        fecha_publicacion = "Friday 08 de May de 2026"  # Valor por defecto
        
        if fecha_elem:
            fecha_match = re.search(r'viernes (\d+) de (\w+) de (\d+)', fecha_elem)
            if fecha_match:
                dia, mes, anio = fecha_match.groups()
                fecha_publicacion = f"Friday {dia} de {mes.title()} de {anio}"
        
        print(f"📅 Fecha: {fecha_publicacion}")
        
        # Buscar el enlace al listado completo (total "53")
        # El sitio tiene una tabla con los totales
        total_link = None
        for link in soup.find_all('a'):
            if link.get_text(strip=True) == '53':
                total_link = link.get('href')
                break
        
        if not total_link:
            print("⚠️ No se encontró el enlace al total. Usando URL directa...")
            total_link = "/listado-resultado-tesis"
        
        # Navegar al listado completo
        url_listado = f"{url_base}{total_link}"
        print(f"🔗 Navegando a: {url_listado}")
        
        response2 = requests.get(url_listado, headers=headers, timeout=30)
        response2.raise_for_status()
        
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        
        # Extraer todas las tesis
        tesis_extraidas = []
        
        # Buscar todos los enlaces a detalle de tesis
        enlaces_tesis = soup2.find_all('a', href=re.compile(r'/detalle/tesis/\d+'))
        
        registros_procesados = set()
        
        for enlace in enlaces_tesis:
            href = enlace.get('href')
            if not href:
                continue
            
            # Extraer registro ID
            registro_match = re.search(r'/detalle/tesis/(\d+)', href)
            if not registro_match:
                continue
            
            registro_id = registro_match.group(1)
            
            # Evitar duplicados
            if registro_id in registros_procesados:
                continue
            
            registros_procesados.add(registro_id)
            
            # Buscar el rubro (texto del enlace o elemento padre)
            rubro = enlace.get_text(strip=True)
            
            # Si el texto es muy corto, buscar en el elemento padre
            if not rubro or len(rubro) < 20:
                parent = enlace.find_parent('li')
                if parent:
                    # Buscar todos los enlaces en el li
                    for link in parent.find_all('a'):
                        texto = link.get_text(strip=True)
                        if texto and not texto.startswith('Registro digital:') and len(texto) > 20:
                            rubro = texto[:200]
                            break
            
            if not rubro or len(rubro) < 10:
                rubro = f"Tesis {registro_id}"
            
            tesis_extraidas.append({
                'registroId': registro_id,
                'registro': registro_id,
                'rubro': rubro[:200],
                'url': f"{url_base}{href}"
            })
        
        print(f"✅ Extraídas {len(tesis_extraidas)} tesis")
        
        # Filtrar tesis prioritarias (CONAGUA, AMPARO, LFPCA, etc.)
        palabras_clave = ['CONAGUA', 'AMPARO', 'LFPCA', 'NULIDAD', 'CONTENCIOSO', 'ADMINISTRATIV']
        
        tesis_prioritarias = [
            t for t in tesis_extraidas
            if any(palabra.lower() in t['rubro'].lower() for palabra in palabras_clave)
        ]
        
        tesis_referencia = [t for t in tesis_extraidas if t not in tesis_prioritarias]
        
        print(f"🎯 Prioritarias: {len(tesis_prioritarias)}")
        print(f"📚 Referencia: {len(tesis_referencia)}")
        
        # Crear resultado
        resultado = {
            "metadata": {
                "fecha_publicacion": fecha_publicacion,
                "fecha_extraccion": datetime.now().isoformat(),
                "total_tesis": len(tesis_extraidas),
                "tesis_prioritarias": len(tesis_prioritarias),
                "tesis_referencia": len(tesis_referencia),
                "criterio_priorizacion": "CONAGUA, AMPARO, LFPCA, NULIDAD, CONTENCIOSO, ADMINISTRATIV",
                "fuente": url_base
            },
            "tesisPrioritarias": tesis_prioritarias,
            "tesisReferencia": tesis_referencia
        }
        
        # Guardar en archivo
        os.makedirs('datos', exist_ok=True)
        
        fecha_archivo = datetime.now().strftime('%Y%m%d')
        nombre_archivo = f"datos/tesis_scjn_{fecha_archivo}.json"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Guardado en: {nombre_archivo}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    resultado = extraer_tesis_scjn()
    print("\n" + "="*60)
    print("✅ EXTRACCIÓN COMPLETADA")
    print("="*60)
