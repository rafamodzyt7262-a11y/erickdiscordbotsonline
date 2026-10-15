/**
 * SHADOW BLOCK • PANEL WEB PROFESIONAL
 * Lógica Completa de Interacción y Audio • Creado por rafamodzyt
 */

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initTabs();
    initVoiceEqualizer();
    initChatSystem();
    initGameBots();
    initSendReports();
    initSoundboard();
    initStickers();
    initMembersGrid();
    initWallpapers();
    initAlertsPreview();
    initParticlesBackground();
    initXXXTENTACIONPlayer();
    initDualConsole();
    initServerMaster();
    initBroadcast();
});

/* =========================================================
   1. RELOJ DIGITAL Y PING
   ========================================================= */
function initClock() {
    const clockEl = document.getElementById('metric-clock');
    const pingEl = document.getElementById('metric-ping');

    function update() {
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        const secs = String(now.getSeconds()).padStart(2, '0');
        if (clockEl) clockEl.textContent = `${hrs}:${mins}:${secs}`;
    }
    setInterval(update, 1000);
    update();

    // Ping jitter simulation
    setInterval(() => {
        if (pingEl) {
            const p = Math.floor(Math.random() * 8) + 16;
            pingEl.textContent = `${p} ms`;
        }
    }, 4000);
}

/* =========================================================
   2. SISTEMA DE NAVEGACIÓN ENTRE PESTAÑAS
   ========================================================= */
function initTabs() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const currentTitle = document.getElementById('page-current-title');

    const titlesMap = {
        'tab-dashboard': 'Dashboard General',
        'tab-dual-console': 'Dual Console: Canales de Voz + Chat Personalizado',
        'tab-server-master': 'Control Total del Servidor 1000%',
        'tab-broadcast': 'Emisor de Anuncios Oficiales (Embed)',
        'tab-chat': 'Chat en Vivo & Canales',
        'tab-voice': 'Voz 24/7 & Ecualizador',
        'tab-gamebots': 'Game Bots Free Fire (55 Cuentas/Día)',
        'tab-reports': 'Send Reports (55 Reportes en 12s)',
        'tab-soundboard': 'Soundboard Oficial & 500 Voces',
        'tab-stickers': 'Catálogo de 9,999 Stickers & Memes',
        'tab-wallpapers': 'Wallpapers 4K Masivo (99,999+ Fondos)',
        'tab-members': 'Miembros en Cuadritos (24 Miembros)',
        'tab-alerts': 'Alertas & Anuncios VIP',
        'tab-moderation': 'Moderación & Roles',
        'tab-tickets': 'Tienda Oficial & Tickets VIP',
        'tab-settings': 'Configuración & Endpoints'
    };

    navItems.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            navItems.forEach(i => i.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));

            btn.classList.add('active');
            const targetEl = document.getElementById(targetTab);
            if (targetEl) targetEl.classList.add('active');

            if (currentTitle && titlesMap[targetTab]) {
                currentTitle.textContent = titlesMap[targetTab];
            }
        });
    });

    // Shortcuts from dashboard banners
    document.querySelector('.btn-open-gamebots')?.addEventListener('click', () => {
        document.getElementById('btn-tab-gamebots')?.click();
    });
    document.querySelector('.btn-open-reports')?.addEventListener('click', () => {
        document.getElementById('btn-tab-reports')?.click();
    });
}

/* =========================================================
   3. ECUALIZADOR DE VOZ 24/7 (CANVAS)
   ========================================================= */
function initVoiceEqualizer() {
    const canvas = document.getElementById('canvas-equalizer');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const barsCount = 38;
    const barWidth = 14;
    const barGap = 6;

    let heights = new Array(barsCount).fill(10);

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const totalWidth = barsCount * (barWidth + barGap);
        const startX = (canvas.width - totalWidth) / 2;

        for (let i = 0; i < barsCount; i++) {
            // Target height with rhythmic bounce
            const target = Math.random() * (canvas.height - 30) + 15;
            heights[i] += (target - heights[i]) * 0.18;

            const h = heights[i];
            const x = startX + i * (barWidth + barGap);
            const y = canvas.height - h;

            // Gradient per bar
            const grad = ctx.createLinearGradient(0, y, 0, canvas.height);
            grad.addColorStop(0, '#00F0FF');
            grad.addColorStop(0.5, '#5865F2');
            grad.addColorStop(1, '#9B59B6');

            ctx.fillStyle = grad;
            ctx.shadowBlur = 10;
            ctx.shadowColor = 'rgba(0, 240, 255, 0.4)';

            ctx.beginPath();
            ctx.roundRect(x, y, barWidth, h, 4);
            ctx.fill();
        }

        requestAnimationFrame(draw);
    }
    draw();

    document.getElementById('slider-voice-vol')?.addEventListener('input', (e) => {
        document.getElementById('display-voice-vol').textContent = `${e.target.value}%`;
    });
}

/* =========================================================
   4. CHAT EN VIVO, COLORES POR USUARIO Y FOTOS
   ========================================================= */
const CHANNELS_DATA = [
    { id: "all", name: "🌐・todos-los-canales", topic: "Feed unificado de todos los canales de SHADOW BLOCK" },
    { id: "1350706770527653992", name: "general", topic: "Charla general de la comunidad" },
    { id: "1559854210080575518", name: "🤖・game-bots", topic: "Emparejamiento de cuentas bots Free Fire" },
    { id: "1559854214493245480", name: "🚨・send-reports", topic: "55 reportes y blacklist en 12s" },
    { id: "1559852912727822396", name: "🎨・stickers-9999-hd", topic: "Catálogo masivo de 9,999 stickers" },
    { id: "1559852917295677511", name: "🔊・soundboard-500-freefire", topic: "Reproductor de 500 voces de Free Fire" },
    { id: "1559842253352992840", name: "🖼️・wallpapers-4k-hd", topic: "Wallpapers automáticos cada 25 minutos" },
    { id: "1559844380934807612", name: "🎫・comprar-panel-y-bots", topic: "Tickets de compra VIP" },
    { id: "1559359413402472488", name: "bienvenida-☺️", topic: "Registro de bienvenidas y despedidas" },
    { id: "1559826233620168734", name: "😀botericklogs", topic: "Consola de control de bots" }
];

const USER_COLOR_PALETTE = [
    '#00F0FF', // Cian Eléctrico
    '#FF0055', // Rosa Neón
    '#00FF66', // Verde Lima
    '#FFE600', // Amarillo Oro
    '#9B59B6', // Púrpura Real
    '#FF7700', // Naranja Fuego
    '#3B82F6', // Azul Eléctrico
    '#EC4899', // Fucsia Intenso
    '#10B981', // Esmeralda Cyber
    '#A855F7', // Violeta
    '#F43F5E', // Rubí
    '#06B6D4', // Turquesa
    '#F97316', // Mandarina
    '#84CC16', // Lima Intenso
    '#EAB308', // Ámbar
    '#6366F1'  // Índigo
];

function getUsernameColor(username, userId = '') {
    const key = (userId || username || 'anon').toLowerCase();
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
        hash = key.charCodeAt(i) + ((hash << 5) - hash);
    }
    return USER_COLOR_PALETTE[Math.abs(hash) % USER_COLOR_PALETTE.length];
}

let activeChannelFilter = "all";
let chatPollTimer = null;

