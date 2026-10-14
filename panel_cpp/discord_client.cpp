#include "discord_client.h"
#include <windows.h>
#include <winhttp.h>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <regex>

#pragma comment(lib, "winhttp.lib")

static std::wstring ToWide(const std::string& str) {
    if (str.empty()) return L"";
    int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), NULL, 0);
    std::wstring wstr(size_needed, 0);
    MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), &wstr[0], size_needed);
    return wstr;
}

static std::string ToUtf8(const std::wstring& wstr) {
    if (wstr.empty()) return "";
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), NULL, 0, NULL, NULL);
    std::string str(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), &str[0], size_needed, NULL, NULL);
    return str;
}

static std::string EscapeJson(const std::string& s) {
    std::ostringstream o;
    for (char c : s) {
        switch (c) {
        case '"': o << "\\\""; break;
        case '\\': o << "\\\\"; break;
        case '\b': o << "\\b"; break;
        case '\f': o << "\\f"; break;
        case '\n': o << "\\n"; break;
        case '\r': o << "\\r"; break;
        case '\t': o << "\\t"; break;
        default:
            if ('\x00' <= c && c <= '\x1f') {
                o << "\\u" << std::hex << std::setw(4) << std::setfill('0') << (int)c;
            } else {
                o << c;
            }
        }
    }
    return o.str();
}

DiscordClient::DiscordClient() {
    guild_id = "1350706770527653989";
    webhook_url = "https://discord.com/api/webhooks/1559831359885680731/sknZANo0tcmUqcpUvMVaL32J9DJELoUxp4l9ynHQZJG4pNZGQJuzEDzUu3tkhqgvU0rm";
    const char* env_admin = std::getenv("ADMIN_BOT_TOKEN");
    if (env_admin) token = env_admin;
    const char* env_bot1 = std::getenv("DISCORD_TOKEN");
    if (env_bot1) bot1_token = env_bot1;
}

DiscordResponse DiscordClient::Request(const std::string& method, const std::string& endpoint, const std::string& json_payload) {
    DiscordResponse response;

    HINTERNET hSession = WinHttpOpen(L"DiscordDX11Panel/1.0",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) {
        response.error = "Error al abrir sesion WinHTTP";
        return response;
    }

    HINTERNET hConnect = WinHttpConnect(hSession, L"discord.com", INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConnect) {
        WinHttpCloseHandle(hSession);
        response.error = "Error al conectar con discord.com";
        return response;
    }

    std::wstring wEndpoint = ToWide(endpoint);
    std::wstring wMethod = ToWide(method);

    HINTERNET hRequest = WinHttpOpenRequest(hConnect, wMethod.c_str(), wEndpoint.c_str(),
        NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES,
        WINHTTP_FLAG_SECURE);

    if (!hRequest) {
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        response.error = "Error al crear request WinHTTP";
        return response;
    }

    // Cabeceras
    std::string headers = "Authorization: Bot " + token + "\r\nContent-Type: application/json\r\nUser-Agent: DiscordDX11Panel/1.0\r\n";
    std::wstring wHeaders = ToWide(headers);

    BOOL bResults = WinHttpSendRequest(hRequest,
        wHeaders.c_str(), (DWORD)wHeaders.length(),
        (LPVOID)json_payload.c_str(), (DWORD)json_payload.length(),
        (DWORD)json_payload.length(), 0);

    if (bResults) {
        bResults = WinHttpReceiveResponse(hRequest, NULL);
    }

    if (bResults) {
        DWORD dwStatusCode = 0;
        DWORD dwSize = sizeof(dwStatusCode);
        WinHttpQueryHeaders(hRequest,
            WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
            WINHTTP_HEADER_NAME_BY_INDEX,
            &dwStatusCode, &dwSize, WINHTTP_NO_HEADER_INDEX);
        response.status_code = (int)dwStatusCode;

        // Leer cuerpo de la respuesta
        DWORD dwDownloaded = 0;
        do {
            dwSize = 0;
            if (!WinHttpQueryDataAvailable(hRequest, &dwSize)) break;
            if (dwSize == 0) break;

            std::vector<char> buffer(dwSize + 1);
            if (WinHttpReadData(hRequest, buffer.data(), dwSize, &dwDownloaded)) {
                buffer[dwDownloaded] = '\0';
                response.body.append(buffer.data(), dwDownloaded);
            }
        } while (dwSize > 0);
    } else {
        response.error = "Fallo en WinHttpSendRequest o ReceiveResponse: " + std::to_string(GetLastError());
    }

    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    return response;
}

