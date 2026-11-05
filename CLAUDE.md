# Istruzioni per Claude Code

Nota: una **copia** dei loghi è anche nel repo `olivieridomenicopodcast/DomePodcast-Studio` (cartella `brand/`). Qui restano i file originali, necessari alla PWA in `docs/`. Dopo OGNI modifica ai loghi esegui `python3 tools/sincronizza_brand.py --git` (dalla radice di questo repo): copia tutto in DomePodcast-Studio e fa commit e push. Se hai modificato la copia di là, usa `--inverso` prima. Vedi il `README.md`.

Questo repo contiene i loghi di **Olivieri Domenico** (Niky), podcast coach, editor e sound designer. Rispondi in italiano.

## Cosa è "il logo"

- **Logo ufficiale** = `logo/ufficiale/logo-ufficiale.svg` (icona quadrata, monogramma DO bianco su sfumatura indaco, due onde che escono dalla O) e il suo lockup `logo/ufficiale/logo-ufficiale-orizzontale.svg`.
- **Varianti ufficiali** = tutto quello in `logo/varianti/` (nero, arancione bianco/viola, marchi senza sfondo, monocolore). Sono lo stesso logo in altri colori.
- `logo/banner/` contiene i banner LinkedIn (1584×396), generati da `tools/genera_logo.py` (`banner_linkedin`). Nuovi banner o formati social: aggiungi una funzione lì, tieni il contenuto lontano dall'angolo in basso a sinistra (foto profilo).
- `docs/` è una **PWA** per scaricare i loghi (uno per uno o tutto in ZIP), pubblicata con GitHub Pages. È generata: dopo ogni modifica ai loghi esegui `python3 tools/costruisci_app.py` e fai commit di `docs/`. Non editare a mano `docs/file`, `docs/sw.js`, `docs/catalogo.json`, lo ZIP. L'interfaccia sta in `docs/index.html`, `stile.css`, `app.js` (modificabili).
- `archivio/` contiene prove scartate (incluso il vecchio logo con la "P"): **non usarle e non ripristinarle**.

## Quando ti chiedono di usare il logo

1. Usa **sempre il logo ufficiale** se non è indicato altro.
2. Usa una variante solo se serve per il fondo o il formato (scuro, stampa monocolore, ecc.) — vedi la tabella nel `README.md`.
3. Preferisci l'**SVG**; il PNG ha sfondo trasparente.
4. Colori e font: `brand.json`. Font: Inter. Colore principale: indaco `#2A1FA6 → #5B45F2`.
5. Copia/referenzia i file, non ridisegnare il logo a mano.

## Quando ti chiedono di modificare o creare varianti

- Non toccare a mano gli SVG: modifica `tools/genera_logo.py` (aggiungi un tema in `THEMES`) e rigenera con i comandi del `README.md`.
- Non cambiare forma, proporzioni o spessori di D, O e onde: sono la parte fissa del logo.
- Se cambi il logo ufficiale, chiedi prima conferma a Niky.
- Dopo una modifica rigenera anche i PNG e le anteprime, e aggiorna il `README.md` se aggiungi/rimuovi varianti.

## Git

- Niky ha detto di fare **sempre in autonomia** commit, push e merge in `main`, senza chiedere conferma ogni volta.
- Dopo ogni modifica: commit con messaggio chiaro, push sul branch di lavoro e merge in `main` (che è il ramo da cui parte la PWA con GitHub Pages).
- Non aprire pull request se non richiesto: porta le modifiche in `main` con un merge/push diretto.
