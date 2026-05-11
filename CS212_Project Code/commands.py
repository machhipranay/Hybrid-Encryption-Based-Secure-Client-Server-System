import hashlib
from datetime import datetime
import random
import string

stats = {
    "clients": 0,
    "commands": 0
}

def handle_command(cmd, role="user"):
    stats["commands"] += 1

    if cmd.startswith("ECHO"):
        return cmd[5:]

    elif cmd.startswith("REVERSE"):
        return cmd[8:][::-1]

    elif cmd.startswith("TIME"):
        return str(datetime.now())

    elif cmd.startswith("HASH"):
        return hashlib.sha256(cmd[5:].encode()).hexdigest()

    elif cmd.startswith("UPPER"):
        return cmd[6:].upper()

    elif cmd.startswith("LOWER"):
        return cmd[6:].lower()

    elif cmd.startswith("LEN"):
        return str(len(cmd[4:]))

    elif cmd.startswith("PAL"):
        text = cmd[4:]
        return "YES" if text == text[::-1] else "NO"

    elif cmd.startswith("RANDOM"):
        parts = cmd.split()
        length = int(parts[1]) if len(parts) > 1 else 10
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    elif cmd.startswith("CALC"):
        try:
            expr = cmd[5:]
            return str(eval(expr))
        except:
            return "Invalid expression"

    elif cmd.startswith("WHOAMI"):
        return f"Role: {role}"

    elif cmd.startswith("STATS"):
        if role != "admin":
            return "Unauthorized"
        return str(stats)

    elif cmd.startswith("CLEARSTATS"):
        if role != "admin":
            return "Unauthorized"
        stats["commands"] = 0
        stats["clients"] = 0
        return "Stats reset"

    elif cmd.startswith("HELP"):
        return help_text()

    elif cmd.startswith("EXIT"):
        return "Disconnecting from server..."

    else:
        return "Invalid command"
    
def help_text():
    return (
        "Available Commands:\n"
        "\tECHO <msg>\n"
        "\tREVERSE <msg>\n"
        "\tTIME\n"
        "\tHASH <msg>\n"
        "\tUPPER <msg>\n"
        "\tLOWER <msg>\n"
        "\tLEN <msg>\n"
        "\tPAL <msg> (palindrome check)\n"
        "\tRANDOM <length>\n"
        "\tCALC <expression>\n"
        "\tWHOAMI\n"
        "\tSTATS (admin only)\n"
        "\tCLEARSTATS (admin only)\n"
        "\tHELP\n"
        "\tEXIT"
    )