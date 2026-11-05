#!/usr/bin/env python3
"""Sincronizza i loghi fra Crea-loghi (originali, usati dalla PWA) e DomePodcast-Studio/brand/ (copia).

Cosa viene sincronizzato (specchio esatto: aggiunge, aggiorna e RIMUOVE i file che non esistono piu' dall'altra parte):
  logo/  archivio/  brand.json  tools/genera_logo.py  tools/renderizza_png.js
NON viene toccato nient'altro: README.md e CLAUDE.md dei due repo restano diversi di proposito,
e la PWA (docs/) e gli script della PWA esistono solo in Crea-loghi.

Uso (dalla radice di Crea-loghi):
  python3 tools/sincronizza_brand.py --prova      # mostra cosa cambierebbe, senza toccare nulla
  python3 tools/sincronizza_brand.py              # Crea-loghi  ->  DomePodcast-Studio/brand/
  python3 tools/sincronizza_brand.py --git        # come sopra + commit e push su main del repo di destinazione
  python3 tools/sincronizza_brand.py --inverso    # DomePodcast-Studio/brand/  ->  Crea-loghi (se hai modificato la copia)

Posizione di DomePodcast-Studio: variabile DOMEPODCAST_STUDIO oppure la cartella accanto a questo repo
(../domepodcast-studio, ../DomePodcast-Studio); se non c'e' viene clonata da GitHub.
"""
import os, sys, shutil, filecmp, subprocess, argparse

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://github.com/olivieridomenicopodcast/DomePodcast-Studio"
CARTELLE = ["logo", "archivio"]
FILE = [("brand.json", "brand.json"), ("tools/genera_logo.py", "tools/genera_logo.py"), ("tools/renderizza_png.js", "tools/renderizza_png.js")]

def trova_studio():
    cand = [os.environ.get("DOMEPODCAST_STUDIO")] + [os.path.join(os.path.dirname(AQUI), n) for n in ("domepodcast-studio", "DomePodcast-Studio")]
    for c in cand:
        if c and os.path.isdir(os.path.join(c, ".git")): return c
    dest = os.path.join(os.path.dirname(AQUI), "domepodcast-studio")
    print("Clono DomePodcast-Studio in", dest)
    subprocess.run(["git", "clone", URL, dest], check=True)
    return dest

def elenco(base):
    out = set()
    for d, _, fs in os.walk(base):
        for f in fs: out.add(os.path.relpath(os.path.join(d, f), base))
    return out

def specchia_cartella(src, dst, prova, log):
    s = elenco(src) if os.path.isdir(src) else set(); d = elenco(dst) if os.path.isdir(dst) else set()
    for r in sorted(s):
        a, b = os.path.join(src, r), os.path.join(dst, r)
        if r not in d: log.append(("+ nuovo   ", b))
        elif not filecmp.cmp(a, b, shallow=False): log.append(("~ aggiorna", b))
        else: continue
        if not prova:
            os.makedirs(os.path.dirname(b), exist_ok=True); shutil.copy2(a, b)
    for r in sorted(d - s):
        b = os.path.join(dst, r); log.append(("- rimuovi ", b))
        if not prova: os.remove(b)
    if not prova and os.path.isdir(dst):   # toglie le cartelle rimaste vuote
        for dd, sub, fs in os.walk(dst, topdown=False):
            if not os.listdir(dd): os.rmdir(dd)

def specchia_file(src, dst, prova, log):
    if not os.path.isfile(src): return
    if not os.path.isfile(dst): log.append(("+ nuovo   ", dst))
    elif not filecmp.cmp(src, dst, shallow=False): log.append(("~ aggiorna", dst))
    else: return
    if not prova:
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)

def git(repo, *a, check=True):
    return subprocess.run(["git", "-C", repo, *a], check=check, capture_output=True, text=True)

def main():
    p = argparse.ArgumentParser(description="Sincronizza i loghi fra Crea-loghi e DomePodcast-Studio/brand")
    p.add_argument("--prova", action="store_true", help="mostra le differenze senza modificare nulla")
    p.add_argument("--inverso", action="store_true", help="copia da DomePodcast-Studio/brand verso Crea-loghi")
    p.add_argument("--git", action="store_true", help="dopo la copia fa commit e push (main) nel repo di destinazione")
    a = p.parse_args()
    studio = trova_studio(); brand = os.path.join(studio, "brand")
    sorg, dest = (brand, AQUI) if a.inverso else (AQUI, brand)
    repo_dest = AQUI if a.inverso else studio
    print(("Da DomePodcast-Studio/brand a Crea-loghi" if a.inverso else "Da Crea-loghi a DomePodcast-Studio/brand") + ("  [PROVA]" if a.prova else ""))
    log = []
    for c in CARTELLE: specchia_cartella(os.path.join(sorg, c), os.path.join(dest, c), a.prova, log)
    for f1, f2 in FILE: specchia_file(os.path.join(sorg, f1), os.path.join(dest, f2), a.prova, log)
    for tipo, percorso in log: print(tipo, os.path.relpath(percorso, dest))
    print(f"{len(log)} differenze" + (" (nessuna modifica fatta)" if a.prova else "") if log else "Gia' tutto allineato.")
    if a.git and not a.prova and log:
        git(repo_dest, "add", "-A")
        if git(repo_dest, "status", "--porcelain").stdout.strip():
            msg = "Sincronizza loghi con " + ("DomePodcast-Studio" if a.inverso else "Crea-loghi") + "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
            git(repo_dest, "commit", "-m", msg)
            r = git(repo_dest, "push", "origin", "HEAD:main", check=False)
            print("Commit e push fatti su", repo_dest if r.returncode == 0 else "-> push FALLITO: " + r.stderr)

if __name__ == "__main__":
    main()