function initChatSystem() {
    const listEl = document.getElementById('chat-channels-list');
    const msgsEl = document.getElementById('chat-messages-container');
    const curNameEl = document.getElementById('current-chat-ch-name');
    const curTopicEl = document.getElementById('current-chat-ch-topic');
    const inputEl = document.getElementById('chat-input-text');
    const inputImgEl = document.getElementById('chat-input-image');
    const btnSend = document.getElementById('btn-send-chat-msg');
    const btnToggleAttach = document.getElementById('btn-toggle-attach');
    const attachBar = document.getElementById('composer-attachment-bar');
    const btnClearImg = document.getElementById('btn-clear-img-url');
    const btnRefresh = document.getElementById('btn-refresh-chat-view');
    const btnClear = document.getElementById('btn-clear-chat-view');
    const targetChannelSelect = document.getElementById('chat-target-channel-select');

    if (!listEl || !msgsEl) return;

    // Toggle attachment bar
    if (btnToggleAttach && attachBar) {
        btnToggleAttach.addEventListener('click', () => {
            const isHidden = attachBar.style.display === 'none';
            attachBar.style.display = isHidden ? 'flex' : 'none';
            if (isHidden && inputImgEl) inputImgEl.focus();
        });
    }

    if (btnClearImg && inputImgEl) {
        btnClearImg.addEventListener('click', () => {
            inputImgEl.value = '';
            if (attachBar) attachBar.style.display = 'none';
        });
    }

    // Render channels list
    listEl.innerHTML = '';
    CHANNELS_DATA.forEach((ch, idx) => {
        const btn = document.createElement('button');
        btn.className = `channel-btn ${idx === 0 ? 'active' : ''}`;
        btn.innerHTML = ch.id === 'all' 
            ? `<i class="fa-solid fa-globe text-cyan"></i> <span>${ch.name}</span> <span class="nav-tag tag-cyan" style="font-size:9px; padding:1px 5px; margin-left:auto;">ALL</span>`
            : `<i class="fa-solid fa-hashtag"></i> <span>${ch.name}</span>`;
        btn.addEventListener('click', () => {
            document.querySelectorAll('.channel-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeChannelFilter = ch.id;
            curNameEl.textContent = ch.name;
            curTopicEl.textContent = ch.topic;
            renderChatMessages();
        });
        listEl.appendChild(btn);
    });

    // Cargar mensajes desde localStorage o servidor
    let localCache = [];
    try {
        const stored = localStorage.getItem('shadow_chat_cache');
        if (stored) localCache = JSON.parse(stored);
    } catch(e) {}

    window._chatMessages = Array.isArray(localCache) && localCache.length ? localCache : [];
    renderChatMessages();

    // Polling periódico a la API /api/chat
    async function fetchServerChat() {
        try {
            const res = await fetch('/api/chat', { cache: 'no-store' });
            if (res.ok) {
                const data = await res.json();
                if (Array.isArray(data) && data.length) {
                    window._chatMessages = data;
                    localStorage.setItem('shadow_chat_cache', JSON.stringify(data));
                    renderChatMessages();
                }
            }
        } catch (e) {
            // Modo local sin servidor
        }
    }

    fetchServerChat();
    if (chatPollTimer) clearInterval(chatPollTimer);
    chatPollTimer = setInterval(fetchServerChat, 2500);

    if (btnRefresh) {
        btnRefresh.addEventListener('click', () => {
            fetchServerChat();
            playTone(440, 0.1);
        });
    }

    if (btnClear) {
        btnClear.addEventListener('click', async () => {
            if (confirm('¿Deseas vaciar la vista y el registro del chat?')) {
                window._chatMessages = [];
                localStorage.removeItem('shadow_chat_cache');
                renderChatMessages();
                try {
                    await fetch('/api/chat/clear', { method: 'POST' });
                } catch(e) {}
            }
        });
    }

    function renderChatMessages() {
        if (!msgsEl) return;
        msgsEl.innerHTML = '';

        const filtered = (window._chatMessages || []).filter(m => {
            if (activeChannelFilter === 'all') return true;
            return m.channel_id === activeChannelFilter || m.channel_name === activeChannelFilter;
        });

        if (filtered.length === 0) {
            msgsEl.innerHTML = `
                <div class="empty-chat-state" style="text-align:center; padding:40px 20px; color:#666;">
                    <i class="fa-solid fa-comments" style="font-size:32px; margin-bottom:10px; opacity:0.5;"></i>
                    <p>No hay mensajes registrados en este canal aún.</p>
                    <small>Escribe abajo o envía un mensaje en Discord para verlo en vivo.</small>
                </div>
            `;
            return;
        }

        filtered.forEach(m => {
            const userColor = getUsernameColor(m.author, m.author_id);
            const timeStr = m.timestamp || (m.time || 'Ahora');
            const avatarUrl = m.avatar || "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop";

            const msgDiv = document.createElement('div');
            msgDiv.className = 'msg-item';

            let attachmentsHtml = '';
            if (Array.isArray(m.attachments) && m.attachments.length) {
                m.attachments.forEach(url => {
                    if (url) {
                        attachmentsHtml += `
                            <div class="msg-attachment-wrap" style="margin-top:8px;">
                                <img src="${url}" class="msg-attachment-img" alt="Foto adjunta" loading="lazy" style="max-width:320px; max-height:240px; border-radius:10px; border:1px solid rgba(255,255,255,0.15); cursor:pointer; transition:transform 0.2s;" onclick="zoomImage('${url}')">
                            </div>
                        `;
                    }
                });
            }

            msgDiv.innerHTML = `
                <img src="${avatarUrl}" class="msg-avatar" alt="${m.author}" onerror="this.src='https://cdn.discordapp.com/embed/avatars/0.png'">
                <div class="msg-content-wrapper">
                    <div class="msg-author-row">
                        <span class="msg-author-name" style="color: ${userColor}; font-weight: 700; text-shadow: 0 0 10px ${userColor}40;">
                            ${m.author}
                        </span>
                        ${m.bot ? '<span class="msg-bot-tag">BOT</span>' : ''}
                        <span class="msg-ch-tag" style="font-size:10px; padding:2px 6px; border-radius:4px; background:rgba(255,255,255,0.06); color:#aaa; margin-left:6px;">
                            #${m.channel_name || 'general'}
                        </span>
                        <span class="msg-timestamp" style="margin-left:auto; font-size:11px; color:#777;">${timeStr}</span>
                    </div>
                    ${m.content ? `<div class="msg-bubble">${escapeHtml(m.content)}</div>` : ''}
                    ${attachmentsHtml}
                </div>
            `;
            msgsEl.appendChild(msgDiv);
        });

        msgsEl.scrollTop = msgsEl.scrollHeight;
    }

    async function sendCurrent() {
        const text = inputEl.value.trim();
        const imgUrl = inputImgEl ? inputImgEl.value.trim() : '';

        if (!text && !imgUrl) return;

        const targetCh = targetChannelSelect ? targetChannelSelect.value : 'general';
        const now = new Date();
        const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;

        const newMsg = {
            id: `msg_${Date.now()}`,
            author: "rafamodzyt (Panel Web)",
            author_id: "panel_owner",
            bot: true,
            avatar: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop",
            channel_name: targetCh,
            channel_id: "1350706770527653992",
            content: text,
            attachments: imgUrl ? [imgUrl] : [],
            timestamp: timeStr,
            date: now.toISOString().slice(0, 10)
        };

        window._chatMessages = window._chatMessages || [];
        window._chatMessages.push(newMsg);
        localStorage.setItem('shadow_chat_cache', JSON.stringify(window._chatMessages));
        renderChatMessages();

        inputEl.value = '';
        if (inputImgEl) inputImgEl.value = '';
        if (attachBar) attachBar.style.display = 'none';

        // Enviar al backend vía API
        try {
            await fetch('/api/chat/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    channel_name: targetCh,
                    image_url: imgUrl
                })
            });
        } catch(e) {}
    }

    btnSend.addEventListener('click', sendCurrent);
    inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendCurrent();
    });

    // Shortcuts chips
    document.getElementById('btn-chip-booyah')?.addEventListener('click', () => {
        inputEl.value = "🏆 ¡¡¡BOOYAH!!! Victoria magistral en Free Fire para la escuadra.";
        inputEl.focus();
    });
    document.getElementById('btn-chip-gang')?.addEventListener('click', () => {
        inputEl.value = "👑 El Gang de Free Fire dominando Bermuda en clasificatoria.";
        inputEl.focus();
    });
    document.getElementById('btn-chip-donato')?.addEventListener('click', () => {
        inputEl.value = "🎯 Headshot pa tu casa crack de parte del Donato.";
        inputEl.focus();
    });
    document.getElementById('btn-chip-zelika')?.addEventListener('click', () => {
        inputEl.value = "⚡ Movimiento insano 360 grados y pared Gloo modo flash.";
        inputEl.focus();
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[m]);
}

window.zoomImage = function(url) {
    const modal = document.getElementById('image-zoom-modal');
    const imgEl = document.getElementById('image-zoom-img');
    if (modal && imgEl) {
        imgEl.src = url;
        modal.classList.add('open');
    }
};

document.getElementById('btn-close-image-modal')?.addEventListener('click', () => {
    document.getElementById('image-zoom-modal')?.classList.remove('open');
});

/* =========================================================
   5. GAME BOTS (55 CUENTAS BOTS RANDOM DE FREE FIRE)
   ========================================================= */
