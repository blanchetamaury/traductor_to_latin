import libpy as lp
import os
import sys
import json, urllib.parse, urllib.request, urllib.error

def get_trad(word):
    params = urllib.parse.urlencode({
        "q": word,
        "langpair": "fr|la"
    })
    url = f"https://api.mymemory.translated.net/get?{params}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.load(r)
    except urllib.error.URLError as e:
        print("Erreur réseau :", e)
        return None
    best = data.get("responseData", {}).get("translatedText")
    if best:
        return best.lower()
    for m in data.get("matches", []):
        if m.get("translation"):
            return m["translation"].lower()
    return None


def add_csv(name, new1, new2):
    fd_in = os.open(name + ".csv", os.O_WRONLY | os.O_APPEND)
    os.write(fd_in, '\n'.encode() + new1.encode() + ','.encode())
    os.write(fd_in, new2.encode())

def add_new_word_verif(cleaned_str, fd_in, fd):
    os.write(fd_in, "\nAdd new word ".encode() + cleaned_str.encode() + "? (yes/no)\n".encode())
    str = ''
    while 1:
        char = os.read(fd, 1).decode() # decode = passer de bytes a string et inversement
        str += char
        if char == '\n':
            find = str.strip() # retirer le \n en trop
            if find == "yes":
                add_csv("database", cleaned_str, get_trad(cleaned_str))
                return 0
            else:
                return 1

def main():
    list = lp.import_csv("database")
    fd_in = sys.stdout.fileno()
    fd = sys.stdin.fileno()
    str = ''
    tra = ''
    line = ''
    while 1:
        os.write(fd_in, b'\x1b[2J\x1b[H')  # ANSI CSI: efface + home
        fr_field = line.strip() + " " * max(0, 32 - lp.strlen(line.strip()))
        la_field = tra.strip() + " " * max(0, 32 - lp.strlen(tra.strip()))
        os.write(fd_in, b"----------------------------------------\n")
        os.write(fd_in, b"| FR : " + fr_field.encode() + b"|\n")
        os.write(fd_in, b"| LA : " + la_field.encode() + b"|\n")
        os.write(fd_in, b"----------------------------------------\n")
        os.write(fd_in, b"INPUT: " + str.encode())
        char = os.read(fd, 1).decode() # decode = passer de bytes a string et inversement
        str += char
        if char == '\n':
            cleaned_str = str.strip() # retirer le \n en trop
            if cleaned_str == "exit":
                    os.close(fd)
                    os.close(fd_in)
                    return 0
            status = 0
            for i in list:
                if i['francais'] == cleaned_str:
                    status = 1
                    os.write(fd_in, i['latin'].encode() + '\n'.encode())
                    tra = i['latin']
                    line = str
            if status == 0:
                os.write(fd_in, "Error word not found\n".encode())
                add = add_new_word_verif(cleaned_str, fd_in, fd)
                if add == 0:
                    list = lp.import_csv("database")
            str = ''
    return 0

if __name__ == "__main__":
    main()