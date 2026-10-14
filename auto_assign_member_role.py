import sys
import os
import time
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import urllib.request
import json
from config import ADMIN_BOT_TOKEN, GUILD_ID

MEMBER_ROLE_ID = "1559846472080687196"

def get_headers():
    return {
        "Authorization": f"Bot {ADMIN_BOT_TOKEN}",
        "User-Agent": "DiscordBot (https://github.com/rafamodzyt, 1.0)",
        "Content-Type": "application/json"
    }

def scan_and_assign():
    channels_url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels"
    req = urllib.request.Request(channels_url, headers=get_headers())
    with urllib.request.urlopen(req) as resp:
        channels = json.loads(resp.read().decode())

    seen_users = {}
    for ch in channels:
        if ch.get("type") in (0, 5): # text / announcement
            try:
                m_url = f"https://discord.com/api/v10/channels/{ch['id']}/messages?limit=100"
                m_req = urllib.request.Request(m_url, headers=get_headers())
                with urllib.request.urlopen(m_req) as m_resp:
                    msgs = json.loads(m_resp.read().decode())
                    for m in msgs:
                        author = m.get("author")
                        if author and not author.get("bot"):
                            seen_users[author["id"]] = author
            except Exception:
                pass

    print(f"Usuarios humanos detectados en canales: {len(seen_users)}")
    
    # Cargar nombres de roles
    roles_url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles"
    req_roles = urllib.request.Request(roles_url, headers=get_headers())
    role_map = {}
    try:
        with urllib.request.urlopen(req_roles) as r_resp:
            for r in json.loads(r_resp.read().decode()):
                role_map[r["id"]] = r["name"]
    except Exception:
        pass

    members_list = []
    assigned_count = 0
    for uid, u in seen_users.items():
        username = u.get("username", uid)
        try:
            mem_url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{uid}"
            mem_req = urllib.request.Request(mem_url, headers=get_headers())
            with urllib.request.urlopen(mem_req) as mem_resp:
                mem = json.loads(mem_resp.read().decode())
                user_obj = mem.get("user", u)
                roles = mem.get("roles", [])
                
                # Asignar Member si no lo tiene
                if MEMBER_ROLE_ID not in roles:
                    add_url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{uid}/roles/{MEMBER_ROLE_ID}"
                    add_req = urllib.request.Request(add_url, headers=get_headers(), method="PUT")
                    with urllib.request.urlopen(add_req) as add_resp:
                        print(f"[OK] Rol Member asignado a: {username} ({uid})")
                        assigned_count += 1
                        roles.append(MEMBER_ROLE_ID)
                else:
                    print(f"[INFO] {username} ya tiene el rol Member.")

                avatar_hash = user_obj.get("avatar") or ""
                avatar_url = f"https://cdn.discordapp.com/avatars/{uid}/{avatar_hash}.png" if avatar_hash else ""
                
                role_names = [role_map.get(rid, rid) for rid in roles]
                members_list.append({
                    "id": uid,
                    "name": username,
                    "tag": f"{username}#{user_obj.get('discriminator', '0000')}",
                    "nick": mem.get("nick") or username,
                    "status": "ONLINE",
                    "bot": user_obj.get("bot", False),
                    "roles": role_names,
                    "joined_at": mem.get("joined_at", "")[:10],
                    "avatar_url": avatar_url
                })
                time.sleep(1.0)
        except Exception as ex:
            print(f"[ERROR] Procesando {username}: {ex}")
            time.sleep(1.5)

    # Guardar en live_members.json
    try:
        live_file = "live_members.json"
        data = {"server_name": "SHADOW BLOCK", "guild_id": str(GUILD_ID), "events": [], "members": []}
        if os.path.exists(live_file):
            with open(live_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        data["members"] = members_list
        with open(live_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[EXITO] {len(members_list)} miembros sincronizados en live_members.json")
    except Exception as e:
        print(f"[ERROR] Guardando live_members.json: {e}")

    print(f"Finalizado. Total de roles asignados: {assigned_count}")

if __name__ == "__main__":
    scan_and_assign()
