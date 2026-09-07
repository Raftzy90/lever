#!/usr/bin/env python3

import os
import re
import time
import shutil
import subprocess
import requests
from datetime import datetime

# ============================================================
# LEVER STALK
# PUBLIC OSINT + DEVICE UTILITY
# Version 2.0
# ============================================================

VERSION = "2.0"

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"

UA = {
    "User-Agent":
        "Mozilla/5.0 (Linux; Android 10) "
        "AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36"
}


# ============================================================
# SCREEN
# ============================================================

def clear():
    os.system("clear")


def line():
    print(CYAN + "═" * 58 + RESET)


def loading(text="Loading"):
    chars = ["|", "/", "-", "\\"]

    for i in range(12):
        print(
            f"\r{YELLOW}{text} {chars[i % len(chars)]}{RESET}",
            end="",
            flush=True
        )
        time.sleep(0.08)

    print("\r" + " " * 60 + "\r", end="")


# ============================================================
# LOGO
# ============================================================

def logo():
    clear()

    print(CYAN + r"""
██╗     ███████╗██╗   ██╗███████╗██████╗
██║     ██╔════╝██║   ██║██╔════╝██╔══██╗
██║     █████╗  ██║   ██║█████╗  ██████╔╝
██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████╗███████╗ ╚████╔╝ ███████╗██║  ██║
╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

 ██████╗██████╗  █████╗ ███████╗██╗   ██╗
██╔════╝██╔══██╗██╔══██╗██╔════╝╚██╗ ██╔╝
██║     ██████╔╝███████║███████╗ ╚████╔╝
██║     ██╔══██╗██╔══██║╚════██║  ╚██╔╝
╚██████╗██║  ██║██║  ██║███████║   ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝
""" + RESET)

    print(
        MAGENTA +
        "              L E V E R   S T A L K" +
        RESET
    )

    print(
        YELLOW +
        "          PUBLIC OSINT + DEVICE TOOL" +
        RESET
    )

    line()


# ============================================================
# VALIDATION
# ============================================================

def valid_username(username):
    username = username.strip().lstrip("@")

    if not username:
        return False

    if len(username) > 50:
        return False

    if username.startswith(("http://", "https://")):
        return False

    if any(x in username for x in ["/", "\\", " ", "\n", "\r"]):
        return False

    return bool(re.fullmatch(r"[A-Za-z0-9._-]+", username))


def ask_username():
    while True:
        username = input(
            f"{CYAN}Masukkan username: {WHITE}"
        ).strip().lstrip("@")

        if valid_username(username):
            return username

        print(
            RED +
            "Username tidak valid." +
            RESET
        )

        print(
            YELLOW +
            "Gunakan huruf, angka, titik, _ atau -." +
            RESET
        )


def ask_id(label):
    while True:
        value = input(
            f"{CYAN}{label}: {WHITE}"
        ).strip()

        if not value:
            print(RED + "ID tidak boleh kosong." + RESET)
            continue

        if len(value) > 50:
            print(RED + "ID terlalu panjang." + RESET)
            continue

        if re.fullmatch(r"[A-Za-z0-9._-]+", value):
            return value

        print(RED + "Format ID tidak valid." + RESET)


# ============================================================
# PUBLIC URL CHECK
# ============================================================

def check_public_page(url):
    try:
        r = requests.get(
            url,
            headers=UA,
            timeout=10,
            allow_redirects=True
        )

        return {
            "status": r.status_code,
            "final_url": r.url,
            "available": r.status_code == 200
        }

    except requests.RequestException as e:
        return {
            "status": "ERROR",
            "final_url": url,
            "available": False,
            "error": str(e)
        }


# ============================================================
# REPORT
# ============================================================

def save_report(category, target, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    safe_category = re.sub(
        r"[^A-Za-z0-9_-]",
        "_",
        category.lower()
    )

    filename = (
        f"lever_stalk_{safe_category}_"
        f"{timestamp}.txt"
    )

    with open(filename, "w", encoding="utf-8") as f:

        f.write("=" * 44 + "\n")
        f.write("             LEVER STALK REPORT\n")
        f.write("=" * 44 + "\n")

        f.write(f"Category : {category}\n")
        f.write(f"Target   : {target}\n")

        f.write(
            "Time     : " +
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ) +
            "\n"
        )

        f.write("-" * 44 + "\n")

        for key, value in results.items():
            f.write(f"{key}: {value}\n")

        f.write("-" * 44 + "\n")
        f.write("PUBLIC INFORMATION ONLY\n")
        f.write("=" * 44 + "\n")

    return filename