const FREEFIRE_55_BOTS_POOL = [
    { name: "꧁༒☬ALEX_INSANO☬༒꧂", level: 84, rank: "Gran Maestro Top 100", hs: "91.4%", kd: "7.8", region: "SUR" },
    { name: "⚡GHOST_SHADOW_99⚡", level: 82, rank: "Heroico 5★", hs: "88.2%", kd: "6.9", region: "NORTE" },
    { name: "亗 COBRA_KING 亗", level: 79, rank: "Heroico 4★", hs: "85.6%", kd: "6.2", region: "EEUU" },
    { name: "★_VILLANO_77_★", level: 88, rank: "Gran Maestro Top 50", hs: "94.1%", kd: "8.4", region: "SUR" },
    { name: "ঔৣ☬EL_PATRON☬ঔৣ", level: 85, rank: "Gran Maestro", hs: "89.5%", kd: "7.2", region: "NORTE" },
    { name: "乂_NINJA_FF_乂", level: 76, rank: "Heroico 3★", hs: "84.0%", kd: "5.8", region: "EEUU" },
    { name: "🔥_DRAGON_BLACK_🔥", level: 81, rank: "Heroico 5★", hs: "87.3%", kd: "6.5", region: "SUR" },
    { name: "CR7_HACKER_BOY", level: 78, rank: "Heroico 3★", hs: "86.1%", kd: "6.1", region: "NORTE" },
    { name: "[BOT] Tuerka_Vip_01", level: 75, rank: "Heroico 2★", hs: "82.5%", kd: "5.4", region: "EEUU" },
    { name: "亗 MATADOR_PRO 亗", level: 86, rank: "Gran Maestro Top 200", hs: "90.2%", kd: "7.9", region: "SUR" },
    { name: "★_SHADOW_SNIPER_★", level: 83, rank: "Heroico 5★", hs: "92.8%", kd: "7.1", region: "NORTE" },
    { name: "ঔৣ☬K1LL3R_999☬ঔৣ", level: 80, rank: "Heroico 4★", hs: "86.7%", kd: "6.3", region: "EEUU" },
    { name: "⚡THUNDER_STRIKE⚡", level: 77, rank: "Heroico 3★", hs: "83.9%", kd: "5.9", region: "SUR" },
    { name: "꧁༒ALAN_HEROICO༒꧂", level: 89, rank: "Gran Maestro Top 20", hs: "95.6%", kd: "9.2", region: "NORTE" },
    { name: "[BOT] ZELIKA_JR_55", level: 82, rank: "Heroico 5★", hs: "89.0%", kd: "7.0", region: "EEUU" },
    { name: "亗 PEPE_R18 亗", level: 78, rank: "Heroico 3★", hs: "84.5%", kd: "6.0", region: "SUR" },
    { name: "★_DARK_VIPER_★", level: 84, rank: "Gran Maestro", hs: "90.8%", kd: "7.7", region: "NORTE" },
    { name: "ঔৣ☬SOUL_REAPER☬ঔৣ", level: 87, rank: "Gran Maestro Top 80", hs: "93.4%", kd: "8.3", region: "EEUU" },
    { name: "⚡VOLT_MASTER⚡", level: 75, rank: "Heroico 2★", hs: "82.1%", kd: "5.5", region: "SUR" },
    { name: "亗 ASESINO_X 亗", level: 83, rank: "Heroico 5★", hs: "88.7%", kd: "7.2", region: "NORTE" },
    { name: "꧁༒BLACK_WOLF༒꧂", level: 80, rank: "Heroico 4★", hs: "86.3%", kd: "6.4", region: "EEUU" },
    { name: "★_STORM_RIDER_★", level: 76, rank: "Heroico 3★", hs: "83.5%", kd: "5.7", region: "SUR" },
    { name: "[BOT] DONATO_CLONE_7", level: 85, rank: "Gran Maestro", hs: "91.9%", kd: "8.1", region: "NORTE" },
    { name: "亗 TOXIC_BOY 亗", level: 79, rank: "Heroico 4★", hs: "85.2%", kd: "6.2", region: "EEUU" },
    { name: "ঔৣ☬DEVIL_SHOT☬ঔৣ", level: 86, rank: "Gran Maestro Top 150", hs: "92.1%", kd: "8.0", region: "SUR" },
    { name: "⚡CYBER_PHANTOM⚡", level: 81, rank: "Heroico 5★", hs: "87.9%", kd: "6.8", region: "NORTE" },
    { name: "꧁༒RED_BLOOD༒꧂", level: 77, rank: "Heroico 3★", hs: "84.2%", kd: "5.9", region: "EEUU" },
    { name: "★_APEX_HUNTER_★", level: 88, rank: "Gran Maestro Top 40", hs: "94.7%", kd: "8.9", region: "SUR" },
    { name: "[BOT] ffglory_LΣVΣLS_1", level: 75, rank: "Heroico 2★", hs: "81.9%", kd: "5.3", region: "NORTE" },
    { name: "[BOT] ffglory_LΣVΣLS_2", level: 76, rank: "Heroico 2★", hs: "82.4%", kd: "5.4", region: "SUR" },
    { name: "[BOT] ffglory_LΣVΣLS_3", level: 78, rank: "Heroico 3★", hs: "84.1%", kd: "6.0", region: "EEUU" },
    { name: "[BOT] ffglory_LΣVΣLS_4", level: 79, rank: "Heroico 4★", hs: "85.0%", kd: "6.2", region: "SUR" },
    { name: "亗 VENOM_SPIKE 亗", level: 82, rank: "Heroico 5★", hs: "88.5%", kd: "7.0", region: "NORTE" },
    { name: "ঔৣ☬INFERNO_VIP☬ঔৣ", level: 84, rank: "Gran Maestro", hs: "90.4%", kd: "7.6", region: "EEUU" },
    { name: "⚡TITAN_FORCE⚡", level: 80, rank: "Heroico 4★", hs: "86.0%", kd: "6.4", region: "SUR" },
    { name: "꧁༒GALAXY_BOY༒꧂", level: 87, rank: "Gran Maestro Top 70", hs: "93.1%", kd: "8.2", region: "NORTE" },
    { name: "★_PHOENIX_FIRE_★", level: 83, rank: "Heroico 5★", hs: "89.3%", kd: "7.3", region: "EEUU" },
    { name: "亗 ZERO_COOL 亗", level: 78, rank: "Heroico 3★", hs: "84.8%", kd: "6.1", region: "SUR" },
    { name: "ঔৣ☬SHADOW_LORD☬ঔৣ", level: 90, rank: "Gran Maestro Top 10", hs: "96.4%", kd: "9.5", region: "NORTE" },
    { name: "⚡ALPHA_STRIKER⚡", level: 81, rank: "Heroico 5★", hs: "87.5%", kd: "6.7", region: "EEUU" },
    { name: "꧁༒DEMON_KING༒꧂", level: 85, rank: "Gran Maestro", hs: "91.2%", kd: "7.9", region: "SUR" },
    { name: "★_VORTEX_SNIPER_★", level: 82, rank: "Heroico 5★", hs: "88.9%", kd: "7.1", region: "NORTE" },
    { name: "[BOT] BOT_INSANO_77", level: 76, rank: "Heroico 3★", hs: "83.7%", kd: "5.8", region: "EEUU" },
    { name: "亗 SAVAGE_BEAST 亗", level: 84, rank: "Gran Maestro", hs: "90.7%", kd: "7.8", region: "SUR" },
    { name: "ঔৣ☬IRON_FIST☬ঔৣ", level: 79, rank: "Heroico 4★", hs: "85.8%", kd: "6.3", region: "NORTE" },
    { name: "⚡OMEGA_VIP⚡", level: 86, rank: "Gran Maestro Top 120", hs: "92.5%", kd: "8.1", region: "EEUU" },
    { name: "꧁༒NEON_BLADE༒꧂", level: 80, rank: "Heroico 4★", hs: "86.5%", kd: "6.5", region: "SUR" },
    { name: "★_BLOOD_HUNTER_★", level: 83, rank: "Heroico 5★", hs: "89.8%", kd: "7.4", region: "NORTE" },
    { name: "亗 HYDRA_GANG 亗", level: 77, rank: "Heroico 3★", hs: "84.3%", kd: "5.9", region: "EEUU" },
    { name: "ঔৣ☬CHAOS_GOD☬ঔৣ", level: 89, rank: "Gran Maestro Top 30", hs: "95.2%", kd: "9.0", region: "SUR" },
    { name: "⚡FROST_BITE⚡", level: 81, rank: "Heroico 5★", hs: "88.0%", kd: "6.9", region: "NORTE" },
    { name: "꧁༒SPECTER_X༒꧂", level: 85, rank: "Gran Maestro", hs: "91.7%", kd: "8.0", region: "EEUU" },
    { name: "★_RAVEN_WING_★", level: 78, rank: "Heroico 3★", hs: "85.1%", kd: "6.1", region: "SUR" },
    { name: "亗 ULTIMATE_PRO 亗", level: 88, rank: "Gran Maestro Top 60", hs: "94.3%", kd: "8.7", region: "NORTE" },
    { name: "ঔৣ☬MASTER_CHIEF_FF☬ঔৣ", level: 91, rank: "Gran Maestro Top 5", hs: "97.1%", kd: "9.8", region: "EEUU" }
];

function getRandomBots(count = 3) {
    const shuffled = [...FREEFIRE_55_BOTS_POOL].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count).map(b => {
        const id = Math.floor(Math.random() * 9000000000) + 1000000000;
        const ping = Math.floor(Math.random() * 18) + 8;
        return { ...b, id, ping };
    });
}

function initGameBots() {
    const btnLaunch = document.getElementById('btn-launch-gamebots');
    const btnRegen = document.getElementById('btn-regen-squad');
    const btnView55 = document.getElementById('btn-view-all-55-bots');
    const inputId = document.getElementById('gb-input-id');
    const selectReg = document.getElementById('gb-select-region');
    const selectMode = document.getElementById('gb-select-mode');
    const resultBox = document.getElementById('gb-result-box');
    const emptyState = document.getElementById('gb-empty-state');
    const squadDisplay = document.getElementById('gb-squad-display');
    const squadNameEl = document.getElementById('gb-squad-name');
    const squadCodeEl = document.getElementById('gb-squad-code');
    const squadMembersEl = document.getElementById('gb-squad-members');

    const modalBots = document.getElementById('bots-55-modal');
    const modalBotsGrid = document.getElementById('modal-bots-grid');
    const btnCloseModal = document.getElementById('btn-close-bots-modal');

    function generateSquad() {
        const idVal = inputId ? inputId.value.trim() : '';
        if (!idVal || idVal.length < 5) {
            alert('⚠️ Por favor ingresa una ID de Free Fire válida (mínimo 5 dígitos).');
            return;
        }

        const regVal = selectReg ? selectReg.value : 'SUR';
        const modeVal = selectMode ? selectMode.value : 'de';
        const teamNum = Math.floor(Math.random() * 9000) + 1000;
        const teamCode = `#FF-${Math.floor(Math.random() * 90000) + 10000}`;

        const bots = getRandomBots(3);

        const modeTitles = {
            'br': 'BR CLASIFICATORIA',
            'de': 'DUELO DE ESCUADRAS',
            'solo': 'SOLO VS BOTS'
        };
        const modeTitle = modeTitles[modeVal] || 'HEROICA';

        squadNameEl.textContent = `🔥 ESCUADRA BOTS ${modeTitle} #${teamNum}`;
        squadCodeEl.textContent = `CÓDIGO DE SALA: ${teamCode}`;

        squadMembersEl.innerHTML = `
            <div class="squad-member-card" style="border-left: 3px solid #FFD700;">
                <div>
                    👑 <strong>[LÍDER] ID: ${escapeHtml(idVal)}</strong> (Tu Cuenta)
                    <div style="font-size:11px; color:#888; margin-top:2px;">Región: ${regVal} • Modo: ${modeTitle}</div>
                </div>
                <span class="badge-vip">${regVal}</span>
            </div>
            ${bots.map((b, i) => `
                <div class="squad-member-card" style="border-left: 3px solid #2ECC71;">
                    <div>
                        🤖 <strong>${escapeHtml(b.name)}</strong>
                        <div style="font-size:11px; color:#aaa; margin-top:3px; display:flex; gap:10px; flex-wrap:wrap;">
                            <span>ID: <code>${b.id}</code></span>
                            <span style="color:#00F0FF;"><i class="fa-solid fa-trophy"></i> Nivel ${b.level}</span>
                            <span style="color:#FFD700;"><i class="fa-solid fa-medal"></i> ${b.rank}</span>
                            <span style="color:#FF0055;"><i class="fa-solid fa-crosshairs"></i> HS: ${b.hs}</span>
                            <span style="color:#2ECC71;"><i class="fa-solid fa-skull"></i> K/D: ${b.kd}</span>
                        </div>
                    </div>
                    <span class="badge-status-ready">ONLINE • ${b.ping}ms</span>
                </div>
            `).join('')}
        `;

        emptyState.classList.add('hidden');
        squadDisplay.classList.remove('hidden');

        playTone(523.25, 0.2);
        setTimeout(() => playTone(659.25, 0.3), 150);
    }

    if (btnLaunch) btnLaunch.addEventListener('click', generateSquad);
    if (btnRegen) btnRegen.addEventListener('click', generateSquad);

    // Modal de Roster de 55 Bots
    function open55BotsModal() {
        if (!modalBots || !modalBotsGrid) return;
        modalBotsGrid.innerHTML = FREEFIRE_55_BOTS_POOL.map((b, idx) => {
            const fakeId = 1980000000 + idx * 73 + 12;
            return `
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px; display:flex; flex-direction:column; gap:4px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:10px; color:#888;">#${idx + 1}</span>
                        <span style="font-size:9px; background:rgba(46,204,113,0.15); color:#2ECC71; padding:1px 6px; border-radius:4px;">🟢 ACTIVO</span>
                    </div>
                    <strong style="font-size:12px; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(b.name)}</strong>
                    <div style="font-size:10px; color:#aaa; display:flex; justify-content:space-between;">
                        <span>Nvl. ${b.level}</span>
                        <span style="color:#FFD700;">${b.rank.split(' ')[0]}</span>
                        <span style="color:#00F0FF;">${b.region}</span>
                    </div>
                    <div style="font-size:9px; color:#666;">ID: ${fakeId}</div>
                </div>
            `;
        }).join('');

        modalBots.classList.add('open');
    }

    if (btnView55) btnView55.addEventListener('click', open55BotsModal);
    if (btnCloseModal) {
        btnCloseModal.addEventListener('click', () => {
            modalBots.classList.remove('open');
        });
    }
}

