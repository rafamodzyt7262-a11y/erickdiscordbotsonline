#pragma once
#include <vector>
#include <string>

struct StickerItem {
    const char* id;
    const char* name;
    const char* category;
    const char* url;
};

static const char* g_StickerCategories[] = {
    "Todos",
    "Pepe & Wojaks",
    "GigaChad & Sigma",
    "Cheems & Doge",
    "Gatos & Memes Tiernos",
    "Karely Ruiz HD",
    "Gaming & Streamers",
    "Clasicos del Internet & Troll",
    "Anime & Reacciones",
    "Emojis Gigantes HD",
    "Sonrisas & Caras Virales"
};

static const StickerItem g_StickersList[] = {
    // 1. Pepe & Wojaks
    { "pepe_hype", "Pepe Hype", "Pepe & Wojaks", "https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif" },
    { "pepe_sad", "Pepe Sad", "Pepe & Wojaks", "https://media.giphy.com/media/7SF5scGB2AFrgsXP63/giphy.gif" },
    { "pepe_happy", "Pepe Happy", "Pepe & Wojaks", "https://media.giphy.com/media/eHpWHuEUxHIre/giphy.gif" },
    { "pepe_clown", "Pepe Payaso", "Pepe & Wojaks", "https://media.giphy.com/media/rxy55jHaig164/giphy.gif" },
    { "pepe_hacker", "Pepe Hacker", "Pepe & Wojaks", "https://media.giphy.com/media/QNFhOolVeCzPQ2EBR5/giphy.gif" },
    { "pepe_coffee", "Pepe Cafecito", "Pepe & Wojaks", "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif" },
    { "pepe_smug", "Pepe Smug", "Pepe & Wojaks", "https://media.giphy.com/media/cJMmZY7jSCtwN420Yl/giphy.gif" },
    { "pepe_dance", "Pepe Baile", "Pepe & Wojaks", "https://media.giphy.com/media/blSTtZehjAZ8I/giphy.gif" },
    { "pepe_rich", "Pepe Millonario", "Pepe & Wojaks", "https://media.giphy.com/media/67ThRZlYBvibtdF9JH/giphy.gif" },
    { "pepe_comiendo", "Pepe Popcorn", "Pepe & Wojaks", "https://media.giphy.com/media/t3kWZZ0OOwb96/giphy.gif" },
    { "wojak_pointing", "Soyjak Senalando", "Pepe & Wojaks", "https://i.imgflip.com/4a034w.png" },
    { "wojak_doomer", "Wojak Doomer", "Pepe & Wojaks", "https://i.imgflip.com/3r2q8n.png" },
    { "wojak_crying", "Wojak Llorando", "Pepe & Wojaks", "https://i.imgflip.com/1otk96.jpg" },
    { "wojak_chad", "Yes Chad", "Pepe & Wojaks", "https://i.imgflip.com/3oevdk.jpg" },
    { "wojak_mask", "Wojak Mascara Sonriendo", "Pepe & Wojaks", "https://i.imgflip.com/49eg1t.jpg" },

    // 2. GigaChad & Sigma
    { "gigachad_smile", "GigaChad Sonrisa", "GigaChad & Sigma", "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif" },
    { "gigachad_walk", "GigaChad Caminata", "GigaChad & Sigma", "https://media.giphy.com/media/kwcRp24Wz4lZm/giphy.gif" },
    { "bateman_card", "Bateman Business Card", "GigaChad & Sigma", "https://media.giphy.com/media/3YuR4vIZlTRxqN8qJL/giphy.gif" },
    { "walter_white_danger", "I Am The Danger", "GigaChad & Sigma", "https://media.giphy.com/media/3ohc11Uljkf3lQ0WCE/giphy.gif" },
    { "gus_fring_adjust", "Gus Fring Corbata", "GigaChad & Sigma", "https://media.giphy.com/media/WbDhQijOJ5TCMQPNJK/giphy.gif" },
    { "saul_goodman_3d", "Saul Goodman 3D", "GigaChad & Sigma", "https://media.giphy.com/media/8XEQRJsRWcTgA/giphy.gif" },
    { "homelander_smile", "Homelander Sonrisa", "GigaChad & Sigma", "https://media.giphy.com/media/W3H7yzvQowNSy124C8/giphy.gif" },
    { "rock_eyebrow", "The Rock Ceja Levantada", "GigaChad & Sigma", "https://media.giphy.com/media/26ghbWoXv3G6ypo8o/giphy.gif" },
    { "dicaprio_toast", "DiCaprio Brindis Gatsby", "GigaChad & Sigma", "https://media.giphy.com/media/GCLlQnV7dXZ2E/giphy.gif" },

    // 3. Cheems & Doge
    { "cheems_bonk", "Cheems Bonk", "Cheems & Doge", "https://media.giphy.com/media/qs427OHakAH238b9xD/giphy.gif" },
    { "cheems_burger", "Cheems Hamburmgesa", "Cheems & Doge", "https://i.imgflip.com/43wwhc.jpg" },
    { "buff_doge", "Buff Doge Fuerte", "Cheems & Doge", "https://i.imgflip.com/45v7t9.png" },
    { "doge_classic", "Doge Original Wow", "Cheems & Doge", "https://i.imgflip.com/4t0m5.jpg" },
    { "doge_glasses", "Doge Lentes Thug Life", "Cheems & Doge", "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif" },
    { "cheems_fire", "Cheems This is Fine", "Cheems & Doge", "https://media.giphy.com/media/9M5jK4GXmD5o1irGrF/giphy.gif" },

    // 4. Gatos & Memes Tiernos
    { "pop_cat", "Pop Cat Abriendo Boca", "Gatos & Memes Tiernos", "https://media.giphy.com/media/S6VGjvmFRu5QgxWsul/giphy.gif" },
    { "bongo_cat", "Bongo Cat Tambores", "Gatos & Memes Tiernos", "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" },
    { "smug_cat", "Gato Sonrisa Burlona", "Gatos & Memes Tiernos", "https://i.imgflip.com/345v97.jpg" },
    { "crying_cat", "Gato Llorando Ojos Grandes", "Gatos & Memes Tiernos", "https://i.imgflip.com/265j72.jpg"},
    { "huh_cat", "Gato Diciendo HUH?", "Gatos & Memes Tiernos", "https://media.giphy.com/media/GRkye9457EK2Toc9Jv/giphy.gif" },
    { "cat_vibe", "Gato Asintiendo con Musica", "Gatos & Memes Tiernos", "https://media.giphy.com/media/GeimqsH0TLDt4tScGw/giphy.gif" },

    // 5. Karely Ruiz HD
    { "karely_avatar", "Karely Ruiz HD Perfil", "Karely Ruiz HD", "https://media.giphy.com/media/l41lFw057lAJQMwg0/giphy.gif" },
    { "karely_saludo", "Karely Saludo Bonito", "Karely Ruiz HD", "https://media.giphy.com/media/3o7TKMt1VVNkHV2PaE/giphy.gif" },
    { "karely_beso", "Karely Mandando Beso", "Karely Ruiz HD", "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif" },
    { "karely_sonrisa", "Karely Sonrisa Radiante", "Karely Ruiz HD", "https://media.giphy.com/media/l41lFw057lAJQMwg0/giphy.gif" },
    { "karely_queen", "Karely Corona de Reina", "Karely Ruiz HD", "https://media.giphy.com/media/l41lFw057lAJQMwg0/giphy.gif" },

    // 6. Gaming & Streamers
    { "gta_here_we_go", "CJ Ah Shit Here We Go Again", "Gaming & Streamers", "https://media.giphy.com/media/6ILjOfJ1oL7NAk9qae/giphy.gif" },
    { "minecraft_creeper", "Minecraft Creeper Aww Man", "Gaming & Streamers", "https://media.giphy.com/media/10AoZDUmPrhNVC/giphy.gif" },
    { "among_us_sus", "Among Us Impostor Sus", "Gaming & Streamers", "https://media.giphy.com/media/RtdRhc7TxBxB0YAsK6/giphy.gif" },
    { "press_f", "Press F to Pay Respects", "Gaming & Streamers", "https://i.imgflip.com/26jxvz.jpg" },
    { "dark_souls_died", "Dark Souls YOU DIED", "Gaming & Streamers", "https://media.giphy.com/media/TbONGqAdpTWQW3Hz5V/giphy.gif" },
    { "cyberpunk_keanu", "Keanu Wake Up Samurai", "Gaming & Streamers", "https://media.giphy.com/media/fA7rLtaJ5HxUFYL5D0/giphy.gif" },

    // 7. Clasicos del Internet & Troll
    { "trollface", "Trollface Sonrisa Problem?", "Clasicos del Internet & Troll", "https://i.imgflip.com/4t0m5.jpg" },
    { "rickroll", "Rick Astley Never Gonna Give You Up", "Clasicos del Internet & Troll", "https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif" },
    { "this_is_fine", "This is Fine Perro en Fuego", "Clasicos del Internet & Troll", "https://media.giphy.com/media/9M5jK4GXmD5o1irGrF/giphy.gif" },
    { "disaster_girl", "Nina Sonriendo con Casa Quemada", "Clasicos del Internet & Troll", "https://i.imgflip.com/23ls.jpg" },
    { "stonks", "Hombre Maniqui STONKS", "Clasicos del Internet & Troll", "https://i.imgflip.com/31hg56.png" },
    { "coffin_dance", "Bailarines del Ataud Ghana", "Clasicos del Internet & Troll", "https://media.giphy.com/media/j6ZlX8ghxNFRknObVk/giphy.gif" },

    // 8. Anime & Reacciones
    { "anya_heh", "Anya Forger Sonrisa Heh", "Anime & Reacciones", "https://media.giphy.com/media/FWAcpJsFT9mVRv0e7a/giphy.gif" },
    { "zero_two_dance", "Zero Two Baile Viral", "Anime & Reacciones", "https://media.giphy.com/media/pCO5tKdP22RC8/giphy.gif" },
    { "goku_ultra", "Goku Ultra Instinto Aura", "Anime & Reacciones", "https://media.giphy.com/media/19JSJ5ucu91R5D7a3w/giphy.gif" },
    { "saitama_ok", "Saitama One Punch Man OK", "Anime & Reacciones", "https://i.imgflip.com/w1uun.jpg" },
    { "dio_da", "Kono DIO Da!", "Anime & Reacciones", "https://media.giphy.com/media/kiJEGxbplHfT5zkCDJ/giphy.gif" },

    // 9. Emojis Gigantes HD
    { "skull_3d", "Calavera 3D HD", "Emojis Gigantes HD", "https://media.giphy.com/media/vjjCsx3izfRSq4CJcp/giphy.gif" },
    { "fire_flame", "Fuego Ardiente HD", "Emojis Gigantes HD", "https://media.giphy.com/media/Lopx9eUi34rbq/giphy.gif" },
    { "hundred_points", "100 Puntos Oficial", "Emojis Gigantes HD", "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif" },
    { "clown_face", "Cara de Payaso HD", "Emojis Gigantes HD", "https://media.giphy.com/media/rxy55jHaig164/giphy.gif" },
    { "crying_laughing", "Llorando de Risa HD", "Emojis Gigantes HD", "https://media.giphy.com/media/10JhviFuU2gWD6/giphy.gif" },
    { "rocket_launch", "Cohete Despegando HD", "Emojis Gigantes HD", "https://media.giphy.com/media/mi6ZXUCiqaC64/giphy.gif" },

    // 10. Sonrisas & Caras Virales
    { "kermit_tea", "Rana Rene Tomando Te", "Sonrisas & Caras Virales", "https://media.giphy.com/media/3o85xGocUH8RYoDKKs/giphy.gif" },
    { "elmo_fire", "Elmo en Llamas Infierno", "Sonrisas & Caras Virales", "https://media.giphy.com/media/yr7n0u3qzO9nG/giphy.gif" },
    { "shaq_shimmy", "Shaquille O'Neal Moviendo Hombros", "Sonrisas & Caras Virales", "https://media.giphy.com/media/UO5elnTqo4vSg/giphy.gif" },
    { "shut_up_money", "Fry Shut Up and Take My Money", "Sonrisas & Caras Virales", "https://media.giphy.com/media/sDcfxFDozb3bO/giphy.gif" },
    { "homer_bushes", "Homero Escondiendose en Arbustos", "Sonrisas & Caras Virales", "https://media.giphy.com/media/COYGe9rZvfiaQ/giphy.gif" }
};
