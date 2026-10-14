# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
"""
Base de Datos de 500 Voces y Audios de Free Fire, The Donato, Zelika, Hackers y El Gang
Servidor SHADOW BLOCK • rafamodzyt
"""

CATEGORIES = [
    {"id": "donato", "name": "🎯 The Donato (1-100)", "range": (1, 100)},
    {"id": "zelika", "name": "🔥 Zelika Insano (101-200)", "range": (101, 200)},
    {"id": "hackers", "name": "🤖 Hackers & Aimbot (201-300)", "range": (201, 300)},
    {"id": "gang", "name": "👑 El Gang de Free Fire (301-400)", "range": (301, 400)},
    {"id": "booyah", "name": "🏆 Booyah & Armas (401-500)", "range": (401, 500)}
]

VOICE_TEMPLATES = {
    "donato": [
        "Headshot pa tu casa crack de parte del Donato",
        "Watafac pero que tiro le meti a ese manco",
        "Risa demente del Donato jajaja se fue al lobby",
        "No te lo puedo creer hermano que rusheo tan epico",
        "Manco a mimir que aca manda el Donato",
        "Dios mio que disparo a la cabeza con la M1887",
        "Se asomo y lo mande al lobby de un toque",
        "Tranquilos cracks que esta partida la ganamos nosotros",
        "Miren esa jugada insana ni en sus sueños la hacen",
        "Pa tu casa manco que aca no hay piedad"
    ],
    "zelika": [
        "Que onda cracks aqui Zelika en racha insana",
        "Movimiento insano en 360 grados pared gloo al instante",
        "Pared gloo agachado modo flash no me pueden tocar",
        "Todo rojo a la cabeza ningun tiro amarillo",
        "Dominando el mapa Bermuda como un verdadero insano",
        "Miren como rompo ese chaleco en un segundo",
        "Rusheando a cuatro mancos al mismo tiempo",
        "Zelika en su prime dando todo capa con MP40",
        "Agarrate que aca llego la pesadilla de las escuadras",
        "Un movimiento en zigzag y ya quedaron eliminados"
    ],
    "hackers": [
        "Aimbot activado todo rojo a la cabeza automaticamente",
        "Bypass antiban confirmado indetectable en el servidor",
        "Vuelo y teletransporte directo arriba de la garita",
        "Mira pegada al casco no fallo ni una sola bala",
        "Antena y radar de escuadras viendo a traves de paredes",
        "Velocidad aumentada modo flash por todo el mapa",
        "Bala magica atravesando arboles y piedras",
        "Regedit y macro activados al maximo nivel",
        "Todo capa sin retroceso la mira nunca se mueve",
        "Protocolo hacker iniciado borrando a la escuadra enemiga"
    ],
    "gang": [
        "El Gang de Free Fire dominando toda la partida",
        "Rushea por la izquierda que yo entro por la ventana",
        "Tirame botiquines y balas AR que no tengo nada",
        "Granada cocinada adentro de casa L los tenemos atrapados",
        "Cubranme que estoy reviviendo al companero rapido",
        "Aca somos la escuadra invicta nadie nos tumba",
        "Caemos en Clock Tower a darnos con todo",
        "El Gang activo controlando la zona segura",
        "Pongan tres paredes gloo y aguanten la posicion",
        "Coordinacion perfecta de escuadra victoria asegurada"
    ],
    "booyah": [
        "Booyah victoria magistral en Bermuda partida ganada",
        "Rafaga letal de MP40 Cobra quemando chalecos",
        "M1887 un solo tiro y a mimir al piso",
        "Disparo certero de AWM a 500 metros sin fallo",
        "Pared gloo salvadora en el ultimo segundo de vida",
        "Groza con chip nivel tres destrozando enemigos",
        "Doble escopeta y rusheo suicida para ganar",
        "Ultima zona cerrandose y nos llevamos el Booyah",
        "Nivel heroico alcanzado con honores en clasificatoria",
        "Emote de risa y trofeo en la cara del enemigo"
    ]
}

def get_voice_by_id(sound_id: int):
    """Devuelve los datos de una voz del 1 al 500."""
    sound_id = max(1, min(500, sound_id))
    
    if 1 <= sound_id <= 100:
        cat_key = "donato"
        cat_name = "🎯 The Donato"
        sub_id = sound_id
    elif 101 <= sound_id <= 200:
        cat_key = "zelika"
        cat_name = "🔥 Zelika Insano"
        sub_id = sound_id - 100
    elif 201 <= sound_id <= 300:
        cat_key = "hackers"
        cat_name = "🤖 Hackers & Aimbot"
        sub_id = sound_id - 200
    elif 301 <= sound_id <= 400:
        cat_key = "gang"
        cat_name = "👑 El Gang de Free Fire"
        sub_id = sound_id - 300
    else:
        cat_key = "booyah"
        cat_name = "🏆 Booyah & Armas"
        sub_id = sound_id - 400
        
    templates = VOICE_TEMPLATES[cat_key]
    text = templates[(sub_id - 1) % len(templates)]
    variant = (sub_id - 1) // len(templates) + 1
    
    title = f"{cat_name} #{sound_id:03d} (Variante {variant})"
    return {
        "id": sound_id,
        "title": title,
        "category": cat_name,
        "cat_key": cat_key,
        "text": f"{text} (Clip #{sound_id:03d})"
    }

def get_voices_for_category(cat_key: str, limit: int = 25):
    """Obtiene una lista de voces para menús de Discord (máximo 25 por SelectMenu)."""
    cat_info = next((c for c in CATEGORIES if c["id"] == cat_key), CATEGORIES[0])
    start, end = cat_info["range"]
    voices = []
    for sid in range(start, min(start + limit, end + 1)):
        voices.append(get_voice_by_id(sid))
    return voices

if __name__ == "__main__":
    print("Probando base de datos de 500 voces de Free Fire...")
    for tid in [1, 50, 101, 150, 201, 250, 301, 350, 401, 500]:
        v = get_voice_by_id(tid)
        print(f" - #{v['id']:03d}: {v['title']} -> '{v['text']}'")