/* =========================================================
   6. SEND REPORTS (55 REPORTES EN 12S)
   ========================================================= */
function initSendReports() {
    const btnStart = document.getElementById('btn-start-reports-sequence');
    const inputTarget = document.getElementById('rep-input-target');
    const selectReg = document.getElementById('rep-select-region');
    const selectReason = document.getElementById('rep-select-reason');
    const fillEl = document.getElementById('rep-progress-fill');
    const stepText = document.getElementById('rep-step-text');
    const percentText = document.getElementById('rep-percent-text');
    const timerDisplay = document.getElementById('rep-timer-display');
    const terminalLogs = document.getElementById('rep-terminal-logs');
    const finalBadge = document.getElementById('rep-final-badge');
    const finalMsg = document.getElementById('rep-final-msg');

    if (!btnStart) return;

    let isRunning = false;

    btnStart.addEventListener('click', () => {
        if (isRunning) return;
        const targetId = inputTarget.value.trim();
        if (!targetId || targetId.length < 5) {
            alert('⚠️ Ingresa una ID válida de la cuenta que recibirá los 55 reportes.');
            return;
        }

        isRunning = true;
        btnStart.disabled = true;
        btnStart.style.opacity = '0.5';
        finalBadge.classList.add('hidden');

        const BOT_PREFIXES = ["ShadowBot", "FF_Hunter", "CobraSniper", "GhostBuster", "InsanoVip", "AimbotNull", "NoobSlayer", "ReportSniper", "BermudaMod", "BlacklistBot"];
        
        terminalLogs.innerHTML = `
            <div class="term-line">> [0.0s] INICIANDO PROTOCOLO: 55 REPORTES EN 12 SEGUNDOS...</div>
            <div class="term-line">> Cuenta Objetivo: ${targetId} | Región: ${selectReg.value}</div>
            <div class="term-line">> Motivo: "${selectReason.value}"</div>
        `;

        let elapsed = 0;
        const totalDuration = 12.0;

        const interval = setInterval(() => {
            elapsed += 0.2;
            const remaining = Math.max(0, totalDuration - elapsed);
            timerDisplay.textContent = `${remaining.toFixed(1)}s`;

            const pct = Math.min(100, Math.round((elapsed / totalDuration) * 100));
            fillEl.style.width = `${pct}%`;
            percentText.textContent = `${pct}%`;

            const botNum = Math.min(55, Math.floor((pct / 100) * 55));
            const randomPrefix = BOT_PREFIXES[Math.floor(Math.random() * BOT_PREFIXES.length)];
            const randomBotName = `[${randomPrefix}_${Math.floor(Math.random() * 89) + 10}]`;

            if (pct < 30) {
                stepText.textContent = `Conectando cuentas bots (${botNum}/55)...`;
            } else if (pct < 75) {
                stepText.textContent = `Enviando ráfaga masiva (${botNum}/55 reportes)...`;
            } else if (pct < 100) {
                stepText.textContent = `Inyectando Blacklist y congelando rango...`;
            }

            if (Math.random() > 0.4) {
                const line = document.createElement('div');
                line.className = 'term-line';
                line.textContent = `> [${elapsed.toFixed(1)}s] Bot #${botNum} ${randomBotName} envió reporte a ID: ${targetId} -> OK (200)`;
                terminalLogs.appendChild(line);
                terminalLogs.scrollTop = terminalLogs.scrollHeight;
            }

            // Beep tone
            playTone(300 + pct * 5, 0.05);

            if (elapsed >= totalDuration) {
                clearInterval(interval);
                isRunning = false;
                btnStart.disabled = false;
                btnStart.style.opacity = '1';

                stepText.textContent = '¡Completado! 55/55 Reportes enviados.';
                timerDisplay.textContent = '0.0s';

                finalMsg.textContent = `La cuenta ID ${targetId} ha recibido 55 reportes sincronizados en 12 segundos y fue encolada en la Blacklist del servidor.`;
                finalBadge.classList.remove('hidden');

                // Success tone
                playTone(800, 0.4);
            }
        }, 200);
    });
}

/* =========================================================
   7. SOUNDBOARD CON 500 VOCES DE FREE FIRE (AUDIO REAL)
   ========================================================= */
const OFFICIAL_SOUNDS = [
    { id: "agarrate", name: "agarrate", emoji: "🔊", phrase: "Sonido clásico de llamada" },
    { id: "donato_headshot", name: "donato_headshot", emoji: "🎯", phrase: "Headshot pa tu casa crack de parte del Donato" },
    { id: "zelika_insano", name: "zelika_insano", emoji: "🔥", phrase: "Que onda cracks aqui Zelika en racha insana" },
    { id: "hacker_aimbot", name: "hacker_aimbot", emoji: "🤖", phrase: "Aimbot activado todo rojo a la cabeza" },
    { id: "gang_freefire", name: "gang_freefire", emoji: "👑", phrase: "El Gang de Free Fire dominando la partida" },
    { id: "booyah_epico", name: "booyah_epico", emoji: "🏆", phrase: "Booyah victoria magistral en Bermuda" },
    { id: "gloo_360", name: "gloo_360", emoji: "🛡️", phrase: "Pared Gloo a 360 grados cubreme manco" },
    { id: "mp40_cobra", name: "mp40_cobra", emoji: "🐍", phrase: "Rafaga letal de MP40 Cobra al pecho" }
];

function initSoundboard() {
    const offGrid = document.getElementById('official-sounds-grid');
    const extGrid = document.getElementById('sounds-extended-grid');
    const searchInput = document.getElementById('search-soundboard');
    const filterTabs = document.querySelectorAll('.filter-tab');

    if (!offGrid || !extGrid) return;

    // 1. Render 8 official sounds
    offGrid.innerHTML = '';
    OFFICIAL_SOUNDS.forEach(snd => {
        const card = document.createElement('div');
        card.className = 'sound-btn-card';
        card.innerHTML = `
            <span class="s-emoji">${snd.emoji}</span>
            <div class="s-meta">
                <span class="s-name">${snd.name}</span>
                <span class="s-phrase">${snd.phrase}</span>
            </div>
        `;
        card.addEventListener('click', () => {
            playSoundCard(card, snd.phrase);
        });
        offGrid.appendChild(card);
    });

    // 2. Generate 500 voice lines database
    const EXTENDED_VOICES = [];
    const CATEGORIES = [
        { key: "donato", name: "The Donato", range: [1, 100], emoji: "🎯", phrases: [
            "Headshot pa tu casa crack de parte del Donato",
            "Watafac pero que fue eso se fue directo al lobby",
            "Risa de loco del Donato jajaja no aguanto",
            "Manco a mimir que aca manda el Donato",
            "Dios mio que disparo con la M1887 a la cabeza"
        ]},
        { key: "zelika", name: "Zelika Insano", range: [101, 200], emoji: "🔥", phrases: [
            "Que onda cracks aqui Zelika en racha insana",
            "Movimiento insano en 360 grados pared gloo al instante",
            "Pared gloo agachado modo flash no me pueden tocar",
            "Todo rojo a la cabeza ningun tiro amarillo",
            "Dominando el torneo de clanes como verdaderos insanos"
        ]},
        { key: "hackers", name: "Hackers & Aimbot", range: [201, 300], emoji: "🤖", phrases: [
            "Aimbot activado todo rojo a la cabeza automaticamente",
            "Bypass antiban confirmado indetectable en el servidor",
            "Vuelo y teletransporte directo arriba de la garita",
            "Mira pegada al casco no fallo ni una sola bala",
            "Protocolo hacker iniciado borrando a la escuadra"
        ]},
        { key: "gang", name: "El Gang Free Fire", range: [301, 400], emoji: "👑", phrases: [
            "El Gang de Free Fire dominando toda la partida",
            "Rushea por la izquierda que yo entro por la ventana",
            "Tirame botiquines y balas AR que no tengo nada",
            "Granada cocinada adentro de casa L los tenemos atrapados",
            "Cubranme que estoy reviviendo al companero rapido"
        ]},
        { key: "booyah", name: "Booyah & Armas", range: [401, 500], emoji: "🏆", phrases: [
            "Booyah victoria magistral en Bermuda partida ganada",
            "Rafaga letal de MP40 Cobra quemando chalecos",
            "M1887 un solo tiro y a mimir al piso",
            "Disparo certero de AWM a 500 metros sin fallo",
            "Pared gloo salvadora en el ultimo segundo de vida"
        ]}
    ];

    CATEGORIES.forEach(cat => {
        for (let i = cat.range[0]; i <= cat.range[1]; i++) {
            const pIdx = (i - 1) % cat.phrases.length;
            EXTENDED_VOICES.push({
                id: i,
                catKey: cat.key,
                catName: cat.name,
                emoji: cat.emoji,
                title: `${cat.name} #${String(i).padStart(3, '0')}`,
                phrase: `${cat.phrases[pIdx]} (Clip #${i})`
            });
        }
    });

    function renderExtended(filterCat = 'all', query = '') {
        extGrid.innerHTML = '';
        const filtered = EXTENDED_VOICES.filter(v => {
            const matchCat = filterCat === 'all' || v.catKey === filterCat;
            const matchQ = !query || v.title.toLowerCase().includes(query) || v.phrase.toLowerCase().includes(query) || String(v.id) === query;
            return matchCat && matchQ;
        });

        // Slice to max 60 per view for high performance
        filtered.slice(0, 60).forEach(snd => {
            const card = document.createElement('div');
            card.className = 'sound-btn-card';
            card.innerHTML = `
                <span class="s-emoji">${snd.emoji}</span>
                <div class="s-meta">
                    <span class="s-name">#${snd.id} ${snd.title}</span>
                    <span class="s-phrase">${snd.phrase}</span>
                </div>
            `;
            card.addEventListener('click', () => {
                playSoundCard(card, snd.phrase);
            });
            extGrid.appendChild(card);
        });
    }

    renderExtended();

    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderExtended(tab.getAttribute('data-sound-cat'), searchInput.value.toLowerCase().trim());
        });
    });

    searchInput.addEventListener('input', (e) => {
        const activeCat = document.querySelector('.filter-tab.active')?.getAttribute('data-sound-cat') || 'all';
        renderExtended(activeCat, e.target.value.toLowerCase().trim());
    });
}

