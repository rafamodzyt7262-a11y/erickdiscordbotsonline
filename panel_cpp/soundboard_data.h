#pragma once
#include <string>
#include <vector>

struct SoundItem {
    const char* id;
    const char* name;
    const char* category;
    const char* emoji;
    const char* phrase;
};

static const char* g_SoundCategories[] = {
    "Todos",
    "Free Fire Voces & Armas",
    "Memes Virales & Efectos",
    "Gaming & Esports",
    "Reacciones y Trolls"
};

static const SoundItem g_SoundList[] = {
    // 1. Free Fire Voces Oficiales (Donato, Zelika, Hackers, Gang, Booyah)
    { "ff_donato_headshot", "Donato: Headshot Pa Tu Casa", "Free Fire Voces & Armas", "🎯", "Headshot pa tu casa crack de parte del Donato!" },
    { "ff_zelika_insano", "Zelika: Racha Insana 360", "Free Fire Voces & Armas", "🔥", "Que onda cracks aqui Zelika en racha insana con movimiento 360!" },
    { "ff_hacker_aimbot", "Hacker: Aimbot Todo Rojo", "Free Fire Voces & Armas", "🤖", "Aimbot activado todo rojo a la cabeza sin retroceso!" },
    { "ff_gang_ff", "El Gang de Free Fire Dominando", "Free Fire Voces & Armas", "👑", "El Gang de Free Fire dominando la partida en Bermuda!" },
    { "ff_booyah_epico", "Booyah Victoria Magistral", "Free Fire Voces & Armas", "🏆", "Booyah victoria magistral en Bermuda partida ganada!" },
    { "ff_gloo_360", "Pared Gloo 360 Modo Flash", "Free Fire Voces & Armas", "🛡️", "Pared Gloo a 360 grados cubreme manco!" },
    { "ff_mp40_cobra_v", "MP40 Cobra Rafaga Letal", "Free Fire Voces & Armas", "🐍", "Rafaga letal de MP40 Cobra al pecho!" },
    { "ff_first_blood", "Primera Sangre!", "Free Fire Voces & Armas", "🩸", "¡PRIMERA SANGRE! El enemigo ha caido." },
    { "ff_double_kill", "Doble Asesinato", "Free Fire Voces & Armas", "🔥", "¡DOBLE ASESINATO! Racha letal activada." },
    { "ff_triple_kill", "Triple Asesinato", "Free Fire Voces & Armas", "⚡", "¡TRIPLE ASESINATO! Dominando la zona." },
    { "ff_quadra_kill", "Cuadruple Asesinato", "Free Fire Voces & Armas", "💥", "¡CUADRUPLE ASESINATO! Escuadra enemiga aniquilada." },
    { "ff_booyah", "BOOYAH!", "Free Fire Voces & Armas", "👑", "¡¡¡BOOYAH!!! Victoria Magistral en Free Fire." },
    { "ff_awm_headshot", "AWM Headshot", "Free Fire Voces & Armas", "🎯", "PUM! Disparo critico a la cabeza con AWM." },
    { "ff_mp40_cobra", "MP40 Cobra Rafaga", "Free Fire Voces & Armas", "🐍", "Trrrrrrr! Rafaga letal de MP40 Evolutiva al pecho." },
    { "ff_m1887_oneshot", "M1887 Dos Tiros One-Shot", "Free Fire Voces & Armas", "🔫", "BAM BAM! Doble cañonazo a quemarropa." },
    { "ff_gloo_wall", "Pared Gloo Desplegada", "Free Fire Voces & Armas", "🛡️", "Klang! Pared Gloo colocada a 360 grados." },
    { "ff_alok_drop", "Alok Drop The Beat", "Free Fire Voces & Armas", "🎵", "Drop the beat! Aura de velocidad y curacion activa." },
    { "ff_chrono_shield", "Chrono Escudo Tunel", "Free Fire Voces & Armas", "🔮", "Campo de fuerza activado! Balas bloqueadas." },
    { "ff_wukong_bush", "Wukong Camuflaje Arbusto", "Free Fire Voces & Armas", "🌿", "Shhh... Transformacion en arbusto ninja." },
    { "ff_airdrop", "Airdrop Cayendo", "Free Fire Voces & Armas", "📦", "Avion pasando! Caja de suministros con Groza lista." },
    { "ff_danger_zone", "Zona de Peligro Bombardeo", "Free Fire Voces & Armas", "💣", "Cuidado! Bombardeo aereo en curso en tu zona." },
    { "ff_revive_me", "Ayuda! Vengan por mi!", "Free Fire Voces & Armas", "🚑", "Me tumbaron! Vengan a revivirme detras de la roca!" },
    { "ff_medkit", "Curando Botiquin", "Free Fire Voces & Armas", "🩹", "Usando botiquin... 4 segundos para full vida." },
    { "ff_enemy_spotted", "Enemigo a la Vista!", "Free Fire Voces & Armas", "👀", "Enemigo marcado a 150 metros en la casa L." },
    { "ff_safe_zone", "Zona Segura Reduciendose", "Free Fire Voces & Armas", "🏃", "Corre a zona! El gas de la zona segura avanza." },
    { "ff_kelly_dash", "Kelly Sprint Veloz", "Free Fire Voces & Armas", "👟", "Velocidad maxima al 120%." },
    { "ff_hayato_bushido", "Hayato Espiritu Bushido", "Free Fire Voces & Armas", "⚔️", "Penetracion de armadura duplicada al tener poca vida." },

    // 2. Memes Virales & Efectos
    { "meme_gigachad", "GigaChad Sigma Phonk", "Memes Virales & Efectos", "🗿", "Can you feel my heart... Chad theme activado." },
    { "meme_vine_boom", "Vine Boom Impacto", "Memes Virales & Efectos", "💥", "BOOOOOM! Sonido clasico de shock." },
    { "meme_bruh", "Bruh Sound Effect #2", "Memes Virales & Efectos", "💀", "BRUH... Momento epico de decepcion." },
    { "meme_airhorn", "Airhorn Trap Dubstep", "Memes Virales & Efectos", "📢", "Bwa bwa bwa bwaaaaa! Sirena de MLG." },
    { "meme_coffin", "Coffin Dance Astronomia", "Memes Virales & Efectos", "⚰️", "Los hombres del ataued bailando en el servidor." },
    { "meme_emotional", "Emotional Damage!", "Memes Virales & Efectos", "💔", "EMOTIONAL DAMAGE! Daño psicologico infligido." },
    { "meme_metal_pipe", "Metal Pipe Falling 4K", "Memes Virales & Efectos", "🔩", "Klanggg crrshhhh! Tubo metalico cayendo al suelo." },
    { "meme_siuuu", "Siuuu Cristiano Ronaldo", "Memes Virales & Efectos", "⚽", "SIIIIUUUUUUU! Golazo legendario." },
    { "meme_gta_sa", "Ah Shit Here We Go Again", "Memes Virales & Efectos", "🚴", "CJ volviendo a Grove Street." },
    { "meme_tacos", "Tacos de Tripa", "Memes Virales & Efectos", "🌮", "Deme cinco de tripa bien dorada con todo jefe!" },
    { "meme_roblox_oof", "Roblox Classic Oof", "Memes Virales & Efectos", "🧱", "OOF! Personaje desarmado en piezas." },
    { "meme_run", "Run! Dun dun dun dun", "Memes Virales & Efectos", "🏃‍♂️", "RUN! Corre por tu vida que te persiguen." },
    { "meme_fbi", "FBI Open Up!", "Memes Virales & Efectos", "🚨", "FBI OPEN UP! Puerta derribada." },
    { "meme_windows_xp", "Windows XP Earrape", "Memes Virales & Efectos", "💻", "Sonido de inicio de Windows XP a 200dB." },
    { "meme_trololo", "Eduard Khil Trololo", "Memes Virales & Efectos", "🎩", "Trololololol hahahaha trololo." },

    // 3. Gaming & Esports
    { "game_cs_bomb", "The Bomb Has Been Planted", "Gaming & Esports", "⏱️", "Terrorists win. La bomba ha sido plantada en B." },
    { "game_cod_hitmarker", "Call of Duty Hitmarker", "Gaming & Esports", "🎯", "Tick-tick-tick! Sonido satisfactorio de hitmarker." },
    { "game_halo_announcer", "Double Kill Halo", "Gaming & Esports", "🪐", "Voz epica del anunciador de Halo." },
    { "game_minecraft_lvl", "Minecraft Level Up Ding", "Gaming & Esports", "💎", "Ding ding ding! Nivel de experiencia subido." },
    { "game_gta_wasted", "GTA Wasted / Eliminado", "Gaming & Esports", "🪦", "Pantalla gris y sonido clasico de WASTED." },
    { "game_zelda_chest", "Zelda Cofre Tesoro Secreto", "Gaming & Esports", "🗝️", "Da-da-da-DAAAA! Objeto legendario obtenido." },
    { "game_mario_coin", "Super Mario Moneda 1-Up", "Gaming & Esports", "🍄", "Tinnggg! Vida extra obtenida." }
};
