import os
import re

# Configuración
BASE_DIR = r"c:\Users\25166122M\github\presentationsAI2026\LLM\bloques"
OUTPUT_FILE = os.path.join(BASE_DIR, "Curso_Completo_IA_Salud.qmd")

# Archivos a fusionar en orden (según _quarto.yml)
FILES_TO_MERGE = [
    "LLM_Fundamentals_Architecture_Medicine.qmd",
    "Advanced_Prompt_Engineering_Transformer_Architectures.qmd",
    "Advanced_Clinical_AI_Systems_RAG_FineTuning.qmd",
    "Critical_Infrastructure_LLM_Deployment_Health.qmd",
    "Ethics_Bias_Security_Generative_AI_Health.qmd"
]

# Títulos de Módulos
MODULE_TITLES = [
    "Módulo 1: Fundamentos y Arquitectura",
    "Módulo 2: Ingeniería de Prompts Avanzada",
    "Módulo 3: Sistemas Clínicos Avanzados (RAG/Fine-Tuning)",
    "Módulo 4: Infraestructura Crítica y Despliegue",
    "Módulo 5: Ética, Sesgos y Seguridad"
]

BG_COLORS = ["#0f172a", "#1e1e2e", "#0f172a", "#111827", "#1f2937"]

YAML_HEADER = """---
title: "Inteligencia Artificial Generativa en Medicina"
subtitle: "Curso Completo: De la Teoría a la Práctica Clínica"
author: "Antonio Otal"
format:
  revealjs:
    embed-resources: true
    theme: [default, Curso_Completo_IA_Salud.scss]
    width: 1600
    height: 900
    margin: 0.05
    min-scale: 0.2
    max-scale: 2.0
    transition: slide
    background-transition: fade
    controls: true
    progress: true
    center: false
    slide-number: c/t
    show-slide-number: all
    menu: true
    chalkboard: false
    overview: true
    code-line-numbers: true
    citations-hover: true
    link-external-newwindow: true
bibliography: references.bib
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
lang: es
---

"""

def clean_qmd_content(content):
    # Eliminar YAML header (--- ... ---)
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Eliminar sección de Bibliografía final.
    # Estrategia más segura: Buscar solo headers específicos al final del archivo o que sean claramente la sección de referencias.
    # Buscamos "## Bibliografía" o "# Bibliografía" seguido opcionalmente de atributos, y luego :: {#refs} ...
    
    # Regex explicada:
    # ^#+\s+ -> Inicio de línea con 1 o más # y espacios
    # (Bibliografía|Referencias|Bibliography|References) -> Palabras clave
    # .* -> Resto de la línea (incluyendo {.scrollable} etc)
    # \n -> Salto de línea
    # (?:.|\n)* -> Todo lo que sigue (greedy)
    # $ -> Fin del string
    
    # Usamos MULTILINE para que ^ coincida con inicio de línea
    regex_bib = r'^#+\s+(Bibliografía|Referencias|Bibliography|References).*?(\n:::\s+\{#refs\}.*?:::)?$'
    
    # Intentamos truncar desde el encabezado de bibliografía hacia abajo
    # split divide el string. Tomamos la primera parte.
    # Dividimos por líneas para iterar y cortar de forma segura
    lines = content.split('\n')
    cleaned_lines = []
    found_bib = False
    
    for line in lines:
        # Detectar header de bibliografía
        if re.match(r'^#+\s+(Bibliografía|Evaluación|Referencias|Bibliography|References)', line, re.IGNORECASE):
            # Verificar si parece ser la sección final (heurística: suele estar cerca del final, o ser explícita)
            # Para estar seguros, asumimos que si dice "Bibliografía" es la sección final que queremos borrar.
            # EXCEPCIÓN: "Referencias Clave" o similar dentro de un texto. 
            # Verificamos si es solo la palabra clave o tiene atributos de clase
            clean_line = re.sub(r'\{.*?\}', '', line).strip() # Quitar atributos pandoc
            clean_line = re.sub(r'#+\s+', '', clean_line).strip()
            
            if clean_line.lower() in ['bibliografía', 'referencias', 'bibliography', 'references']:
                found_bib = True
                break # Dejamos de añadir líneas
        
        # También detectar el bloque div de refs directamente si no hay header
        if line.strip() == '::: {#refs}':
            found_bib = True
            break
            
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()

def main():
    print(f"Generando {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(YAML_HEADER)
        
        for i, filename in enumerate(FILES_TO_MERGE):
            filepath = os.path.join(BASE_DIR, filename)
            module_title = MODULE_TITLES[i] if i < len(MODULE_TITLES) else f"Módulo {i+1}"
            bg_color = BG_COLORS[i % len(BG_COLORS)]
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        
                        cleaned_content = clean_qmd_content(content)
                        
                        outfile.write(f"\n# {module_title} {{background-color=\"{bg_color}\"}}\n\n")
                        outfile.write(cleaned_content)
                        outfile.write("\n\n")
                        
                        print(f" [OK] Merged: {filename}")
                except Exception as e:
                    print(f" [ERROR] Fallo al procesar {filename}: {e}")
            else:
                print(f" [WARNING] Archivo no encontrado: {filename}")
        
        outfile.write("\n# Bibliografía Global\n\n::: {#refs}\n:::\n")
    print("Fusión completada.")

if __name__ == "__main__":
    main()