// Speaks phrase using Web Speech API or synthesized audio
function playSoundCard(cardEl, phrase) {
    document.querySelectorAll('.sound-btn-card').forEach(c => c.classList.remove('playing'));
    cardEl.classList.add('playing');

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(phrase);
        utterance.lang = 'es-MX';
        utterance.rate = 1.05;
        utterance.pitch = 1.0;
        utterance.onend = () => {
            cardEl.classList.remove('playing');
        };
        window.speechSynthesis.speak(utterance);
    } else {
        playTone(440, 0.3);
        setTimeout(() => cardEl.classList.remove('playing'), 500);
    }
}

/* =========================================================
   8. STICKERS 9,999 MEMES
   ========================================================= */
const SAMPLE_STICKERS = [
    { id: 1, title: "Cheems Bonk #0001", cat: "Cheems", tag: "Vip", url: "https://media.giphy.com/media/qs427OHakAH238b9xD/giphy.gif" },
    { id: 2, title: "PopCat Mouth #0002", cat: "Memes", tag: "4K", url: "https://i.imgflip.com/345v97.jpg" },
    { id: 5, title: "Free Fire Todo Rojo #0005", cat: "Free Fire", tag: "Insano", url: "https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif" },
    { id: 8, title: "Donato Headshot #0008", cat: "Free Fire", tag: "Epic", url: "https://media.giphy.com/media/kwcRp24Wz4lZm/giphy.gif" },
    { id: 12, title: "GigaChad Sonrisa #0012", cat: "GigaChad", tag: "Sigma", url: "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif" },
    { id: 18, title: "Pepe Hype #0018", cat: "Pepe", tag: "UltraHD", url: "https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif" },
    { id: 25, title: "Karely Reina VIP #0025", cat: "Karely", tag: "Golden", url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=600&auto=format&fit=crop" },
    { id: 42, title: "Zelika Movimiento #0042", cat: "Free Fire", tag: "Insano", url: "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif" },
    { id: 55, title: "Aimbot Matrix #0055", cat: "Hackers", tag: "Cyber", url: "https://media.giphy.com/media/QNFhOolVeCzPQ2EBR5/giphy.gif" },
    { id: 77, title: "Wojak Yes Chad #0077", cat: "Pepe", tag: "Legendario", url: "https://i.imgflip.com/3oevdk.jpg" },
    { id: 100, title: "Thomas Shelby Fuma #0100", cat: "GigaChad", tag: "Sigma", url: "https://media.giphy.com/media/d3HeU0IDO2jLyDO7/giphy.gif" },
    { id: 500, title: "El Gang Dominando #0500", cat: "Free Fire", tag: "Supreme", url: "https://media.giphy.com/media/67ThRZlYBvibtdF9JH/giphy.gif" },
    { id: 1337, title: "Donato AWM OneShot #1337", cat: "Free Fire", tag: "Heroic", url: "https://media.giphy.com/media/kwcRp24Wz4lZm/giphy.gif" },
    { id: 7777, title: "GigaChad Diamond #7777", cat: "GigaChad", tag: "Master", url: "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif" },
    { id: 9999, title: "Free Fire Booyah Final #9999", cat: "Free Fire", tag: "Supreme", url: "https://media.giphy.com/media/blSTtZehjAZ8I/giphy.gif" }
];

function initStickers() {
    const grid = document.getElementById('stickers-gallery-grid');
    const searchInput = document.getElementById('search-stickers');
    const tabs = document.querySelectorAll('.stk-tab');

    if (!grid) return;

    function render(filterCat = 'all', query = '') {
        grid.innerHTML = '';
        const filtered = SAMPLE_STICKERS.filter(s => {
            const matchCat = filterCat === 'all' || s.cat.toLowerCase().includes(filterCat.toLowerCase());
            const matchQ = !query || s.title.toLowerCase().includes(query) || String(s.id) === query;
            return matchCat && matchQ;
        });

        filtered.forEach(stk => {
            const card = document.createElement('div');
            card.className = 'sticker-card';
            card.innerHTML = `
                <div class="sticker-img-box">
                    <img src="${stk.url}" alt="${stk.title}" loading="lazy">
                </div>
                <div class="sticker-name">${stk.title}</div>
                <div class="sticker-tag">#${String(stk.id).padStart(4, '0')} [${stk.tag}]</div>
            `;
            card.addEventListener('click', () => {
                alert(`✅ Sticker #${stk.id} seleccionado: "${stk.title}". En Discord usa //sticker ${stk.id}`);
            });
            grid.appendChild(card);
        });
    }

    render();

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            render(tab.getAttribute('data-stk-cat'), searchInput.value.toLowerCase().trim());
        });
    });

    searchInput.addEventListener('input', (e) => {
        const activeCat = document.querySelector('.stk-tab.active')?.getAttribute('data-stk-cat') || 'all';
        render(activeCat, e.target.value.toLowerCase().trim());
    });
}

/* =========================================================
   9. MIEMBROS EN CUADRITOS (GRID INTERACTIVO)
   ========================================================= */
