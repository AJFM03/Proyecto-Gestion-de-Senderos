import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import json
from PIL import Image
from pathlib import Path

st.set_page_config(
    page_title="Senderos · Panamá",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── ESTILOS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Outfit:wght@300;400;500;600&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background-color: #060e08;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(20,83,45,0.55) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%,  rgba(6,78,59,0.45) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
}

/* ── OCULTAR ELEMENTOS DEFAULT ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }

/* ── ENCABEZADO CUSTOM ── */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'Outfit', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 600;
    color: #ecfdf5;
    line-height: 1.1;
    margin: 0 0 0.5rem;
    text-shadow: 0 0 60px rgba(74,222,128,0.15);
}
.hero-title em {
    font-style: italic;
    color: #86efac;
}
.hero-sub {
    font-size: 0.9rem;
    color: #6ee7b7;
    font-weight: 300;
    letter-spacing: 0.05em;
}
.hero-divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #4ade80, transparent);
    margin: 1.4rem auto 0;
}

/* ── PANEL DE CONTROL ── */
.panel-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #a7f3d0;
    letter-spacing: 0.03em;
    margin-bottom: 0.2rem;
}
.panel-desc {
    font-size: 0.7rem;
    color: #4ade80;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
/* Estilo del st.container(border=True) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(160deg, rgba(6,78,59,0.4) 0%, rgba(4,47,36,0.65) 100%) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), inset 0 1px 0 rgba(74,222,128,0.07) !important;
}
.panel-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #a7f3d0;
    letter-spacing: 0.03em;
    margin-bottom: 0.2rem;
}
.panel-desc {
    font-size: 0.75rem;
    color: #6ee7b7;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(74,222,128,0.1);
}

/* ── LABELS ── */
label, .stSelectbox label, p {
    color: #a7f3d0 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── SELECTBOX ── */
div[data-baseweb="select"] > div {
    background: rgba(4,47,36,0.7) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: 10px !important;
    color: #ecfdf5 !important;
    transition: border-color 0.2s;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(74,222,128,0.5) !important;
}
div[data-baseweb="select"] svg { fill: #4ade80 !important; }

/* ── TOGGLE ── */
div[data-testid="stToggle"] {
    background: rgba(4,47,36,0.6);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 10px;
    padding: 10px 14px;
}

/* ── BOTÓN ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #166534 0%, #14532d 100%) !important;
    color: #ecfdf5 !important;
    border: 1px solid rgba(74,222,128,0.4) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(22,101,52,0.3) !important;
    margin-top: 0.5rem;
}
.stButton > button:hover:not(:disabled) {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    color: #052e16 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(34,197,94,0.35) !important;
    border-color: #22c55e !important;
}
.stButton > button:disabled {
    opacity: 0.35 !important;
    cursor: not-allowed !important;
}

/* ── MÉTRICAS ── */
div[data-testid="stMetric"] {
    background: linear-gradient(160deg, rgba(6,78,59,0.5) 0%, rgba(4,47,36,0.7) 100%) !important;
    border: 1px solid rgba(74,222,128,0.15) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
    text-align: center !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important;
    transition: transform 0.2s;
}
div[data-testid="stMetric"]:hover { transform: translateY(-2px); }
div[data-testid="stMetricLabel"] {
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #6ee7b7 !important;
}
div[data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.6rem !important;
    color: #a7f3d0 !important;
}

/* ── SUCCESS / ERROR ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 3px !important;
    font-size: 0.88rem !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(74,222,128,0.12) !important;
    margin: 1rem 0 !important;
}

/* ── PASO A PASO ── */
.step-box {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    border-radius: 10px;
    background: rgba(6,78,59,0.3);
    border: 1px solid rgba(74,222,128,0.08);
    margin-bottom: 6px;
    font-size: 0.88rem;
    color: #d1fae5;
    transition: background 0.2s;
}
.step-box:hover { background: rgba(6,78,59,0.5); }
.step-icon { font-size: 1rem; flex-shrink: 0; }

/* ── AVISOS CONTEXTUALES ── */
.aviso-card {
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 10px;
    border-left: 4px solid;
}
.aviso-titulo {
    display: block;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    margin-bottom: 6px;
}
.aviso-item {
    font-size: 0.8rem;
    padding: 3px 0 3px 8px;
    opacity: 0.9;
    line-height: 1.5;
}
.aviso-lluvia {
    background: rgba(30, 58, 138, 0.25);
    border-color: #3b82f6;
    color: #bfdbfe;
}
.aviso-lluvia .aviso-titulo { color: #93c5fd; }
.aviso-peligro {
    background: rgba(153, 27, 27, 0.25);
    border-color: #ef4444;
    color: #fecaca;
}
.aviso-peligro .aviso-titulo { color: #f87171; }
.aviso-moderado {
    background: rgba(120, 53, 15, 0.25);
    border-color: #f59e0b;
    color: #fde68a;
}
.aviso-moderado .aviso-titulo { color: #fbbf24; }
.aviso-ok {
    background: rgba(6, 78, 59, 0.35);
    border-color: #22c55e;
    color: #bbf7d0;
}
.aviso-ok .aviso-titulo { color: #86efac; }
.tramo-bloqueado {
    font-size: 0.78rem;
    padding: 4px 0 4px 8px;
    opacity: 0.9;
    font-family: 'Courier New', monospace;
}

/* ── BADGE DE ESFUERZO ── */
.esfuerzo-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
}
.badge-facil    { background: rgba(34,197,94,0.15);  border: 1px solid rgba(34,197,94,0.4);  color: #86efac; }
.badge-moderado { background: rgba(251,191,36,0.12); border: 1px solid rgba(251,191,36,0.35); color: #fde68a; }
.badge-intenso  { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.35);  color: #fca5a5; }

/* ── FAUNA Y FLORA ── */
.fauna-flora-panel {
    background: linear-gradient(160deg, rgba(6,78,59,0.35) 0%, rgba(4,47,36,0.55) 100%);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 16px;
    padding: 18px 16px;
    backdrop-filter: blur(8px);
}
.fauna-flora-titulo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #a7f3d0;
    letter-spacing: 0.03em;
    margin-bottom: 4px;
}
.fauna-flora-sub {
    font-size: 0.68rem;
    color: #4ade80;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(74,222,128,0.12);
}
.especie-card {
    background: rgba(6,78,59,0.3);
    border: 1px solid rgba(74,222,128,0.1);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 8px;
    transition: background 0.2s;
}
.especie-card:hover { background: rgba(6,78,59,0.5); }
.especie-emoji { font-size: 1.3rem; margin-right: 8px; }
.especie-nombre {
    font-weight: 600;
    font-size: 0.85rem;
    color: #d1fae5;
}
.especie-nombre-cientifico {
    font-size: 0.72rem;
    color: #6ee7b7;
    font-style: italic;
    margin-bottom: 3px;
}
.especie-desc {
    font-size: 0.75rem;
    color: #a7f3d0;
    opacity: 0.85;
    line-height: 1.4;
}
.especie-tag {
    display: inline-block;
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 999px;
    margin-top: 5px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.tag-fauna {
    background: rgba(251,191,36,0.15);
    border: 1px solid rgba(251,191,36,0.3);
    color: #fde68a;
}
.tag-flora {
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.3);
    color: #86efac;
}
.tag-ave {
    background: rgba(96,165,250,0.15);
    border: 1px solid rgba(96,165,250,0.3);
    color: #bfdbfe;
}
.seccion-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4ade80;
    margin: 12px 0 6px;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #060e08; }
::-webkit-scrollbar-thumb { background: #166534; border-radius: 3px; }

/* ── AVISOS ── */
.aviso-card {
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.82rem;
    line-height: 1.5;
    font-family: 'Outfit', sans-serif;
}
.aviso-lluvia {
    background: rgba(37, 99, 235, 0.12);
    border: 1px solid rgba(96, 165, 250, 0.35);
    color: #bfdbfe;
}
.aviso-peligro {
    background: rgba(220, 38, 38, 0.12);
    border: 1px solid rgba(248, 113, 113, 0.4);
    color: #fca5a5;
}
.aviso-moderado {
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(251, 191, 36, 0.35);
    color: #fde68a;
}
.aviso-ok {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.2);
    color: #86efac;
}
.aviso-titulo {
    font-weight: 600;
    font-size: 0.85rem;
    margin-bottom: 5px;
    display: block;
}
.aviso-item {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    margin-top: 4px;
}
.tramo-bloqueado {
    background: rgba(220,38,38,0.15);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 8px;
    padding: 6px 10px;
    margin-bottom: 4px;
    font-size: 0.8rem;
    color: #fca5a5;
}
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🌿 Panamá · Rutas Naturales</div>
    <h1 class="hero-title">Gestión de <em>Senderos</em></h1>
    <p class="hero-sub">Optimización de rutas para una experiencia de senderismo excepcional</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── CONFIGURACIÓN DE MAPAS ──────────────────────────────────────────────────
mapas = {
    "Trillo Tití": {
        "imagen": "Captura de pantalla 2025-04-19 172647.png",
        "json": "grafo_Trillotiti_v2.json",
        "nodos": {
            "A": (400, 87),  "B": (330, 130), "C": (224, 80),
            "D": (218, 206), "E": (142, 158), "F": (35, 193),
            "G": (120, 307), "H": (201, 346)
        }
    },
    "Summit": {
        "imagen": "Mapa_Summit_v2.png",
        "json": "grafo_Summit_v2.json",
        "nodos": {
            "A": (124, 383), "B": (69, 359),  "C": (67, 318),
            "D": (142, 274), "E": (259, 157), "F": (207, 85),
            "G": (312, 79),  "H": (301, 149)
        }
    },
    "Gamboa": {
        "imagen": "Mapa_Gamboa_v2.png",
        "json": "grafo_Gamboa_v2.json",
        "nodos": {
            "A": (152, 36),  "B": (153, 103), "C": (203, 160),
            "D": (262, 145), "E": (376, 171), "F": (412, 230),
            "G": (526, 145), "H": (574, 108)
        }
    }
}

# ── FAUNA Y FLORA POR SENDERO ────────────────────────────────────────────────
FAUNA_FLORA = {
    "Trillo Tití": {
        "fauna": [
            {
                "emoji": "🐒", "nombre": "Monos",
                "cientifico": "Primates sp.",
                "desc": "Varias especies de monos habitan el dosel del sendero. Se desplazan en grupos y son fácilmente detectables por el sonido.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🦥", "nombre": "Perezoso",
                "cientifico": "Bradypus variegatus",
                "desc": "Habitante del dosel, casi inmóvil durante el día. Busca manchas de luz solar en la copa de los árboles.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🦎", "nombre": "Iguana Verde",
                "cientifico": "Iguana iguana",
                "desc": "Frecuente en ramas bajas cerca de quebradas. Puede alcanzar 1.5m de largo. Completamente inofensiva.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🦜", "nombre": "Tucán",
                "cientifico": "Ramphastos sulfuratus",
                "desc": "Inconfundible por su enorme pico multicolor. Se avista al amanecer en los árboles más altos del sendero.",
                "tag": "tag-ave"
            },
            {
                "emoji": "🐦", "nombre": "Garza",
                "cientifico": "Ardea alba",
                "desc": "Ave acuática elegante de plumaje blanco. Frecuente en zonas húmedas y quebradas del sendero.",
                "tag": "tag-ave"
            },
        ],
        "flora": [
            {
                "emoji": "🌊", "nombre": "Mangle Rojo",
                "cientifico": "Rhizophora mangle",
                "desc": "Común en las costas del Pacífico, fundamental para el ecosistema marino. Sus raíces aéreas son características.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌳", "nombre": "Cedro Amargo",
                "cientifico": "Cedrela odorata",
                "desc": "Árbol maderable característico de los bosques secos de la región. Su madera aromática es muy apreciada.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌸", "nombre": "Roble",
                "cientifico": "Tabebuia rosea",
                "desc": "Árbol conocido por su floración rosada, muy común en la zona costera. Uno de los árboles más vistosos de Panamá.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌲", "nombre": "Espavé",
                "cientifico": "Anacardium excelsum",
                "desc": "Árbol de gran tamaño, típico de los bosques húmedos y ribereños del Pacífico. Pariente silvestre del marañón.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌿", "nombre": "Bromelias",
                "cientifico": "Familia Bromeliaceae",
                "desc": "Plantas epífitas que crecen sobre los árboles y son abundantes en la flora de la región. Forman micro-ecosistemas.",
                "tag": "tag-flora"
            },
        ]
    },
    "Summit": {
        "fauna": [
            {
                "emoji": "🦁", "nombre": "Jaguar",
                "cientifico": "Panthera onca",
                "desc": "El felino más grande de América. Presencia comprobada en el área aunque difícil de avistar. Su rastro puede verse en el barro.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🦥", "nombre": "Perezoso de Tres Dedos",
                "cientifico": "Bradypus variegatus",
                "desc": "Habitante del dosel, casi inmóvil durante el día. Busca manchas de luz solar en la copa de los árboles.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🐦", "nombre": "Águila Harpía",
                "cientifico": "Harpia harpyja",
                "desc": "Ave rapaz más poderosa del mundo. El Summit tiene uno de los pocos programas de cría en cautiverio de esta especie.",
                "tag": "tag-ave"
            },
            {
                "emoji": "🐊", "nombre": "Cocodrilo Americano",
                "cientifico": "Crocodylus acutus",
                "desc": "Avistado en las orillas del Canal de Panamá. Especie protegida; observar desde distancia segura.",
                "tag": "tag-fauna"
            },
        ],
        "flora": [
            {
                "emoji": "🌴", "nombre": "Palma Real",
                "cientifico": "Roystonea regia",
                "desc": "Palmera majestuosa de tronco plateado. Sus frutos son alimento clave para tucanes y loros.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌸", "nombre": "Orquídea del Espíritu Santo",
                "cientifico": "Peristeria elata",
                "desc": "Flor nacional de Panamá. Florece entre julio y agosto con una flor interior que simula una paloma blanca.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌳", "nombre": "Árbol de Panamá",
                "cientifico": "Sterculia apetala",
                "desc": "Árbol nacional de Panamá, de copa ancha y semillas comestibles. Identificable por su corteza grisácea.",
                "tag": "tag-flora"
            },
        ]
    },
    "Gamboa": {
        "fauna": [
            {
                "emoji": "🐒", "nombre": "Mono Aullador",
                "cientifico": "Alouatta palliata",
                "desc": "Sus rugidos resuenan kilómetros a la redonda. Se avista en grupos al amanecer en las copas de los árboles más altos.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🐒", "nombre": "Mono Capuchino",
                "cientifico": "Cebus capucinus",
                "desc": "Primate curioso e inteligente, fácil de observar cerca de los caminos. Se desplaza en grupos familiares ruidosos.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🦥", "nombre": "Oso Perezoso",
                "cientifico": "Bradypus variegatus",
                "desc": "Se cuelga inmóvil de las ramas durante horas. Busca la luz solar en el dosel para regular su temperatura corporal.",
                "tag": "tag-fauna"
            },
            {
                "emoji": "🦜", "nombre": "Tucán",
                "cientifico": "Ramphastos sulfuratus",
                "desc": "Su gran pico colorido lo hace inconfundible. Habita el dosel del bosque y se alimenta de frutas silvestres.",
                "tag": "tag-ave"
            },
            {
                "emoji": "🦡", "nombre": "Coatí (Gatosolo)",
                "cientifico": "Nasua narica",
                "desc": "Mamífero sociable de hocico alargado. Se mueve en grupos por el suelo del bosque buscando insectos y frutas.",
                "tag": "tag-fauna"
            },
        ],
        "flora": [
            {
                "emoji": "🌳", "nombre": "Caoba",
                "cientifico": "Swietenia macrophylla",
                "desc": "Una de las maderas más valiosas del mundo. Árbol majestuoso de copa amplia, protegido por su alto valor ecológico.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌸", "nombre": "Crespón",
                "cientifico": "Lagerstroemia speciosa",
                "desc": "Árbol ornamental de flores rosadas o lilas muy llamativas. Florece profusamente durante la estación seca.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌸", "nombre": "Roble",
                "cientifico": "Tabebuia rosea",
                "desc": "Árbol de floración rosada espectacular. Uno de los más fotografiados en la temporada seca de Panamá.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌲", "nombre": "Árbol de Panamá",
                "cientifico": "Sterculia apetala",
                "desc": "Árbol nacional de Panamá. Su gran tamaño y copa densa lo convierten en refugio de numerosas especies de aves.",
                "tag": "tag-flora"
            },
            {
                "emoji": "🌺", "nombre": "Membrillo",
                "cientifico": "Gustavia superba",
                "desc": "Árbol de flores grandes y blancas muy fragantes. Sus frutos redondos son consumidos por monos y agutíes.",
                "tag": "tag-flora"
            },
        ]
    }
}

# ── SESSION STATE ───────────────────────────────────────────────────────────
if "ruta_resultado" not in st.session_state:
    st.session_state.ruta_resultado = None
if "sendero_activo" not in st.session_state:
    st.session_state.sendero_activo = None

# ── LAYOUT — 3 columnas: panel | mapa | fauna/flora ─────────────────────────
panel, col_mapa, col_fauna = st.columns([1, 2, 1.5], gap="large")

with panel:
    # Título ENCIMA del cuadro
    st.markdown("""
    <div class="panel-title">Configurar Ruta</div>
    <div class="panel-desc">Parámetros del recorrido</div>
    """, unsafe_allow_html=True)

    # Cuadro con los widgets adentro
    with st.container(border=True):
        mapa_seleccionado = st.selectbox("Sendero", mapas.keys())
        config     = mapas[mapa_seleccionado]
        nodos_mapa = config["nodos"]
        nodos      = list(nodos_mapa.keys())

        if st.session_state.sendero_activo != mapa_seleccionado:
            st.session_state.ruta_resultado = None
            st.session_state.sendero_activo = mapa_seleccionado

        c1, c2 = st.columns(2)
        with c1:
            inicio = st.selectbox("🚩 Inicio", nodos)
        with c2:
            fin = st.selectbox("🏁 Destino", nodos)

        criterio = st.selectbox(
            "Tipo de ruta",
            ["🟢 Ruta más segura", "⚡ Ruta más rápida", "📏 Ruta más corta", "⚖️ Ruta balanceada"],
        )

        sendero_mojado = st.toggle("🌧️  Sendero mojado (lluvia)")

        calcular = st.button(
            "✦ Calcular Ruta Óptima",
            disabled=(inicio == fin),
            use_container_width=True
        )

        if inicio == fin:
            st.warning("El inicio y destino deben ser diferentes.")

# ── CARGAR IMAGEN Y JSON ────────────────────────────────────────────────────
base_dir = Path(__file__).parent

try:
    imagen = Image.open(base_dir / config["imagen"])
except FileNotFoundError:
    st.error(f"Imagen no encontrada: {config['imagen']}")
    st.stop()

try:
    with open(base_dir / config["json"]) as f:
        data = json.load(f)
except FileNotFoundError:
    st.error(f"Datos no encontrados: {config['json']}")
    st.stop()

# ── HELPER: DIBUJAR MAPA ────────────────────────────────────────────────────
def dibujar_mapa(imagen, nodos_mapa, inicio, fin, ruta=None, titulo="", tramos_bloqueados=None):
    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor('#060e08')
    ax.set_facecolor('#060e08')

    ax.imshow(imagen, alpha=0.88)
    ax.axis("off")

    # Bordes del mapa
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Tramos bloqueados por lluvia (línea roja punteada)
    bloqueados_set = set()
    if tramos_bloqueados:
        for o, d, _ in tramos_bloqueados:
            bloqueados_set.add((o, d))
            bloqueados_set.add((d, o))
            if o in nodos_mapa and d in nodos_mapa:
                x1, y1 = nodos_mapa[o]
                x2, y2 = nodos_mapa[d]
                # Glow rojo
                ax.plot([x1,x2],[y1,y2], color='#ef4444', linewidth=8, alpha=0.12, zorder=1)
                # Línea punteada roja
                ax.plot([x1,x2],[y1,y2], color='#ef4444', linewidth=2,
                        linestyle='--', dashes=(4, 4), alpha=0.8, zorder=2)
                # Ícono de bloqueo en el centro del tramo
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                ax.annotate("🚫", xy=(mx, my), fontsize=9,
                            ha='center', va='center', zorder=7,
                            bbox=dict(boxstyle='round,pad=0.15',
                                      facecolor='#7f1d1d', edgecolor='#ef4444',
                                      alpha=0.85, linewidth=0.8))

    # Conexiones de fondo (gris suave)
    if ruta:
        for conexion in data.get("conexiones", []):
            o, d = conexion["origen"], conexion["destino"]
            if o not in nodos_mapa or d not in nodos_mapa:
                continue
            x1, y1 = nodos_mapa[o]
            x2, y2 = nodos_mapa[d]
            en_ruta = any(
                (ruta[i] == o and ruta[i+1] == d) or
                (ruta[i] == d and ruta[i+1] == o)
                for i in range(len(ruta)-1)
            )
            if not en_ruta:
                ax.plot([x1,x2],[y1,y2], color='#1a3a2a', linewidth=1.5, alpha=0.5, zorder=1)

    # Línea de ruta animada con glow
    if ruta:
        for u, v in zip(ruta, ruta[1:]):
            if u not in nodos_mapa or v not in nodos_mapa:
                continue
            x1, y1 = nodos_mapa[u]
            x2, y2 = nodos_mapa[v]
            # Sombra/glow
            ax.plot([x1,x2],[y1,y2], color='#22c55e', linewidth=9,  alpha=0.15, zorder=2, solid_capstyle='round')
            ax.plot([x1,x2],[y1,y2], color='#22c55e', linewidth=5,  alpha=0.3,  zorder=2, solid_capstyle='round')
            # Línea principal
            ax.plot([x1,x2],[y1,y2], color='#4ade80', linewidth=2.5, alpha=0.95, zorder=3, solid_capstyle='round')

    # Nodos
    for nodo, (x, y) in nodos_mapa.items():
        en_ruta = ruta and nodo in ruta

        if nodo == inicio:
            color, size, ring = '#22c55e', 130, '#86efac'
        elif nodo == fin:
            color, size, ring = '#fbbf24', 130, '#fde68a'
        elif en_ruta:
            color, size, ring = '#f87171', 90,  '#fca5a5'
        else:
            color, size, ring = '#1e4d35', 70,  '#2d6b4a'

        # Anillo exterior
        ax.scatter(x, y, s=size*2.2, color=ring, alpha=0.25, zorder=4)
        # Punto principal
        ax.scatter(x, y, s=size, color=color, zorder=5, edgecolors='white', linewidths=1.2)

        # Etiqueta con fondo
        ax.annotate(
            nodo,
            xy=(x, y), xytext=(x + 10, y - 6),
            color='white',
            fontsize=10, fontweight='bold',
            fontfamily='DejaVu Sans',
            zorder=6,
            bbox=dict(
                boxstyle='round,pad=0.25',
                facecolor='#052e16',
                edgecolor='#2d6b4a',
                alpha=0.75,
                linewidth=0.8
            )
        )

    # Leyenda
    leyenda = [
        mpatches.Patch(color='#22c55e', label='Inicio'),
        mpatches.Patch(color='#fbbf24', label='Destino'),
        mpatches.Patch(color='#f87171', label='En ruta'),
        mpatches.Patch(color='#1e4d35', label='Nodo'),
    ]
    if tramos_bloqueados:
        leyenda.append(mpatches.Patch(color='#ef4444', label='🚫 Bloqueado (lluvia)'))
    ax.legend(
        handles=leyenda,
        loc='lower right',
        framealpha=0.6,
        facecolor='#052e16',
        edgecolor='#166534',
        labelcolor='white',
        fontsize=8,
        borderpad=0.8
    )

    ax.set_title(titulo, color='#86efac', fontsize=10, pad=12,
                 fontfamily='DejaVu Sans', fontstyle='italic')

    fig.tight_layout(pad=0.5)
    return fig

# ── UMBRALES DE BLOQUEO POR LLUVIA ──────────────────────────────────────────
# Tramos con dificultad >= este valor se consideran INACCESIBLES bajo lluvia
UMBRAL_BLOQUEO_LLUVIA = 5   # dificultad base >= 5 → bloqueado si llueve

# ── HELPER: RENDERIZAR UN AVISO ──────────────────────────────────────────────
def _renderizar_aviso(tipo, titulo, mensajes, rec_titulo=None, rec_items=None):
    css = {"lluvia": "aviso-lluvia", "peligro": "aviso-peligro",
           "moderado": "aviso-moderado", "ok": "aviso-ok"}[tipo]
    items_html = "".join([f'<div class="aviso-item"><span>{m}</span></div>' for m in mensajes])
    rec_html = ""
    if rec_titulo:
        rec_items_html = "".join([f'<div class="aviso-item"><span>{r}</span></div>' for r in (rec_items or [])])
        rec_html = f'<div style="margin-top:8px;"><span class="aviso-titulo" style="opacity:0.8">{rec_titulo}</span>{rec_items_html}</div>'
    st.markdown(
        f'<div class="aviso-card {css}">'
        f'<span class="aviso-titulo">{titulo}</span>'
        f'{items_html}{rec_html}'
        f'</div>',
        unsafe_allow_html=True
    )

# ── AVISOS DE LLUVIA (van debajo del mapa) ────────────────────────────────────
def mostrar_avisos_lluvia(sendero_mojado, tramos_bloqueados):
    """Muestra avisos de clima y tramos bloqueados — se renderizan bajo el mapa."""

    if sendero_mojado:
        _renderizar_aviso("lluvia",
            "🌧️ Sendero Mojado — Condiciones Adversas",
            [
                "El terreno mojado aumenta el tiempo de recorrido en un 30% y la dificultad en un 50%.",
                "Los tramos de alta dificultad se vuelven extremadamente peligrosos bajo lluvia.",
                "Dijkstra ha recalculado la ruta evitando los tramos inaccesibles.",
            ],
            "🎒 Se recomienda llevar:",
            [
                "🥾 Botas de senderismo impermeables con buena tracción",
                "🧥 Impermeable o poncho de lluvia",
                "🦯 Bastones de trekking para mayor estabilidad",
                "🔦 Linterna (la visibilidad puede reducirse)",
                "🩹 Botiquín de primeros auxilios básico",
                "📱 Teléfono con batería cargada y GPS descargado",
                "💧 Agua extra (el esfuerzo aumenta con terreno mojado)",
            ]
        )

    if tramos_bloqueados:
        nombres = ", ".join([f"{t[0]}→{t[1]}" for t in tramos_bloqueados])
        _renderizar_aviso("peligro",
            f"⛔ {len(tramos_bloqueados)} Tramo(s) Inaccesible(s) por Lluvia",
            [f"Los siguientes tramos han sido bloqueados por riesgo extremo: {nombres}",
             "Dijkstra buscó automáticamente una ruta alternativa segura."]
        )

# ── AVISOS DE TIPO DE RUTA (van en el panel) ──────────────────────────────────
def mostrar_avisos_ruta(tipo_ruta):
    """Muestra recomendaciones según el tipo de ruta — se renderizan en el panel."""

    if "segura" in tipo_ruta:
        _renderizar_aviso("ok",
            f"{tipo_ruta} — Caminos cómodos y accesibles",
            ["Se priorizan tramos de baja dificultad. Los tramos exigentes han sido penalizados fuertemente.",
             "Ideal para familias, principiantes o personas con movilidad reducida."],
            "💡 Recomendaciones:",
            [
                "🥤 Llevar al menos 1.5 litros de agua",
                "🧴 Protector solar y repelente de insectos",
                "👟 Calzado cómodo con suela antideslizante",
                "🍫 Snacks energéticos para mantener el ritmo",
            ]
        )
    elif "rápida" in tipo_ruta:
        _renderizar_aviso("moderado",
            f"{tipo_ruta} — Menor tiempo de recorrido",
            ["Dijkstra minimizó el tiempo total. El camino puede incluir tramos de dificultad media.",
             "Se recomienda buena condición física básica para mantener el ritmo."],
            "💡 Recomendaciones:",
            [
                "🥾 Calzado con buen soporte de tobillo",
                "💧 Al menos 2 litros de agua",
                "🧢 Gorra para protección solar",
                "⌚ Monitorea tu ritmo para llegar en el tiempo estimado",
            ]
        )
    elif "corta" in tipo_ruta:
        _renderizar_aviso("moderado",
            f"{tipo_ruta} — Menor distancia recorrida",
            ["Dijkstra minimizó los metros totales. Esta ruta puede incluir tramos técnicos o empinados.",
             "La ruta más corta no siempre es la más fácil — verifica el índice de esfuerzo."],
            "💡 Recomendaciones:",
            [
                "🥾 Botas de senderismo con buen soporte",
                "💧 Al menos 2 litros de agua",
                "🦯 Considera bastones si hay tramos de alta dificultad",
                "⚠️ Presta atención al índice de esfuerzo antes de salir",
            ]
        )
    elif "balanceada" in tipo_ruta:
        _renderizar_aviso("ok",
            f"{tipo_ruta} — Equilibrio entre distancia, tiempo y dificultad",
            ["Dijkstra buscó el mejor compromiso entre los tres factores.",
             "Recomendada para la primera visita al sendero o cuando no hay una prioridad clara."],
            "💡 Recomendaciones generales:",
            [
                "🥾 Botas de senderismo con soporte de tobillo",
                "💧 Al menos 2 litros de agua",
                "🍌 Alimentos energéticos para recorridos medianos",
                "🧢 Protección solar",
            ]
        )

# ── CALCULAR RUTA ───────────────────────────────────────────────────────────
if calcular:
    G = nx.Graph()
    tramos_bloqueados = []   # tramos excluidos por lluvia + dificultad extrema

    for conexion in data["conexiones"]:
        distancia  = conexion["distancia"]
        tiempo     = conexion["tiempo"]
        dificultad = conexion["dificultad"]

        # ── Bloqueo de tramos inaccesibles bajo lluvia ──
        # Si la dificultad base ya es máxima Y llueve → tramo completamente inaccesible
        if sendero_mojado and dificultad >= UMBRAL_BLOQUEO_LLUVIA:
            tramos_bloqueados.append((conexion["origen"], conexion["destino"], dificultad))
            continue  # NO agregar esta arista al grafo → Dijkstra no puede usarla

        # ── Ajuste por lluvia (tramos que sí son accesibles) ──
        if sendero_mojado:
            tiempo     *= 1.3
            dificultad *= 1.5
        dificultad = min(dificultad, 5)
        if sendero_mojado and dificultad >= 5:
            tiempo *= 2

        # ── Mapeo de tipo de ruta → criterio + penalización ──────────────────
        MAPA_RUTA = {
            "🟢 Ruta más segura":   ("dificultad", "Fácil"),
            "⚡ Ruta más rápida":   ("tiempo",     "Moderado"),
            "📏 Ruta más corta":    ("distancia",  "Moderado"),
            "⚖️ Ruta balanceada":   ("balanceado", "Moderado"),
        }
        criterio_interno, nivel_ruta = MAPA_RUTA[criterio]

        # ── Ajuste por nivel_ruta ──
        if nivel_ruta == "Fácil":
            penalizacion = dificultad ** 2.5
            tiempo       = tiempo * (1 + (dificultad - 1) * 0.4)
            distancia    = distancia * (1 + (dificultad - 1) * 0.2)
        elif nivel_ruta == "Moderado":
            penalizacion = dificultad ** 1.5
            tiempo       = tiempo * (1 + (dificultad - 1) * 0.15)
            distancia    = distancia * (1 + (dificultad - 1) * 0.05)
        else:
            penalizacion = 1 / (dificultad + 0.5)
            tiempo       = tiempo * 0.85
            distancia    = distancia

        peso_balanceado = (distancia * 1.0) + (tiempo * 0.5) + (dificultad * penalizacion)

        G.add_edge(
            conexion["origen"], conexion["destino"],
            distancia=distancia,
            tiempo=tiempo,
            dificultad=dificultad,
            balanceado=peso_balanceado
        )

    try:
        weight_key = "balanceado" if criterio_interno == "balanceado" else criterio_interno
        ruta = nx.dijkstra_path(G, inicio, fin, weight=weight_key)

        distancia_total  = sum(G[u][v]["distancia"]  for u, v in zip(ruta, ruta[1:]))
        tiempo_total     = sum(G[u][v]["tiempo"]     for u, v in zip(ruta, ruta[1:]))
        dificultad_total = sum(G[u][v]["dificultad"] for u, v in zip(ruta, ruta[1:]))
        esfuerzo         = (distancia_total * 1.2) + (dificultad_total * 3)

        if esfuerzo < 10:
            nivel_esfuerzo = ("🟢 Fácil", "badge-facil")
        elif esfuerzo < 20:
            nivel_esfuerzo = ("🟡 Moderado", "badge-moderado")
        else:
            nivel_esfuerzo = ("🔴 Intenso", "badge-intenso")

        st.session_state.ruta_resultado = {
            "ruta":              ruta,
            "distancia_total":   distancia_total,
            "tiempo_total":      tiempo_total,
            "dificultad_total":  dificultad_total,
            "esfuerzo":          esfuerzo,
            "nivel_esfuerzo":    nivel_esfuerzo,
            "inicio":            inicio,
            "fin":               fin,
            "tramos_bloqueados": tramos_bloqueados,
            "sendero_mojado":    sendero_mojado,
            "tipo_ruta":         criterio,       # nombre visible: "🟢 Ruta más segura" etc.
            "nivel_ruta":        nivel_ruta,     # interno: "Fácil", "Moderado", "Difícil"
        }

    except nx.NetworkXNoPath:
        st.session_state.ruta_resultado = None
        # Mostrar qué tramos fueron bloqueados para explicar por qué no hay ruta
        with panel:
            st.error("⛔ No existe ruta accesible entre los nodos seleccionados.")
            if tramos_bloqueados:
                st.markdown(
                    '<div class="aviso-card aviso-peligro">'
                    '<span class="aviso-titulo">Los siguientes tramos fueron bloqueados por lluvia extrema:</span>'
                    + "".join([f'<div class="tramo-bloqueado">🚫 Tramo {o}→{d} (dificultad original: {dif}/5 — inaccesible bajo lluvia)</div>'
                               for o, d, dif in tramos_bloqueados])
                    + '<div style="margin-top:8px;font-size:0.8rem;opacity:0.8">💡 Intenta con un sendero diferente o desactiva el modo lluvia.</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

# ── RENDERIZAR MAPA ──────────────────────────────────────────────────────────
res = st.session_state.ruta_resultado

with col_mapa:
    if res:
        titulo = f"{mapa_seleccionado}  ·  {res['inicio']} → {res['fin']}  ·  {' → '.join(res['ruta'])}"
        if res["tramos_bloqueados"]:
            titulo += "  ·  ⚠️ tramos bloqueados por lluvia"
        fig = dibujar_mapa(imagen, nodos_mapa, res["inicio"], res["fin"],
                           ruta=res["ruta"], titulo=titulo,
                           tramos_bloqueados=res["tramos_bloqueados"])
    else:
        titulo = f"{mapa_seleccionado}  ·  Selecciona inicio y destino"
        fig = dibujar_mapa(imagen, nodos_mapa, inicio, fin, titulo=titulo)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # ── Avisos de lluvia — debajo del mapa ──────────────────────────────────
    if res and (res["sendero_mojado"] or res["tramos_bloqueados"]):
        st.markdown("---")
        mostrar_avisos_lluvia(res["sendero_mojado"], res["tramos_bloqueados"])

    # ── Aviso previo sin calcular: toggle activo pero sin ruta aún ──────────
    elif not res and sendero_mojado:
        st.markdown("---")
        mostrar_avisos_lluvia(sendero_mojado=True, tramos_bloqueados=[])

# ── RESULTADOS ───────────────────────────────────────────────────────────────
if res:
    with panel:
        # ── Aviso de tipo de ruta — en el panel ─────────────────────────────
        st.markdown("---")
        mostrar_avisos_ruta(res["tipo_ruta"])
        st.markdown("---")

        label, css_class = res["nivel_esfuerzo"]
        st.markdown(
            f'<div style="text-align:center; margin-bottom:1rem;">'
            f'<span class="esfuerzo-badge {css_class}">{label}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.success(f"**{' → '.join(res['ruta'])}**")

        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)
        with m1: st.metric("📏 Distancia", f"{res['distancia_total']}")
        with m2: st.metric("⏱ Tiempo",    f"{res['tiempo_total']:.1f} min")
        with m3: st.metric("⛰ Dificultad",f"{res['dificultad_total']:.1f}")
        with m4: st.metric("🔥 Esfuerzo", f"{res['esfuerzo']:.1f}")

        st.markdown("---")
        st.markdown(
            '<p style="font-size:0.7rem; letter-spacing:0.15em; color:#4ade80; text-transform:uppercase; margin-bottom:0.8rem;">Ruta paso a paso</p>',
            unsafe_allow_html=True
        )

        for i, nodo in enumerate(res["ruta"]):
            if i == 0:
                icono, texto = "🚩", f"Inicio en <strong>{nodo}</strong>"
            elif i == len(res["ruta"]) - 1:
                icono, texto = "🏁", f"Llegada a <strong>{nodo}</strong>"
            else:
                icono, texto = "➡️", f"Continuar a <strong>{nodo}</strong>"

            st.markdown(
                f'<div class="step-box">'
                f'<span class="step-icon">{icono}</span>'
                f'<span>{texto}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

# ── FAUNA Y FLORA ─────────────────────────────────────────────────────────────
if res:
    datos = FAUNA_FLORA.get(mapa_seleccionado, {})
    fauna = datos.get("fauna", [])
    flora = datos.get("flora", [])

    def especie_html(e):
        label = "Ave" if e["tag"] == "tag-ave" else ("Flora" if e["tag"] == "tag-flora" else "Fauna")
        return (
            f'<div class="especie-card">'
            f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
            f'<span class="especie-emoji">{e["emoji"]}</span>'
            f'<div>'
            f'<div class="especie-nombre">{e["nombre"]}</div>'
            f'<div class="especie-nombre-cientifico">{e["cientifico"]}</div>'
            f'</div></div>'
            f'<div class="especie-desc">{e["desc"]}</div>'
            f'<span class="especie-tag {e["tag"]}">{label}</span>'
            f'</div>'
        )

    fauna_html = "".join([especie_html(e) for e in fauna])
    flora_html = "".join([especie_html(e) for e in flora])

    with col_fauna:
        st.markdown(
            f'<div class="fauna-flora-panel">'

            # ── Título general ──
            f'<div class="fauna-flora-titulo">🌿 Fauna & Flora</div>'
            f'<div class="fauna-flora-sub">{mapa_seleccionado} · Avistamientos frecuentes</div>'

            # ── Grid de dos columnas ──
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">'

            # Columna fauna
            f'<div>'
            f'<div class="seccion-label">🦜 Fauna</div>'
            f'{fauna_html}'
            f'</div>'

            # Columna flora
            f'<div>'
            f'<div class="seccion-label">🌺 Flora</div>'
            f'{flora_html}'
            f'</div>'

            f'</div>'  # cierre grid
            f'</div>', # cierre panel-+
            unsafe_allow_html=True
        )

        #streamlit run Codigo_Inicial.py
