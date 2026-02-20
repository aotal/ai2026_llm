# **Manual de Ingeniería y Arquitectura para la Generación de Presentaciones Quarto Reveal.js de Alta Fidelidad: Compendio de Conocimiento para Modelos de Lenguaje**

## **1\. Fundamentos Arquitectónicos y Filosofía del Sistema**

La generación de presentaciones técnicas mediante Quarto y Reveal.js representa un cambio de paradigma fundamental en la comunicación científica y corporativa: la transición de la edición visual directa (WYSIWYG) a la "Presentación como Código" (Presentation as Code). Para un Modelo de Lenguaje Grande (LLM) que aspira a la maestría en este dominio, no basta con entender la sintaxis Markdown superficial; es imperativo comprender la arquitectura de compilación subyacente que transforma el texto plano en experiencias web interactivas y dinámicas. Este manual establece la "Verdad Terrestre" (Ground Truth) técnica necesaria para generar código Quarto robusto, semánticamente correcto y visualmente sofisticado, mitigando las alucinaciones comunes y optimizando la utilidad práctica de las respuestas generadas.

### **1.1. La Canalización de Compilación: De Markdown a DOM**

El proceso de creación de una presentación Reveal.js en Quarto no es una conversión directa. Es una orquestación compleja de múltiples motores de ejecución y filtros de transformación. Un LLM experto debe visualizar este flujo para diagnosticar errores y predecir el comportamiento del código generado.

1. **Ingestión y Ejecución (Computational Engine):** El archivo fuente .qmd es procesado inicialmente por Knitr (para R) o Jupyter (para Python/Julia). En esta etapa, el código ejecutable se evalúa. El LLM debe entender que las opciones de ejecución (eval, echo, output) determinan qué contenido pasa a la siguiente fase. El resultado es un archivo Markdown intermedio (.md) que contiene el texto original más los resultados de la computación (imágenes, tablas, texto) incrustados como Markdown estándar o HTML crudo.1  
2. **Transformación del Árbol de Sintaxis Abstracta (AST):** Pandoc analiza el archivo .md y construye un AST. Aquí es donde Quarto inyecta su lógica específica mediante filtros Lua. Estructuras como ::: {.columns} o ::: {.callout} no son HTML nativo ni Markdown estándar; son directivas que los filtros Lua interceptan y transforman en las estructuras HTML complejas que Reveal.js requiere (por ejemplo, divs anidados con clases reveal, slides, stack, etc.). Una alucinación común en LLMs es intentar escribir HTML manual (\<div class="column"\>) en lugar de usar la sintaxis de "Divs" de Pandoc, lo que a menudo rompe el diseño responsivo de Reveal.js.3  
3. **Inyección de Recursos y Renderizado:** Finalmente, se aplica la plantilla de Reveal.js. Se inyectan las hojas de estilo CSS (compiladas desde SASS), las bibliotecas JavaScript (incluyendo plugins como Chalkboard o Menu) y se genera el archivo HTML final. Este archivo es una aplicación web completa, no un documento estático.

### **1.2. Anatomía Semántica de la Diapositiva**

La unidad atómica de una presentación Reveal.js es la etiqueta \<section\>. Sin embargo, en Quarto, la delimitación de estas secciones se infiere heurísticamente a partir de la jerarquía de encabezados Markdown.