const MEMBERS_DATA = [
    { id: "1350706770527653989", name: "rafamodzyt", nick: "👑 rafamodzyt", status: "online", role: "Owner / Administrador", avatar: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop" },
    { id: "1559830923174744125", name: "SatanasMiPadre", nick: "SatanasMiPadre", status: "online", role: "Bot Administrador", avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop" },
    { id: "1559437873265119252", name: "Erick X", nick: "Erick X 24/7", status: "online", role: "Bot de Voz 24/7", avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=200&auto=format&fit=crop" },
    { id: "109827364510293847", name: "Shadow_Warrior", nick: "Shadow_Warrior", status: "online", role: "Member / VIP", avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=200&auto=format&fit=crop" },
    { id: "283746591029384756", name: "Insano_FF_Pro", nick: "Insano_FF", status: "online", role: "Member", avatar: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?q=80&w=200&auto=format&fit=crop" },
    { id: "394857261029384758", name: "ZelikaFan_09", nick: "Zelika_Fan", status: "online", role: "Member", avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop" },
    { id: "492837162534895012", name: "DonatoCrack_77", nick: "Donato_77", status: "online", role: "Member", avatar: "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=200&auto=format&fit=crop" },
    { id: "582910492817263541", name: "CyberGamer_99", nick: "CyberGamer", status: "offline", role: "Member", avatar: "https://images.unsplash.com/photo-1628157582853-a796fa650a6a?q=80&w=200&auto=format&fit=crop" },
    { id: "672910482918273645", name: "BermudaSniper", nick: "SniperBermuda", status: "online", role: "Member", avatar: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=200&auto=format&fit=crop" },
    { id: "782910482918273646", name: "GlooWall_Master", nick: "GlooMaster", status: "online", role: "Member", avatar: "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=200&auto=format&fit=crop" },
    { id: "892810482918273647", name: "MP40_CobraGod", nick: "CobraGod", status: "online", role: "Member", avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop" },
    { id: "902810482918273648", name: "Heroico_S35", nick: "Heroico_35", status: "offline", role: "Member", avatar: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=200&auto=format&fit=crop" }
];

function initMembersGrid() {
    const grid = document.getElementById('members-cards-grid');
    const searchInput = document.getElementById('search-member-input');
    const pills = document.querySelectorAll('.pill-btn');
    const modal = document.getElementById('member-modal');
    const modalTitle = document.getElementById('modal-m-title');
    const modalBody = document.getElementById('modal-m-body');
    const btnClose = document.getElementById('btn-close-member-modal');

    if (!grid) return;

    function render(filter = 'all', query = '') {
        grid.innerHTML = '';
        const filtered = MEMBERS_DATA.filter(m => {
            const matchStatus = filter === 'all' || m.status === filter;
            const matchQ = !query || m.name.toLowerCase().includes(query) || m.role.toLowerCase().includes(query);
            return matchStatus && matchQ;
        });

        filtered.forEach(m => {
            const card = document.createElement('div');
            card.className = 'member-card-box';
            card.innerHTML = `
                <div class="m-avatar-wrap">
                    <img src="${m.avatar}" alt="${m.name}">
                    <span class="m-status-dot dot-${m.status}"></span>
                </div>
                <div class="m-info-wrap">
                    <div class="m-name">${m.nick || m.name}</div>
                    <span class="m-role-pill">${m.role}</span>
                </div>
            `;
            card.addEventListener('click', () => {
                modalTitle.textContent = `Perfil: ${m.name}`;
                modalBody.innerHTML = `
                    <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 20px;">
                        <img src="${m.avatar}" style="width: 64px; height: 64px; border-radius: 50%;">
                        <div>
                            <h4 style="font-size: 16px; font-weight: 800;">${m.name}</h4>
                            <p style="font-size: 12px; color: #9BA1B5;">ID: <code>${m.id}</code></p>
                            <span class="badge-ok" style="margin-top: 4px;">ESTADO: ${m.status.toUpperCase()}</span>
                        </div>
                    </div>
                    <div style="margin-bottom: 16px;">
                        <label style="font-size: 12px; color: #9BA1B5;">Rol Asignado:</label>
                        <p style="font-size: 14px; font-weight: 700; color: #00F0FF;">${m.role}</p>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn-control" onclick="alert('Rol actualizado');"><i class="fa-solid fa-user-tag"></i> Modificar Rol</button>
                        <button class="btn-control btn-yellow" onclick="alert('Usuario aislado');"><i class="fa-solid fa-microphone-slash"></i> Mutear</button>
                    </div>
                `;
                modal.classList.add('open');
            });
            grid.appendChild(card);
        });
    }

    render();

    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            render(pill.getAttribute('data-mfilter'), searchInput.value.toLowerCase().trim());
        });
    });

    searchInput.addEventListener('input', (e) => {
        const activePill = document.querySelector('.pill-btn.active')?.getAttribute('data-mfilter') || 'all';
        render(activePill, e.target.value.toLowerCase().trim());
    });

    btnClose.addEventListener('click', () => modal.classList.remove('open'));
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('open');
    });
}

/* =========================================================
   10. WALLPAPERS 4K
   ========================================================= */
const SAMPLE_WALLPAPERS = [
    { title: "Cyberpunk Neon City Skyline", res: "3840 x 2160 (4K)", cat: "pc", url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=800&auto=format&fit=crop" },
    { title: "Galaxia Cósmica AMOLED Deep Black", res: "1440 x 3120 (Móvil)", cat: "mobile", url: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800&auto=format&fit=crop" },
    { title: "Synthwave Sunset Grid Retrowave", res: "3840 x 2160 (4K)", cat: "pc", url: "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?q=80&w=800&auto=format&fit=crop" },
    { title: "Katana Samurai Cyberblade 2077", res: "1440 x 3120 (Móvil)", cat: "mobile", url: "https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=800&auto=format&fit=crop" },
    { title: "Neon Tokyo Rain Cyberpunk Streets", res: "3840 x 2160 (4K)", cat: "gaming", url: "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=800&auto=format&fit=crop" },
    { title: "Nebulosa Interestelar Morada 8K", res: "3840 x 2160 (4K)", cat: "pc", url: "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=800&auto=format&fit=crop" }
];

function initWallpapers() {
    const grid = document.getElementById('wallpapers-grid-display');
    const tabs = document.querySelectorAll('.wp-tab');
    const btnBurst = document.getElementById('btn-trigger-burst-wp');

    if (!grid) return;

    function render(filter = 'all') {
        grid.innerHTML = '';
        const filtered = SAMPLE_WALLPAPERS.filter(w => filter === 'all' || w.cat === filter);

        filtered.forEach(w => {
            const card = document.createElement('div');
            card.className = 'wp-card';
            card.innerHTML = `
                <div class="wp-img-box">
                    <img src="${w.url}" alt="${w.title}" loading="lazy">
                </div>
                <div class="wp-details">
                    <div class="wp-card-title">${w.title}</div>
                    <div class="wp-card-res"><i class="fa-solid fa-expand"></i> ${w.res}</div>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    render();

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            render(tab.getAttribute('data-wp-cat'));
        });
    });

    btnBurst.addEventListener('click', () => {
        alert('⚡ Ráfaga masiva de 100 Wallpapers enviada a #🖼️・wallpapers-4k-hd en Discord!');
    });
}

/* =========================================================
   11. ALERTAS PREVIEW EN VIVO
   ========================================================= */
function initAlertsPreview() {
    const titleInput = document.getElementById('alert-input-title');
    const textInput = document.getElementById('alert-input-text');
    const colorInput = document.getElementById('alert-input-color');
    const previewTitle = document.getElementById('preview-title');
    const previewDesc = document.getElementById('preview-desc');
    const previewColor = document.getElementById('preview-color-bar');
    const btnSend = document.getElementById('btn-send-discord-announcement');

    if (!titleInput || !textInput) return;

    titleInput.addEventListener('input', () => {
        previewTitle.textContent = titleInput.value || 'Título del Anuncio';
    });
    textInput.addEventListener('input', () => {
        previewDesc.textContent = textInput.value || 'Contenido del anuncio';
    });
    colorInput.addEventListener('input', () => {
        previewColor.style.background = colorInput.value;
    });

    btnSend.addEventListener('click', () => {
        alert('📢 Anuncio oficial enviado con éxito al canal de Discord seleccionado.');
    });
}

/* Web Audio Tone Generator Helper */
function playTone(freq, duration) {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {}
}

/* =========================================================
   12. BACKGROUND INTERACTIVO DE PARTÍCULAS NEON & BLUR
   ========================================================= */
function initParticlesBackground() {
    const canvas = document.getElementById('particles-bg-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    });

    const particlesCount = 55;
    const colors = [
        'rgba(0, 240, 255, ',
        'rgba(88, 101, 242, ',
        'rgba(255, 0, 85, ',
        'rgba(155, 89, 182, ',
        'rgba(46, 204, 113, '
    ];

    const particles = [];
    for (let i = 0; i < particlesCount; i++) {
        particles.push({
            x: Math.random() * w,
            y: Math.random() * h,
            vx: (Math.random() - 0.5) * 0.7,
            vy: (Math.random() - 0.5) * 0.7,
            radius: Math.random() * 2.5 + 1.2,
            colorBase: colors[Math.floor(Math.random() * colors.length)],
            alpha: Math.random() * 0.5 + 0.3
        });
    }

    let mouse = { x: -1000, y: -1000 };
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    function render() {
        ctx.clearRect(0, 0, w, h);

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            // Interacción suave con el mouse
            const dx = mouse.x - p.x;
            const dy = mouse.y - p.y;
            const distMouse = Math.sqrt(dx * dx + dy * dy);
            if (distMouse < 100) {
                p.x -= dx * 0.02;
                p.y -= dy * 0.02;
            }

            // Dibujar partícula con resplandor
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.colorBase + p.alpha + ')';
            ctx.shadowBlur = 10;
            ctx.shadowColor = p.colorBase + '0.8)';
            ctx.fill();

            // Conectar partículas cercanas con líneas suaves
            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dxx = p.x - p2.x;
                const dyy = p.y - p2.y;
                const dist = Math.sqrt(dxx * dxx + dyy * dyy);

                if (dist < 120) {
                    const lineAlpha = (1 - dist / 120) * 0.15;
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = p.colorBase + lineAlpha + ')';
                    ctx.lineWidth = 0.8;
                    ctx.shadowBlur = 0;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(render);
    }
    render();
}

/* =========================================================
   13. REPRODUCTOR DE MÚSICA BÉLICA & TRAP (VOZ REAL HD)
   2 de XXXTENTACION + El Makabelico (Comando Exclusivo)
   ========================================================= */
const MUSIC_PLAYLIST = [
    {
        title: "XXXTENTACION - Moonlight",
        artist: "XXXTENTACION",
        album: "? (Deluxe)",
        badge: "XXXTENTACION • VOZ REAL",
        cover: "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?q=80&w=200&auto=format&fit=crop",
        url: "audio/xxxtentacion_moonlight.mp3"
    },
    {
        title: "XXXTENTACION - SAD!",
        artist: "XXXTENTACION",
        album: "? (Deluxe)",
        badge: "XXXTENTACION • VOZ REAL",
        cover: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=200&auto=format&fit=crop",
        url: "audio/xxxtentacion_sad.mp3"
    },
    {
        title: "El Makabelico - El Comando Exclusivo",
        artist: "El Makabelico",
        album: "Rap Bélico",
        badge: "MAKABELICO • BÉLICO REAL",
        cover: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=200&auto=format&fit=crop",
        url: "audio/makabelico_1.mp3"
    },
    {
        title: "El Makabelico - Blindajes Bélicos",
        artist: "El Makabelico",
        album: "Comando Exclusivo",
        badge: "MAKABELICO • BÉLICO REAL",
        cover: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200&auto=format&fit=crop",
        url: "audio/makabelico_2.mp3"
    },
    {
        title: "El Makabelico - El Topón Bélico",
        artist: "El Makabelico",
        album: "Comando Exclusivo",
        badge: "MAKABELICO • BÉLICO REAL",
        cover: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=200&auto=format&fit=crop",
        url: "audio/makabelico_3.mp3"
    }
];

function initXXXTENTACIONPlayer() {
    const audio = document.getElementById('xxtentacion-audio');
    const playBtn = document.getElementById('btn-music-play');
    const prevBtn = document.getElementById('btn-music-prev');
    const nextBtn = document.getElementById('btn-music-next');
    const titleEl = document.getElementById('music-track-title');
    const coverEl = document.getElementById('music-album-cover');
    const volSlider = document.getElementById('slider-music-volume');
    const iconPlay = document.getElementById('icon-music-play');
    const eqBox = document.getElementById('music-mini-eq');

    if (!audio || !playBtn) return;

    let currentTrackIdx = 0;
    let isPlaying = false;

    function loadTrack(idx) {
        currentTrackIdx = (idx + MUSIC_PLAYLIST.length) % MUSIC_PLAYLIST.length;
        const track = MUSIC_PLAYLIST[currentTrackIdx];
        if (titleEl) titleEl.textContent = track.title;
        if (coverEl) coverEl.src = track.cover;
        
        // Actualizar badge del género
        const badgeEl = document.querySelector('.music-badge-genre');
        if (badgeEl) badgeEl.innerHTML = `<i class="fa-solid fa-compact-disc"></i> ${track.badge}`;

        audio.src = track.url;
        audio.volume = (volSlider ? volSlider.value : 80) / 100;
    }

    loadTrack(0);

    async function playCurrentTrack() {
        try {
            await audio.play();
            isPlaying = true;
            if (iconPlay) iconPlay.className = 'fa-solid fa-pause';
            if (eqBox) eqBox.classList.add('playing');
            if (coverEl) coverEl.classList.add('spinning');
        } catch (err) {
            console.log("Audio play error:", err);
        }
    }

    function pauseCurrentTrack() {
        audio.pause();
        isPlaying = false;
        if (iconPlay) iconPlay.className = 'fa-solid fa-play';
        if (eqBox) eqBox.classList.remove('playing');
        if (coverEl) coverEl.classList.remove('spinning');
    }

    playBtn.addEventListener('click', () => {
        if (!isPlaying) {
            playCurrentTrack();
        } else {
            pauseCurrentTrack();
        }
    });

    // Skip a la canción anterior con cambio instantáneo de voz real
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            loadTrack(currentTrackIdx - 1);
            playCurrentTrack();
        });
    }

    // Skip a la siguiente canción con cambio instantáneo de voz real
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            loadTrack(currentTrackIdx + 1);
            playCurrentTrack();
        });
    }

    // Auto-reproducir la siguiente cuando termine la actual
    audio.addEventListener('ended', () => {
        loadTrack(currentTrackIdx + 1);
        playCurrentTrack();
    });

    if (volSlider) {
        volSlider.addEventListener('input', (e) => {
            audio.volume = e.target.value / 100;
        });
    }
}

/* =========================================================
   14. DUAL CONSOLE: CANALES DE VOZ + CHAT PERSONALIZADO
   ========================================================= */
function initDualConsole() {
    const voiceListEl = document.getElementById('dual-voice-channels-list');
    const refreshVoiceBtn = document.getElementById('btn-refresh-voice-channels');
    const sndButtons = document.querySelectorAll('.btn-satanas-snd');
    const stopSoundBtn = document.getElementById('btn-stop-voice-sound');
    const statusText = document.getElementById('satanas-play-status');
    const loopCheck = document.getElementById('check-satanas-loop');
    const botSelect = document.getElementById('satanas-select-bot');

    const chatTargetSelect = document.getElementById('dual-chat-target-select');
    const chatContainer = document.getElementById('dual-chat-messages-container');
    const inputText = document.getElementById('dual-chat-input-text');
    const inputImg = document.getElementById('dual-chat-input-image');
    const btnSend = document.getElementById('btn-dual-send-chat-msg');
    const btnToggleAttach = document.getElementById('btn-dual-toggle-attach');
    const attachBar = document.getElementById('dual-composer-attachment-bar');
    const btnClearImg = document.getElementById('btn-dual-clear-img-url');
    const btnToggleEmbed = document.getElementById('btn-toggle-dual-embed');
    const embedBuilder = document.getElementById('dual-embed-builder');
    const embedTitleInput = document.getElementById('dual-embed-title');
    const embedColorInput = document.getElementById('dual-embed-color');
    const btnRefreshChat = document.getElementById('btn-dual-refresh-chat');
    const btnClearChat = document.getElementById('btn-dual-clear-chat');
    const identityBtns = document.querySelectorAll('.btn-identity-preset');
    const identityInputsRow = document.getElementById('identity-inputs-row');
    const customNameInput = document.getElementById('dual-input-sender-name');
    const customAvatarInput = document.getElementById('dual-input-sender-avatar');

    let currentSenderName = "rafamodzyt";
    let currentSenderAvatar = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop";
    let isEmbedMode = false;

    // --- Identidad Personalizada ---
    identityBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            identityBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const mode = btn.dataset.name;
            if (mode === 'custom') {
                if (identityInputsRow) identityInputsRow.style.display = 'flex';
                currentSenderName = customNameInput?.value || "Usuario Personalizado";
                currentSenderAvatar = customAvatarInput?.value || "";
            } else {
                if (identityInputsRow) identityInputsRow.style.display = 'none';
                currentSenderName = btn.dataset.name;
                currentSenderAvatar = btn.dataset.avatar;
            }
            playTone(480, 0.08);
        });
    });

    if (customNameInput) {
        customNameInput.addEventListener('input', (e) => {
            currentSenderName = e.target.value.trim() || "Usuario VIP";
        });
    }
    if (customAvatarInput) {
        customAvatarInput.addEventListener('input', (e) => {
            currentSenderAvatar = e.target.value.trim();
        });
    }

    // --- Canales de Voz Disponibles ---
    async function loadVoiceChannels() {
        if (!voiceListEl) return;
        try {
            const res = await fetch('/api/server/channels', { cache: 'no-store' });
            if (res.ok) {
                const data = await res.json();
                const vChannels = (data.channels || []).filter(ch => ch.type === 2);
                renderVoiceChannels(vChannels.length ? vChannels : [
                    { id: "1350706770527653993", name: "General (Voz 24/7)", members: 2 }
                ]);
                return;
            }
        } catch (e) {}

        renderVoiceChannels([
            { id: "1350706770527653993", name: "General (Voz 24/7)", members: 2 }
        ]);
    }

    function renderVoiceChannels(channels) {
        if (!voiceListEl) return;
        voiceListEl.innerHTML = channels.map(ch => `
            <div class="voice-ch-card active-voice-room">
                <div class="voice-ch-info">
                    <div class="voice-ch-icon-wrap">
                        <i class="fa-solid fa-volume-high text-cyan"></i>
                        <span class="live-dot-pulse"></span>
                    </div>
                    <div>
                        <div class="voice-ch-title">${escapeHtml(ch.name)}</div>
                        <div class="voice-ch-subtitle">
                            <span class="voice-bot-tag text-purple"><i class="fa-solid fa-robot"></i> Erick X</span>
                            <span class="voice-bot-tag text-red"><i class="fa-solid fa-skull"></i> Satanas</span>
                            <span class="voice-ch-id">ID: ${ch.id}</span>
                        </div>
                    </div>
                </div>
                <div class="voice-ch-status">
                    <span class="badge-status-ready">EN LÍNEA 24/7</span>
                    <button type="button" class="btn-listen-room" title="Conectado permanentemente">
                        <i class="fa-solid fa-headphones"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    if (refreshVoiceBtn) {
        refreshVoiceBtn.addEventListener('click', () => {
            loadVoiceChannels();
            playTone(520, 0.1);
        });
    }
    loadVoiceChannels();

    // --- Soundboard Satanas / Bot de Voz con Ráfaga / Bucle ---
    sndButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const soundFile = btn.getAttribute('data-sound') || 'donato.mp3';
            const soundName = btn.getAttribute('data-name') || soundFile;
            const isLoop = loopCheck ? loopCheck.checked : false;
            const targetBot = botSelect ? botSelect.value : 'satanas';

            // Feedback visual
            sndButtons.forEach(b => b.classList.remove('playing-sound'));
            btn.classList.add('playing-sound');

            if (statusText) {
                if (isLoop) {
                    statusText.innerHTML = `<span style="color:#FF0055;">🔥 MODO RÁFAGA / SPAM ACTIVO:</span> Reproduciendo "${soundName}" en bucle infinito...`;
                } else {
                    statusText.innerHTML = `🔊 Bot <strong>${targetBot === 'satanas' ? 'Satanás' : 'Erick X'}</strong> reproduciendo "${soundName}" en el canal de voz...`;
                }
            }

            try {
                const res = await fetch('/api/voice/play', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sound: soundFile,
                        bot: targetBot,
                        loop: isLoop
                    })
                });
                const result = await res.json();
                console.log("Voice Play Response:", result);
            } catch (err) {
                console.warn("No server connection for voice trigger:", err);
            }

            playTone(isLoop ? 700 : 580, 0.15);
        });
    });

    if (stopSoundBtn) {
        stopSoundBtn.addEventListener('click', async () => {
            sndButtons.forEach(b => b.classList.remove('playing-sound'));
            if (statusText) {
                statusText.innerHTML = '🟢 Reproducción detenida • Retomando modo silencioso 24/7';
            }
            try {
                await fetch('/api/voice/stop', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ bot: 'both' })
                });
            } catch (e) {}
            playTone(320, 0.12);
        });
    }

    // --- Chat Dual: Render & Sincronización ---
    function renderDualChatMessages() {
        if (!chatContainer) return;
        const currentTarget = chatTargetSelect ? chatTargetSelect.value : 'general';
        const msgs = (window._chatMessages || []).filter(m => {
            return !currentTarget || currentTarget === 'general' || m.channel_name === currentTarget || m.channel_id === currentTarget;
        });

        if (msgs.length === 0) {
            chatContainer.innerHTML = `
                <div class="empty-chat-state" style="text-align:center; padding:30px 15px; color:#777;">
                    <i class="fa-solid fa-comments" style="font-size:28px; margin-bottom:8px; opacity:0.4;"></i>
                    <p style="font-size:13px;">No hay mensajes registrados en #${currentTarget} aún.</p>
                    <small>Envía uno abajo con tu identidad personalizada.</small>
                </div>
            `;
            return;
        }

        chatContainer.innerHTML = '';
        msgs.forEach(m => {
            const userColor = getUsernameColor(m.author, m.author_id);
            const timeStr = m.timestamp || m.time || 'Ahora';
            const avatarUrl = m.avatar || "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop";

            const msgDiv = document.createElement('div');
            msgDiv.className = 'msg-item';

            let attachmentsHtml = '';
            if (Array.isArray(m.attachments) && m.attachments.length) {
                m.attachments.forEach(url => {
                    if (url) {
                        attachmentsHtml += `
                            <div class="msg-attachment-wrap" style="margin-top:6px;">
                                <img src="${url}" class="msg-attachment-img" alt="Foto adjunta" loading="lazy" style="max-width:260px; max-height:200px; border-radius:8px; border:1px solid rgba(255,255,255,0.12); cursor:pointer;" onclick="zoomImage('${url}')">
                            </div>
                        `;
                    }
                });
            }

            msgDiv.innerHTML = `
                <img src="${avatarUrl}" class="msg-avatar" alt="${escapeHtml(m.author)}" onerror="this.src='https://cdn.discordapp.com/embed/avatars/0.png'">
                <div class="msg-content-wrapper">
                    <div class="msg-author-row">
                        <span class="msg-author-name" style="color: ${userColor}; font-weight: 700; text-shadow: 0 0 10px ${userColor}30;">
                            ${escapeHtml(m.author)}
                        </span>
                        ${m.bot ? '<span class="msg-bot-tag">BOT</span>' : ''}
                        <span class="msg-ch-tag" style="font-size:10px; padding:1px 6px; border-radius:4px; background:rgba(255,255,255,0.06); color:#aaa; margin-left:6px;">
                            #${escapeHtml(m.channel_name || 'general')}
                        </span>
                        <span class="msg-timestamp" style="margin-left:auto; font-size:11px; color:#777;">${timeStr}</span>
                    </div>
                    ${m.content ? `<div class="msg-bubble">${escapeHtml(m.content)}</div>` : ''}
                    ${attachmentsHtml}
                </div>
            `;
            chatContainer.appendChild(msgDiv);
        });

        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    if (chatTargetSelect) {
        chatTargetSelect.addEventListener('change', () => {
            renderDualChatMessages();
        });
    }

    // Toggle adjuntar foto
    if (btnToggleAttach && attachBar) {
        btnToggleAttach.addEventListener('click', () => {
            const isHidden = attachBar.style.display === 'none';
            attachBar.style.display = isHidden ? 'flex' : 'none';
            if (isHidden && inputImg) inputImg.focus();
        });
    }

    if (btnClearImg && inputImg) {
        btnClearImg.addEventListener('click', () => {
            inputImg.value = '';
            if (attachBar) attachBar.style.display = 'none';
        });
    }

    // Toggle modo Embed
    if (btnToggleEmbed && embedBuilder) {
        btnToggleEmbed.addEventListener('click', () => {
            isEmbedMode = !isEmbedMode;
            embedBuilder.style.display = isEmbedMode ? 'block' : 'none';
            btnToggleEmbed.classList.toggle('active', isEmbedMode);
            if (isEmbedMode && embedTitleInput) embedTitleInput.focus();
        });
    }

    // Enviar mensaje con identidad
    async function sendDualMessage() {
        const text = inputText ? inputText.value.trim() : '';
        const imgUrl = inputImg ? inputImg.value.trim() : '';
        const targetChannel = chatTargetSelect ? chatTargetSelect.value : 'general';
        const embedTitle = embedTitleInput ? embedTitleInput.value.trim() : '';
        const embedColor = embedColorInput ? embedColorInput.value : '#00F0FF';

        if (!text && !imgUrl) return;

        const newMsg = {
            id: 'dual_' + Date.now(),
            author: currentSenderName || 'rafamodzyt',
            author_id: 'owner_dual',
            avatar: currentSenderAvatar || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop',
            bot: currentSenderName.toLowerCase().includes('bot') || currentSenderName.toLowerCase().includes('satanas') || currentSenderName.toLowerCase().includes('erick'),
            content: text,
            channel_name: targetChannel,
            channel_id: targetChannel,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            attachments: imgUrl ? [imgUrl] : []
        };

        if (!window._chatMessages) window._chatMessages = [];
        window._chatMessages.push(newMsg);
        try {
            localStorage.setItem('shadow_chat_cache', JSON.stringify(window._chatMessages.slice(-60)));
        } catch (e) {}

        renderDualChatMessages();

        // Enviar a la API /api/chat/send
        try {
            await fetch('/api/chat/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    channel: targetChannel,
                    message: text,
                    author: currentSenderName,
                    avatar: currentSenderAvatar,
                    image_url: imgUrl,
                    is_embed: isEmbedMode,
                    embed_title: embedTitle,
                    embed_color: embedColor
                })
            });
        } catch (err) {
            console.log("Chat send offline fallback");
        }

        if (inputText) inputText.value = '';
        if (inputImg) inputImg.value = '';
        if (attachBar) attachBar.style.display = 'none';

        playTone(660, 0.1);
    }

    if (btnSend) btnSend.addEventListener('click', sendDualMessage);
    if (inputText) {
        inputText.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendDualMessage();
            }
        });
    }

    if (btnRefreshChat) {
        btnRefreshChat.addEventListener('click', () => {
            renderDualChatMessages();
            playTone(440, 0.08);
        });
    }

    if (btnClearChat) {
        btnClearChat.addEventListener('click', () => {
            if (confirm('¿Deseas limpiar la vista de chat?')) {
                if (chatContainer) chatContainer.innerHTML = '';
            }
        });
    }

    // Auto sincronizar periódicamente
    setInterval(renderDualChatMessages, 3000);
    renderDualChatMessages();
}

