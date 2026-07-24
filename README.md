# 🌿 Sistema de Gestión de Senderos

Optimización de rutas mediante el algoritmo de Dijkstra

Sistema web desarrollado en Python y Streamlit que permite calcular rutas óptimas en senderos naturales de Panamá utilizando el algoritmo de Dijkstra sobre grafos ponderados. La aplicación adapta el recorrido según el tipo de ruta seleccionado, las condiciones climáticas y proporciona información sobre biodiversidad y recomendaciones de seguridad.


📌 Características
🗺️ Cálculo de rutas óptimas utilizando el algoritmo de Dijkstra.
🌧️ Simulación de condiciones de lluvia con bloqueo dinámico de senderos peligrosos.
🚶 Cuatro tipos de rutas:
🟢 Ruta más segura
⚡ Ruta más rápida
📏 Ruta más corta
⚖️ Ruta balanceada
🌿 Información de fauna y flora específica para cada sendero.
⚠️ Avisos contextuales sobre clima, equipo recomendado y tramos bloqueados.
📍 Visualización gráfica del recorrido utilizando Matplotlib.
🔄 Ajuste dinámico de pesos según las condiciones del terreno.
📍 Senderos incluidos

El sistema trabaja con tres senderos naturales de Panamá:
🌳 Trillo Tití
🦅 Summit
🐒 Gamboa

Cada sendero se modela como un grafo independiente con nodos y conexiones que contienen información de:
Distancia
Tiempo estimado
Dificultad

🧠 Algoritmo utilizado
El proyecto implementa el algoritmo de Dijkstra, el cual encuentra el camino de menor costo entre dos nodos de un grafo con pesos positivos.
Dependiendo del tipo de ruta seleccionado, el algoritmo optimiza diferentes criterios:

Tipo de Ruta	Criterio
Ruta más segura	Dificultad
Ruta más rápida	Tiempo
Ruta más corta	Distancia
Ruta balanceada	Peso combinado

Además, antes de ejecutar Dijkstra, el sistema modifica dinámicamente los pesos según las condiciones climáticas y la dificultad del terreno.

🌧️ Simulación de lluvia
Cuando el usuario activa el modo Sendero Mojado, el sistema:
Bloquea automáticamente los tramos con dificultad alta.
Incrementa el tiempo estimado de recorrido.
Incrementa la dificultad de los senderos restantes.
Busca rutas alternativas evitando los caminos bloqueados.

Los tramos cerrados se muestran en el mapa mediante líneas rojas punteadas y un símbolo de bloqueo.

🌿 Biodiversidad
Después de calcular una ruta, el sistema presenta información educativa sobre:
Fauna
Monos
Perezosos
Tucanes
Jaguares
Águila Harpía
Coatíes
Iguanas
Flora
Mangle Rojo
Cedro Amargo
Roble
Caoba
Palma Real
Árbol de Panamá
Bromelias

🛠️ Tecnologías utilizadas
Python 3
Streamlit
NetworkX
Matplotlib
JSON

📂 Estructura del proyecto
Sistema-Gestion-Senderos/
│
├── app.py
├── data/
│   ├── trillo_titi.json
│   ├── summit.json
│   └── gamboa.json
│
├── assets/
│
├── utils/
│
├── requirements.txt
│
└── README.md

La estructura puede variar ligeramente dependiendo de la organización final del proyecto.

▶️ Instalación
Clonar el repositorio:
git clone https://github.com/usuario/sistema-gestion-senderos.git

Entrar al proyecto:
cd sistema-gestion-senderos

Instalar dependencias:
pip install -r requirements.txt

Ejecutar la aplicación:
streamlit run app.py

📊 Funcionalidades principales
Selección del sendero.
Selección del punto de inicio y destino.
Selección del tipo de ruta.
Simulación de sendero seco o mojado.
Visualización de la ruta calculada.
Visualización de senderos bloqueados.
Información de biodiversidad.
Recomendaciones de seguridad.

📈 Mejoras futuras
Integración de datos meteorológicos en tiempo real.
Rutas alternativas mediante el algoritmo de Yen.
Ajuste del ritmo del senderista.
Sistema de dificultad física y técnica independiente.
Expansión a más parques nacionales de Panamá.

👥 Autores
Aaron Fehrenbach
Daniela Insturain

📄 Licencia
Este proyecto fue desarrollado con fines académicos para demostrar la aplicación del algoritmo de Dijkstra en la optimización de rutas dentro de un sistema inteligente para la gestión de senderos naturales en Panamá.