DiscordResponse DiscordClient::WebhookRequest(const std::string& json_payload) {
    DiscordResponse response;
    if (webhook_url.empty()) {
        response.error = "URL de Webhook vacia";
        return response;
    }

    // Parsear URL del webhook (discord.com/api/webhooks/...)
    std::string prefix = "https://discord.com";
    std::string endpoint = webhook_url;
    if (endpoint.find(prefix) == 0) {
        endpoint = endpoint.substr(prefix.length());
    }

    HINTERNET hSession = WinHttpOpen(L"DiscordDX11Webhook/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) return response;
    HINTERNET hConnect = WinHttpConnect(hSession, L"discord.com", INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConnect) { WinHttpCloseHandle(hSession); return response; }

    HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"POST", ToWide(endpoint).c_str(), NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
    if (!hRequest) { WinHttpCloseHandle(hConnect); WinHttpCloseHandle(hSession); return response; }

    std::wstring headers = L"Content-Type: application/json\r\n";
    BOOL res = WinHttpSendRequest(hRequest, headers.c_str(), (DWORD)headers.length(), (LPVOID)json_payload.c_str(), (DWORD)json_payload.length(), (DWORD)json_payload.length(), 0);
    if (res) res = WinHttpReceiveResponse(hRequest, NULL);
    if (res) {
        DWORD dwCode = 0, dwSize = sizeof(dwCode);
        WinHttpQueryHeaders(hRequest, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER, WINHTTP_HEADER_NAME_BY_INDEX, &dwCode, &dwSize, WINHTTP_NO_HEADER_INDEX);
        response.status_code = (int)dwCode;
    }
    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);
    return response;
}

// Canales
DiscordResponse DiscordClient::GetChannels() {
    return Request("GET", "/api/v10/guilds/" + guild_id + "/channels");
}

DiscordResponse DiscordClient::CreateChannel(const std::string& name, int type, const std::string& topic, int slowmode) {
    std::ostringstream json;
    json << "{\"name\":\"" << EscapeJson(name) << "\",\"type\":" << type;
    if (!topic.empty()) json << ",\"topic\":\"" << EscapeJson(topic) << "\"";
    if (slowmode > 0) json << ",\"rate_limit_per_user\":" << slowmode;
    json << "}";
    return Request("POST", "/api/v10/guilds/" + guild_id + "/channels", json.str());
}

DiscordResponse DiscordClient::DeleteChannel(const std::string& channel_id) {
    return Request("DELETE", "/api/v10/channels/" + channel_id);
}

DiscordResponse DiscordClient::RenameChannel(const std::string& channel_id, const std::string& new_name) {
    std::string json = "{\"name\":\"" + EscapeJson(new_name) + "\"}";
    return Request("PATCH", "/api/v10/channels/" + channel_id, json);
}

DiscordResponse DiscordClient::LockChannel(const std::string& channel_id) {
    // Niega el permiso SEND_MESSAGES (0x800) a @everyone (id = guild_id)
    std::string json = "{\"id\":\"" + guild_id + "\",\"type\":0,\"allow\":\"0\",\"deny\":\"2048\"}";
    return Request("PUT", "/api/v10/channels/" + channel_id + "/permissions/" + guild_id, json);
}

DiscordResponse DiscordClient::UnlockChannel(const std::string& channel_id) {
    return Request("DELETE", "/api/v10/channels/" + channel_id + "/permissions/" + guild_id);
}

DiscordResponse DiscordClient::SetSlowmode(const std::string& channel_id, int seconds) {
    std::string json = "{\"rate_limit_per_user\":" + std::to_string(seconds) + "}";
    return Request("PATCH", "/api/v10/channels/" + channel_id, json);
}

