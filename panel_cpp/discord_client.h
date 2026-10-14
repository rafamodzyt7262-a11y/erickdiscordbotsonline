#pragma once
#include <string>
#include <vector>

struct DiscordResponse {
    int status_code = 0;
    std::string body;
    std::string error;
    bool success() const { return status_code >= 200 && status_code < 300; }
};

struct DiscordChannelInfo {
    std::string id;
    std::string name;
    int type = 0; // 0=text, 2=voice, 4=category
    std::string topic;
};

struct DiscordRoleInfo {
    std::string id;
    std::string name;
    int color = 0;
    int position = 0;
};

struct DiscordChatMessage {
    std::string id;
    std::string author;
    std::string content;
    std::string timestamp;
};

class DiscordClient {
public:
    std::string token;
    std::string guild_id;
    std::string webhook_url;
    std::string bot1_token; // Erick x

    DiscordClient();

    // Generic Request
    DiscordResponse Request(const std::string& method, const std::string& endpoint, const std::string& json_payload = "");
    DiscordResponse WebhookRequest(const std::string& json_payload);

    // Channels
    DiscordResponse GetChannels();
    DiscordResponse CreateChannel(const std::string& name, int type = 0, const std::string& topic = "", int slowmode = 0);
    DiscordResponse DeleteChannel(const std::string& channel_id);
    DiscordResponse RenameChannel(const std::string& channel_id, const std::string& new_name);
    DiscordResponse LockChannel(const std::string& channel_id);
    DiscordResponse UnlockChannel(const std::string& channel_id);
    DiscordResponse SetSlowmode(const std::string& channel_id, int seconds);
    DiscordResponse SetTopic(const std::string& channel_id, const std::string& topic);

    // Roles
    DiscordResponse GetRoles();
    DiscordResponse CreateRole(const std::string& name, int color_hex);
    DiscordResponse DeleteRole(const std::string& role_id);
    DiscordResponse AddRoleToMember(const std::string& user_id, const std::string& role_id);
    DiscordResponse RemoveRoleFromMember(const std::string& user_id, const std::string& role_id);
    DiscordResponse ModifyRoleColor(const std::string& role_id, int color_hex);
    DiscordResponse RenameRole(const std::string& role_id, const std::string& new_name);

    // Moderation & Member Profiles
    DiscordResponse GetMember(const std::string& user_id);
    DiscordResponse ModifyMemberNick(const std::string& user_id, const std::string& nick);
    DiscordResponse PurgeMessages(const std::string& channel_id, int amount);
    DiscordResponse KickMember(const std::string& user_id, const std::string& reason = "Expulsado desde Panel DX11");
    DiscordResponse BanMember(const std::string& user_id, const std::string& reason = "Baneado desde Panel DX11");
    DiscordResponse UnbanMember(const std::string& user_id);
    DiscordResponse TimeoutMember(const std::string& user_id, int minutes, const std::string& reason = "Aislado desde Panel DX11");
    DiscordResponse RemoveTimeout(const std::string& user_id);

    // Messages, Alerts, Stickers & Wallpapers
    DiscordResponse GetChannelMessages(const std::string& channel_id, int limit = 25);
    DiscordResponse SendTextMessage(const std::string& channel_id, const std::string& content);
    DiscordResponse SendAnsiMessage(const std::string& channel_id, const std::string& text, int color_code);
    DiscordResponse SendEmbed(const std::string& channel_id, const std::string& title, const std::string& description, int color_hex = 0x5865F2, const std::string& footer = "");
    DiscordResponse SendStickerEmbed(const std::string& channel_id, const std::string& name, const std::string& url, const std::string& category = "Sticker Oficial");
    DiscordResponse SendWallpaperEmbed(const std::string& channel_id, const std::string& title, const std::string& url, const std::string& type_label = "PC 4K");
    DiscordResponse SendWebhookMsg(const std::string& content, const std::string& username = "RafaMoDzYT");

    // Emojis & Stickers Server
    DiscordResponse GetGuildEmojis();
    DiscordResponse GetGuildStickers();
    DiscordResponse CreateGuildEmoji(const std::string& name, const std::string& image_data_base64);
    DiscordResponse DeleteGuildEmoji(const std::string& emoji_id);

    // Server Info
    DiscordResponse GetGuild();
    DiscordResponse RenameGuild(const std::string& new_name);

    // Helpers
    std::vector<DiscordChannelInfo> ParseChannels(const std::string& json_body);
    std::vector<DiscordRoleInfo> ParseRoles(const std::string& json_body);
    std::vector<DiscordChatMessage> ParseMessages(const std::string& json_body);
};
