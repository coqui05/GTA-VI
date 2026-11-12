"""Sonido de la ruleta sincronizado con el video de Coqui.

La ruleta (Vice_Spin_Wheel / ruleta.html) gira así:
  ángulo(t) = inicio + E * (1 - (1 - p)^4),  p = (t - t0) / 5.6 s,  8 casillas.
Cada vez que una casilla cruza la flecha suena un "tic" (onda cuadrada 1100 Hz, 0.12 -> 0.001 en 40 ms).
Al terminar suena la fanfarria (triángulo 523-659-784-1047-1319 Hz cada 0.11 s, 0.25 -> 0.001 en 0.5 s).

Uso:
  1) Detectar cambios de casilla bajo la flecha (para ajustar):
     python3 -I sonido_ruleta.py detectar VIDEO.mp4 X Y
        X,Y = píxel (en el video ya vertical 1080x1920) ~50 px debajo de la punta de la flecha.
  2) Ajustar el modelo con dos tics consecutivos del final (los lentos, fiables) y el momento del resultado:
     python3 -I sonido_ruleta.py ajustar T_RESULTADO TIC_PENULTIMO TIC_ULTIMO
  3) Generar el audio (WAV mono 48 kHz):
     python3 -I sonido_ruleta.py generar SALIDA.wav DURACION T0 E R0 T_FANFARRIA
"""
import math, struct, subprocess, sys, wave

DUR_GIRO, CASILLAS = 5.6, 8
PASO = 2 * math.pi / CASILLAS


def detectar(video, x, y):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf",
                          f"crop=20:20:{int(x)-10}:{int(y)-10},scale=1:1:flags=area",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fps = 30.0
    def tipo(c):
        r, g, b = c
        if g > r and g > b: return "T"            # turquesa
        if b > g and r < b * 1.15 and r < 200: return "M"  # morado
        return "R"                                 # rojo/rosa
    prev, ev = None, []
    for i in range(len(raw) // 3):
        t = tipo(raw[i*3:i*3+3])
        if prev and t != prev: ev.append(round(i / fps, 3))
        prev = t
    print("Cambios de casilla (s):", ev)
    print("Usa los dos últimos tics LENTOS antes de que se detenga (ignora los de después del resultado).")


def ajustar(t_res, ta, tb):
    t0 = t_res - DUR_GIRO
    ra = (1 - (ta - t0) / DUR_GIRO) ** 4
    rb = (1 - (tb - t0) / DUR_GIRO) ** 4
    E = PASO / (ra - rb)
    r0 = (E * rb) % PASO
    print(f"T0={t0:.3f}  E={E:.2f}  R0={r0:.3f}")
    for t in tics(t0, E, r0)[-8:]: print(f"  tic modelo: {t:.2f}")


def tics(t0, E, r0):
    out, j = [], 0
    while r0 + j * PASO <= E:
        out.append(t0 + DUR_GIRO * (1 - ((r0 + j * PASO) / E) ** 0.25)); j += 1
    return sorted(out)


def generar(salida, dur, t0, E, r0, t_fan):
    SR = 48000
    buf = [0.0] * int(SR * dur)
    env = lambda tt, g0, T: g0 * (0.001 / g0) ** (min(tt, T) / T)
    for at in tics(t0, E, r0):
        s = int(at * SR)
        for i in range(int(.05 * SR)):
            tt = i / SR
            sq = 1.0 if math.sin(2 * math.pi * 1100 * tt) >= 0 else -1.0
            if 0 <= s + i < len(buf): buf[s + i] += sq * env(tt, .12, .04)
    for k, f in enumerate([523, 659, 784, 1047, 1319]):
        s = int((t_fan + k * .11) * SR)
        for i in range(int(.55 * SR)):
            tt = i / SR; tri = 4 * abs((f * tt) % 1 - .5) - 1
            if 0 <= s + i < len(buf): buf[s + i] += tri * env(tt, .25, .5)
    peak = max(abs(v) for v in buf) or 1
    w = wave.open(salida, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", int(v / peak * .89 * 32767)) for v in buf)); w.close()
    print("Audio listo:", salida)


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "detectar": detectar(a[0], float(a[1]), float(a[2]))
    elif cmd == "ajustar": ajustar(*map(float, a))
    elif cmd == "generar": generar(a[0], *map(float, a[1:]))