DiscordResponse DiscordClient::SetTopic(const std::string& channel_id, const std::string& topic) {
    std::string json = "{\"topic\":\"" + EscapeJson(topic) + "\"}";
    return Request("PATCH", "/api/v10/channels/" + channel_id, json);
}

// Roles
DiscordResponse DiscordClient::GetRoles() {
    return Request("GET", "/api/v10/guilds/" + guild_id + "/roles");
}

DiscordResponse DiscordClient::CreateRole(const std::string& name, int color_hex) {
    std::ostringstream json;
    json << "{\"name\":\"" << EscapeJson(name) << "\",\"color\":" << color_hex << "}";
    return Request("POST", "/api/v10/guilds/" + guild_id + "/roles", json.str());
}

DiscordResponse DiscordClient::DeleteRole(const std::string& role_id) {
    return Request("DELETE", "/api/v10/guilds/" + guild_id + "/roles/" + role_id);
}

DiscordResponse DiscordClient::AddRoleToMember(const std::string& user_id, const std::string& role_id) {
    return Request("PUT", "/api/v10/guilds/" + guild_id + "/members/" + user_id + "/roles/" + role_id);
}

DiscordResponse DiscordClient::RemoveRoleFromMember(const std::string& user_id, const std::string& role_id) {
    return Request("DELETE", "/api/v10/guilds/" + guild_id + "/members/" + user_id + "/roles/" + role_id);
}

DiscordResponse DiscordClient::ModifyRoleColor(const std::string& role_id, int color_hex) {
    std::string json = "{\"color\":" + std::to_string(color_hex) + "}";
    return Request("PATCH", "/api/v10/guilds/" + guild_id + "/roles/" + role_id, json);
}

DiscordResponse DiscordClient::RenameRole(const std::string& role_id, const std::string& new_name) {
    std::string json = "{\"name\":\"" + EscapeJson(new_name) + "\"}";
    return Request("PATCH", "/api/v10/guilds/" + guild_id + "/roles/" + role_id, json);
}

// Moderacion
DiscordResponse DiscordClient::PurgeMessages(const std::string& channel_id, int amount) {
    // Obtener ultimos mensajes
    DiscordResponse get_resp = Request("GET", "/api/v10/channels/" + channel_id + "/messages?limit=" + std::to_string(amount));
    if (!get_resp.success()) return get_resp;

    // Extraer IDs
    std::regex id_regex("\"id\":\\s*\"(\\d+)\"");
    std::smatch match;
    std::string body = get_resp.body;
    std::vector<std::string> ids;
    while (std::regex_search(body, match, id_regex)) {
        ids.push_back(match[1]);
        body = match.suffix().str();
    }

    if (ids.empty()) {
        DiscordResponse r;
        r.status_code = 200;
        r.body = "No messages found";
        return r;
    }

    if (ids.size() == 1) {
        return Request("DELETE", "/api/v10/channels/" + channel_id + "/messages/" + ids[0]);
    }

    std::ostringstream json;
    json << "{\"messages\":[";
    for (size_t i = 0; i < ids.size(); ++i) {
        json << "\"" << ids[i] << "\"" << (i + 1 < ids.size() ? "," : "");
    }
    json << "]}";
    return Request("POST", "/api/v10/channels/" + channel_id + "/messages/bulk-delete", json.str());
}

DiscordResponse DiscordClient::KickMember(const std::string& user_id, const std::string& reason) {
    return Request("DELETE", "/api/v10/guilds/" + guild_id + "/members/" + user_id);
}

DiscordResponse DiscordClient::BanMember(const std::string& user_id, const std::string& reason) {
    std::string json = "{\"delete_message_days\":0}";
    return Request("PUT", "/api/v10/guilds/" + guild_id + "/bans/" + user_id, json);
}

DiscordResponse DiscordClient::UnbanMember(const std::string& user_id) {
    return Request("DELETE", "/api/v10/guilds/" + guild_id + "/bans/" + user_id);
}