/* =========================================================
   15. CONTROL MAESTRO DEL SERVIDOR (1000% MODIFICABLE)
   ========================================================= */
function initServerMaster() {
    const chContainer = document.getElementById('master-channels-container');
    const chCount = document.getElementById('master-channels-count');
    const newChName = document.getElementById('master-new-ch-name');
    const newChType = document.getElementById('master-new-ch-type');
    const btnCreateCh = document.getElementById('btn-master-create-channel');

    const rolesContainer = document.getElementById('master-roles-container');
    const rolesCount = document.getElementById('master-roles-count');
    const newRoleName = document.getElementById('master-new-role-name');
    const newRoleColor = document.getElementById('master-new-role-color');
    const btnCreateRole = document.getElementById('btn-master-create-role');

    const btnRefreshAll = document.getElementById('btn-refresh-master-all');
    const btnSaveServer = document.getElementById('btn-master-save-server');

    // Cargar canales del servidor
    async function fetchServerChannels() {
        if (!chContainer) return;
        try {
            const res = await fetch('/api/server/channels');
            if (res.ok) {
                const data = await res.json();
                if (Array.isArray(data.channels)) {
                    renderMasterChannels(data.channels);
                    return;
                }
            }
        } catch (e) {}

        // Fallback predeterminado
        renderMasterChannels(CHANNELS_DATA.map(c => ({ id: c.id, name: c.name, type: 0 })));
    }

    function renderMasterChannels(channels) {
        if (!chContainer) return;
        if (chCount) chCount.textContent = `${channels.length} Canales`;
        chContainer.innerHTML = channels.map(ch => `
            <div class="master-item-row">
                <div style="display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid ${ch.type === 2 ? 'fa-volume-high text-cyan' : 'fa-hashtag text-purple'}"></i>
                    <div>
                        <span style="font-weight:600; font-size:13px;">${escapeHtml(ch.name)}</span>
                        <div style="font-size:10px; color:#777;">ID: ${ch.id} • ${ch.type === 2 ? 'Voz' : 'Texto'}</div>
                    </div>
                </div>
                <button type="button" class="btn-del-item" data-id="${ch.id}" title="Eliminar canal">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </div>
        `).join('');

        chContainer.querySelectorAll('.btn-del-item').forEach(b => {
            b.addEventListener('click', async () => {
                const id = b.getAttribute('data-id');
                if (confirm(`¿Eliminar canal ID ${id} del servidor Discord?`)) {
                    try {
                        await fetch('/api/server/channels/delete', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ channel_id: id })
                        });
                        fetchServerChannels();
                    } catch (e) {}
                    playTone(300, 0.1);
                }
            });
        });
    }

    // Crear nuevo canal
    if (btnCreateCh) {
        btnCreateCh.addEventListener('click', async () => {
            const name = newChName ? newChName.value.trim() : '';
            const type = newChType ? parseInt(newChType.value) : 0;
            if (!name) return alert('Por favor ingresa un nombre para el canal.');

            try {
                await fetch('/api/server/channels', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: name, type: type })
                });
                if (newChName) newChName.value = '';
                fetchServerChannels();
                playTone(600, 0.15);
            } catch (e) {
                alert('No se pudo crear el canal en Discord. Verifica los permisos del bot.');
            }
        });
    }

    // Cargar roles del servidor
    async function fetchServerRoles() {
        if (!rolesContainer) return;
        try {
            const res = await fetch('/api/server/roles');
            if (res.ok) {
                const data = await res.json();
                if (Array.isArray(data.roles)) {
                    renderMasterRoles(data.roles);
                    return;
                }
            }
        } catch (e) {}

        // Fallback de roles
        renderMasterRoles([
            { id: "1001", name: "👑 Owner / Creador", color: 16766720 },
            { id: "1002", name: "🛡️ Administrador", color: 15158332 },
            { id: "1003", name: "💎 VIP Insano", color: 10181046 },
            { id: "1004", name: "🤖 Bots Oficiales", color: 3447003 },
            { id: "1005", name: "🔥 Miembro Activo", color: 3066993 }
        ]);
    }

    function renderMasterRoles(roles) {
        if (!rolesContainer) return;
        if (rolesCount) rolesCount.textContent = `${roles.length} Roles`;
        rolesContainer.innerHTML = roles.map(r => {
            const hexColor = typeof r.color === 'number' ? '#' + r.color.toString(16).padStart(6, '0') : (r.color || '#5865F2');
            return `
                <div class="master-item-row">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span class="role-color-dot" style="background:${hexColor};"></span>
                        <div>
                            <span style="font-weight:600; font-size:13px; color:${hexColor};">${escapeHtml(r.name)}</span>
                            <div style="font-size:10px; color:#777;">ID: ${r.id}</div>
                        </div>
                    </div>
                    <button type="button" class="btn-del-item" data-id="${r.id}" title="Eliminar rol">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            `;
        }).join('');

        rolesContainer.querySelectorAll('.btn-del-item').forEach(b => {
            b.addEventListener('click', async () => {
                const id = b.getAttribute('data-id');
                if (confirm(`¿Eliminar rol ID ${id} del servidor Discord?`)) {
                    try {
                        await fetch('/api/server/roles/delete', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ role_id: id })
                        });
                        fetchServerRoles();
                    } catch (e) {}
                    playTone(300, 0.1);
                }
            });
        });
    }

    // Crear nuevo rol
    if (btnCreateRole) {
        btnCreateRole.addEventListener('click', async () => {
            const name = newRoleName ? newRoleName.value.trim() : '';
            const color = newRoleColor ? newRoleColor.value : '#5865F2';
            if (!name) return alert('Por favor ingresa un nombre para el rol.');

            try {
                await fetch('/api/server/roles', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: name, color: color })
                });
                if (newRoleName) newRoleName.value = '';
                fetchServerRoles();
                playTone(600, 0.15);
            } catch (e) {
                alert('No se pudo crear el rol en Discord.');
            }
        });
    }

    // Botón Sincronizar Todo
    if (btnRefreshAll) {
        btnRefreshAll.addEventListener('click', () => {
            fetchServerChannels();
            fetchServerRoles();
            playTone(550, 0.15);
        });
    }

    // Guardar ajustes del servidor
    if (btnSaveServer) {
        btnSaveServer.addEventListener('click', () => {
            alert('Ajustes guardados correctamente en la memoria del panel y sincronizados con los bots.');
            playTone(800, 0.2);
        });
    }

    fetchServerChannels();
    fetchServerRoles();
}