# ============================================================
# SOCIAL STALK
# ============================================================

def social_stalk(platform, base_url):

    logo()

    print(
        BOLD +
        MAGENTA +
        f"[ STALK {platform.upper()} ]" +
        RESET
    )

    line()

    username = ask_username()

    url = base_url + username

    print()
    loading("Checking public profile")

    result = check_public_page(url)

    print()

    if result["available"]:

        print(
            GREEN +
            "[+] HALAMAN PUBLIK DITEMUKAN" +
            RESET
        )

    else:

        print(
            YELLOW +
            "[-] Halaman tidak dapat dikonfirmasi" +
            RESET
        )

    print()

    print(
        CYAN + "Username :" +
        WHITE,
        username
    )

    print(
        CYAN + "URL      :" +
        WHITE,
        url
    )

    print(
        CYAN + "HTTP     :" +
        WHITE,
        result["status"]
    )

    results = {
        "Platform": platform,
        "Username": username,
        "URL": url,
        "HTTP Status": result["status"],
        "Accessible": result["available"]
    }

    filename = save_report(
        platform,
        username,
        results
    )

    print()

    print(
        GREEN +
        "[+] Report tersimpan:" +
        RESET
    )

    print(WHITE + filename)

    input(
        f"\n{YELLOW}Tekan ENTER untuk kembali...{RESET}"
    )


# ============================================================
# GAME STALK
# ============================================================

def game_stalk(game):

    logo()

    print(
        BOLD +
        MAGENTA +
        f"[ STALK {game.upper()} ]" +
        RESET
    )

    line()

    game_id = ask_id("Masukkan UID / ID publik")

    print()

    loading("Memproses ID")

    print()

    print(
        GREEN +
        "[+] ID diterima" +
        RESET
    )

    print(
        CYAN + "Game :" +
        WHITE,
        game
    )

    print(
        CYAN + "ID   :" +
        WHITE,
        game_id
    )

    results = {
        "Game": game,
        "Public ID": game_id,
        "Note":
            "ID dicatat sebagai data publik. "
            "Tidak mengakses database privat."
    }

    filename = save_report(
        game,
        game_id,
        results
    )

    print()

    print(
        GREEN +
        "[+] Report tersimpan:" +
        RESET
    )

    print(WHITE + filename)

    input(
        f"\n{YELLOW}Tekan ENTER untuk kembali...{RESET}"
    )


# ============================================================
# WHATSAPP PUBLIC PROFILE
# ============================================================

def whatsapp_stalk():

    logo()

    print(
        BOLD +
        MAGENTA +
        "[ WHATSAPP PUBLIC PROFILE ]" +
        RESET
    )

    line()

    phone = input(
        f"{CYAN}Masukkan nomor WhatsApp (+62...): {WHITE}"
    ).strip()

    phone_clean = re.sub(
        r"[^\d+]",
        "",
        phone
    )

    if not phone_clean:

        print(
            RED +
            "Nomor tidak valid." +
            RESET
        )

        input(
            f"\n{YELLOW}Tekan ENTER...{RESET}"
        )

        return

    if phone_clean.startswith("+"):
        wa_number = phone_clean[1:]
    else:
        wa_number = phone_clean

    if len(wa_number) < 8:

        print(
            RED +
            "Nomor terlalu pendek." +
            RESET
        )

        input(
            f"\n{YELLOW}Tekan ENTER...{RESET}"
        )

        return

    url = f"https://wa.me/{wa_number}"

    print()

    loading(
        "Memeriksa WhatsApp public link"
    )

    result = check_public_page(url)

    print()

    print(
        CYAN +
        "Nomor :" +
        WHITE,
        phone_clean
    )

    print(
        CYAN +
        "URL   :" +
        WHITE,
        url
    )

    print(
        CYAN +
        "HTTP  :" +
        WHITE,
        result["status"]
    )

    print()

    if result["available"]:

        print(
            GREEN +
            "[+] LINK WHATSAPP DAPAT DIAKSES" +
            RESET
        )

    else:

        print(
            YELLOW +
            "[-] Link tidak dapat dikonfirmasi." +
            RESET
        )

    print()

    print(
        YELLOW +
        "Catatan: fitur ini hanya memeriksa "
        "tautan WhatsApp publik."
        + RESET
    )

    print(
        YELLOW +
        "Tidak mengambil chat, password, lokasi, "
        "status, atau data privat."
       