DiscordResponse DiscordClient::TimeoutMember(const std::string& user_id, int minutes, const std::string& reason) {
    time_t now = time(nullptr);
    time_t until = now + (minutes * 60);
    tm utc_tm;
    gmtime_s(&utc_tm, &until);
    char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", &utc_tm);

    std::string json = "{\"communication_disabled_until\":\"" + std::string(buf) + "\"}";
    return Request("PATCH", "/api/v10/guilds/" + guild_id + "/members/" + user_id, json);
}

DiscordResponse DiscordClient::RemoveTimeout(const std::string& user_id) {
    std::string json = "{\"communication_disabled_until\":null}";
    return Request("PATCH", "/api/v10/guilds/" + guild_id + "/members/" + user_id, json);
}

// Administracion de Perfiles de Miembros
DiscordResponse DiscordClient::GetMember(const std::string& user_id) {
    return Request("GET", "/api/v10/guilds/" + guild_id + "/members/" + user_id);
}

DiscordResponse DiscordClient::ModifyMemberNick(const std::string& user_id, const std::string& nick) {
    std::string json = "{\"nick\":\"" + EscapeJson(nick) + "\"}";
    return Request("PATCH", "/api/v10/guilds/" + guild_id + "/members/" + user_id, json);
}

// Mensajes y Alertas
DiscordResponse DiscordClient::GetChannelMessages(const std::string& channel_id, int limit) {
    return Request("GET", "/api/v10/channels/" + channel_id + "/messages?limit=" + std::to_string(limit));
}

DiscordResponse DiscordClient::SendTextMessage(const std::string& channel_id, const std::string& content) {
    std::string json = "{\"content\":\"" + EscapeJson(content) + "\"}";
    return Request("POST", "/api/v10/channels/" + channel_id + "/messages", json);
}

DiscordResponse DiscordClient::SendAnsiMessage(const std::string& channel_id, const std::string& text, int color_code) {
    // Discord ANSI block: ```ansi \u001b[2;XXmTexto\u001b[0m ```
    std::string ansi_text = "```ansi\\n\\u001b[2;" + std::to_string(color_code) + "m" + EscapeJson(text) + "\\u001b[0m\\n```";
    std::string json = "{\"content\":\"" + ansi_text + "\"}";
    return Request("POST", "/api/v10/channels/" + channel_id + "/messages", json);
}

DiscordResponse DiscordClient::SendEmbed(const std::string& channel_id, const std::string& title, const std::string& description, int color_hex, const std::string& footer) {
    std::ostringstream json;
    json << "{\"embeds\":[{"
         << "\"title\":\"" << EscapeJson(title) << "\","
         << "\"description\":\"" << EscapeJson(description) << "\","
         << "\"color\":" << color_hex;
    if (!footer.empty()) {
        json << ",\"footer\":{\"text\":\"" << EscapeJson(footer) << "\"}";
    }
    json << "}]}";
    return Request("POST", "/api/v10/channels/" + channel_id + "/messages", json.str());
}

DiscordResponse DiscordClient::SendStickerEmbed(const std::string& channel_id, const std::string& name, const std::string& url, const std::string& category) {
    std::ostringstream json;
    json << "{\"embeds\":[{"
         << "\"title\":\"" << EscapeJson("Meme / Sticker: " + name) << "\","
         << "\"description\":\"" << EscapeJson("Categoria: " + category + " | Servidor SHADOW BLOCK") << "\","
         << "\"color\": 5793266,"
         << "\"image\":{\"url\":\"" << EscapeJson(url) << "\"},"
         << "\"footer\":{\"text\":\"Enviado desde Panel C++ DX11 por rafamodzyt\"}"
         << "}]}";
    return Request("POST", "/api/v10/channels/" + channel_id + "/messages", json.str());
}

