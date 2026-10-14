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
   4. CHAT EN VIVO Y CANALES
   ========================================================= */
const CHANNELS_DATA = [
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

const INITIAL_MESSAGES = [
    { author: "SatanasMiPadre", bot: true, avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop", text: "🛡️ Bot Administrador conectado 24/7 a SHADOW BLOCK. Creado por rafamodzyt.", color: "cyan", time: "Hoy a las 04:00" },
    { author: "Erick X", bot: true, avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=200&auto=format&fit=crop", text: "🎙️ Voz 24/7 activa en General. Meta hacia 1,000,000 de horas en curso.", color: "green", time: "Hoy a las 04:02" },
    { author: "rafamodzyt", bot: false, avatar: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop", text: "¡El nuevo panel web y de C++ ya están disponibles para todos los miembros!", color: "default", time: "Hoy a las 04:05" }
];

function initChatSystem() {
    const listEl = document.getElementById('chat-channels-list');
    const msgsEl = document.getElementById('chat-messages-container');
    const curNameEl = document.getElementById('current-chat-ch-name');
    const curTopicEl = document.getElementById('current-chat-ch-topic');
    const inputEl = document.getElementById('chat-input-text');
    const btnSend = document.getElementById('btn-send-chat-msg');
    const colorSelect = document.getElementById('chat-color-select');

    if (!listEl || !msgsEl) return;

    // Render channels list
    listEl.innerHTML = '';
    CHANNELS_DATA.forEach((ch, idx) => {
        const btn = document.createElement('button');
        btn.className = `channel-btn ${idx === 0 ? 'active' : ''}`;
        btn.innerHTML = `<i class="fa-solid fa-hashtag"></i> <span>${ch.name}</span>`;
        btn.addEventListener('click', () => {
            document.querySelectorAll('.channel-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            curNameEl.textContent = ch.name;
            curTopicEl.textContent = ch.topic;
        });
        listEl.appendChild(btn);
    });

    // Render initial messages
    msgsEl.innerHTML = '';
    INITIAL_MESSAGES.forEach(m => appendMessage(m));

    function appendMessage(m) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'msg-item';
        msgDiv.innerHTML = `
            <img src="${m.avatar}" class="msg-avatar" alt="${m.author}">
            <div class="msg-content-wrapper">
                <div class="msg-author-row">
                    <span class="msg-author-name">${m.author}</span>
                    ${m.bot ? '<span class="msg-bot-tag">BOT</span>' : ''}
                    <span class="msg-timestamp">${m.time}</span>
                </div>
                <div class="msg-bubble color-${m.color}">${m.text}</div>
            </div>
        `;
        msgsEl.appendChild(msgDiv);
        msgsEl.scrollTop = msgsEl.scrollHeight;
    }

    function sendCurrent() {
        const text = inputEl.value.trim();
        if (!text) return;

        const color = colorSelect.value;
        const now = new Date();
        const timeStr = `Hoy a las ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

        appendMessage({
            author: "rafamodzyt (Panel Web)",
            bot: true,
            avatar: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop",
            text: text,
            color: color,
            time: timeStr
        });

        inputEl.value = '';
    }

    btnSend.addEventListener('click', sendCurrent);
    inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendCurrent();
    });

    // Shortcuts chips
    document.getElementById('btn-chip-booyah')?.addEventListener('click', () => {
        inputEl.value = "🏆 ¡¡¡BOOYAH!!! Victoria magistral en Free Fire para la escuadra.";
    });
    document.getElementById('btn-chip-gang')?.addEventListener('click', () => {
        inputEl.value = "👑 El Gang de Free Fire dominando Bermuda en clasificatoria.";
    });
    document.getElementById('btn-chip-donato')?.addEventListener('click', () => {
        inputEl.value = "🎯 Headshot pa tu casa crack de parte del Donato.";
    });
    document.getElementById('btn-chip-zelika')?.addEventListener('click', () => {
        inputEl.value = "⚡ Movimiento insano 360 grados y pared Gloo modo flash.";
    });
}

/* =========================================================
   5. GAME BOTS (MATCHMAKING FREE FIRE)
   ========================================================= */
function initGameBots() {
    const btnLaunch = document.getElementById('btn-launch-gamebots');
    const inputId = document.getElementById('gb-input-id');
    const selectReg = document.getElementById('gb-select-region');
    const resultBox = document.getElementById('gb-result-box');
    const emptyState = document.getElementById('gb-empty-state');
    const squadDisplay = document.getElementById('gb-squad-display');
    const squadNameEl = document.getElementById('gb-squad-name');
    const squadCodeEl = document.getElementById('gb-squad-code');
    const squadMembersEl = document.getElementById('gb-squad-members');

    if (!btnLaunch) return;

    btnLaunch.addEventListener('click', () => {
        const idVal = inputId.value.trim();
        if (!idVal || idVal.length < 5) {
            alert('⚠️ Por favor ingresa una ID de Free Fire válida (mínimo 5 dígitos).');
            return;
        }

        const regVal = selectReg.value;
        const teamNum = Math.floor(Math.random() * 9000) + 1000;
        const teamCode = `#FF-${Math.floor(Math.random() * 90000) + 10000}`;

        const botNames = [
            `[BOT] Alex_Insano_${Math.floor(Math.random() * 89) + 10}`,
            `[BOT] Ghost_Shadow_${Math.floor(Math.random() * 89) + 10}`,
            `[BOT] Cobra_King_${Math.floor(Math.random() * 89) + 10}`
        ];

        squadNameEl.textContent = `🔥 ESCUADRA BOTS HEROICA #${teamNum}`;
        squadCodeEl.textContent = `CÓDIGO DE SALA: ${teamCode}`;

        squadMembersEl.innerHTML = `
            <div class="squad-member-card">
                <div>👑 <strong>[LÍDER] ID: ${idVal}</strong> (Tu Cuenta)</div>
                <span class="badge-vip">${regVal}</span>
            </div>
            <div class="squad-member-card">
                <div>🤖 <strong>${botNames[0]}</strong> (Nivel 78 • Heroico)</div>
                <span class="badge-status-ready">CONECTADO</span>
            </div>
            <div class="squad-member-card">
                <div>🤖 <strong>${botNames[1]}</strong> (Nivel 82 • Gran Maestro)</div>
                <span class="badge-status-ready">CONECTADO</span>
            </div>
            <div class="squad-member-card">
                <div>🤖 <strong>${botNames[2]}</strong> (Nivel 75 • Heroico)</div>
                <span class="badge-status-ready">CONECTADO</span>
            </div>
        `;

        emptyState.classList.add('hidden');
        squadDisplay.classList.remove('hidden');

        // Play positive sound tone
        playTone(523.25, 0.2); // C5
        setTimeout(() => playTone(659.25, 0.3), 150); // E5
    });
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