* **Encabezados de Nivel 1 (\#):** Definen secciones principales o "pilas" verticales de diapositivas si el modo de navegación es vertical. En el modo predeterminado linear, actúan como diapositivas de título de sección. El LLM debe usar estos encabezados estratégicamente para estructurar la narrativa macro de la presentación.5  
* **Encabezados de Nivel 2 (\#\#):** Constituyen la diapositiva estándar. El contenido bajo este encabezado se encapsula en una \<section\>.  
* **Delimitadores Horizontales (---):** Actúan como separadores forzados de diapositivas. Son cruciales cuando se necesita una diapositiva sin título visible (por ejemplo, para una imagen a pantalla completa o una cita impactante). El uso incorrecto de estos delimitadores dentro de estructuras anidadas es una fuente frecuente de errores de renderizado.5

## ---

**2\. Configuración Maestra del Entorno: El Encabezado YAML**

El control preciso sobre el comportamiento y la apariencia de la presentación reside en el encabezado YAML. Un LLM experto debe ser capaz de configurar estas opciones no solo con valores predeterminados, sino adaptándolos a escenarios específicos (conferencias, dispositivos móviles, quioscos interactivos).

### **2.1. Metadatos y Atribución Académica**

La gestión de metadatos en Quarto ha evolucionado para soportar estructuras complejas, vitales para presentaciones académicas y corporativas.

| Campo | Descripción Técnica y Uso Experto |
| :---- | :---- |
| title | Título principal. Renderizado en la diapositiva de título y en el metadato \<title\> del HTML. |
| subtitle | Subtítulo. Renderizado con menor jerarquía visual bajo el título. |
| author | Soporta listas de objetos complejos. Permite especificar name, orcid, email y affiliations. El LLM debe preferir esta estructura anidada sobre cadenas de texto simples para garantizar un formato correcto en plantillas avanzadas.1 |
| date | Fecha de la presentación. Puede usar formatos automáticos o cadenas específicas. |
| date-format | Controla la visualización de la fecha (ej. long, short, iso). |
| institute | (Deprecado en favor de affiliations) Institución del autor. |

**Ejemplo de Configuración Robusta:**

YAML

title: "Arquitectura de Microservicios en Kubernetes"  
subtitle: "Patrones de Diseño y Estrategias de Despliegue"  
date: last-modified  
date-format: "D MMMM, YYYY"  
author:  
  \- name: "Ing. Sofía Valerom"  
    orcid: "0000-0002-1825-0097"  
    email: "svalerom@tech-corp.com"  
    affiliations:  
      \- name: "Tech Corp Labs"  
        city: "Barcelona"

### **2.2. Geometría del Lienzo y Escalado**

Reveal.js opera sobre un sistema de coordenadas escalable. Definir la geometría correcta es crítico para evitar problemas de visualización en diferentes proyectores y pantallas.

* **width y height:** Definen la resolución base de autoría. El valor predeterminado es 1050x700 (aprox. 3:2). Sin embargo, para entornos modernos, el estándar de facto es 1080p (1920x1080). Un LLM debe recomendar width: 1920 y height: 1080 para presentaciones de "alta calidad" destinadas a monitores modernos, asegurando que las imágenes rasterizadas no se pixelen al escalar.6  
* **margin:** Controla el espacio vacío alrededor del contenido. El defecto es 0.1. Para presentaciones ricas en datos o diagramas grandes, reducirlo a 0.05 maximiza el "real estate" disponible.  
* **min-scale y max-scale:** Limitan cuánto puede crecer o encogerse la presentación para ajustarse a la ventana del navegador. Ajustar max-scale a un valor alto (ej. 2.0) es útil para asegurar legibilidad en pantallas gigantes.6

### **2.3. Configuración de Navegación y UX**

La experiencia del usuario (tanto del presentador como de la audiencia) se configura mediante un conjunto detallado de banderas booleanas y opciones de cadena.

| Opción | Función y Recomendación de Uso | Referencia |
| :---- | :---- | :---- |
| controls | true/false. Muestra flechas de navegación en pantalla. Recomendado true para distribución web asíncrona. | 7 |
| progress | true. Barra de progreso inferior. Útil para que la audiencia estime la duración restante. | 7 |
| history | true. Actualiza la URL del navegador con cada cambio de diapositiva. **Crítico** para compartir enlaces a diapositivas específicas. | 7 |
| hash | true. Similar a history, usa fragmentos de URL (\#/1/2). Esencial para la navegación profunda. | 7 |
| touch | true. Habilita gestos de deslizamiento en móviles/tablets. | 7 |
| center | true/false. Centra verticalmente el contenido. **Experto:** Configurar en false para presentaciones técnicas densas, permitiendo el uso completo del espacio vertical desde el borde superior. | 6 |
| navigation-mode | linear, vertical, grid. linear es estándar. vertical permite organizar temas en pilas (H1 horizontal, H2 vertical). | 7 |

**Implementación de Navegación Vertical:** El modo vertical es una característica distintiva de Reveal.js que permite una estructura bidimensional. Un LLM debe saber cuándo recomendarla: es ideal para cursos o talleres donde los temas principales (H1) fluyen horizontalmente, y los detalles o ejercicios (H2) se profundizan verticalmente, permitiendo al presentador saltar detalles si el tiempo apremia.7

## ---

**3\. Ingeniería de Contenido: Estructuras de Diseño Avanzadas**

La capacidad de un LLM para generar diapositivas estéticamente agradables y funcionalmente robustas depende de su dominio de las estructuras de diseño de Quarto. El texto plano secuencial es insuficiente para presentaciones de alto nivel.

### **3.1. Sistemas de Diseño Multicolumna**

El diseño en columnas es esencial para comparaciones (ej. código vs. salida, antes vs. después). Quarto abstrae la complejidad de CSS Flexbox mediante una sintaxis de Divs específica.

**Patrón de Código Robusto:**

::: {.columns}

::: {.column width="45%"}

### **Concepto Teórico**

El modelo **Transformer** utiliza mecanismos de atención para ponderar la influencia de diferentes partes de la entrada de datos.

* Paralelizable  
* Captura dependencias largas  
  :::

::: {.column width="5%"}

:::

::: {.column width="50%"}

\!(diagrama.png)

:::

:::

**Insights Técnicos:**

* La suma de los anchos debe ser manejada con cuidado. Debido al modelo de caja de CSS y posibles márgenes internos, es seguro apuntar a una suma del 95-98% en lugar del 100% exacto para evitar el desbordamiento de línea, lo que rompería el diseño lado a lado.8  
* La alineación vertical predeterminada es superior (top). Para centrar verticalmente el contenido de las columnas, se puede requerir CSS personalizado o clases utilitarias auxiliares, ya que Reveal.js no expone una opción directa para esto en la sintaxis de columnas de Quarto.4

### **3.2. Posicionamiento Absoluto y Capas**

Para diseños tipo "póster" o superposición de elementos, Quarto ofrece la clase .absolute. Esto permite colocar elementos (imágenes, cajas de texto) en coordenadas precisas, rompiendo el flujo normal del documento.

**Sintaxis:**

\!(imagen.png){.absolute top=50 right=10 width=300}

**Reglas de Uso Experto:**

* Las coordenadas son relativas a la resolución definida en el YAML (width/height). Si se definió una altura de 1080px, bottom=0 coloca el elemento en el píxel 1080\. Esto garantiza que el diseño se mantenga proporcional al escalar la presentación en diferentes pantallas.6  
* **Superposición (Z-Index):** El orden de apilamiento sigue el orden de aparición en el DOM (código Markdown). Los elementos definidos más tarde aparecen encima.  
* **Stacks:** La clase .r-stack permite centrar múltiples elementos uno encima del otro. Combinado con fragmentos, permite crear efectos de "reemplazo" en el mismo lugar físico de la diapositiva.6

### **3.3. Gestión de Desbordamiento y Escalado de Texto**

Uno de los errores más comunes en presentaciones generadas automáticamente es el texto que excede los límites de la diapositiva.

* **Clase .r-fit-text:** Esta utilidad de Reveal.js escala agresivamente el texto para que ocupe el ancho máximo disponible sin desbordarse. Es ideal para títulos de impacto o números grandes ("big stats").6  
* **Diapositivas Desplazables (.scrollable):** Cuando el contenido es inevitablemente largo (ej. una bibliografía o una tabla de datos extensa), se puede aplicar la clase .scrollable al encabezado de la diapositiva (\#\# Título {.scrollable}).  
  * **Advertencia de Interacción:** El uso de .scrollable deshabilita ciertas características de auto-ajuste de Reveal.js (como r-stretch). Un LLM debe advertir sobre esto: no se deben mezclar diseños de ajuste automático con desplazamiento en la misma diapositiva.1

## ---

**4\. Dinamismo y Narrativa Visual: Transiciones y Animaciones**

Una presentación estática es indistinguible de un PDF. Reveal.js ofrece un motor de animación potente que, bien utilizado, refuerza la narrativa cognitiva.

### **4.1. Transiciones de Diapositivas**

Las transiciones no son meros adornos; comunican cambios de contexto. Se configuran globalmente en YAML o localmente por diapositiva.

| Tipo | Descripción y Uso Recomendado | Referencia |
| :---- | :---- | :---- |
| none | Cambio instantáneo. Ideal para secuencias rápidas de imágenes que simulan animación. | 1 |
| fade | Desvanecimiento cruzado. Elegante, profesional, bajo impacto cognitivo. Estándar recomendado. | 1 |
| slide | Desplazamiento lateral. Comunica continuidad lineal. Predeterminado. | 1 |
| convex/concave | Efectos 3D rotativos. Visualmente llamativos pero pueden causar mareo o distracción. Usar con precaución. | 1 |
| zoom | Zoom desde el centro. Útil para indicar "profundización" en un tema. | 1 |

**Configuración Granular:** Es posible definir transiciones de entrada y salida diferentes: \#\# Título {transition="fade-in slide-out"}. Esto permite crear flujos narrativos donde una diapositiva "aparece" suavemente pero "empuja" hacia la siguiente tema.6

### **4.2. Auto-Animate: Continuidad Cognitiva**

La característica auto-animate es una herramienta superior para explicaciones técnicas, especialmente para mostrar la evolución de código o diagramas. Cuando dos diapositivas adyacentes tienen el atributo {auto-animate=true}, Reveal.js intenta interpolar las posiciones y estilos de los elementos coincidentes.

**Mecanismo de Coincidencia:**

* **Texto:** Se empareja automáticamente si es idéntico.  
* **Elementos (Divs, Imágenes):** Requieren un atributo data-id explícito para ser rastreados.

**Ejemplo Práctico (Evolución de Código):**

**Diapositiva 1:**

## **Algoritmo Base {auto-animate=true}python**

def calcular(x):

return x \* x

**Diapositiva 2:**

## **Algoritmo Optimizado {auto-animate=true}python**

def calcular(x):

\# Vectorización con NumPy

return np.square(x)

En este escenario, el bloque de código se redimensionará y las líneas coincidentes se moverán suavemente a sus nuevas posiciones, ayudando a la audiencia a identificar visualmente los cambios (diff) sin esfuerzo cognitivo.6

### **4.3. Fragmentos: Revelación Progresiva**

Los fragmentos permiten mostrar elementos de una diapositiva secuencialmente.

* **Básico:** .fragment hace que el elemento aparezca (fade-in) al avanzar.  
* **Efectos:** .fade-up, .fade-left, .zoom-in, .blur.  
* **Efectos de Salida:** .fade-out (el elemento desaparece), .semi-fade-out (el elemento se atenúa, ideal para listas donde se quiere mantener el contexto pero desenfocar los puntos anteriores).  
* **Resaltado:** .highlight-red, .highlight-blue, .highlight-current-blue (solo resalta mientras es el fragmento activo, luego vuelve a la normalidad).6

**Control de Secuencia:**

El atributo fragment-index permite un control no lineal. Varios elementos pueden tener el mismo índice para aparecer simultáneamente.

* Punto 1 {.fragment fragment-index=1}  
* Punto 2 {.fragment fragment-index=3}  
* Punto 3 (Aparece con el 1\) {.fragment fragment-index=1}

## ---

**5\. Código Ejecutable: La Potencia de Quarto**

A diferencia de PowerPoint, Quarto permite ejecutar código (R, Python, Julia, OJS) y renderizar sus salidas directamente en la diapositiva.

### **5.1. Configuración de Chunks para Presentaciones**

Las opciones de celda (\#|) deben ajustarse para el contexto de proyección, donde el espacio es limitado y la legibilidad es prioritaria.

* **echo: true**: Muestra el código fuente. Esencial para presentaciones docentes o técnicas.  
* **eval: true**: Ejecuta el código y muestra la salida (gráficos, tablas).  
* **output-location**: Controla dónde aparece la salida respecto al código.  
  * fragment: El código se ve primero, la salida aparece tras un clic.  
  * column: Crea un diseño de dos columnas automático (Código izquierda, Salida derecha).  
  * slide: Mueve la salida a una diapositiva nueva generada automáticamente. Útil para gráficos grandes que requieren pantalla completa.1  
* **code-line-numbers**: Permite resaltar líneas de código secuencialmente al avanzar la presentación. Sintaxis: "1,3|5-7" (Primero resalta líneas 1 y 3, luego avanza y resalta del 5 al 7). Esto guía la atención de la audiencia durante la explicación del código.1

### **5.2. Manejo de Código Extenso**

El código que excede el ancho o alto de la diapositiva es un problema recurrente.

* **Altura:** code-block-height en YAML establece una altura máxima para todos los bloques de código, añadiendo barras de desplazamiento si es necesario. Esto evita que un bloque largo empuje el resto del contenido fuera de la diapositiva.7  
* **Ancho:** Quarto/Reveal no ajustan automáticamente las líneas de código largas en la vista de resaltado de sintaxis (syntax highlighting). Se recomienda usar herramientas de formateo (como formatR o black) para limitar el ancho de línea a \~60-80 caracteres antes de renderizar, o usar CSS personalizado para habilitar white-space: pre-wrap en los bloques de código, aunque esto puede afectar la legibilidad de la indentación.7

## ---

**6\. Personalización Estética Profunda: Temas y SASS**

Para alcanzar un nivel de "muy alta calidad", no basta con los temas predeterminados. Un LLM experto debe ser capaz de implementar sistemas de diseño personalizados utilizando SASS (Syntactically Awesome Style Sheets).

### **6.1. Arquitectura de Temas en Quarto**

Quarto utiliza un sistema de capas para compilar el CSS final.

1. **Framework Base:** Estilos core de Reveal.js.  
2. **Tema Quarto:** (ej. theme: moon). Define variables SASS predeterminadas.  
3. **Personalización Usuario:** Archivo .scss proporcionado en el YAML.

**Sintaxis del Archivo SCSS Personalizado:**

El archivo debe estructurarse con decoradores especiales para inyectar variables en el momento correcto del proceso de compilación.

SCSS

/\*-- scss:defaults \--\*/  
// Sobrescribir variables AQUÍ. Esto afecta a todos los cálculos derivados.  
$body-bg: \#1a1a2e;  
$body-color: \#e6e6e6;  
$link-color: \#e94560;  
$presentation-heading-font: "Montserrat", sans-serif;  
$presentation-font-size-root: 40px; // Escala base de todo el texto

/\*-- scss:rules \--\*/  
// Reglas CSS estándar. Usar selectores específicos.  
.reveal.slide h1 {  
  border-bottom: 3px solid $link-color;  
  padding-bottom: 0.5em;  
}

.reveal.code-wrapper code {  
  font-family: "Fira Code", monospace;  
}

**Variables Clave para Personalización:**

* $font-family-sans-serif: Tipografía principal.  
* $presentation-heading-color: Color de los títulos.  
* $code-block-bg: Color de fondo de los bloques de código.  
* $code-block-font-size: Tamaño de fuente del código (reducir ligeramente suele ayudar a encajar más contenido).12

### **6.2. Fondos Avanzados y Parallax**

Reveal.js permite fondos ricos que van más allá de colores sólidos.

* **Imágenes/Videos:** data-background-image="img.jpg", data-background-video="vid.mp4".  
* **Iframes:** data-background-iframe="https://example.com". Permite tener sitios web interactivos como fondo de la diapositiva.  
* **Parallax:** Configurando parallax-background-image y parallax-background-size en el YAML, se crea un efecto de profundidad donde el fondo se mueve más lento que el primer plano al navegar. Esto añade una sensación de continuidad y sofisticación visual "cinemática".1

## ---

**7\. Interactividad y Ecosistema de Extensiones**

Para convertir una presentación en una aplicación interactiva, Quarto integra Observable JS (OJS) y soporta un ecosistema de extensiones.

### **7.1. Observable JS (OJS): Reactividad en el Cliente**

OJS permite crear gráficos y controles interactivos que se ejecutan enteramente en el navegador del usuario, sin necesidad de un servidor backend (a diferencia de Shiny).

**Flujo de Datos:**

Se pueden procesar datos complejos en R o Python durante la compilación y pasarlos a OJS usando ojs\_define().

R

\# En chunk de R  
datos\_procesados \<- raw\_data %\>% filter(...)  
ojs\_define(data \= datos\_procesados)

JavaScript

// En chunk de OJS  
viewof threshold \= Inputs.range(, {label: "Umbral"})  
Plot.plot({  
  marks:  
})

Esta arquitectura híbrida aprovecha la potencia de R/Python para la preparación de datos y la velocidad de D3/Plot/OJS para la visualización interactiva en la presentación.13

### **7.2. Plugins Nativos y Extensiones de la Comunidad**

Quarto viene con plugins esenciales preinstalados y configurables en YAML:

* **Chalkboard:** chalkboard: true. Permite dibujar sobre las diapositivas (ideal para docencia/tablets).  
* **Menu:** menu: true. Navegación lateral por árbol de diapositivas.  
* **Multiplex:** Permite que la audiencia siga la presentación en sus propios dispositivos, sincronizada con el presentador.

**Extensiones Recomendadas:**

La comunidad ha creado extensiones potentes que un LLM debe conocer y saber recomendar instalar (vía quarto add):

* quarto-ext/pointer: Puntero láser virtual que sigue al ratón.  
* quarto-ext/attribution: Citaciones elegantes en el margen.  
* quarto-ext/code-fullscreen: Botón para maximizar bloques de código para mejor lectura.15

## ---

**8\. Prevención de Alucinaciones y Errores Comunes en LLMs**

Un LLM experto debe ser consciente de sus propias tendencias al error cuando genera código Quarto/Reveal.js. A continuación se detallan las "alucinaciones" más frecuentes y la corrección técnica correspondiente.

### **8.1. Alucinación de Sintaxis HTML/CSS**

**Error:** El LLM intenta crear columnas usando \<div style="float:left; width:50%"\>.

**Corrección:** Esto rompe el sistema de escalado de Reveal.js. La única forma robusta es usar los Divs de Pandoc ::: {.columns} que Quarto traduce a la estructura Flexbox específica que Reveal espera.

### **8.2. Invención de Clases CSS**

**Error:** Inventar clases como .text-center o .large-font asumiendo que existen por defecto (como en Bootstrap). **Corrección:** Reveal.js tiene muy pocas clases utilitarias (.r-fit-text, .r-stack, .r-stretch). Cualquier otra clase de estilo debe ser definida explícitamente en el bloque css o archivo .scss, o usar atributos de estilo en línea (menos recomendado).16

### **8.3. Confusión de Contexto de Ejecución**

**Error:** Intentar usar variables de Python dentro de un bloque OJS directamente sin usar ojs\_define.

**Corrección:** OJS corre en el navegador; Python corre en tiempo de compilación. El puente ojs\_define es obligatorio para la transferencia de datos.

### **8.4. Rutas de Recursos**

**Error:** Referenciar imágenes con rutas absolutas locales (C:/Users/...) o asumir que los recursos están en la misma carpeta sin verificar.

**Corrección:** Siempre usar rutas relativas al archivo .qmd y recomendar una estructura de proyecto organizada (ej. carpeta /images).

## ---

**9\. Estrategias de Exportación y Distribución**

El ciclo de vida de la presentación termina con su entrega.

### **9.1. Publicación Web**

La salida predeterminada es un archivo HTML.

* **embed-resources: true**: Genera un único archivo HTML con todas las imágenes, scripts y estilos codificados en base64. Ideal para enviar por email.  
* **embed-resources: false** (default): Mantiene las dependencias en una carpeta \_files. Carga más rápido en web y es mejor para despliegue en GitHub Pages o Netlify.

### **9.2. Exportación a PDF (Modo Impresión)**

Para generar un PDF estático de alta calidad (para archivar o compartir):

1. Abrir la presentación en el navegador.  
2. Añadir ?print-pdf al final de la URL.  
3. Abrir el diálogo de impresión (Ctrl+P).  
4. Configurar: Márgenes "Ninguno", Gráficos de fondo "Activado".  
5. **Automatización:** Usar el paquete pagedown::chrome\_print() en un script de R permite generar el PDF programáticamente, ideal para pipelines de integración continua (CI/CD).7

## ---

**10\. Conclusión**

Dominar Quarto Reveal.js requiere trascender la escritura de contenido para convertirse en un arquitecto de experiencias de información. Este manual ha desglosado las capas técnicas necesarias: desde la configuración precisa del YAML y la estructuración semántica del contenido, hasta la personalización profunda con SASS y la integración de interactividad computacional. Al adherirse a estos patrones de diseño y evitar las trampas comunes de alucinación, un sistema de IA puede generar presentaciones que no solo son visualmente impecables, sino técnicamente robustas, accesibles y funcionalmente superiores a las alternativas tradicionales.

---

**Tabla Resumen de Referencia Rápida para Configuración YAML**

| Categoría | Opción | Valor Recomendado (Experto) | Efecto |
| :---- | :---- | :---- | :---- |
| **Geometría** | width / height | 1920 / 1080 | Alta definición, evita pixelación en pantallas grandes. |
| **Geometría** | margin | 0.05 | Maximiza el espacio útil para contenido técnico. |
| **Navegación** | history | true | Permite compartir enlaces a diapositivas específicas. |
| **Navegación** | navigation-mode | linear | Flujo estándar. Usar vertical solo para estructuras 2D complejas. |
| **Estilo** | center | false | Alineación superior. Mejor para código y listas largas. |
| **Estilo** | theme | \[default, custom.scss\] | Base estándar \+ personalización corporativa/específica. |
| **Código** | code-line-numbers | true | Habilita el resaltado secuencial en bloques de código. |
| **Interacción** | chalkboard | true | Habilita herramientas de dibujo en tiempo real. |

---

**Nota sobre Citaciones:** Las referencias entre corchetes (ej. 1) corresponden a los fragmentos de investigación analizados, garantizando que cada recomendación técnica está respaldada por la documentación oficial de Quarto, Reveal.js o prácticas comunitarias validadas.

#### **Obras citadas**

1. Revealjs Options \- Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/reference/formats/presentations/revealjs.html](https://quarto.org/docs/reference/formats/presentations/revealjs.html)  
2. Execution Options \- Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/computations/execution-options.html](https://quarto.org/docs/computations/execution-options.html)  
3. Custom slide class for a Quarto/revealjs presentation \- General \- Posit Community, fecha de acceso: febrero 11, 2026, [https://forum.posit.co/t/custom-slide-class-for-a-quarto-revealjs-presentation/155948](https://forum.posit.co/t/custom-slide-class-for-a-quarto-revealjs-presentation/155948)  
4. How to use two-column layout with reveal.js? \- Stack Overflow, fecha de acceso: febrero 11, 2026, [https://stackoverflow.com/questions/30861845/how-to-use-two-column-layout-with-reveal-js](https://stackoverflow.com/questions/30861845/how-to-use-two-column-layout-with-reveal-js)  
5. Some tips and tricks for Quarto when rendering as a reveal.js slideshow, fecha de acceso: febrero 11, 2026, [https://www.avonture.be/blog/quarto-revealjs-tips/](https://www.avonture.be/blog/quarto-revealjs-tips/)  
6. Advanced Reveal \- Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/presentations/revealjs/advanced.html](https://quarto.org/docs/presentations/revealjs/advanced.html)  
7. Seven tips for creating Quarto revealjs presentations | Dr Tom Palmer, fecha de acceso: febrero 11, 2026, [https://remlapmot.github.io/post/2025/quarto-revealjs-tips/](https://remlapmot.github.io/post/2025/quarto-revealjs-tips/)  
8. Rows and nested columns in a revealjs presentation · quarto-dev · Discussion \#10061, fecha de acceso: febrero 11, 2026, [https://github.com/quarto-dev/quarto-cli/discussions/10061](https://github.com/quarto-dev/quarto-cli/discussions/10061)  
9. Revealjs Plugins \- Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/extensions/revealjs.html](https://quarto.org/docs/extensions/revealjs.html)  
10. Revealjs \- Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/presentations/revealjs/](https://quarto.org/docs/presentations/revealjs/)  
11. do not create a scrollable code block for more than 18 lines of code for reveal slides · quarto-dev · Discussion \#2910 \- GitHub, fecha de acceso: febrero 11, 2026, [https://github.com/orgs/quarto-dev/discussions/2910](https://github.com/orgs/quarto-dev/discussions/2910)  
12. Reveal Themes \- Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/presentations/revealjs/themes.html](https://quarto.org/docs/presentations/revealjs/themes.html)  
13. Observable JS – Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/interactive/ojs/](https://quarto.org/docs/interactive/ojs/)  
14. How to use a dataframe created in an R code chunk in an ojs code chunk? \- Stack Overflow, fecha de acceso: febrero 11, 2026, [https://stackoverflow.com/questions/73080070/how-to-use-a-dataframe-created-in-an-r-code-chunk-in-an-ojs-code-chunk](https://stackoverflow.com/questions/73080070/how-to-use-a-dataframe-created-in-an-r-code-chunk-in-an-ojs-code-chunk)  
15. Quarto Extensions – Quarto, fecha de acceso: febrero 11, 2026, [https://quarto.org/docs/extensions/listing-revealjs.html](https://quarto.org/docs/extensions/listing-revealjs.html)  
16. LLM hallucinations: Complete guide to AI errors \- SuperAnnotate, fecha de acceso: febrero 11, 2026, [https://www.superannotate.com/blog/ai-hallucinations](https://www.superannotate.com/blog/ai-hallucinations)  
17. LLM hallucinations and failures: lessons from 5 examples \- Evidently AI, fecha de acceso: febrero 11, 2026, [https://www.evidentlyai.com/blog/llm-hallucination-examples](https://www.evidentlyai.com/blog/llm-hallucination-examples)