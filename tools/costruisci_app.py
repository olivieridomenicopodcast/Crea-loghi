"""Costruisce la PWA (cartella docs/) copiando i loghi da logo/ e creando ZIP, catalogo e service worker.

Uso:  python3 tools/costruisci_app.py     (dopo aver rigenerato i loghi: genera_logo.py + renderizza_png.js)
La cartella docs/ si pubblica con GitHub Pages (Settings > Pages > Deploy from a branch > /docs).
"""
import os, json, shutil, hashlib, zipfile
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=ROOT+"/logo/"; D=ROOT+"/docs/"; F=D+"file/"
# (cartella, nome file senza estensione, titolo, nota, sfondo anteprima)
CATALOGO=[
 ("Logo ufficiale","Il logo da usare di default.",[
  ("ufficiale","logo-ufficiale","Icona ufficiale","Quadrata 1024×1024. Foto profilo, app, cover","chiaro"),
  ("ufficiale","logo-ufficiale-orizzontale","Logo orizzontale ufficiale","Con nome e descrizione. Banner, firme email, sito","chiaro")]),
 ("Banner LinkedIn","Formato 1584×396, PNG a doppia risoluzione.",[
  ("banner","banner-linkedin-chiaro","Banner chiaro","Sfondo bianco, versione di riferimento","chiaro"),
  ("banner","banner-linkedin-indaco","Banner indaco","Sfondo viola a tutta larghezza","chiaro")]),
 ("Varianti ufficiali","Stesso logo in altri colori, per fondi e stampe diverse.",[
  ("varianti","icona-nero","Icona nera","Quadrata, lettere bianche","chiaro"),
  ("varianti","icona-arancione-bianco","Icona arancione, lettere bianche","Quadrata","chiaro"),
  ("varianti","icona-arancione-viola","Icona arancione, lettere viola","Quadrata","chiaro"),
  ("varianti","logo-banner-nero","Orizzontale nero","Con nome e descrizione","chiaro"),
  ("varianti","logo-banner-arancione-bianco","Orizzontale arancione, testo bianco","Con nome e descrizione","chiaro"),
  ("varianti","logo-banner-arancione-viola","Orizzontale arancione, testo viola","Con nome e descrizione","chiaro"),
  ("varianti","logo-colore","Orizzontale a colori, senza sfondo","Per fondi chiari","chiaro"),
  ("varianti","logo-nero","Orizzontale nero, senza sfondo","Monocolore, per stampe","chiaro"),
  ("varianti","logo-arancione","Orizzontale arancione, senza sfondo","Monocolore","chiaro"),
  ("varianti","marchio-colore","Marchio a colori","Solo DO e onde, senza sfondo","chiaro"),
  ("varianti","marchio-nero-mono","Marchio nero","Monocolore, per timbri e ricami","chiaro"),
  ("varianti","marchio-arancione-mono","Marchio arancione","Monocolore","chiaro"),
  ("varianti","marchio-bianco-mono","Marchio bianco","Per fondi scuri o foto","scuro")]),
]
shutil.rmtree(F,ignore_errors=True)
cat=[];precache=["./","index.html","stile.css","app.js","catalogo.json","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png","icons/icon-maskable-512.png","logo-olivieri-domenico.zip"]
zp=D+"logo-olivieri-domenico.zip"
z=zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED)
z.writestr("LEGGIMI.txt","Logo Olivieri Domenico\n\nufficiale/  logo ufficiale (da usare di default)\nbanner/     banner LinkedIn 1584x396\nvarianti/   varianti ufficiali (colori e monocolore)\n\nPreferisci SVG (vettoriale); i PNG hanno sfondo trasparente.\n")
for g,desc,items in CATALOGO:
    out=[]
    for cart,nome,titolo,nota,sfondo in items:
        os.makedirs(F+cart,exist_ok=True)
        for ext in ("png","svg"):
            src=f"{L}{cart}/{nome}.{ext}"; shutil.copy(src,f"{F}{cart}/{nome}.{ext}"); z.write(src,f"{cart}/{nome}.{ext}")
            precache.append(f"file/{cart}/{nome}.{ext}")
        out.append(dict(titolo=titolo,nota=nota,sfondo=sfondo,nome=nome,png=f"file/{cart}/{nome}.png",svg=f"file/{cart}/{nome}.svg"))
    cat.append(dict(gruppo=g,descrizione=desc,voci=out))
z.close()
json.dump(dict(gruppi=cat,zip="logo-olivieri-domenico.zip",zip_mb=round(os.path.getsize(zp)/1e6,1)),open(D+"catalogo.json","w"),ensure_ascii=False,indent=1)
h=hashlib.sha1()
for p in sorted(precache):
    fp=D+p
    if os.path.isfile(fp): h.update(open(fp,"rb").read())
ver=h.hexdigest()[:10]
sw=open(ROOT+"/tools/sw.template.js").read().replace("__VERSIONE__",ver).replace("__FILE__",json.dumps(precache))
open(D+"sw.js","w").write(sw)
print("App costruita: versione",ver,"-",len(precache),"file in cache")
