# Receta: video de la ruleta + plantilla "5 pasos"

Receta exacta para que cualquier agente haga los videos **iguales** al aprobado por Coqui
(`entregas/promo-app/2026-11-12-ruleta-gta.mp4`, versión 3). Sigue los pasos en orden y no cambies valores sin
permiso de Coqui.

**Resultado:** MP4 vertical 1080×1920, 30 fps, H.264 + AAC. Dura lo que dure el video de Coqui más 14 s de
plantilla. Ejemplo: 8,8 + 14 = 22,8 s. Lo ideal según Coqui es grabar unos 15 s para llegar a 28–30 s.

---

## 0. Antes de empezar

1. Lee `CLAUDE.md`, `agentes/promo-app.md` y esta receta.
2. Herramientas: los plugins HyperFrames y watch (en `.claude/settings.json`), ffmpeg y Python 3.
   - El CLI de HyperFrames se llama así (en esta receta: `HF`):
     ```bash
     HF="node $(ls -d ~/.claude/plugins/cache/hyperframes/hyperframes/*/ | tail -1)skills/hyperframes/scripts/plugin-cli.mjs"
     ```
   - Antes de tocar composiciones, carga la skill `hyperframes`.
3. Archivos base, que **no se modifican** salvo que Coqui pida cambiar la plantilla:
   - `proyectos/promo-app/pasos-cta/generar.py`: genera la plantilla de 5 pasos y la raíz del video.
   - `proyectos/promo-app/pasos-cta/assets/`: banner, avatar y efectos de sonido (licencia Pixabay, ver `sfx/CREDITS.md`).
   - `proyectos/promo-app/herramientas/sonido_ruleta.py`: sonido de la ruleta sincronizado.
   - `proyectos/promo-app/2026-11-12-ruleta/`: proyecto de ejemplo completo. Cópialo como punto de partida.

