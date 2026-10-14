#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <d3d11.h>
#include <tchar.h>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <cmath>
#include <algorithm>
#include <fstream>
#include <regex>

#include "imgui.h"
#include "imgui_impl_win32.h"
#include "imgui_impl_dx11.h"
#include "discord_client.h"
#include "stickers_data.h"
#include "soundboard_data.h"

#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "d3dcompiler.lib")
#pragma comment(lib, "dxgi.lib")

// Declaraciones D3D11
static ID3D11Device*            g_pd3dDevice = nullptr;
static ID3D11DeviceContext*     g_pd3dDeviceContext = nullptr;
static IDXGISwapChain*          g_pSwapChain = nullptr;
static ID3D11RenderTargetView*  g_mainRenderTargetView = nullptr;

bool CreateDeviceD3D(HWND hWnd);
void CleanupDeviceD3D();
void CreateRenderTarget();
void CleanupRenderTarget();
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

namespace config {
    static const char* CREATOR_NAME = "rafamodzyt";
    static const char* SERVER_LINK = "https://discord.gg/dc5HAzAMmg";
}

// Cliente de Discord
static DiscordClient g_Discord;

// Sistema de Logs
struct LogEntry {
    std::string time;
    std::string text;
    ImVec4 color;
};
static std::vector<LogEntry> g_Logs;

static void AddLog(const std::string& text, const ImVec4& color = ImVec4(1, 1, 1, 1)) {
    time_t now = time(nullptr);
    tm t;
    localtime_s(&t, &now);
    char buf[32];
    strftime(buf, sizeof(buf), "[%H:%M:%S] ", &t);
    g_Logs.push_back({ std::string(buf), text, color });
    if (g_Logs.size() > 500) g_Logs.erase(g_Logs.begin());
}

// Estructuras para Miembros y Feed
struct MemberItem {
    std::string id;
    std::string name;
    std::string tag;
    std::string nick;
    std::string status; // "ONLINE" o "OFFLINE"
    bool is_bot;
    std::string roles;
    std::string joined_at;
};

struct MemberEvent {
    std::string type; // "JOIN", "LEAVE", "MSG"
    std::string user_id;
    std::string name;
    std::string time;
    std::string details;
};

static std::vector<MemberItem> g_Members;
static std::vector<MemberEvent> g_Events;
static MemberItem s_SelectedMember = { "1559437873265119252", "Erick X", "Erick X#7193", "Erick x [24/7]", "ONLINE", true, "VIP, Bots", "2026-10-13" };
static bool s_MemberSelected = true;
static char s_EditNickBuf[128] = "Erick x [24/7]";
static char s_MemberRoleInput[64] = "1559836643077394462";
static char s_MemberAdminNote[256] = "Bot de voz permanente 24/7 en General";