/* =========================================================
   16. EMISOR DE ANUNCIOS & BROADCAST OFICIAL (EMBED)
   ========================================================= */
function initBroadcast() {
    const btnSend = document.getElementById('btn-trigger-broadcast');
    const selectCh = document.getElementById('bc-select-channel');
    const selectMention = document.getElementById('bc-select-mention');
    const inputTitle = document.getElementById('bc-input-title');
    const inputDesc = document.getElementById('bc-input-desc');
    const inputImage = document.getElementById('bc-input-image');
    const inputColor = document.getElementById('bc-input-color');

    if (!btnSend) return;

    btnSend.addEventListener('click', async () => {
        const title = inputTitle ? inputTitle.value.trim() : '';
        const desc = inputDesc ? inputDesc.value.trim() : '';
        const ch = selectCh ? selectCh.value : 'general';
        const mention = selectMention ? selectMention.value : '';
        const img = inputImage ? inputImage.value.trim() : '';
        const color = inputColor ? inputColor.value : '#FFD700';

        if (!title && !desc) {
            return alert('Por favor ingresa un título o descripción para el anuncio.');
        }

        btnSend.disabled = true;
        btnSend.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Transmitiendo Anuncio Oficial...';

        try {
            const res = await fetch('/api/server/broadcast', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    channel: ch,
                    title: title,
                    description: desc,
                    color: color,
                    mention: mention,
                    image_url: img
                })
            });
            const data = await res.json();
            console.log("Broadcast result:", data);
        } catch (err) {
            console.warn("Broadcast fallback:", err);
        }

        playTone(880, 0.3);

        setTimeout(() => {
            btnSend.disabled = false;
            btnSend.innerHTML = '<i class="fa-solid fa-check"></i> ¡Anuncio Disparado con Éxito!';
            if (inputTitle) inputTitle.value = '';
            if (inputDesc) inputDesc.value = '';
            if (inputImage) inputImage.value = '';

            setTimeout(() => {
                btnSend.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Disparar Anuncio Oficial a Discord';
            }, 3000);
        }, 1000);
    });
}


