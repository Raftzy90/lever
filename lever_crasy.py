#!/usr/bin/env python3

import os
import re
import time
import requests
from datetime import datetime

# =========================
# LEVER STALK
# PUBLIC OSINT ONLY
# =========================

VERSION = "1.0"

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
        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120 Mobile Safari/537.36"
}


# =========================
# SCREEN
# =========================

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

    print("\r" + " " * 35 + "\r", end="")


# =========================
# LOGO
# =========================

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

    print(MAGENTA + "              L E V E R   S T A L K" + RESET)
    print(YELLOW + "                PUBLIC OSINT TOOL" + RESET)
    line()


# =========================
# VALIDATION
# =========================

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

    if not re.fullmatch(r"[A-Za-z0-9._-]+", username):
        return False

    return True


def ask_username():
    while True:
        username = input(
            f"{CYAN}Masukkan username: {WHITE}"
        ).strip().lstrip("@")

        if valid_username(username):
            return username

        print(RED + "Username tidak valid." + RESET)
        print(
            YELLOW +
            "Gunakan huruf, angka, titik, _, atau - saja."
            + RESET
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


# =========================
# PUBLIC URL CHECK
# =========================

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


# =========================
# REPORT
# =========================

def save_report(category, target, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = (
        f"lever_stalk_{category.lower().replace(' ', '_')}"
        f"_{timestamp}.txt"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("============================================\n")
        f.write("             LEVER STALK REPORT\n")
        f.write("============================================\n")
        f.write(f"Category : {category}\n")
        f.write(f"Target   : {target}\n")
        f.write(
            f"Time     : "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        f.write("--------------------------------------------\n")

        for key, value in results.items():
            f.write(f"{key}: {value}\n")

        f.write("--------------------------------------------\n")
        f.write("PUBLIC INFORMATION ONLY\n")
        f.write("============================================\n")

    return filename


# =========================
# SOCIAL STALK
# =========================

def social_stalk(platform, base_url):
    logo()

    print(BOLD + MAGENTA + f"[ STALK {platform.upper()} ]" + RESET)
    line()

    username = ask_username()

    url = base_url + username

    print()
    loading("Checking public profile")

    result = check_public_page(url)

    print()

    if result["available"]:
        print(GREEN + "[+] HALAMAN PUBLIK DITEMUKAN" + RESET)
    else:
        print(
            YELLOW +
            "[-] Halaman tidak dapat dikonfirmasi"
            + RESET
        )

    print()
    print(CYAN + "Username :" + WHITE, username)
    print(CYAN + "URL      :" + WHITE, url)
    print(CYAN + "HTTP     :" + WHITE, result["status"])

    results = {
        "Platform": platform,
        "Username": username,
        "URL": url,
        "HTTP Status": result["status"],
        "Accessible": result["available"]
    }

    filename = save_report(platform, username, results)

    print()
    print(GREEN + "[+] Report tersimpan:" + RESET)
    print(WHITE + filename)

    input(
        f"\n{YELLOW}Tekan ENTER untuk kembali...{RESET}"
    )


# =========================
# GAME STALK
# =========================

def game_stalk(game):
    logo()

    print(BOLD + MAGENTA + f"[ STALK {game.upper()} ]" + RESET)
    line()

    game_id = ask_id("Masukkan UID / ID publik")

    print()
    loading("Memproses ID")

    print()
    print(GREEN + "[+] ID diterima" + RESET)
    print(CYAN + "Game :" + WHITE, game)
    print(CYAN + "ID   :" + WHITE, game_id)

    results = {
        "Game": game,
        "Public ID": game_id,
        "Note":
            "ID dicatat sebagai data publik. "
            "Tidak mengakses database privat."
    }

    filename = save_report(game, game_id, results)

    print()
    print(GREEN + "[+] Report tersimpan:" + RESET)
    print(WHITE + filename)

    input(
        f"\n{YELLOW}Tekan ENTER untuk kembali...{RESET}"
    )


# =========================
# ABOUT
# =========================

def about():
    logo()

    print(BOLD + MAGENTA + "[ ABOUT LEVER STALK ]" + RESET)
    line()

    print(WHITE + """
LEVER STALK adalah tool OSINT sederhana untuk
mencari dan memeriksa informasi yang tersedia
secara publik.

Fitur:
  • Instagram
  • TikTok
  • Twitter
  • Facebook
  • X
  • Free Fire
  • Mobile Legends
  • FC Mobile
  • Magic Chess

Tool ini TIDAK:
  • mengambil password
  • mencuri cookie/token
  • membobol akun
  • membaca DM
  • melacak lokasi pribadi
  • mengakses database privat
  • melewati login
""" + RESET)

    print(YELLOW + "Version: " + VERSION + RESET)

    input(
        f"\n{YELLOW}Tekan ENTER untuk kembali...{RESET}"
    )


# =========================
# MAIN MENU
# =========================

def menu():
    while True:

        logo()

        print(BOLD + WHITE + "[ MENU UTAMA ]" + RESET)
        line()

        print(f"{GREEN}[1]{RESET} STALK INSTAGRAM")
        print(f"{CYAN}[2]{RESET} STALK TIKTOK")
        print(f"{MAGENTA}[3]{RESET} STALK TWITTER")
        print(f"{YELLOW}[4]{RESET} STALK FACEBOOK")
        print(f"{BLUE}[5]{RESET} STALK X")
        print(f"{GREEN}[6]{RESET} STALK FREE FIRE")
        print(f"{CYAN}[7]{RESET} STALK MOBILE LEGENDS")
        print(f"{MAGENTA}[8]{RESET} STALK FC MOBILE")
        print(f"{YELLOW}[9]{RESET} STALK MAGIC CHESS")
        print(f"{WHITE}[10]{RESET} ABOUT")
        print(f"{RED}[0]{RESET} EXIT")

        line()

        choice = input(
            f"{BOLD}{CYAN}LEVER-STALK > {WHITE}"
        ).strip()

        if choice == "1":
            social_stalk(
                "Instagram",
                "https://www.instagram.com/"
            )

        elif choice == "2":
            social_stalk(
                "TikTok",
                "https://www.tiktok.com/@"
            )

        elif choice == "3":
            social_stalk(
                "Twitter",
                "https://twitter.com/"
            )

        elif choice == "4":
            social_stalk(
                "Facebook",
                "https://www.facebook.com/"
            )

        elif choice == "5":
            social_stalk(
                "X",
                "https://x.com/"
            )

        elif choice == "6":
            game_stalk("Free Fire")

        elif choice == "7":
            game_stalk("Mobile Legends")

        elif choice == "8":
            game_stalk("FC Mobile")

        elif choice == "9":
            game_stalk("Magic Chess")

        elif choice == "10":
            about()

        elif choice == "0":
            clear()
            print(
                GREEN +
                "\nTerima kasih telah menggunakan LEVER STALK.\n"
                + RESET
            )
            break

        else:
            print(
                RED +
                "\nPilihan tidak tersedia!"
                + RESET
            )
            time.sleep(1)


# =========================
# START
# =========================

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        clear()
        print(
            YELLOW +
            "\nProgram dihentikan.\n" +
            RESET
        )