## 1. Revisar el video de Coqui

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,color_transfer -of compact VIDEO.MOV
```
- Los iPhone graban **vertical con rotación** (salen como 1920×1080 con `rotation=-90`) y en **HDR**
  (`color_transfer=arib-std-b67`). El paso 3 corrige las dos cosas.
- Mira cuadros sueltos (4 por segundo) para ubicar: cuándo toca SPIN, cuándo se frena la ruleta y en qué segundo
  aparece la pantalla del resultado (`T_RESULTADO`). En el ejemplo: toque ≈0,65 s, frena ≈5,4 s y resultado 6,27 s.
- **No se corta el giro.** El video de Coqui va completo, sin quitar ni un cuadro del giro.

## 2. Crear el proyecto nuevo

```bash
cd proyectos/promo-app
NUEVO=AAAA-MM-DD-nombre
cp -r 2026-11-12-ruleta $NUEVO
rm -rf $NUEVO/.hyperframes $NUEVO/assets/footage/*
```
El `.gitignore` del proyecto ya excluye `assets/footage/`: los videos de Coqui **no se suben** (el repo es público).

## 3. Pasar el video a vertical y SDR (colores normales)

```bash
ffmpeg -y -i VIDEO.MOV -map 0:v:0 -an \
  -vf "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,eq=saturation=1.12:contrast=1.04" \
  -c:v libx264 -crf 17 -preset medium -g 15 -movflags +faststart $NUEVO/assets/footage/ruleta.mp4
```
- Si el video **no es HDR**, usa solo `-vf "scale=1080:1920,eq=saturation=1.12:contrast=1.04"`.
- El audio original no se usa: es casi silencio y el sonido de la ruleta se genera aparte (paso 5).

## 4. Fondo de la plantilla (último cuadro, poco oscuro y poco desenfocado)

```bash
ffmpeg -y -sseof -0.1 -i $NUEVO/assets/footage/ruleta.mp4 -frames:v 1 -update 1 \
  -vf "boxblur=6:1,eq=brightness=-0.06:saturation=0.95" $NUEVO/assets/footage/fondo-final.jpg
```
Coqui pidió que el fondo **no se vea tan oscuro ni tan difuminado**. No subas el blur de 6 ni oscurezcas más de -0.06.

## 5. Sonido de la ruleta (el mismo de su HTML, sincronizado)

El sonido sale del HTML original de la ruleta: un "tic" por casilla (onda cuadrada de 1100 Hz) y una fanfarria de
5 notas al ganar. **No uses clicks de librería**, porque Coqui los rechazó.

1. Ubica la punta de la flecha en `ruleta.mp4` (ya vertical) y toma un punto unos 50 px debajo, dentro de las
   casillas. En el ejemplo fue x=445, y=725.
2. Detecta los cambios de casilla:
   ```bash
   python3 -I herramientas/sonido_ruleta.py detectar $NUEVO/assets/footage/ruleta.mp4 445 725
   ```
3. Toma los **dos últimos tics lentos** antes de que se detenga (en el ejemplo, 4,167 y 4,633). Ignora los que salen
   después del resultado: son la animación de la pantalla de premio. Ajusta el modelo con el momento del resultado:
   ```bash
   python3 -I herramientas/sonido_ruleta.py ajustar 6.25 4.167 4.633
   # -> T0=0.650  E=64.42  R0=0.448
   ```
   Comprueba que los "tic modelo" coincidan con los cambios detectados de la zona lenta (±0,03 s).
   - `T_RESULTADO` = primer cuadro donde aparece la pantalla de premio, menos 0,02 s. `T0` = `T_RESULTADO` − 5,6.
   - Si la cámara se mueve mucho, prueba 2 o 3 puntos cerca de la flecha y quédate con los tics que se repiten
     en todos, solo en la zona lenta (de 1 a 2,5 s antes del resultado). `E` tiene que quedar entre 38 y 63.
   - Ejemplos aprobados:
     | Video | Duración | T_RESULTADO | Tics usados | T0 | E | R0 | Fanfarria |
     |---|---|---|---|---|---|---|---|
     | IMG_3105 (`2026-11-12-ruleta`) | 8.8 | 6.25 | 4.167 / 4.633 | 0.65 | 64.5 | 0.45 | 6.27 |
     | IMG_3108 (`2026-11-12-ruleta-2`) | 10.26 | 7.81 | 5.55 / 5.967 | 2.21 | 53.08 | 0.623 | 7.83 |
     | IMG_3154 (`2026-11-13-ruleta-3`) | 10.8 | 8.05 | 5.633 / 6.05 | 2.45 | 42.61 | 0.693 | 8.07 |
4. Genera el audio. Argumentos: duración del video, T0, E, R0 y el segundo de la fanfarria (= `T_RESULTADO`):
   ```bash
   python3 -I herramientas/sonido_ruleta.py generar $NUEVO/assets/sfx/ruleta-giro.wav 8.8 0.65 64.5 0.45 6.27
   ```

## 6. Configurar `intro.json`

```json
{
 "duration": 8.8,
 "endbg": "assets/footage/fondo-final.jpg",
 "sfx": [
  ["i-ruleta", "ruleta-giro.wav", 0.0, 0.9, 8.8],
  ["i-wh", "whoosh", 8.5, 0.6, 0.57]
 ]
}
```
- `duration` = duración exacta del video de Coqui.
- El `whoosh` va 0,3 s antes del final del video. Para otra duración, usa `duration - 0.3`.
- Nada más: **sin** golpe grave ni brillo en el resultado (Coqui quiere solo el sonido de su ruleta).

## 7. Ajustar `compositions/intro.html`

Copia el del ejemplo y cambia **solo los tiempos** según el video nuevo:

| Qué | Valor en el ejemplo | Regla |
|---|---|---|
| `data-duration` del `<video>` | 8.8 | = duración del video |
| Golpe de cámara (`#intro-cam` scale 1.12, 0,45 s, `power3.out`) | 6.3 | = `T_RESULTADO` |
| Destello blanco (0,75 → 0 en 0,45 s, con `immediateRender: false`) | 6.32 | resultado + 0,02 |
| Sale "CAN I LAND GTA VI?" (blur 10 px, 0,15 s) | 6.3 | = resultado |
| Entra "IT LANDED ON" (blur 8 → 0, 0,22 s) | 6.38 | resultado + 0,08 |
| Entra "GTA VI!" (scale 0,3 → 1, `back.out(2.2)`, 0,5 s) | 6.46 | resultado + 0,16 |
| Salida: cámara a 1,3 y negro a **0,3** (0,35 s) | 8.45 | duración − 0,35 |

Diseño fijo del intro:
- Arriba, sobre un degradado oscuro de 560 px: **"CAN I LAND GTA VI?"** (Archivo Black 80 px, "GTA VI?" con
  degradado rosa → dorado). Se ve **desde el cuadro 0**, porque es el gancho.
- Al caer: **"IT LANDED ON GTA VI!"** en el mismo lugar.
- **Sin letreros abajo.** Coqui pidió quitar "WATCH WHERE IT STOPS", "ONE TAKE · NO CUTS" y la franja de la nota.
- Cambia el texto del gancho solo si el premio es otro, y siempre en inglés.

## 8. Generar y revisar

```bash
cd proyectos/promo-app/$NUEVO
python3 -I ../pasos-cta/generar.py . intro.json   # crea index.html y las escenas s1..s5 a continuación del video
$HF check --json          # debe dar "ok": true (el aviso line_unread de #s3-typed es normal)
$HF snapshot --at 0,3,T_RESULTADO+0.1,DURACION+1,DURACION+12 --json
```
Mira las imágenes antes de renderizar: el gancho tiene que verse en el cuadro 0, el destello y "GTA VI!" en el
resultado, y la plantilla legible sobre el fondo.

## 9. Render y entrega

```bash
$HF render --quality delivery --output /tmp/.../render.mp4
ffmpeg -y -i /tmp/.../render.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k \
  -movflags +faststart ../../../entregas/promo-app/AAAA-MM-DD-nombre.mp4
```
- Volumen: -14 LUFS, el estándar de redes.
- Guarda la entrega en `entregas/promo-app/AAAA-MM-DD-nombre.mp4`. Si pesa más de 50 MB, entrégala solo en el chat.
- Commit y push a la rama del agente. Muéstrale el MP4 a Coqui en el chat y resume en 2 o 3 líneas qué hiciste.

---

## La plantilla "5 pasos" (no se toca)

Dura 14 s y la genera `generar.py`. Ya está aprobada por Coqui (v3):

| Paso | Dura | Qué pasa |
|---|---|---|
| 1 · LIKE THE VIDEO | 2,0 s | El toque presiona el pulgar, se pinta rosa-dorado y salen chispas de diamante |
| 2 · SUBSCRIBE | 2,2 s | "SUBSCRIBE" pasa a "SUBSCRIBED ✓" y luego se toca la campanita, que se mueve y se pone dorada |
| 3 · DROP A COMMENT | 3,0 s | Se escribe "This channel is fire 💎", se envía y aparece publicado |
| 4 · SHARE IT | 2,2 s | Se abre el menú de compartir y se toca "Copy link" |
| 5 · VISIT THE CHANNEL | 4,6 s | Captura tipo YouTube en modo oscuro (banner, foto, The Diamond Royale, @TheDiamondRoyale, bit.ly/4iD7KGP). Se toca **Subscribe** → "🔔 Subscribed" y luego **el link de la bio**, que abre una página con barra de carga |

- Números: Montserrat 900 cursiva, relleno cromado y sombra rosa desplazada. Entran girando en 3D con rebote, un aro
  dorado, dos contornos (azul y rosa) y un brillo que los cruza.
- Arriba siempre: "Giveaway rules at the link · Not affiliated with Rockstar Games" y la barra de 5 segmentos.
- Títulos, "STEP 0X" y la nota de arriba llevan sombra para que se lean sobre el fondo claro.

## Otros juegos (ejemplo: vasos y bola, `2026-11-12-vasos`)

- **Si la grabación ya trae el sonido del juego** (se oye en el audio original), úsalo en vez de generar uno:
  ```bash
  ffmpeg -y -ss INICIO -i VIDEO.MOV -map 0:a:0 -af "highpass=f=100,afftdn=nf=-30,acompressor=threshold=-32dB:ratio=4:attack=5:release=120:makeup=8,loudnorm=I=-16:TP=-2:LRA=9" -ar 48000 -ac 2 assets/sfx/juego-audio.wav
  ```
  y en `intro.json` pon `["i-juego", "juego-audio.wav", 0.0, 1.0, DURACION]`.
- Se puede recortar **solo el tiempo muerto del inicio**, antes de que empiece el juego (en los vasos: 2,2 s). Lo
  que muestra el juego (revuelto, elección y resultado) no se corta.
- El fondo de la plantilla sale del cuadro donde **se ve el premio claro** (`-ss` en ese segundo), no del último
  cuadro si la mano lo tapa.
- `intro.html` admite varias etapas de texto (ver `2026-11-12-vasos/compositions/intro.html`): gancho → durante el
  juego → al elegir → al acertar → en el premio (con golpe de cámara y destello).

## Estilo "más llamativo" (ruleta 3)

`2026-11-13-ruleta-3/compositions/intro.html`: frases cortas que cambian con cada momento del giro (antes, al
arrancar, al frenar, al final). Cada palabra entra con golpe (escala 2,2 → 1 con desenfoque), la cámara empuja en
cada frase y al ganar hay destello, sacudida, zoom, tinte rosa y un texto gigante dorado.
Voz: se puede usar `hyperframes tts` (Kokoro, gratis y local), pero necesita `pip install kokoro-onnx soundfile`
y en esta nube ese permiso está bloqueado. Pídele a Coqui que lo autorice antes de intentarlo.

## Textos: nunca repetir

Coqui pidió **no repetir nunca** los textos de un video a otro, ni en el video ni en los títulos. Antes de escribir,
revisa esta lista y agrega los tuyos al terminar.

| Video | Textos en pantalla | Comentario del paso 3 (`"comment"` en `intro.json`) | Título |
|---|---|---|---|
| Ruleta 1 | CAN I LAND GTA VI? / IT LANDED ON GTA VI! | This channel is fire | I Spun the Wheel… and It Landed on GTA VI 😱🎰 |
| Ruleta 2 | (mismos que ruleta 1, hecho antes de esta regla) | This channel is fire | Spun It Again… GTA VI AGAIN?! 😱🎰 |
| Vasos | KEEP YOUR EYE ON THE BALL / DON'T BLINK... / WHICH CUP HAS IT? / FOUND IT! / PERFECT PICK! | Need more of these! | Can You Track the Ball? I Went for GTA VI 👀🥤 |
| Ruleta 3 | NO RETRIES. / ALL OR NOTHING. / HERE WE GO! / SLOWING DOWN... / COME ON... COME ON! / JACKPOT!! / TOP PRIZE | Insane luck bro | Jackpot or Bust? Watch Till the Last Tick 🤑🎰 |

Los títulos de la plantilla de 5 pasos (LIKE THE VIDEO, SUBSCRIBE, etc.) son fijos: son la plantilla.

## Reglas que no se rompen

- **No se ponen cifras falsas** de suscriptores ni de videos en la captura del canal (Coqui pidió 8765; se le dijo que
  no). Se deja sin esa línea o con los números reales.
- No se pone la línea "CLAIM NOW" de la bio en la captura.
- El giro va completo, sin cortes que cambien el resultado.
- Los textos que se publican van en **inglés**.
- Los videos de Coqui y su cara o datos no se suben al repositorio.
- Si el video se va a publicar en el canal (no solo para la clase), avisa a Coqui: en su pantalla salen "CLAIM",
  "Unlock more attempts" y arte oficial de GTA VI. Ofrécele desenfocarlos.