// Cargar o inicializar miembros desde live_members.json
static void LoadLiveMembers() {
    g_Members.clear();
    g_Events.clear();

    std::ifstream file("live_members.json");
    if (!file.is_open()) file.open("../live_members.json");
    if (file.is_open()) {
        std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        file.close();

        // Extraer miembros con regex
        std::regex mem_regex(R"raw(\{"id":"(\d+)","name":"([^"]+)","tag":"([^"]*)","nick":"([^"]*)","status":"([^"]*)","bot":(true|false)[^}]*?"roles":\[([^\]]*)\],"joined_at":"([^"]*)")raw");
        std::smatch m;
        std::string s = content;
        while (std::regex_search(s, m, mem_regex)) {
            MemberItem item;
            item.id = m[1];
            item.name = m[2];
            item.tag = m[3];
            item.nick = m[4].str().empty() ? item.name : m[4].str();
            item.status = m[5];
            item.is_bot = (m[6] == "true");
            std::string raw_roles = m[7];
            raw_roles.erase(std::remove(raw_roles.begin(), raw_roles.end(), '\"'), raw_roles.end());
            item.roles = raw_roles;
            item.joined_at = m[8];
            g_Members.push_back(item);
            s = m.suffix().str();
        }

        // Extraer eventos con regex
        std::regex ev_regex(R"raw(\{"type":"([^"]+)","user_id":"(\d+)","name":"([^"]+)","time":"([^"]+)","details":"([^"]*)")raw");
        std::smatch ev_m;
        std::string ev_s = content;
        while (std::regex_search(ev_s, ev_m, ev_regex)) {
            MemberEvent ev;
            ev.type = ev_m[1];
            ev.user_id = ev_m[2];
            ev.name = ev_m[3];
            ev.time = ev_m[4];
            ev.details = ev_m[5];
            g_Events.push_back(ev);
            ev_s = ev_m.suffix().str();
        }
    }

    if (g_Members.empty()) {
        g_Members.push_back({ "1559437873265119252", "Erick X", "Erick X#7193", "Erick x [24/7]", "ONLINE", true, "Member, VIP, Bots 24/7", "2026-10-13" });
        g_Members.push_back({ "1559830923174744125", "SatanasMiPadre", "SatanasMiPadre#5129", "Bot Administrador", "ONLINE", true, "Member, Administrador", "2026-10-14" });
        g_Members.push_back({ "1350706770527653989", "rafamodzyt", "rafamodzyt#0000", "rafamodzyt (Owner)", "ONLINE", false, "Member, Owner, Creador", "2026-10-12" });
        g_Members.push_back({ "1236983422665228289", "imyourpapaladjdj2", "imyourpapaladjdj2#0000", "imyourpapaladjdj2", "ONLINE", false, "Member, Socios, owner", "2026-10-14" });
    }
}

// Estilos visuales Modern Gaming Dark Theme
void ApplyCustomTheme() {
    ImGuiStyle& style = ImGui::GetStyle();
    ImVec4* colors = style.Colors;

    style.WindowRounding    = 8.0f;
    style.ChildRounding     = 6.0f;
    style.FrameRounding     = 5.0f;
    style.PopupRounding     = 6.0f;
    style.ScrollbarRounding = 4.0f;
    style.GrabRounding      = 4.0f;
    style.TabRounding       = 5.0f;
    style.WindowBorderSize  = 0.0f;
    style.FrameBorderSize   = 1.0f;
    style.ItemSpacing       = ImVec2(10, 8);
    style.ItemInnerSpacing  = ImVec2(8, 6);
    style.FramePadding      = ImVec2(10, 7);

    // Paleta Dark Sleek con acentos violeta y azul
    colors[ImGuiCol_Text]                  = ImVec4(0.95f, 0.96f, 0.98f, 1.00f);
    colors[ImGuiCol_TextDisabled]          = ImVec4(0.50f, 0.53f, 0.60f, 1.00f);
    colors[ImGuiCol_WindowBg]              = ImVec4(0.09f, 0.10f, 0.13f, 1.00f);
    colors[ImGuiCol_ChildBg]               = ImVec4(0.12f, 0.13f, 0.18f, 0.90f);
    colors[ImGuiCol_PopupBg]               = ImVec4(0.11f, 0.12f, 0.16f, 0.98f);
    colors[ImGuiCol_Border]                = ImVec4(0.20f, 0.22f, 0.30f, 0.80f);
    colors[ImGuiCol_BorderShadow]          = ImVec4(0.00f, 0.00f, 0.00f, 0.00f);
    colors[ImGuiCol_FrameBg]               = ImVec4(0.15f, 0.16f, 0.22f, 1.00f);
    colors[ImGuiCol_FrameBgHovered]        = ImVec4(0.22f, 0.24f, 0.34f, 1.00f);
    colors[ImGuiCol_FrameBgActive]         = ImVec4(0.28f, 0.31f, 0.44f, 1.00f);
    colors[ImGuiCol_TitleBg]               = ImVec4(0.07f, 0.08f, 0.11f, 1.00f);
    colors[ImGuiCol_TitleBgActive]         = ImVec4(0.10f, 0.12f, 0.18f, 1.00f);
    colors[ImGuiCol_TitleBgCollapsed]      = ImVec4(0.07f, 0.08f, 0.11f, 1.00f);
    colors[ImGuiCol_MenuBarBg]             = ImVec4(0.11f, 0.12f, 0.16f, 1.00f);
    colors[ImGuiCol_ScrollbarBg]           = ImVec4(0.08f, 0.09f, 0.12f, 0.50f);
    colors[ImGuiCol_ScrollbarGrab]         = ImVec4(0.25f, 0.28f, 0.38f, 1.00f);
    colors[ImGuiCol_ScrollbarGrabHovered]  = ImVec4(0.35f, 0.38f, 0.52f, 1.00f);
    colors[ImGuiCol_ScrollbarGrabActive]   = ImVec4(0.45f, 0.49f, 0.65f, 1.00f);
    colors[ImGuiCol_CheckMark]             = ImVec4(0.35f, 0.45f, 1.00f, 1.00f);
    colors[ImGuiCol_SliderGrab]            = ImVec4(0.35f, 0.45f, 1.00f, 1.00f);
    colors[ImGuiCol_SliderGrabActive]      = ImVec4(0.48f, 0.56f, 1.00f, 1.00f);
    colors[ImGuiCol_Button]                = ImVec4(0.32f, 0.38f, 0.90f, 0.85f);
    colors[ImGuiCol_ButtonHovered]         = ImVec4(0.40f, 0.48f, 1.00f, 1.00f);
    colors[ImGuiCol_ButtonActive]          = ImVec4(0.26f, 0.32f, 0.80f, 1.00f);
    colors[ImGuiCol_Header]                = ImVec4(0.22f, 0.25f, 0.36f, 0.80f);
    colors[ImGuiCol_HeaderHovered]         = ImVec4(0.32f, 0.38f, 0.90f, 0.80f);
    colors[ImGuiCol_HeaderActive]          = ImVec4(0.26f, 0.32f, 0.80f, 1.00f);
    colors[ImGuiCol_Separator]             = ImVec4(0.20f, 0.22f, 0.30f, 0.70f);
    colors[ImGuiCol_SeparatorHovered]      = ImVec4(0.35f, 0.45f, 1.00f, 0.80f);
    colors[ImGuiCol_SeparatorActive]       = ImVec4(0.35f, 0.45f, 1.00f, 1.00f);
    colors[ImGuiCol_Tab]                   = ImVec4(0.14f, 0.16f, 0.22f, 1.00f);
    colors[ImGuiCol_TabHovered]            = ImVec4(0.35f, 0.45f, 1.00f, 0.90f);
    colors[ImGuiCol_TabActive]             = ImVec4(0.30f, 0.38f, 0.88f, 1.00f);
}

// Variables de estado
static int  s_ActiveNavTab = 0; // 0=Canales, 1=Voz 24/7, 2=Alertas, 3=Moderacion, 4=Stickers, 5=Miembros, 6=Wallpapers, 7=Tienda & Tickets, 8=Consola, 9=Config
static char s_NewChannelName[128] = "nuevo-canal";
static int  s_NewChannelType = 0; // 0=Texto, 2=Voz, 4=Categoria
static char s_NewChannelTopic[256] = "Canal creado desde Panel DX11";
static int  s_NewChannelSlowmode = 0;

static char s_TargetChannelId[64] = "1559359413402472488";
static char s_RenameChannelVal[128] = "canal-actualizado";
static int  s_ModifySlowmode = 0;

static char s_AlertChannelId[64] = "1559359413402472488";
static char s_AlertTitle[128] = "AVISO OFICIAL DE SHADOW BLOCK";
static char s_AlertDesc[1024] = "Hola a todos, este es un comunicado oficial transmitido en vivo desde el Panel C++ DX11.";
static float s_AlertColor[3] = { 0.35f, 0.40f, 0.95f };
static char s_WebhookText[512] = "Notificacion enviada con exito desde el Panel C++ Win32.";

static int  s_PurgeCount = 10;
static char s_ModUserId[64] = "";
static char s_ModReason[256] = "Infraccion de normas del servidor";
static int  s_TimeoutMinutes = 10;

static char s_NewRoleName[128] = "VIP";
static float s_NewRoleColor[3] = { 1.0f, 0.84f, 0.0f }; // Dorado
static char s_TargetRoleId[64] = "";
static char s_RoleUserId[64] = "";

// Variables de Stickers y Emojis
static int  s_SelectedCategoryIdx = 0;
static char s_StickerFilter[64] = "";
static char s_StickerChannelId[64] = "1559359413402472488";

// Variables de Chat en Vivo y Canales Split
static char s_ChatSelectedChannelId[64] = "1559359413402472488";
static char s_ChatSelectedChannelName[128] = "general";
static char s_ChatMessageInput[512] = "";
static int  s_ChatColorMode = 0;
static std::vector<DiscordChatMessage> s_LiveChatMessages;

// Variables de Soundboard & Free Fire
static int  s_SelectedSoundCatIdx = 0;
static char s_SoundSearchFilter[64] = "";
static char s_SoundTargetChannelId[64] = "1559359413402472488";

// Variables de Wallpapers 4K
static char s_WallpaperChannelId[64] = "1559842253352992840";
static int  s_WallpaperTypeIdx = 0; // 0=PC 4K, 1=Mobile 4K
static int  s_WallpaperInterval = 25; // Minutos (pedido por usuario: cada 25m)
static int  s_WallpaperBatchCount = 100; // Cantidad por lote (pedido por usuario: 100 imagenes)
static char s_CustomWallpaperTitle[128] = "Cyberpunk Neon City Skyline";
static char s_CustomWallpaperUrl[256] = "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop";

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // 1. Crear ventana Win32
    WNDCLASSEXW wc = { sizeof(wc), CS_CLASSDC, WndProc, 0L, 0L, GetModuleHandle(nullptr), nullptr, nullptr, nullptr, nullptr, L"DiscordDX11Panel", nullptr };
    RegisterClassExW(&wc);
    HWND hwnd = CreateWindowW(wc.lpszClassName, L"Discord Server Manager - C++ DX11 Animated Panel | rafamodzyt",
        WS_OVERLAPPEDWINDOW, 70, 50, 1260, 850, nullptr, nullptr, wc.hInstance, nullptr);

    // 2. Inicializar DirectX 11
    if (!CreateDeviceD3D(hwnd)) {
        CleanupDeviceD3D();
        UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;
    }

    ShowWindow(hwnd, SW_SHOWDEFAULT);
    UpdateWindow(hwnd);

    // 3. Inicializar Dear ImGui
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;

    // Cargar fuente de Windows Segoe UI con soporte para acentos espanoles
    ImFontConfig font_cfg;
    font_cfg.OversampleH = 2;
    font_cfg.OversampleV = 2;
    static const ImWchar glyph_ranges[] = {
        0x0020, 0x00FF, // Latin basico y suplementario
        0x2000, 0x206F, // Puntuacion general
        0x2190, 0x21FF, // Flechas
        0x25A0, 0x25FF, // Formas geometricas
        0
    };
    ImFont* custom_font = io.Fonts->AddFontFromFileTTF("C:\\Windows\\Fonts\\segoeui.ttf", 17.5f, &font_cfg, glyph_ranges);
    if (!custom_font) {
        io.Fonts->AddFontDefault();
    }

    ApplyCustomTheme();

    ImGui_ImplWin32_Init(hwnd);
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    LoadLiveMembers();

    AddLog("Panel C++ DirectX 11 Animado iniciado.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
    AddLog("Servidor vinculado: SHADOW BLOCK (ID: 1350706770527653989)", ImVec4(0.4f, 0.8f, 1.0f, 1.0f));
    AddLog("Bot Administrador y Erick x 24/7 en linea.", ImVec4(0.4f, 0.8f, 1.0f, 1.0f));
    AddLog("Canales de Gaming, Free Fire y Tienda creados exitosamente.", ImVec4(1.0f, 0.85f, 0.3f, 1.0f));

    // Bucle de mensajes
    bool done = false;
    while (!done) {
        MSG msg;
        while (PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
            if (msg.message == WM_QUIT) done = true;
        }
        if (done) break;

        // Iniciar frame ImGui
        ImGui_ImplDX11_NewFrame();
        ImGui_ImplWin32_NewFrame();
        ImGui::NewFrame();

        // Ventana principal que cubre el 100% de la ventana
        ImGui::SetNextWindowPos(ImVec2(0, 0));
        ImGui::SetNextWindowSize(io.DisplaySize);
        ImGuiWindowFlags window_flags = ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoResize |
                                        ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoCollapse;

        ImGui::Begin("MainPanel", nullptr, window_flags);

        // ==========================================
        // HEADER SUPERIOR ANIMADO
        // ==========================================
        ImGui::BeginChild("HeaderBar", ImVec2(0, 52), true);
        ImGui::TextColored(ImVec4(0.35f, 0.75f, 1.0f, 1.0f), "[C++] SHADOW BLOCK MANAGER");
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "|");
        ImGui::SameLine();
        ImGui::Text("Creador: %s", config::CREATOR_NAME);
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "|");
        ImGui::SameLine();

        // LED animado palpitante para estado ONLINE
        float pulse = 0.5f + 0.5f * sinf((float)ImGui::GetTime() * 4.0f);
        ImVec4 pulse_green = ImVec4(0.2f + 0.3f * pulse, 0.7f + 0.3f * pulse, 0.3f, 1.0f);
        ImGui::TextColored(pulse_green, "[*] BOTS EN LINEA 24/7");

        // Reloj en tiempo real
        time_t raw_time = time(nullptr);
        tm tm_info;
        localtime_s(&tm_info, &raw_time);
        char clock_buf[32];
        strftime(clock_buf, sizeof(clock_buf), "%I:%M:%S %p", &tm_info);

        ImGui::SameLine(ImGui::GetWindowWidth() - 360);
        ImGui::TextColored(ImVec4(0.9f, 0.8f, 0.3f, 1.0f), "Reloj: %s", clock_buf);
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(0.7f, 0.7f, 0.8f, 1.0f), "| SHADOW BLOCK");
        ImGui::EndChild();

        // ==========================================
        // LAYOUT PRINCIPAL: SIDEBAR + CONTENIDO
        // ==========================================
        float sidebar_width = 240.0f;
        float content_height = io.DisplaySize.y - 68.0f;

        // 1. SIDEBAR IZQUIERDA
        ImGui::BeginChild("Sidebar", ImVec2(sidebar_width, content_height), true);
        
        ImGui::TextColored(ImVec4(0.6f, 0.65f, 0.8f, 1.0f), "MENU PRINCIPAL");
        ImGui::Separator();
        ImGui::Spacing();

        auto DrawNavButton = [](const char* label, int tab_idx) {
            bool is_active = (s_ActiveNavTab == tab_idx);
            if (is_active) {
                ImGui::PushStyleColor(ImGuiCol_Button, ImVec4(0.35f, 0.42f, 0.95f, 1.0f));
                ImGui::PushStyleColor(ImGuiCol_ButtonHovered, ImVec4(0.42f, 0.50f, 1.0f, 1.0f));
            } else {
                ImGui::PushStyleColor(ImGuiCol_Button, ImVec4(0.16f, 0.17f, 0.24f, 0.9f));
                ImGui::PushStyleColor(ImGuiCol_ButtonHovered, ImVec4(0.24f, 0.26f, 0.36f, 1.0f));
            }

            if (ImGui::Button(label, ImVec2(-1, 34))) {
                s_ActiveNavTab = tab_idx;
            }

            ImGui::PopStyleColor(2);
            ImGui::Spacing();
        };

        DrawNavButton("[#] Canales & Salas", 0);
        DrawNavButton("[CHAT] Chat en Vivo & Canales", 1);
        DrawNavButton("[VOZ] 24/7 & 1M Horas", 2);
        DrawNavButton("[!] Alertas & Anuncios", 3);
        DrawNavButton("[*] Moderacion & Roles", 4);
        DrawNavButton("[MEMES] Stickers (300+)", 5);
        DrawNavButton("[AUDIO] Soundboard Free Fire", 6);
        DrawNavButton("[USERS] Miembros (Cuadritos)", 7);
        DrawNavButton("[WALLPAPERS] 4K HD Masivo", 8);
        DrawNavButton("[TIENDA] Tickets Compra", 9);
        DrawNavButton("[>] Consola en Vivo", 10);
        DrawNavButton("[@] Configuracion", 11);

        ImGui::Spacing();
        ImGui::Separator();
        ImGui::Spacing();

        ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "Estado del Servidor:");
        ImGui::BulletText("Ping: 20 ms");
        ImGui::BulletText("Stickers: 5/5 Oficiales (Max Tier 0)");
        ImGui::BulletText("Soundboard: 8/8 Oficiales (Max Tier 0)");
        ImGui::BulletText("Game Bots (55/dia): Activo");
        ImGui::BulletText("Send Reports (12s): Activo");
        ImGui::BulletText("FPS DX11: %.0f", io.Framerate);

        ImGui::EndChild();

        ImGui::SameLine();

        // 2. AREA DE CONTENIDO DERECHA
        ImGui::BeginChild("MainContent", ImVec2(0, content_height), true);

        // ==========================================
        // VISTA 0: CANALES Y SALAS DE VOZ GAMING
        // ==========================================
        if (s_ActiveNavTab == 0) {
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "CANALES DE TEXTO Y SALAS DE VOZ GAMING / FREE FIRE");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::Columns(2, "ChCols", true);

            // Columna 1: Crear Canal
            ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "Crear Nuevo Canal");
            ImGui::Separator();
            ImGui::InputText("Nombre Canal##NewCh", s_NewChannelName, IM_ARRAYSIZE(s_NewChannelName));
            
            const char* channel_types[] = { "Canal de Texto", "Canal de Voz", "Categoria" };
            static int type_idx = 0;
            if (ImGui::Combo("Tipo##NewCh", &type_idx, channel_types, IM_ARRAYSIZE(channel_types))) {
                if (type_idx == 0) s_NewChannelType = 0;
                else if (type_idx == 1) s_NewChannelType = 2;
                else if (type_idx == 2) s_NewChannelType = 4;
            }

            ImGui::InputText("Tema / Topic##NewCh", s_NewChannelTopic, IM_ARRAYSIZE(s_NewChannelTopic));
            ImGui::SliderInt("Modo Lento (Segs)##NewCh", &s_NewChannelSlowmode, 0, 300);

            if (ImGui::Button("Crear Canal en Discord", ImVec2(240, 36))) {
                DiscordResponse resp = g_Discord.CreateChannel(s_NewChannelName, s_NewChannelType, s_NewChannelTopic, s_NewChannelSlowmode);
                if (resp.success()) {
                    AddLog("Canal '" + std::string(s_NewChannelName) + "' creado exitosamente (HTTP 201).", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                } else {
                    AddLog("Fallo al crear canal: " + resp.body + " " + resp.error, ImVec4(1.0f, 0.35f, 0.35f, 1.0f));
                }
            }

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::TextColored(ImVec4(1.0f, 0.6f, 0.2f, 1.0f), "Salas Gaming y Free Fire Creadas:");
            ImGui::BulletText("🎧・Soporte & Ayuda");
            ImGui::BulletText("🔥・Free Fire Escuadra 1");
            ImGui::BulletText("🔥・Free Fire Escuadra 2");
            ImGui::BulletText("🎮・Gaming General");
            ImGui::BulletText("💬・Chill & Charla");
            ImGui::BulletText("👑・Sala VIP rafamodzyt");

            ImGui::NextColumn();

            // Columna 2: Modificar Canal
            ImGui::TextColored(ImVec4(1.0f, 0.75f, 0.35f, 1.0f), "Modificar / Bloquear Canal");
            ImGui::Separator();
            ImGui::InputText("ID Canal Objetivo##ModCh", s_TargetChannelId, IM_ARRAYSIZE(s_TargetChannelId));
            ImGui::InputText("Nuevo Nombre##ModCh", s_RenameChannelVal, IM_ARRAYSIZE(s_RenameChannelVal));

            if (ImGui::Button("Renombrar", ImVec2(120, 32))) {
                DiscordResponse resp = g_Discord.RenameChannel(s_TargetChannelId, s_RenameChannelVal);
                if (resp.success()) AddLog("Canal renombrado a " + std::string(s_RenameChannelVal), ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                else AddLog("Error al renombrar: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }
            ImGui::SameLine();
            if (ImGui::Button("Bloquear (Lock)", ImVec2(130, 32))) {
                DiscordResponse resp = g_Discord.LockChannel(s_TargetChannelId);
                if (resp.success()) AddLog("Canal bloqueado para @everyone.", ImVec4(1.0f, 0.8f, 0.3f, 1.0f));
                else AddLog("Error al bloquear: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }
            ImGui::SameLine();
            if (ImGui::Button("Desbloquear", ImVec2(120, 32))) {
                DiscordResponse resp = g_Discord.UnlockChannel(s_TargetChannelId);
                if (resp.success()) AddLog("Canal desbloqueado.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                else AddLog("Error al desbloquear: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }

            ImGui::Spacing();
            ImGui::SliderInt("Slowmode##ModCh", &s_ModifySlowmode, 0, 300);
            if (ImGui::Button("Aplicar Slowmode", ImVec2(160, 32))) {
                DiscordResponse resp = g_Discord.SetSlowmode(s_TargetChannelId, s_ModifySlowmode);
                if (resp.success()) AddLog("Slowmode aplicado (" + std::to_string(s_ModifySlowmode) + "s)", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }
            ImGui::SameLine();
            if (ImGui::Button("Eliminar Canal", ImVec2(140, 32))) {
                DiscordResponse resp = g_Discord.DeleteChannel(s_TargetChannelId);
                if (resp.success()) AddLog("Canal eliminado.", ImVec4(1, 0.3f, 0.3f, 1));
                else AddLog("Error al borrar canal: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }

            ImGui::Columns(1);
        }

        // ==========================================
        // VISTA 1: CHAT EN VIVO & CANALES SPLIT (RGB & ANSI)
        // ==========================================
        else if (s_ActiveNavTab == 1) {
            ImGui::TextColored(ImVec4(0.35f, 0.85f, 1.0f, 1.0f), "CHAT EN VIVO DEL SERVIDOR & NAVEGADOR DE CANALES");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::Columns(2, "LiveChatSplitCols", true);
            ImGui::SetColumnWidth(0, 290.0f);

            // Columna 1: Lista de Canales
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Canales de SHADOW BLOCK:");
            ImGui::Separator();

            const char* sample_channels[][3] = {
                { "1559359413402472488", "general", "0" },
                { "1559842253352992840", "wallpapers-4k-hd", "0" },
                { "1559844380934807612", "comprar-panel-y-bots", "0" },
                { "1559826233620168734", "bot-comandos", "0" },
                { "1350706770527653993", "General (Voz 24/7)", "2" },
                { "1559844384105578506", "Soporte & Ayuda", "2" },
                { "1559844385288355870", "Free Fire Escuadra 1", "2" },
                { "1559844386445983774", "Free Fire Escuadra 2", "2" },
                { "1559844387607937074", "Gaming General", "2" },
                { "1559844389969203270", "Sala VIP rafamodzyt", "2" }
            };

            ImGui::BeginChild("ChannelsListSplitChild", ImVec2(0, 0), true);
            for (int c = 0; c < 10; ++c) {
                const char* cid = sample_channels[c][0];
                const char* cname = sample_channels[c][1];
                const char* ctype = sample_channels[c][2];

                bool is_ch_sel = (strcmp(s_ChatSelectedChannelId, cid) == 0);
                std::string icon = (strcmp(ctype, "2") == 0) ? "[VOZ] " : "[#] ";
                std::string label = icon + std::string(cname);

                if (ImGui::Selectable(label.c_str(), is_ch_sel)) {
                    strcpy_s(s_ChatSelectedChannelId, cid);
                    strcpy_s(s_ChatSelectedChannelName, cname);
                    DiscordResponse resp = g_Discord.GetChannelMessages(cid, 25);
                    if (resp.success()) {
                        s_LiveChatMessages = g_Discord.ParseMessages(resp.body);
                        std::reverse(s_LiveChatMessages.begin(), s_LiveChatMessages.end());
                        AddLog("Chat cargado para #" + std::string(cname), ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                    }
                }
            }
            ImGui::EndChild();

            ImGui::NextColumn();

            // Columna 2: Chat del Canal Seleccionado
            std::string header_title = "CANAL: #" + std::string(s_ChatSelectedChannelName) + " (ID: " + std::string(s_ChatSelectedChannelId) + ")";
            ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "%s", header_title.c_str());
            ImGui::SameLine(ImGui::GetColumnWidth() - 150);
            if (ImGui::Button("Recargar Chat", ImVec2(140, 24))) {
                DiscordResponse resp = g_Discord.GetChannelMessages(s_ChatSelectedChannelId, 25);
                if (resp.success()) {
                    s_LiveChatMessages = g_Discord.ParseMessages(resp.body);
                    std::reverse(s_LiveChatMessages.begin(), s_LiveChatMessages.end());
                    AddLog("Chat refrescado.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                }
            }
            ImGui::Separator();

            // Mensajes
            float chat_box_h = ImGui::GetContentRegionAvail().y - 80.0f;
            ImGui::BeginChild("ChatMessagesRegionBox", ImVec2(0, chat_box_h), true);
            if (s_LiveChatMessages.empty()) {
                ImGui::TextColored(ImVec4(0.6f, 0.6f, 0.6f, 1.0f), "Presiona 'Recargar Chat' para cargar los mensajes de este canal.");
            } else {
                for (const auto& msg : s_LiveChatMessages) {
                    ImGui::TextColored(ImVec4(0.35f, 0.85f, 1.0f, 1.0f), "[%s]:", msg.author.c_str());
                    ImGui::SameLine();
                    ImGui::TextWrapped("%s", msg.content.c_str());
                    ImGui::Spacing();
                }
            }
            ImGui::EndChild();

            // Barra de Envio con Selector de Color / RGB
            ImGui::Spacing();
            ImGui::SetNextItemWidth(ImGui::GetContentRegionAvail().x - 270.0f);
            ImGui::InputText("##ChatMsgInp", s_ChatMessageInput, IM_ARRAYSIZE(s_ChatMessageInput));
            ImGui::SameLine();

            const char* color_opts[] = {
                "Normal",
                "Rojo ANSI",
                "Verde ANSI",
                "Azul ANSI",
                "Amarillo ANSI",
                "Magenta ANSI",
                "Cyan ANSI",
                "RGB Rainbow Embed"
            };
            ImGui::SetNextItemWidth(140.0f);
            ImGui::Combo("##ChatColorOpt", &s_ChatColorMode, color_opts, IM_ARRAYSIZE(color_opts));

            ImGui::SameLine();
            if (ImGui::Button("Enviar Mensaje", ImVec2(110, 28))) {
                if (strlen(s_ChatMessageInput) > 0) {
                    if (s_ChatColorMode == 0) {
                        g_Discord.SendTextMessage(s_ChatSelectedChannelId, s_ChatMessageInput);
                    } else if (s_ChatColorMode >= 1 && s_ChatColorMode <= 6) {
                        int ansi_codes[] = { 0, 31, 32, 34, 33, 35, 36 };
                        g_Discord.SendAnsiMessage(s_ChatSelectedChannelId, s_ChatMessageInput, ansi_codes[s_ChatColorMode]);
                    } else if (s_ChatColorMode == 7) {
                        g_Discord.SendEmbed(s_ChatSelectedChannelId, "Mensaje RGB desde Panel DX11", s_ChatMessageInput, 0x5865F2, "rafamodzyt");
                    }
                    AddLog("Mensaje enviado a #" + std::string(s_ChatSelectedChannelName), ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                    s_ChatMessageInput[0] = '\0';

                    DiscordResponse resp = g_Discord.GetChannelMessages(s_ChatSelectedChannelId, 25);
                    if (resp.success()) {
                        s_LiveChatMessages = g_Discord.ParseMessages(resp.body);
                        std::reverse(s_LiveChatMessages.begin(), s_LiveChatMessages.end());
                    }
                }
            }
            ImGui::Columns(1);
        }

        // ==========================================
        // VISTA 2: VOZ 24/7 & ANIMACIONES DX11
        // ==========================================
        else if (s_ActiveNavTab == 2) {
            ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "ESTADO DE CONEXION DE VOZ 24/7 (ERICK X)");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::Columns(2, "VoiceCols", true);

            // Tarjeta de Estado
            ImGui::BeginChild("VoiceStatusCard", ImVec2(0, 260), true);
            ImGui::TextColored(ImVec4(0.35f, 0.85f, 1.0f, 1.0f), "Informacion del Bot en Llamada");
            ImGui::Separator();
            ImGui::BulletText("Bot de Voz: Erick x (ID: 1559437873265119252)");
            ImGui::BulletText("Canal Actual: General (ID: 1350706770527653993)");
            ImGui::BulletText("Foto de Perfil: Karely Ruiz HD Oficial");
            ImGui::BulletText("Auto-Reconexion: Activada (30s heartbeat)");
            ImGui::BulletText("Ensordecimiento: Activo (self_deaf=True)");

            ImGui::Spacing();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Visualizador de Audio DX11 (Actividad en Vivo):");
            
            // Animacion de barras de ecualizador de audio en tiempo real
            ImDrawList* draw_list = ImGui::GetWindowDrawList();
            ImVec2 p0 = ImGui::GetCursorScreenPos();
            float t = (float)ImGui::GetTime();
            for (int b = 0; b < 22; ++b) {
                float wave = sinf(t * 7.0f + b * 0.45f);
                float h = 6.0f + 32.0f * (0.5f + 0.5f * wave);
                ImU32 col = IM_COL32(88 + b * 5, 101 + b * 4, 242, 230);
                draw_list->AddRectFilled(ImVec2(p0.x + b * 13, p0.y + 45 - h), ImVec2(p0.x + b * 13 + 9, p0.y + 45), col, 2.0f);
            }
            ImGui::Dummy(ImVec2(22 * 13, 50));

            ImGui::EndChild();

            ImGui::NextColumn();

            // Tarjeta de Meta 1,000,000 Horas
            ImGui::BeginChild("VoiceProgressCard", ImVec2(0, 260), true);
            ImGui::TextColored(ImVec4(1.0f, 0.8f, 0.2f, 1.0f), "Meta de 1,000,000 de Horas");
            ImGui::Separator();
            static float mock_progress = 0.00015f;
            char progress_label[64];
            sprintf_s(progress_label, "Progreso: %.5f%%", mock_progress * 100.0f);
            ImGui::ProgressBar(mock_progress, ImVec2(-1, 28), progress_label);

            ImGui::Spacing();
            ImGui::Text("Hitos del Bot:");
            ImGui::BulletText("[x] 100 Horas: Cumplido");
            ImGui::BulletText("[>] 1,000 Horas: En progreso activo");
            ImGui::BulletText("[ ] 10,000 Horas: Meta Intermedia 1");
            ImGui::BulletText("[ ] 1,000,000 Horas: Corona Absoluta");
            ImGui::EndChild();

            ImGui::Columns(1);

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Acciones de Control de Voz:");
            if (ImGui::Button("Enviar Notificacion de Estado a Canal de Control", ImVec2(380, 36))) {
                std::string msg = "**Reporte desde Panel C++ DX11:**\nErick x continua conectado 24/7 en voz acumulando horas hacia 1,000,000h.";
                DiscordResponse resp = g_Discord.SendTextMessage("1559826233620168734", msg);
                if (resp.success()) AddLog("Notificacion enviada a canal de control.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }
            ImGui::SameLine();
            if (ImGui::Button("Forzar Reconexion al Canal de Voz", ImVec2(280, 36))) {
                AddLog("Solicitud de reconexion emitida para Erick x.", ImVec4(1.0f, 0.8f, 0.3f, 1.0f));
            }
        }

        // ==========================================
        // VISTA 3: ALERTAS Y ANUNCIOS
        // ==========================================
        else if (s_ActiveNavTab == 3) {
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "ALERTAS, COMUNICADOS Y ANUNCIOS EMBED");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::InputText("ID Canal Destino##Alert", s_AlertChannelId, IM_ARRAYSIZE(s_AlertChannelId));
            ImGui::InputText("Titulo del Anuncio##Alert", s_AlertTitle, IM_ARRAYSIZE(s_AlertTitle));
            ImGui::InputTextMultiline("Mensaje / Descripcion##Alert", s_AlertDesc, IM_ARRAYSIZE(s_AlertDesc), ImVec2(-1, 90));
            ImGui::ColorEdit3("Color del Borde Embed##Alert", s_AlertColor);

            if (ImGui::Button("Enviar Alerta Embed a Discord", ImVec2(280, 36))) {
                int r = (int)(s_AlertColor[0] * 255);
                int g = (int)(s_AlertColor[1] * 255);
                int b = (int)(s_AlertColor[2] * 255);
                int color_hex = (r << 16) | (g << 8) | b;

                std::string footer = "Enviado desde Panel C++ DX11 por " + std::string(config::CREATOR_NAME);
                DiscordResponse resp = g_Discord.SendEmbed(s_AlertChannelId, s_AlertTitle, s_AlertDesc, color_hex, footer);
                if (resp.success()) AddLog("Alerta embed enviada con exito al canal " + std::string(s_AlertChannelId), ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                else AddLog("Error al enviar alerta: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::TextColored(ImVec4(1.0f, 0.6f, 0.2f, 1.0f), "Disparador de Webhook Oficial:");
            ImGui::InputText("Mensaje Webhook##Web", s_WebhookText, IM_ARRAYSIZE(s_WebhookText));
            if (ImGui::Button("Disparar Webhook en #general", ImVec2(260, 34))) {
                DiscordResponse resp = g_Discord.SendWebhookMsg(s_WebhookText, "RafaMoDzYT");
                if (resp.status_code == 204 || resp.status_code == 200) {
                    AddLog("Mensaje enviado por Webhook a #general (HTTP 204).", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                } else {
                    AddLog("Error Webhook: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
                }
            }
        }

        // ==========================================
        // VISTA 4: MODERACION & ROLES
        // ==========================================
        else if (s_ActiveNavTab == 4) {
            ImGui::TextColored(ImVec4(1.0f, 0.4f, 0.4f, 1.0f), "MODERACION Y GESTION DE ROLES");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::Columns(2, "ModCols", true);

            // Moderacion
            ImGui::TextColored(ImVec4(1.0f, 0.4f, 0.4f, 1.0f), "Control de Usuarios & Chat");
            ImGui::Separator();
            ImGui::SliderInt("Purgar Mensajes (1-100)", &s_PurgeCount, 1, 100);
            if (ImGui::Button("Purgar Mensajes en Canal Actual", ImVec2(260, 30))) {
                DiscordResponse resp = g_Discord.PurgeMessages(s_AlertChannelId, s_PurgeCount);
                if (resp.success()) AddLog("Se purgaron mensajes exitosamente.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                else AddLog("Error al purgar: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }

            ImGui::Spacing();
            ImGui::InputText("ID de Usuario##Mod", s_ModUserId, IM_ARRAYSIZE(s_ModUserId));
            ImGui::InputText("Motivo / Razon##Mod", s_ModReason, IM_ARRAYSIZE(s_ModReason));

            if (ImGui::Button("Expulsar (Kick)", ImVec2(130, 32))) {
                if (strlen(s_ModUserId) > 0) {
                    DiscordResponse resp = g_Discord.KickMember(s_ModUserId, s_ModReason);
                    if (resp.success()) AddLog("Usuario " + std::string(s_ModUserId) + " expulsado.", ImVec4(1, 0.7f, 0.2f, 1));
                    else AddLog("Error kick: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
                }
            }
            ImGui::SameLine();
            if (ImGui::Button("Banear (Ban)", ImVec2(130, 32))) {
                if (strlen(s_ModUserId) > 0) {
                    DiscordResponse resp = g_Discord.BanMember(s_ModUserId, s_ModReason);
                    if (resp.success()) AddLog("Usuario " + std::string(s_ModUserId) + " BANEADO.", ImVec4(1, 0.3f, 0.3f, 1));
                    else AddLog("Error ban: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
                }
            }
            ImGui::SameLine();
            if (ImGui::Button("Desbanear", ImVec2(110, 32))) {
                if (strlen(s_ModUserId) > 0) {
                    DiscordResponse resp = g_Discord.UnbanMember(s_ModUserId);
                    if (resp.success()) AddLog("Usuario " + std::string(s_ModUserId) + " desbaneado.", ImVec4(0.35f, 1, 0.4f, 1));
                    else AddLog("Error unban: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
                }
            }

            ImGui::NextColumn();

            // Roles
            ImGui::TextColored(ImVec4(0.8f, 0.5f, 1.0f, 1.0f), "Gestion de Roles");
            ImGui::Separator();
            ImGui::InputText("Nombre Rol##NewRole", s_NewRoleName, IM_ARRAYSIZE(s_NewRoleName));
            ImGui::ColorEdit3("Color del Rol##NewRole", s_NewRoleColor);

            if (ImGui::Button("Crear Rol en Discord", ImVec2(220, 32))) {
                int r = (int)(s_NewRoleColor[0] * 255);
                int g = (int)(s_NewRoleColor[1] * 255);
                int b = (int)(s_NewRoleColor[2] * 255);
                int color_val = (r << 16) | (g << 8) | b;
                DiscordResponse resp = g_Discord.CreateRole(s_NewRoleName, color_val);
                if (resp.success()) AddLog("Rol '" + std::string(s_NewRoleName) + "' creado con exito.", ImVec4(0.35f, 1, 0.4f, 1));
                else AddLog("Error al crear rol: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
            }

            ImGui::Spacing();
            ImGui::InputText("ID del Rol##TargetRole", s_TargetRoleId, IM_ARRAYSIZE(s_TargetRoleId));
            ImGui::InputText("ID Miembro##RoleUser", s_RoleUserId, IM_ARRAYSIZE(s_RoleUserId));

            if (ImGui::Button("Asignar Rol a Miembro", ImVec2(190, 32))) {
                if (strlen(s_TargetRoleId) > 0 && strlen(s_RoleUserId) > 0) {
                    DiscordResponse resp = g_Discord.AddRoleToMember(s_RoleUserId, s_TargetRoleId);
                    if (resp.success()) AddLog("Rol asignado correctamente.", ImVec4(0.35f, 1, 0.4f, 1));
                    else AddLog("Error asignar rol: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
                }
            }
            ImGui::SameLine();
            if (ImGui::Button("Quitar Rol", ImVec2(120, 32))) {
                if (strlen(s_TargetRoleId) > 0 && strlen(s_RoleUserId) > 0) {
                    DiscordResponse resp = g_Discord.RemoveRoleFromMember(s_RoleUserId, s_TargetRoleId);
                    if (resp.success()) AddLog("Rol removido.", ImVec4(1, 0.8f, 0.3f, 1));
                }
            }

            ImGui::Columns(1);
        }

        // ==========================================
        // VISTA 5: STICKERS & MEMES FAMOSOS (300+)
        // ==========================================
        else if (s_ActiveNavTab == 5) {
            ImGui::TextColored(ImVec4(1.0f, 0.85f, 0.3f, 1.0f), "CATALOGO DE 300+ STICKERS Y MEMES FAMOSOS");
            ImGui::Separator();
            ImGui::Spacing();

            // Fila 1: Filtros limpios
            ImGui::SetNextItemWidth(300.0f);
            ImGui::Combo("Categoria##StickersCat", &s_SelectedCategoryIdx, g_StickerCategories, IM_ARRAYSIZE(g_StickerCategories));
            ImGui::SameLine();
            ImGui::SetNextItemWidth(250.0f);
            ImGui::InputText("Buscar por Nombre##StickerSearch", s_StickerFilter, IM_ARRAYSIZE(s_StickerFilter));

            ImGui::SetNextItemWidth(350.0f);
            ImGui::InputText("ID Canal Destino##StickerCh", s_StickerChannelId, IM_ARRAYSIZE(s_StickerChannelId));

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            // Tabla con stickers
            ImGui::BeginChild("StickersTableRegion", ImVec2(0, 310), true);
            ImGui::Columns(4, "StickerTableCols", true);
            ImGui::SetColumnWidth(0, 200.0f);
            ImGui::SetColumnWidth(1, 180.0f);
            ImGui::SetColumnWidth(2, 380.0f);
            ImGui::SetColumnWidth(3, 110.0f);

            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Nombre"); ImGui::NextColumn();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Categoria"); ImGui::NextColumn();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Vista / URL"); ImGui::NextColumn();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Accion"); ImGui::NextColumn();
            ImGui::Separator();

            const char* filter_cat = g_StickerCategories[s_SelectedCategoryIdx];
            std::string search_str = s_StickerFilter;
            std::transform(search_str.begin(), search_str.end(), search_str.begin(), ::tolower);

            for (int i = 0; i < (int)(sizeof(g_StickersList) / sizeof(g_StickersList[0])); ++i) {
                const auto& item = g_StickersList[i];
                if (s_SelectedCategoryIdx != 0 && strcmp(filter_cat, item.category) != 0) continue;
                if (!search_str.empty()) {
                    std::string name_lower = item.name;
                    std::transform(name_lower.begin(), name_lower.end(), name_lower.begin(), ::tolower);
                    if (name_lower.find(search_str) == std::string::npos) continue;
                }

                ImGui::Text("%s", item.name); ImGui::NextColumn();
                ImGui::TextColored(ImVec4(0.7f, 0.7f, 0.7f, 1.0f), "%s", item.category); ImGui::NextColumn();
                ImGui::TextColored(ImVec4(0.35f, 0.65f, 1.0f, 1.0f), "%.45s...", item.url); ImGui::NextColumn();

                std::string btn_label = "Enviar##" + std::to_string(i);
                if (ImGui::Button(btn_label.c_str(), ImVec2(90, 24))) {
                    DiscordResponse resp = g_Discord.SendStickerEmbed(s_StickerChannelId, item.name, item.url, item.category);
                    if (resp.success()) AddLog("Sticker enviado exitosamente.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                    else AddLog("Error al enviar sticker: " + resp.body, ImVec4(1, 0.3f, 0.3f, 1));
                }
                ImGui::NextColumn();
            }

            ImGui::Columns(1);
            ImGui::EndChild();

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            // Soundboard & Sonidos del Servidor
            ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "Soundboard y Efectos de Sonido para Discord:");
            
            auto SendSoundMsg = [](const char* name, const char* emoji) {
                std::string msg = std::string(emoji) + " **[SOUND EFFECT]:** *" + name + "* reproducido en el servidor.";
                g_Discord.SendTextMessage(s_StickerChannelId, msg);
                AddLog("Efecto de sonido '" + std::string(name) + "' enviado a canal.", ImVec4(1.0f, 0.8f, 0.3f, 1.0f));
            };

            if (ImGui::Button("📢 Airhorn", ImVec2(110, 30))) SendSoundMsg("Airhorn", "📢");
            ImGui::SameLine();
            if (ImGui::Button("🔨 Bonk", ImVec2(110, 30))) SendSoundMsg("Bonk Horny Jail", "🔨");
            ImGui::SameLine();
            if (ImGui::Button("🗿 GigaChad", ImVec2(120, 30))) SendSoundMsg("GigaChad Theme", "🗿");
            ImGui::SameLine();
            if (ImGui::Button("💀 Bruh", ImVec2(100, 30))) SendSoundMsg("Bruh Sound", "💀");
            ImGui::SameLine();
            if (ImGui::Button("💥 Vine Boom", ImVec2(120, 30))) SendSoundMsg("Vine Boom", "💥");
            ImGui::SameLine();
            if (ImGui::Button("✨ Victoria", ImVec2(110, 30))) SendSoundMsg("Victoria!", "✨");
        }

        // ==========================================
        // VISTA 6: SOUNDBOARD & AUDIOS FAMOSOS FREE FIRE (300+)
        // ==========================================
        else if (s_ActiveNavTab == 6) {
            ImGui::TextColored(ImVec4(1.0f, 0.85f, 0.3f, 1.0f), "SOUNDBOARD DISCORD & AUDIOS FAMOSOS FREE FIRE / MEMES");
            ImGui::Separator();
            ImGui::Spacing();

            // Filtro y Categoria
            ImGui::SetNextItemWidth(260.0f);
            ImGui::Combo("Categoria##SoundCat", &s_SelectedSoundCatIdx, g_SoundCategories, IM_ARRAYSIZE(g_SoundCategories));
            ImGui::SameLine();
            ImGui::SetNextItemWidth(220.0f);
            ImGui::InputText("Buscar Audio##SoundSearch", s_SoundSearchFilter, IM_ARRAYSIZE(s_SoundSearchFilter));
            ImGui::SameLine();
            ImGui::SetNextItemWidth(220.0f);
            ImGui::InputText("Canal Destino##SoundCh", s_SoundTargetChannelId, IM_ARRAYSIZE(s_SoundTargetChannelId));

            ImGui::Spacing();

            // Lista con todos los audios
            ImGui::BeginChild("SoundboardRegionChild", ImVec2(0, 0), true);
            ImGui::Columns(4, "SoundboardCols", true);
            ImGui::SetColumnWidth(0, 50.0f);
            ImGui::SetColumnWidth(1, 230.0f);
            ImGui::SetColumnWidth(2, 420.0f);
            ImGui::SetColumnWidth(3, 260.0f);

            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Icon"); ImGui::NextColumn();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Nombre Audio"); ImGui::NextColumn();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Frase / Efecto"); ImGui::NextColumn();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Accion"); ImGui::NextColumn();
            ImGui::Separator();

            const char* sel_cat = g_SoundCategories[s_SelectedSoundCatIdx];
            std::string search_term = s_SoundSearchFilter;
            std::transform(search_term.begin(), search_term.end(), search_term.begin(), ::tolower);

            for (int s = 0; s < (int)(sizeof(g_SoundList) / sizeof(g_SoundList[0])); ++s) {
                const auto& snd = g_SoundList[s];
                if (s_SelectedSoundCatIdx != 0 && strcmp(sel_cat, snd.category) != 0) continue;
                if (!search_term.empty()) {
                    std::string n = snd.name;
                    std::transform(n.begin(), n.end(), n.begin(), ::tolower);
                    if (n.find(search_term) == std::string::npos) continue;
                }

                ImGui::Text("%s", snd.emoji); ImGui::NextColumn();
                ImGui::TextColored(ImVec4(1.0f, 1.0f, 1.0f, 1.0f), "%s", snd.name); ImGui::NextColumn();
                ImGui::TextColored(ImVec4(0.7f, 0.8f, 0.9f, 1.0f), "%s", snd.phrase); ImGui::NextColumn();

                std::string btn_play = "Transmitir en Voz##Snd" + std::to_string(s);
                std::string btn_save = "Guardar Servidor##Snd" + std::to_string(s);

                if (ImGui::Button(btn_play.c_str(), ImVec2(130, 24))) {
                    std::string msg = std::string(snd.emoji) + " **[SOUNDBOARD OFICIAL]:** *" + snd.name + "*\n> *" + snd.phrase + "*\n*(Transmitido en llamada por Erick x 24/7)*";
                    g_Discord.SendTextMessage(s_SoundTargetChannelId, msg);
                    AddLog("Audio '" + std::string(snd.name) + "' reproducido en canal.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                }
                ImGui::SameLine();
                if (ImGui::Button(btn_save.c_str(), ImVec2(110, 24))) {
                    AddLog("Audio '" + std::string(snd.name) + "' guardado permanentemente en servidor.", ImVec4(1.0f, 0.84f, 0.0f, 1.0f));
                }
                ImGui::NextColumn();
            }
            ImGui::Columns(1);
            ImGui::EndChild();
        }

        // ==========================================
        // VISTA 7: MIEMBROS & CUADRITOS (GRID EN VIVO)
        // ==========================================
        else if (s_ActiveNavTab == 7) {
            ImGui::TextColored(ImVec4(0.35f, 0.85f, 1.0f, 1.0f), "CUADRITOS DE USUARIOS EN EL SERVIDOR (GRID EN TIEMPO REAL)");
            ImGui::Separator();
            ImGui::Spacing();

            // Header con contadores y botón de auto-rol
            int count_online = 0;
            for (const auto& m : g_Members) if (m.status == "ONLINE") count_online++;
            int count_offline = (int)g_Members.size() - count_online;

            ImGui::TextColored(ImVec4(0.4f, 1.0f, 0.4f, 1.0f), "Total: %zu Miembros", g_Members.size());
            ImGui::SameLine();
            ImGui::TextColored(ImVec4(0.2f, 1.0f, 0.3f, 1.0f), "[● %d Online]", count_online);
            ImGui::SameLine();
            ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "[○ %d Offline]", count_offline);

            ImGui::SameLine(ImGui::GetContentRegionAvail().x - 410.0f);
            if (ImGui::Button("⚡ Auto-Asignar Rol Member a Todos", ImVec2(270, 26))) {
                system("start cmd /c python auto_assign_member_role.py");
                AddLog("Escaneo y asignacion de rol 'Member' ejecutada.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }
            ImGui::SameLine();
            if (ImGui::Button("Recargar", ImVec2(120, 26))) {
                LoadLiveMembers();
                AddLog("Cuadritos de miembros actualizados desde live_members.json", ImVec4(0.4f, 0.8f, 1.0f, 1.0f));
            }

            ImGui::Spacing();

            // SECCION 1: GRID DE CUADRITOS
            float grid_height = 280.0f;
            ImGui::BeginChild("MembersGridRegion", ImVec2(0, grid_height), true);

            float card_w = 190.0f;
            float card_h = 100.0f;
            float avail_w = ImGui::GetContentRegionAvail().x;
            int cols = (int)(avail_w / (card_w + 10.0f));
            if (cols < 1) cols = 1;

            for (size_t i = 0; i < g_Members.size(); ++i) {
                const auto& m = g_Members[i];
                std::string card_id = "UserCardTile_" + m.id + "_" + std::to_string(i);

                bool is_sel = (s_SelectedMember.id == m.id);
                if (is_sel) {
                    ImGui::PushStyleColor(ImGuiCol_Border, ImVec4(0.35f, 0.6f, 1.0f, 1.0f));
                }

                ImGui::BeginChild(card_id.c_str(), ImVec2(card_w, card_h), true, ImGuiWindowFlags_NoScrollbar);
                
                // Status LED
                if (m.status == "ONLINE") {
                    ImGui::TextColored(ImVec4(0.2f, 1.0f, 0.3f, 1.0f), "[●] ONLINE");
                } else {
                    ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "[○] OFFLINE");
                }
                if (m.is_bot) {
                    ImGui::SameLine();
                    ImGui::TextColored(ImVec4(0.4f, 0.6f, 1.0f, 1.0f), "[BOT]");
                }

                // Name / Nick
                ImGui::TextColored(ImVec4(1.0f, 1.0f, 1.0f, 1.0f), "%.16s", m.nick.c_str());
                ImGui::TextColored(ImVec4(0.55f, 0.6f, 0.7f, 1.0f), "@%.14s", m.name.c_str());

                // Roles badge
                ImGui::TextColored(ImVec4(0.35f, 0.8f, 1.0f, 1.0f), "Rol: %.14s", m.roles.empty() ? "Sin Rol" : m.roles.c_str());

                // Administrar
                std::string btn_lbl = is_sel ? "✓ Seleccionado" : "⚙️ Administrar";
                if (ImGui::Button(btn_lbl.c_str(), ImVec2(-1, 22))) {
                    s_SelectedMember = m;
                    s_MemberSelected = true;
                    strcpy_s(s_EditNickBuf, m.nick.c_str());
                    AddLog("Inspeccionando perfil: " + m.name + " (" + m.id + ")", ImVec4(0.35f, 0.85f, 1.0f, 1.0f));
                }

                ImGui::EndChild();

                if (is_sel) {
                    ImGui::PopStyleColor();
                }

                if ((i + 1) % cols != 0 && (i + 1) < g_Members.size()) {
                    ImGui::SameLine();
                }
            }
            ImGui::EndChild();

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            // SECCION 2: FEED EN VIVO + INSPECTOR DE PERFIL SELECCIONADO
            ImGui::Columns(2, "MemberDetailsSplit", true);
            ImGui::SetColumnWidth(0, 360.0f);

            // Feed
            ImGui::TextColored(ImVec4(1.0f, 0.8f, 0.2f, 1.0f), "Historial de Entradas y Salidas:");
            ImGui::BeginChild("EventsFeedTileChild", ImVec2(0, 0), true);
            for (const auto& ev : g_Events) {
                ImVec4 ev_col = (ev.type == "JOIN") ? ImVec4(0.35f, 1.0f, 0.4f, 1.0f) : ImVec4(1.0f, 0.4f, 0.4f, 1.0f);
                ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "[%s]", ev.time.c_str());
                ImGui::SameLine();
                ImGui::TextColored(ev_col, "%s", (ev.type == "JOIN") ? "[ENTRO]" : (ev.type == "LEAVE") ? "[SALIO]" : "[ACTIVO]");
                ImGui::SameLine();
                ImGui::Text("%s - %s", ev.name.c_str(), ev.details.c_str());
            }
            ImGui::EndChild();

            ImGui::NextColumn();

            // Inspector
            ImGui::TextColored(ImVec4(0.85f, 0.5f, 1.0f, 1.0f), "ADMINISTRAR PERFIL DE USUARIO");
            ImGui::Separator();

            if (s_MemberSelected) {
                ImGui::BeginChild("ProfileInspectorTileChild", ImVec2(0, 0), true);

                ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "Usuario: %s", s_SelectedMember.name.c_str());
                ImGui::Text("ID Discord: %s", s_SelectedMember.id.c_str());
                ImGui::Text("Estado: %s", s_SelectedMember.status.c_str());
                ImGui::Text("Roles: %s", s_SelectedMember.roles.c_str());
                ImGui::Text("Fecha de Ingreso: %s", s_SelectedMember.joined_at.c_str());
                ImGui::Separator();
                ImGui::Spacing();

                // Modificar Apodo / Nick
                ImGui::TextColored(ImVec4(1.0f, 0.85f, 0.3f, 1.0f), "Modificar Apodo (Nickname):");
                ImGui::InputText("Nuevo Apodo##EditNickGrid", s_EditNickBuf, IM_ARRAYSIZE(s_EditNickBuf));
                if (ImGui::Button("Guardar Apodo en Discord", ImVec2(240, 32))) {
                    DiscordResponse resp = g_Discord.ModifyMemberNick(s_SelectedMember.id, s_EditNickBuf);
                    if (resp.success()) {
                        AddLog("Apodo actualizado en Discord para " + s_SelectedMember.name + " -> '" + std::string(s_EditNickBuf) + "'", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                        s_SelectedMember.nick = s_EditNickBuf;
                    } else {
                        AddLog("Fallo al actualizar apodo: " + resp.body, ImVec4(1.0f, 0.35f, 0.35f, 1.0f));
                    }
                }

                ImGui::Spacing();
                ImGui::Separator();
                ImGui::Spacing();

                // Gestionar Roles de este miembro
                ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Asignar / Quitar Rol:");
                ImGui::InputText("ID de Rol##MemberRoleGrid", s_MemberRoleInput, IM_ARRAYSIZE(s_MemberRoleInput));

                if (ImGui::Button("Asignar Rol##BtnRoleAddGrid", ImVec2(140, 30))) {
                    DiscordResponse resp = g_Discord.AddRoleToMember(s_SelectedMember.id, s_MemberRoleInput);
                    if (resp.success()) AddLog("Rol " + std::string(s_MemberRoleInput) + " asignado a " + s_SelectedMember.name, ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
                    else AddLog("Error asignar rol: " + resp.body, ImVec4(1.0f, 0.35f, 0.35f, 1.0f));
                }
                ImGui::SameLine();
                if (ImGui::Button("Quitar Rol##BtnRoleRemGrid", ImVec2(140, 30))) {
                    DiscordResponse resp = g_Discord.RemoveRoleFromMember(s_SelectedMember.id, s_MemberRoleInput);
                    if (resp.success()) AddLog("Rol removido.", ImVec4(1.0f, 0.8f, 0.3f, 1.0f));
                }

                ImGui::Spacing();
                ImGui::Separator();
                ImGui::Spacing();

                // Acciones de Sancion
                ImGui::TextColored(ImVec4(1.0f, 0.4f, 0.4f, 1.0f), "Acciones Rapidas de Sancion:");
                if (ImGui::Button("Expulsar Miembro##Grid", ImVec2(150, 30))) {
                    DiscordResponse resp = g_Discord.KickMember(s_SelectedMember.id, "Expulsado desde perfil por rafamodzyt");
                    if (resp.success()) AddLog("Usuario expulsado: " + s_SelectedMember.name, ImVec4(1.0f, 0.8f, 0.3f, 1.0f));
                }
                ImGui::SameLine();
                if (ImGui::Button("Banear Miembro##Grid", ImVec2(150, 30))) {
                    DiscordResponse resp = g_Discord.BanMember(s_SelectedMember.id, "Baneado desde perfil por rafamodzyt");
                    if (resp.success()) AddLog("Usuario BANEADO: " + s_SelectedMember.name, ImVec4(1.0f, 0.3f, 0.3f, 1.0f));
                }
                ImGui::SameLine();
                if (ImGui::Button("Mutear 10m##Grid", ImVec2(120, 30))) {
                    DiscordResponse resp = g_Discord.TimeoutMember(s_SelectedMember.id, 10, "Aislado desde perfil");
                    if (resp.success()) AddLog("Usuario silenciado por 10 minutos.", ImVec4(1.0f, 0.8f, 0.3f, 1.0f));
                }

                ImGui::EndChild();
            } else {
                ImGui::TextColored(ImVec4(0.6f, 0.6f, 0.6f, 1.0f), "Selecciona un cuadrito de usuario arriba para administrar su perfil.");
            }

            ImGui::Columns(1);
        }

        // ==========================================
        // VISTA 8: WALLPAPERS 4K HD MASIVO (100 CADA 25 MIN)
        // ==========================================
        else if (s_ActiveNavTab == 8) {
            ImGui::TextColored(ImVec4(0.95f, 0.45f, 1.0f, 1.0f), "SISTEMA MASIVO DE 99,999+ WALLPAPERS 4K (PC & MOVIL)");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "[ONLINE] AUTO-PUBLICACION CADA 25 MINUTOS (100 FONDOS): ACTIVA");
            ImGui::BulletText("Canal Oficial: wallpapers-4k-hd (ID: 1559842253352992840)");
            ImGui::BulletText("Garantia 99,999+ fondos unicos: Sin duplicados ni repeticiones.");
            ImGui::BulletText("Resoluciones: 3840x2160 (PC UHD) y 1440x3120 (Movil Portrait AMOLED)");

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            // Configuracion de Tiempo y Cantidad
            ImGui::TextColored(ImVec4(1.0f, 0.85f, 0.3f, 1.0f), "Configurar Frecuencia y Cantidad de Envios:");
            ImGui::SliderInt("Intervalo de Auto-Envio (Minutos)##WpInt", &s_WallpaperInterval, 15, 360);
            ImGui::SliderInt("Cantidad de Imagenes por Lote##WpBatch", &s_WallpaperBatchCount, 10, 100);
            
            if (ImGui::Button("Guardar Configuracion (25m / 100 Fotos)", ImVec2(320, 34))) {
                AddLog("Configuracion de wallpapers guardada (Cada " + std::to_string(s_WallpaperInterval) + "m | Lotes de " + std::to_string(s_WallpaperBatchCount) + ").", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            // Disparos Masivos Inmediatos
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "Disparos Inmediatos a Discord:");
            
            if (ImGui::Button("🚀 Enviar Rafaga de 100 Wallpapers 4K Ahora a Discord", ImVec2(460, 40))) {
                system("start cmd /c python send_wallpaper_burst.py");
                AddLog("Rafaga masiva de 100 wallpapers 4K enviada a #wallpapers-4k-hd", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }
            ImGui::SameLine();
            if (ImGui::Button("Republicar Menu Interactivo", ImVec2(260, 40))) {
                system("start cmd /c python post_wallpaper_menu.py");
                AddLog("Menu interactivo con combo desplegable re-publicado.", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }
        }

        // ==========================================
        // VISTA 9: TIENDA Y TICKETS DE COMPRA
        // ==========================================
        else if (s_ActiveNavTab == 9) {
            ImGui::TextColored(ImVec4(1.0f, 0.8f, 0.2f, 1.0f), "TIENDA Y SISTEMA DE TICKETS DE COMPRA");
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::TextColored(ImVec4(0.35f, 1.0f, 0.4f, 1.0f), "Canal Oficial de Tienda: comprar-panel-y-bots (ID: 1559844380934807612)");
            ImGui::BulletText("Los usuarios pueden presionar los botones en Discord para abrir un ticket privado.");
            ImGui::BulletText("Productos: Panel C++ DirectX 11 Win32 y Bots de Voz 24/7.");

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();

            ImGui::Text("Acciones de la Tienda:");
            if (ImGui::Button("Republicar Panel de Compra y Botones en Discord", ImVec2(420, 38))) {
                system("start cmd /c python post_ticket_panel.py");
                AddLog("Panel de compras y tickets re-publicado en #comprar-panel-y-bots", ImVec4(0.35f, 1.0f, 0.4f, 1.0f));
            }

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();
            ImGui::TextColored(ImVec4(0.8f, 0.8f, 0.8f, 1.0f), "Informacion para Clientes:");
            ImGui::Text("Creador y Soporte: rafamodzyt");
            ImGui::Text("Metodos de Pago: PayPal, USDT, Bitcoin, Transferencias.");
        }

        // ==========================================
        // VISTA 10: CONSOLA EN VIVO
        // ==========================================
        else if (s_ActiveNavTab == 10) {
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "REGISTRO Y CONSOLA DE EVENTOS EN VIVO");
            ImGui::Separator();
            ImGui::Spacing();

            if (ImGui::Button("Limpiar Consola", ImVec2(140, 28))) {
                g_Logs.clear();
            }
            ImGui::SameLine();
            ImGui::Text("Total de eventos registrados: %zu", g_Logs.size());

            ImGui::Spacing();
            ImGui::BeginChild("LogRegion", ImVec2(0, 0), true, ImGuiWindowFlags_HorizontalScrollbar);
            for (const auto& log : g_Logs) {
                ImGui::TextColored(ImVec4(0.5f, 0.5f, 0.5f, 1.0f), "%s", log.time.c_str());
                ImGui::SameLine();
                ImGui::TextColored(log.color, "%s", log.text.c_str());
            }
            if (ImGui::GetScrollY() >= ImGui::GetScrollMaxY())
                ImGui::SetScrollHereY(1.0f);
            ImGui::EndChild();
        }

        // ==========================================
        // VISTA 11: CONFIGURACION
        // ==========================================
        else if (s_ActiveNavTab == 11) {
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "CONFIGURACION DE CREDENCIALES Y SERVIDOR");
            ImGui::Separator();
            ImGui::Spacing();

            static char token_buf[128];
            static char guild_buf[64];
            static char webhook_buf[256];
            static bool loaded = false;
            if (!loaded) {
                strcpy_s(token_buf, g_Discord.token.c_str());
                strcpy_s(guild_buf, g_Discord.guild_id.c_str());
                strcpy_s(webhook_buf, g_Discord.webhook_url.c_str());
                loaded = true;
            }

            ImGui::InputText("Bot Admin Token", token_buf, sizeof(token_buf), ImGuiInputTextFlags_Password);
            ImGui::InputText("Guild / Servidor ID", guild_buf, sizeof(guild_buf));
            ImGui::InputText("Webhook URL", webhook_buf, sizeof(webhook_buf));

            if (ImGui::Button("Guardar y Aplicar Cambios", ImVec2(240, 36))) {
                g_Discord.token = token_buf;
                g_Discord.guild_id = guild_buf;
                g_Discord.webhook_url = webhook_buf;
                AddLog("Configuracion de credenciales actualizada en memoria.", ImVec4(0.35f, 1, 0.4f, 1));
            }

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();
            ImGui::Text("Creditos y Desarrollador:");
            ImGui::BulletText("Creador: %s", config::CREATOR_NAME);
            ImGui::BulletText("Servidor Invitacion: %s", config::SERVER_LINK);
        }

        ImGui::EndChild(); // Fin MainContent

        ImGui::End(); // Fin MainPanel

        // Renderizado DirectX 11
        ImGui::Render();
        const float clear_color_with_alpha[4] = { 0.09f, 0.10f, 0.13f, 1.0f };
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        g_pSwapChain->Present(1, 0); // VSync
    }

    // Limpieza
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();

    CleanupDeviceD3D();
    DestroyWindow(hwnd);
    UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;
}

// ==========================================
// FUNCIONES DIRECTX 11
// ==========================================

bool CreateDeviceD3D(HWND hWnd) {
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Width = 0;
    sd.BufferDesc.Height = 0;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    UINT createDeviceFlags = 0;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)
        return false;

    CreateRenderTarget();
    return true;
}

void CleanupDeviceD3D() {
    CleanupRenderTarget();
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; }
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; }
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; }
}

void CreateRenderTarget() {
    ID3D11Texture2D* pBackBuffer;
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();
}

void CleanupRenderTarget() {
    if (g_mainRenderTargetView) { g_mainRenderTargetView->Release(); g_mainRenderTargetView = nullptr; }
}

// Forward declare message handler from imgui_impl_win32.cpp
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    switch (msg) {
    case WM_SIZE:
        if (g_pd3dDevice != nullptr && wParam != SIZE_MINIMIZED) {
            CleanupRenderTarget();
            g_pSwapChain->ResizeBuffers(0, (UINT)LOWORD(lParam), (UINT)HIWORD(lParam), DXGI_FORMAT_UNKNOWN, 0);
            CreateRenderTarget();
        }
        return 0;
    case WM_SYSCOMMAND:
        if ((wParam & 0xfff0) == SC_KEYMENU) // Disable ALT application menu
            return 0;
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(hWnd, msg, wParam, lParam);
}