DiscordResponse DiscordClient::SendWallpaperEmbed(const std::string& channel_id, const std::string& title, const std::string& url, const std::string& type_label) {
    std::ostringstream json;
    json << "{\"embeds\":[{"
         << "\"title\":\"" << EscapeJson("WALLPAPER 4K: " + title) << "\","
         << "\"description\":\"" << EscapeJson("Resolucion: Ultra HD 4K | Tipo: " + type_label + " | Servidor SHADOW BLOCK") << "\","
         << "\"color\": 5793266,"
         << "\"image\":{\"url\":\"" << EscapeJson(url) << "\"},"
         << "\"footer\":{\"text\":\"Publicado desde Panel C++ DX11 por rafamodzyt\"}"
         << "}]}";
    return Request("POST", "/api/v10/channels/" + channel_id + "/messages", json.str());
}

DiscordResponse DiscordClient::SendWebhookMsg(const std::string& content, const std::string& username) {
    std::ostringstream json;
    json << "{\"content\":\"" << EscapeJson(content) << "\",\"username\":\"" << EscapeJson(username) << "\"}";
    return WebhookRequest(json.str());
}

// Emojis y Stickers del Servidor
DiscordResponse DiscordClient::GetGuildEmojis() {
    return Request("GET", "/api/v10/guilds/" + guild_id + "/emojis");
}

DiscordResponse DiscordClient::GetGuildStickers() {
    return Request("GET", "/api/v10/guilds/" + guild_id + "/stickers");
}

DiscordResponse DiscordClient::CreateGuildEmoji(const std::string& name, const std::string& image_data_base64) {
    std::string json = "{\"name\":\"" + EscapeJson(name) + "\",\"image\":\"" + EscapeJson(image_data_base64) + "\"}";
    return Request("POST", "/api/v10/guilds/" + guild_id + "/emojis", json);
}

DiscordResponse DiscordClient::DeleteGuildEmoji(const std::string& emoji_id) {
    return Request("DELETE", "/api/v10/guilds/" + guild_id + "/emojis/" + emoji_id);
}

// Servidor
DiscordResponse DiscordClient::GetGuild() {
    return Request("GET", "/api/v10/guilds/" + guild_id + "?with_counts=true");
}

DiscordResponse DiscordClient::RenameGuild(const std::string& new_name) {
    std::string json = "{\"name\":\"" + EscapeJson(new_name) + "\"}";
    return Request("PATCH", "/api/v10/guilds/" + guild_id, json);
}

// Parsing liviano
std::vector<DiscordChannelInfo> DiscordClient::ParseChannels(const std::string& json_body) {
    std::vector<DiscordChannelInfo> list;
    // Regex para extraer campos basicos con delimitador raw personalizado
    std::regex ch_regex(R"raw(\{"id":"(\d+)","type":(\d+)[^}]*?"name":"([^"]+)")raw");
    std::smatch match;
    std::string s = json_body;
    while (std::regex_search(s, match, ch_regex)) {
        DiscordChannelInfo ch;
        ch.id = match[1];
        ch.type = std::stoi(match[2]);
        ch.name = match[3];
        list.push_back(ch);
        s = match.suffix().str();
    }
    return list;
}

std::vector<DiscordRoleInfo> DiscordClient::ParseRoles(const std::string& json_body) {
    std::vector<DiscordRoleInfo> list;
    std::regex role_regex(R"raw(\{"id":"(\d+)","name":"([^"]+)"[^}]*?"color":(\d+))raw");
    std::smatch match;
    std::string s = json_body;
    while (std::regex_search(s, match, role_regex)) {
        DiscordRoleInfo r;
        r.id = match[1];
        r.name = match[2];
        r.color = std::stoi(match[3]);
        list.push_back(r);
        s = match.suffix().str();
    }
    return list;
}

std::vector<DiscordChatMessage> DiscordClient::ParseMessages(const std::string& json_body) {
    std::vector<DiscordChatMessage> list;
    // Regex para capturar id, contenido y autor de cada mensaje
    std::regex msg_regex(R"raw(\{"id":"(\d+)"[^}]*?"content":"([^"]*)"[^}]*?"username":"([^"]+)")raw");
    std::smatch match;
    std::string s = json_body;
    while (std::regex_search(s, match, msg_regex)) {
        DiscordChatMessage m;
        m.id = match[1];
        m.content = match[2];
        m.author = match[3];
        list.push_back(m);
        s = match.suffix().str();
    }
    return list;
}


