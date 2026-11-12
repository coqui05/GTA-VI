"""Genera las escenas del video 'pasos-cta' (HyperFrames)."""
import os, sys, json

OUT = sys.argv[1]
# Opcional: JSON con el video de Coqui que va antes de la plantilla
INTRO = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
OFF = INTRO["duration"] if INTRO else 0.0

ICON = {
    "thumb": "M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z",
    "bell": "M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z",
    "share": "M14 9V5l7 7-7 7v-4.1c-5 0-8.5 1.6-11 5.1 1-5 4-10 11-11z",
    "send": "M2.01 21L23 12 2.01 3 2 10l15 2-15 2z",
    "link": "M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z",
    "msg": "M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z",
    "check": "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z",
    "more": "M6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z",
    "diamond": "M6 3h12l4 6-10 12L2 9z",
}

def svg(name, size, fill="#fff", extra=""):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" {extra}>'
            f'<path d="{ICON[name]}" fill="{fill}"/></svg>')

COMMON_CSS = """
#root { position:absolute; inset:0; font-family:'Outfit',sans-serif; color:#fff; }
.step-tag { position:absolute; left:0; right:0; top:300px; text-align:center; font:700 34px 'Outfit';
  letter-spacing:.32em; color:#f3c56b; text-shadow:0 2px 0 rgba(10,4,24,.9),0 0 18px rgba(10,4,24,.95); }
.num-wrap { position:absolute; left:0; right:0; top:320px; height:480px; display:flex; justify-content:center; }
.num-in { position:absolute; left:0; right:0; top:0; bottom:0; display:flex; justify-content:center; }
.num-glow, .num-fill, .num-echo, .num-shine { position:absolute; font:italic 900 470px/1 'Montserrat'; letter-spacing:-.04em; padding:0 40px; }
.num-glow { color:#ff5d8f; filter:blur(40px); opacity:.85; }
.num-fill { background:linear-gradient(175deg,#ffffff 0%,#f4fbff 38%,#9fe4ff 50%,#5fb8ff 62%,#ff6fa0 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  -webkit-text-stroke:4px rgba(255,255,255,.9); filter:drop-shadow(10px 12px 0 #ff2d6f); }
.num-echo { color:transparent; -webkit-text-stroke:5px #7fe3ff; opacity:0; }
.num-echo.e2 { -webkit-text-stroke-color:#ff5d8f; }
.num-shine { color:transparent; background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.95) 50%,transparent 60%);
  background-size:300% 100%; background-position:120% 0; -webkit-background-clip:text; background-clip:text; }
.num-ring { position:absolute; left:50%; top:50%; width:440px; height:440px; margin:-220px 0 0 -220px; border-radius:50%;
  border:10px solid #f3c56b; opacity:0; box-shadow:0 0 40px rgba(243,197,107,.8); }
.label { position:absolute; left:0; right:0; top:800px; text-align:center; font:400 86px/1 'Archivo Black';
  letter-spacing:.01em; filter:drop-shadow(0 4px 0 rgba(10,4,24,.9)) drop-shadow(0 0 22px rgba(10,4,24,.9)); }
.label span { display:inline-block; margin:0 12px; }
.label .acc { background:linear-gradient(90deg,#ff5d8f,#f3c56b); -webkit-background-clip:text;
  background-clip:text; color:transparent; }
.glass { position:absolute; background:linear-gradient(160deg,rgba(70,36,120,.72),rgba(20,11,38,.78));
  border:2px solid rgba(255,255,255,.22); border-radius:44px;
  box-shadow:0 30px 80px rgba(10,4,30,.55), inset 0 1px 0 rgba(255,255,255,.3); backdrop-filter:blur(18px); }
.tap { position:absolute; left:0; top:0; width:76px; height:76px; margin:-38px 0 0 -38px; border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.95) 0 38%,rgba(255,255,255,.35) 40% 100%);
  box-shadow:0 10px 30px rgba(0,0,0,.45); z-index:20; }
.spark { position:absolute; left:0; top:0; width:22px; height:22px; margin:-11px 0 0 -11px; }
"""

def head(sid, n, words):
    lab = "".join(f'<span id="{sid}-w{i}" class="{"acc" if acc else ""}">{w}</span>'
                  for i, (w, acc) in enumerate(words))
    return f"""
  <div id="{sid}-tag" class="step-tag" data-layout-allow-occlusion>STEP 0{n}</div>
  <div id="{sid}-num" class="num-wrap" data-layout-allow-occlusion><div class="num-ring"></div><div class="num-in" data-layout-allow-occlusion><div class="num-echo e1" data-layout-allow-occlusion>{n}</div><div class="num-echo e2" data-layout-allow-occlusion>{n}</div><div class="num-glow" data-layout-allow-occlusion>{n}</div><div class="num-fill" data-layout-allow-occlusion>{n}</div><div class="num-shine" data-layout-allow-occlusion>{n}</div></div></div>
  <div id="{sid}-label" class="label">{lab}</div>"""

def head_js(sid, nwords, first=False):
    # entrada del número: rebote con desenfoque; en la escena 1 ya está visible en el cuadro 0
    N = f"#{sid}-num"
    if first:
        num = (f'tl.fromTo("{N} .num-in",{{scale:.7,rotationY:-55,rotation:-8,transformPerspective:900,filter:"blur(3px)"}},'
               f'{{scale:1,rotationY:0,rotation:0,filter:"blur(0px)",duration:.6,ease:"back.out(2.2)"}},0);')
    else:
        num = (f'tl.fromTo("{N} .num-in",{{scale:.15,rotationY:-110,rotation:-14,opacity:0,transformPerspective:900,filter:"blur(20px)"}},'
               f'{{scale:1,rotationY:0,rotation:0,opacity:1,filter:"blur(0px)",duration:.62,ease:"back.out(1.9)"}},0);')
    land = .2
    fx = [num,
          f'tl.fromTo("{N} .num-glow",{{opacity:1,scale:1.35}},{{opacity:.85,scale:1,duration:.7,ease:"power3.out"}},{land});',
          f'tl.fromTo("{N} .e1",{{opacity:.95,scale:1}},{{opacity:0,scale:1.45,duration:.5,ease:"power2.out"}},{land+.05:.2f});',
          f'tl.fromTo("{N} .e2",{{opacity:.85,scale:1}},{{opacity:0,scale:1.8,duration:.6,ease:"power2.out"}},{land+.12:.2f});',
          f'tl.fromTo("{N} .num-ring",{{opacity:1,scale:.3}},{{opacity:0,scale:1.9,duration:.65,ease:"expo.out"}},{land:.2f});',
          f'tl.fromTo("{N} .num-shine",{{backgroundPosition:"120% 0"}},{{backgroundPosition:"-20% 0",duration:.6,ease:"power2.inOut"}},{land+.35:.2f});']
    js = fx + ([f'tl.fromTo("#{sid}-tag",{{opacity:0,y:-24}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},.05);'] if not first else [])
    for i in range(nwords):
        if first:
            js.append(f'tl.fromTo("#{sid}-w{i}",{{opacity:1,y:0}},{{opacity:1,y:0,duration:.1}},0);'); continue
        js.append(f'tl.fromTo("#{sid}-w{i}",{{opacity:0,filter:"blur(8px)",y:18}},'
                  f'{{opacity:1,filter:"blur(0px)",y:0,duration:.22,ease:"power3.out"}},{(0 if first else .14)+i*.08:.2f});')
    return "\n    ".join(js)

def tap_js(sid, x0, y0, x1, y1, t_arrive, t_press, tid="tap"):
    """El punto de toque entra, presiona y se queda."""
    return f"""
    tl.fromTo("#{sid}-{tid}",{{x:{x0},y:{y0},opacity:0,scale:1.3}},{{x:{x1},y:{y1},opacity:1,scale:1,duration:{t_press-t_arrive:.2f},ease:"power3.out"}},{t_arrive});
    tl.to("#{sid}-{tid}",{{scale:.72,duration:.08,ease:"power2.in"}},{t_press});
    tl.to("#{sid}-{tid}",{{scale:1,duration:.22,ease:"back.out(3)"}},{t_press+.08:.2f});"""

def tap_move_js(sid, x1, y1, t_start, t_press, tid="tap"):
    return f"""
    tl.to("#{sid}-{tid}",{{x:{x1},y:{y1},duration:{t_press-t_start:.2f},ease:"power2.inOut"}},{t_start});
    tl.to("#{sid}-{tid}",{{scale:.72,duration:.08,ease:"power2.in"}},{t_press});
    tl.to("#{sid}-{tid}",{{scale:1,duration:.22,ease:"back.out(3)"}},{t_press+.08:.2f});"""

def exit_js(sid, kind, t):
    sel = f'"#{sid}-stage"'
    if kind == "blur":
        return f'tl.to({sel},{{opacity:0,scale:1.06,filter:"blur(14px)",duration:.2,ease:"power3.in"}},{t});'
    if kind == "whip":
        return f'tl.to({sel},{{y:-420,opacity:0,filter:"blur(16px)",duration:.22,ease:"power3.in"}},{t});'
    if kind == "zoom":
        return f'tl.to({sel},{{scale:1.6,opacity:0,filter:"blur(20px)",duration:.24,ease:"power3.in"}},{t});'
    return ""

def sparks_html(sid, n=10):
    return "".join(f'<div id="{sid}-sp{i}" class="spark">{svg("diamond", 22, "#f3c56b" if i%2 else "#7fe3ff")}</div>'
                   for i in range(n))

def sparks_js(sid, cx, cy, t, n=10, r=170):
    import math
    out = []
    for i in range(n):
        a = i / n * 2 * math.pi + .3
        dx, dy = math.cos(a) * r * (1 + .25 * (i % 3)), math.sin(a) * r * (1 + .25 * (i % 3))
        out.append(f'tl.fromTo("#{sid}-sp{i}",{{x:{cx},y:{cy},opacity:1,scale:.4,rotation:0}},'
                   f'{{x:{cx+dx:.0f},y:{cy+dy:.0f},opacity:0,scale:1.2,rotation:{(i%2*2-1)*120},duration:.7,ease:"power3.out"}},{t});')
    return "\n    ".join(out)

def scene(sid, dur, body, js, css=""):
    return f"""<template>
  <style>{COMMON_CSS}{css}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-layout-allow-overlap>
    <div id="{sid}-stage" style="position:absolute;inset:0;transform-origin:540px 800px;">{body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""

scenes = []

# ---------- 1. LIKE ----------
sid, dur = "s1", 2.0
body = head(sid, 1, [("LIKE", False), ("THE VIDEO", True)]) + f"""
  <div id="{sid}-card" class="glass" style="left:270px;top:1000px;width:540px;height:150px;border-radius:75px;">
    <div id="{sid}-up" style="position:absolute;left:62px;top:35px;width:80px;height:80px;">
      <svg id="{sid}-up-off" viewBox="0 0 24 24" width="80" height="80" style="position:absolute;inset:0;"><path d="{ICON['thumb']}" fill="none" stroke="#fff" stroke-width="1.6"/></svg>
      <svg id="{sid}-up-on" viewBox="0 0 24 24" width="80" height="80" style="position:absolute;inset:0;"><defs><linearGradient id="{sid}-g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff5d8f"/><stop offset="1" stop-color="#f3c56b"/></linearGradient></defs><path d="{ICON['thumb']}" fill="url(#{sid}-g)"/></svg>
    </div>
    <div id="{sid}-txt-off" style="position:absolute;left:166px;top:42px;font:700 56px/66px 'Outfit';">Like</div>
    <div id="{sid}-txt-on" style="position:absolute;left:166px;top:42px;font:700 56px/66px 'Outfit';color:#ffd0de;">Liked</div>
    <div style="position:absolute;left:356px;top:30px;width:3px;height:90px;background:rgba(255,255,255,.25);"></div>
    <svg viewBox="0 0 24 24" width="74" height="74" style="position:absolute;left:410px;top:38px;transform:rotate(180deg);"><path d="{ICON['thumb']}" fill="none" stroke="rgba(255,255,255,.75)" stroke-width="1.6"/></svg>
  </div>
  {sparks_html(sid)}
  <div id="{sid}-tap" class="tap"></div>"""
js = head_js(sid, 2, first=True) + f"""
    tl.fromTo("#{sid}-card",{{y:90,opacity:0,filter:"blur(10px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:.5,ease:"expo.out"}},.25);
    tl.set("#{sid}-up-on",{{scale:0,opacity:0,transformOrigin:"50% 50%"}},0);
    tl.set("#{sid}-txt-on",{{opacity:0}},0);""" + tap_js(sid, 760, 1500, 372, 1075, .55, 1.0) + f"""
    tl.to("#{sid}-up-off",{{opacity:0,duration:.1}},1.05);
    tl.to("#{sid}-up-on",{{scale:1,opacity:1,rotation:-14,duration:.32,ease:"back.out(3)"}},1.05);
    tl.to("#{sid}-up-on",{{rotation:0,duration:.3,ease:"power2.out"}},1.37);
    tl.to("#{sid}-txt-off",{{opacity:0,filter:"blur(6px)",duration:.12}},1.05);
    tl.fromTo("#{sid}-txt-on",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.16}},1.1);
    tl.to("#{sid}-card",{{borderColor:"rgba(255,93,143,.8)",boxShadow:"0 30px 90px rgba(255,93,143,.45), inset 0 1px 0 rgba(255,255,255,.3)",duration:.3}},1.05);
    {sparks_js(sid, 372, 1075, 1.06)}
    tl.to("#{sid}-tap",{{opacity:0,duration:.15}},1.5);
    {exit_js(sid, "blur", dur-.2)}"""
scenes.append((sid, dur, scene(sid, dur, body, js)))

# ---------- 2. SUBSCRIBE ----------
sid, dur = "s2", 2.2
body = head(sid, 2, [("SUBSCRIBE", True)]) + f"""
  <div id="{sid}-btn" style="position:absolute;left:150px;top:1000px;width:620px;height:150px;border-radius:75px;
       background:linear-gradient(135deg,#ff2d55,#ff5d8f);box-shadow:0 26px 70px rgba(255,45,85,.5);overflow:hidden;">
    <div id="{sid}-btn-grey" style="position:absolute;inset:0;background:rgba(58,40,90,.96);opacity:0;"></div>
    <div id="{sid}-t1" style="position:absolute;left:0;right:0;top:44px;text-align:center;font:400 54px/62px 'Archivo Black';letter-spacing:.04em;">SUBSCRIBE</div>
    <div id="{sid}-t2" style="position:absolute;left:0;right:0;top:44px;text-align:center;font:400 50px/62px 'Archivo Black';letter-spacing:.04em;opacity:0;">
      SUBSCRIBED <svg viewBox="0 0 24 24" width="50" height="50" style="vertical-align:-6px"><path d="{ICON['check']}" fill="#7fe3ff"/></svg></div>
  </div>
  <div id="{sid}-bell" class="glass" style="left:790px;top:1000px;width:150px;height:150px;border-radius:50%;">
    <div id="{sid}-bell-i" style="position:absolute;left:37px;top:35px;width:76px;height:76px;transform-origin:50% 10%;">
      <svg viewBox="0 0 24 24" width="76" height="76"><path id="{sid}-bell-p" d="{ICON['bell']}" fill="#fff"/></svg></div>
  </div>
  <div id="{sid}-tap" class="tap"></div>"""
js = head_js(sid, 1) + f"""
    tl.fromTo("#{sid}-btn",{{x:-160,opacity:0,filter:"blur(12px)"}},{{x:0,opacity:1,filter:"blur(0px)",duration:.5,ease:"expo.out"}},.25);
    tl.fromTo("#{sid}-bell",{{x:160,opacity:0,filter:"blur(12px)"}},{{x:0,opacity:1,filter:"blur(0px)",duration:.5,ease:"expo.out"}},.32);""" + tap_js(sid, 600, 1520, 460, 1075, .5, .8) + f"""
    tl.to("#{sid}-btn",{{scale:.95,duration:.08}},.8);
    tl.to("#{sid}-btn",{{scale:1,duration:.3,ease:"back.out(3)"}},.88);
    tl.to("#{sid}-btn-grey",{{opacity:1,duration:.2}},.85);
    tl.to("#{sid}-btn",{{boxShadow:"0 26px 70px rgba(20,8,50,.5)",duration:.2}},.85);
    tl.to("#{sid}-t1",{{y:-50,opacity:0,filter:"blur(6px)",duration:.16,ease:"power3.in"}},.85);
    tl.fromTo("#{sid}-t2",{{y:50,opacity:0,filter:"blur(6px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:.26,ease:"expo.out"}},.95);""" + tap_move_js(sid, 865, 1075, 1.1, 1.38) + f"""
    tl.to("#{sid}-bell-p",{{fill:"#f3c56b",duration:.1}},1.4);
    tl.to("#{sid}-bell",{{borderColor:"rgba(243,197,107,.9)",boxShadow:"0 26px 80px rgba(243,197,107,.45)",duration:.2}},1.4);
    tl.to("#{sid}-bell-i",{{keyframes:[{{rotation:22,duration:.07}},{{rotation:-18,duration:.08}},{{rotation:12,duration:.08}},{{rotation:-6,duration:.08}},{{rotation:0,duration:.1}}]}},1.4);
    tl.to("#{sid}-tap",{{opacity:0,duration:.15}},1.8);
    {exit_js(sid, "whip", dur-.22)}"""
scenes.append((sid, dur, scene(sid, dur, body, js)))

# ---------- 3. COMMENT ----------
sid, dur = "s3", 3.0
text = (INTRO or {}).get("comment", "This channel is fire")  # cambia en cada video
chars = "".join(f'<span id="{sid}-c{i}">{"&nbsp;" if ch==" " else ch}</span>' for i, ch in enumerate(text))
body = head(sid, 3, [("DROP A", False), ("COMMENT", True)]) + f"""
  <div id="{sid}-card" class="glass" style="left:110px;top:950px;width:860px;height:360px;border-radius:40px;overflow:hidden;">
    <div style="position:absolute;left:36px;top:26px;font:700 36px 'Outfit';">Comments</div>
    <div id="{sid}-post" style="position:absolute;left:36px;top:92px;right:36px;height:110px;">
      <div style="position:absolute;left:0;top:4px;width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#2fb3b0,#7fe3ff);"></div>
      <div style="position:absolute;left:96px;top:0;font:500 28px 'Outfit';color:rgba(255,255,255,.65);">@you · just now</div>
      <div style="position:absolute;left:96px;top:38px;font:700 40px 'Outfit';">{text} <svg viewBox="0 0 24 24" width="38" height="38" style="vertical-align:-6px"><path d="{ICON['diamond']}" fill="#7fe3ff"/></svg></div>
    </div>
    <div style="position:absolute;left:30px;top:250px;width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#2fb3b0,#7fe3ff);"></div>
    <div id="{sid}-field" style="position:absolute;left:122px;top:240px;width:580px;height:92px;border-radius:46px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.18);">
      <div id="{sid}-ph" style="position:absolute;left:32px;top:22px;font:500 38px 'Outfit';color:rgba(255,255,255,.62);">Add a comment...</div>
      <div id="{sid}-typed" style="position:absolute;left:32px;top:22px;font:700 38px 'Outfit';white-space:nowrap;">{chars}<span id="{sid}-caret" style="display:inline-block;width:3px;height:40px;background:#ff5d8f;vertical-align:-6px;margin-left:4px;"></span></div>
    </div>
    <div id="{sid}-send" style="position:absolute;left:724px;top:240px;width:92px;height:92px;border-radius:50%;background:linear-gradient(135deg,#ff5d8f,#f3c56b);">
      <svg viewBox="0 0 24 24" width="48" height="48" style="position:absolute;left:24px;top:22px;"><path d="{ICON['send']}" fill="#fff"/></svg></div>
  </div>
  <div id="{sid}-tap" class="tap"></div>"""
t0, step = .55, .042
typing = "\n    ".join(f'tl.set("#{sid}-c{i}",{{opacity:1}},{t0+i*step:.3f});' for i in range(len(text)))
t_end = t0 + len(text) * step
js = head_js(sid, 2) + f"""
    tl.fromTo("#{sid}-card",{{y:120,opacity:0,filter:"blur(12px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:.5,ease:"expo.out"}},.22);
    tl.set("#{sid}-typed span:not(#{sid}-caret)",{{opacity:0}},0);
    tl.set("#{sid}-post",{{opacity:0}},0);
    tl.set("#{sid}-ph",{{opacity:0}},{t0});
    {typing}""" + tap_js(sid, 980, 1620, 880, 1236, t_end - .25, t_end + .12) + f"""
    tl.to("#{sid}-send",{{scale:.88,duration:.08}},{t_end+.12:.2f});
    tl.to("#{sid}-send",{{scale:1,rotation:360,duration:.4,ease:"back.out(2)"}},{t_end+.2:.2f});
    tl.to("#{sid}-typed",{{y:-150,x:-60,opacity:0,filter:"blur(8px)",duration:.25,ease:"power3.in"}},{t_end+.16:.2f});
    tl.fromTo("#{sid}-post",{{y:60,opacity:0,scale:.92,filter:"blur(8px)"}},{{y:0,opacity:1,scale:1,filter:"blur(0px)",duration:.4,ease:"expo.out"}},{t_end+.3:.2f});
    tl.set("#{sid}-ph",{{opacity:1}},{t_end+.42:.2f});
    tl.to("#{sid}-tap",{{opacity:0,duration:.15}},{t_end+.5:.2f});
    {exit_js(sid, "blur", dur-.2)}"""
scenes.append((sid, dur, scene(sid, dur, body, js)))

# ---------- 4. SHARE ----------
sid, dur = "s4", 2.2
items = [("link", "Copy link"), ("msg", "Message"), ("send", "Send"), ("more", "More")]
sheet = ""
for i, (ic, lab) in enumerate(items):
    cx = 105 + i * 210
    sheet += f"""
    <div id="{sid}-it{i}" style="position:absolute;left:{cx-60}px;top:22px;width:120px;text-align:center;">
      <div id="{sid}-ic{i}" style="width:100px;height:100px;margin:0 auto;border-radius:50%;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.2);position:relative;">
        <svg viewBox="0 0 24 24" width="52" height="52" style="position:absolute;left:22px;top:22px;"><path d="{ICON[ic]}" fill="#fff"/></svg></div>
      <div id="{sid}-lb{i}" style="margin-top:10px;font:600 28px 'Outfit';white-space:nowrap;margin-left:-20px;margin-right:-20px;">{lab}</div>
    </div>"""
body = head(sid, 4, [("SHARE", True), ("IT", False)]) + f"""
  <div id="{sid}-btn" class="glass" style="left:330px;top:960px;width:420px;height:140px;border-radius:70px;">
    <svg viewBox="0 0 24 24" width="74" height="74" style="position:absolute;left:62px;top:33px;"><path d="{ICON['share']}" fill="#7fe3ff"/></svg>
    <div style="position:absolute;left:160px;top:36px;font:700 56px/66px 'Outfit';">Share</div>
  </div>
  <div id="{sid}-sheet" class="glass" style="left:120px;top:1130px;width:840px;height:190px;border-radius:40px;">{sheet}
  </div>
  <div id="{sid}-tap" class="tap"></div>"""
js = head_js(sid, 2) + f"""
    tl.fromTo("#{sid}-btn",{{scale:.6,opacity:0,filter:"blur(12px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.5,ease:"back.out(1.7)"}},.22);
    tl.set("#{sid}-sheet",{{opacity:0}},0);""" + tap_js(sid, 760, 1560, 540, 1030, .45, .75) + f"""
    tl.to("#{sid}-btn",{{scale:.93,duration:.08}},.75);
    tl.to("#{sid}-btn",{{scale:1,borderColor:"rgba(127,227,255,.85)",boxShadow:"0 26px 80px rgba(127,227,255,.4)",duration:.3,ease:"back.out(3)"}},.83);
    tl.fromTo("#{sid}-sheet",{{y:140,opacity:0,filter:"blur(10px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:.45,ease:"expo.out"}},.85);
    tl.fromTo("#{sid}-sheet > div",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power3.out",stagger:.06}},.92);""" + tap_move_js(sid, 225, 1202, 1.2, 1.5) + f"""
    tl.to("#{sid}-ic0",{{background:"linear-gradient(135deg,#ff5d8f,#f3c56b)",borderColor:"rgba(255,255,255,.6)",scale:1.12,duration:.2,ease:"back.out(3)"}},1.52);
    tl.to("#{sid}-ic0",{{scale:1,duration:.2}},1.72);
    tl.to("#{sid}-lb0",{{color:"#f3c56b",duration:.15}},1.52);
    tl.to("#{sid}-tap",{{opacity:0,duration:.15}},1.8);
    {exit_js(sid, "zoom", dur-.24)}"""
scenes.append((sid, dur, scene(sid, dur, body, js)))

# ---------- 5. CANAL (captura tipo YouTube, modo oscuro) ----------
sid, dur = "s5", 4.6
YT_CSS = """
#s5-tag { top:300px; }
#s5-num { top:330px; height:230px; }
#s5-num .num-glow, #s5-num .num-fill, #s5-num .num-echo, #s5-num .num-shine { font-size:220px; }
#s5-num .num-ring { width:230px; height:230px; margin:-115px 0 0 -115px; border-width:7px; }
#s5-label { top:568px; font-size:62px; }
.yt { position:absolute; left:60px; top:650px; width:960px; height:680px; background:#0f0f0f; border-radius:40px;
  overflow:hidden; font-family:'Roboto',sans-serif; color:#f1f1f1; box-shadow:0 40px 120px rgba(0,0,0,.7);
  border:1px solid rgba(255,255,255,.08); }
"""
body = head(sid, 5, [("VISIT THE", False), ("CHANNEL", True)]) + f"""
  <div id="{sid}-card" class="yt">
    <svg viewBox="0 0 24 24" width="48" height="48" style="position:absolute;left:30px;top:26px;"><path d="M15.4 4.6L14 3.2 5.2 12l8.8 8.8 1.4-1.4L8 12z" fill="#f1f1f1"/></svg>
    <svg viewBox="0 0 24 24" width="46" height="46" style="position:absolute;left:800px;top:27px;"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="#f1f1f1" stroke-width="2"/><path d="M15.5 15.5L21 21" stroke="#f1f1f1" stroke-width="2.2" stroke-linecap="round"/></svg>
    <svg viewBox="0 0 24 24" width="46" height="46" style="position:absolute;left:880px;top:27px;"><circle cx="12" cy="5" r="2" fill="#f1f1f1"/><circle cx="12" cy="12" r="2" fill="#f1f1f1"/><circle cx="12" cy="19" r="2" fill="#f1f1f1"/></svg>
    <img id="{sid}-banner" src="assets/banner.jpg" style="position:absolute;left:35px;top:100px;width:890px;height:245px;border-radius:20px;object-fit:cover;" />
    <img id="{sid}-av" src="assets/avatar-yt.jpg" style="position:absolute;left:35px;top:378px;width:160px;height:160px;border-radius:50%;object-fit:cover;" />
    <div style="position:absolute;left:228px;top:392px;font:700 48px/1.1 'Roboto';letter-spacing:-.01em;">The Diamond Royale</div>
    <div style="position:absolute;left:228px;top:456px;font:500 30px 'Roboto';color:#f1f1f1;">@TheDiamondRoyale</div>
    <div id="{sid}-link" style="position:absolute;left:216px;top:494px;padding:6px 12px;border-radius:12px;font:500 28px 'Roboto';color:#f1f1f1;">
      <svg viewBox="0 0 24 24" width="30" height="30" style="vertical-align:-7px;margin-right:6px;"><path id="{sid}-link-i" d="{ICON['link']}" fill="#f1f1f1"/></svg><span id="{sid}-link-t">bit.ly/4iD7KGP</span></div>
    <div id="{sid}-btn" style="position:absolute;left:35px;top:572px;width:890px;height:76px;border-radius:38px;background:#f1f1f1;">
      <div id="{sid}-b1" style="position:absolute;left:0;right:0;top:0;height:76px;display:flex;align-items:center;justify-content:center;font:500 32px 'Roboto';color:#0f0f0f;">Subscribe</div>
      <div id="{sid}-b2" style="position:absolute;left:0;right:0;top:0;height:76px;display:flex;align-items:center;justify-content:center;font:500 32px 'Roboto';color:#f1f1f1;opacity:0;">
        <svg viewBox="0 0 24 24" width="34" height="34" style="vertical-align:-7px;margin-right:10px;"><path d="{ICON['bell']}" fill="#f1f1f1"/></svg>Subscribed
        <svg viewBox="0 0 24 24" width="30" height="30" style="vertical-align:-7px;margin-left:6px;"><path d="M7 10l5 5 5-5z" fill="#f1f1f1"/></svg></div>
    </div>
    <div id="{sid}-web" style="position:absolute;left:0;right:0;top:395px;bottom:0;background:#1f1f1f;border-radius:32px 32px 0 0;box-shadow:0 -20px 60px rgba(0,0,0,.6);">
      <div style="position:absolute;left:430px;top:14px;width:100px;height:8px;border-radius:4px;background:#5a5a5a;"></div>
      <div style="position:absolute;left:35px;top:44px;width:890px;height:76px;border-radius:38px;background:#2e2e2e;display:flex;align-items:center;padding-left:30px;font:500 32px 'Roboto';color:#f1f1f1;">
        <svg viewBox="0 0 24 24" width="30" height="30" style="margin-right:14px;"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6z" fill="#aaa"/></svg>bit.ly/4iD7KGP</div>
      <div style="position:absolute;left:35px;top:138px;width:890px;height:6px;border-radius:3px;background:#3a3a3a;overflow:hidden;">
        <div id="{sid}-load" style="width:100%;height:100%;background:#3ea6ff;transform-origin:0 50%;"></div></div>
      <div style="position:absolute;left:35px;top:180px;width:600px;height:34px;border-radius:10px;background:#2a2a2a;"></div>
      <div style="position:absolute;left:35px;top:232px;width:820px;height:24px;border-radius:8px;background:#262626;"></div>
      <div style="position:absolute;left:35px;top:272px;width:700px;height:24px;border-radius:8px;background:#262626;"></div>
      <div style="position:absolute;left:35px;top:312px;width:760px;height:24px;border-radius:8px;background:#262626;"></div>
    </div>
  </div>
  <div id="{sid}-tap" class="tap"></div>"""
js = head_js(sid, 2) + f"""
    tl.set("#{sid}-web",{{y:320}},0);
    tl.fromTo("#{sid}-card",{{y:260,scale:.9,opacity:0,filter:"blur(14px)"}},{{y:0,scale:1,opacity:1,filter:"blur(0px)",duration:.65,ease:"expo.out"}},.2);""" + tap_js(sid, 900, 1750, 540, 1258, 1.0, 1.4) + f"""
    tl.to("#{sid}-btn",{{scale:.96,duration:.08}},1.4);
    tl.to("#{sid}-btn",{{scale:1,backgroundColor:"#272727",duration:.25,ease:"power2.out"}},1.48);
    tl.to("#{sid}-b1",{{opacity:0,duration:.08}},1.46);
    tl.to("#{sid}-b2",{{opacity:1,duration:.12}},1.5);
 """ + tap_move_js(sid, 400, 1166, 1.8, 2.15) + f"""
    tl.to("#{sid}-link",{{backgroundColor:"rgba(255,255,255,.16)",duration:.08}},2.15);
    tl.to("#{sid}-link-t",{{color:"#3ea6ff",duration:.1}},2.15);
    tl.to("#{sid}-link-i",{{fill:"#3ea6ff",duration:.1}},2.15);
    tl.to("#{sid}-link",{{backgroundColor:"rgba(255,255,255,0)",duration:.25}},2.35);
    tl.to("#{sid}-tap",{{opacity:0,duration:.2}},2.4);
    tl.to("#{sid}-web",{{y:0,duration:.5,ease:"expo.out"}},2.4);
    tl.fromTo("#{sid}-load",{{scaleX:0}},{{scaleX:.85,duration:1.4,ease:"power2.out"}},2.6);"""
scenes.append((sid, dur, scene(sid, dur, body, js, YT_CSS)))

os.makedirs(f"{OUT}/compositions", exist_ok=True)
for sid, dur, html in scenes:
    open(f"{OUT}/compositions/{sid}.html", "w").write(html)

# ---------- raíz ----------
starts, t = [], OFF
for sid, dur, _ in scenes:
    starts.append((sid, round(t, 2), dur)); t += dur
total = round(t, 2)
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
    f'data-start="{st}" data-duration="{d}" data-track-index="2" data-track-kind="graphics" '
    f'data-width="1080" data-height="1920"></div>' for sid, st, d in starts)
if INTRO:
    hosts = (f'      <img id="endbg" class="clip" src="{INTRO["endbg"]}" data-start="{OFF}" data-duration="{round(total-OFF,2)}" data-track-index="1" '
             f'style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;" />\n'
             f'      <div id="intro" data-composition-id="intro" data-composition-src="compositions/intro.html" data-start="0" '
             f'data-duration="{OFF}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>\n') + hosts
S = {sid: st for sid, st, _ in starts}
sfx = [  # (id, archivo, tiempo, volumen, duración)
    ("a-pop1", "pop", S["s1"] + .18, .8, .7), ("a-tap1", "click-soft", S["s1"] + 1.0, 1, .37),
    ("a-spark1", "sparkle", S["s1"] + 1.05, .55, 1.6),
    ("a-wh1", "whoosh-short", S["s2"] - .2, .6, .57), ("a-pop2", "pop", S["s2"] + .2, .8, .7),
    ("a-tap2", "click", S["s2"] + .8, .9, .37), ("a-tap2b", "click-soft", S["s2"] + 1.38, 1, .37),
    ("a-wh2", "whoosh", S["s3"] - .22, .55, .57), ("a-pop3", "pop", S["s3"] + .2, .8, .7),
    ("a-type", "typing", S["s3"] + .55, .5, .85), ("a-tap3", "click-soft", S["s3"] + .55 + len(text) * .042 + .12, 1, .37),
    ("a-wh3", "whoosh-short", S["s4"] - .2, .6, .57), ("a-pop4", "pop", S["s4"] + .2, .8, .7),
    ("a-tap4", "click", S["s4"] + .75, .9, .37), ("a-tap4b", "click-soft", S["s4"] + 1.5, 1, .37),
    ("a-wh4", "whoosh", S["s5"] - .24, .55, .57), ("a-hit", "impact-bass-1", S["s5"] + .1, .7, 2.1),
    ("a-tap5", "click", S["s5"] + 1.4, .9, .37), ("a-tap5b", "click-soft", S["s5"] + 2.15, 1, .37), ("a-wh5", "whoosh-short", S["s5"] + 2.4, .5, .57),
]
if INTRO:
    sfx = [tuple(x) for x in INTRO["sfx"]] + sfx
audio = "\n".join(
    f'      <audio id="{i}" class="clip" src="assets/sfx/{f if '.' in f else f + '.mp3'}" data-start="{t:.2f}" data-duration="{d}" '
    f'data-track-index="{10+n%3}" data-volume="{v}"></audio>' for n, (i, f, t, v, d) in enumerate(sfx))
seg = "".join(f'<div class="seg"><div id="seg{i}" class="seg-fill"></div></div>' for i in range(5))
seg_js = "\n      ".join(
    f'tl.fromTo("#seg{i}",{{scaleX:{0.6 if st==0 else 0}}},{{scaleX:1,duration:.4,ease:"power3.out"}},{st});' for i, (sid, st, d) in enumerate(starts))
spark_stars = "".join(
    f'<svg class="star" viewBox="0 0 24 24" width="{s}" height="{s}" style="left:{x}px;top:{y}px;opacity:{o}"><path d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z" fill="#fff"/></svg>'
    for x, y, s, o in [(90, 420, 26, .5), (960, 380, 20, .45), (150, 1180, 18, .35), (930, 980, 24, .4), (60, 760, 14, .35), (1010, 700, 16, .35)])

index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --night:#140b26; --pink:#ff5d8f; --teal:#2fb3b0; --gold:#f3c56b; --ice:#7fe3ff; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
      #root {{ position:relative; width:100%; height:100%; font-family:'Outfit',sans-serif; color:#fff; }}
      #bg {{ position:absolute; inset:0; background:
          radial-gradient(120% 60% at 50% 78%, #ff5d8f 0%, #b23a8f 22%, #4a1d6e 45%, #140b26 72%); }}
      #sun {{ position:absolute; left:250px; top:1130px; width:580px; height:580px; border-radius:50%;
          background:linear-gradient(180deg,#f3c56b 0%,#ff8a7a 45%,#ff5d8f 80%);
          -webkit-mask:linear-gradient(180deg,#000 0 52%,transparent 52% 56%,#000 56% 63%,transparent 63% 68%,#000 68% 74%,transparent 74% 80%,#000 80% 85%,transparent 85%);
          filter:drop-shadow(0 0 60px rgba(255,93,143,.7)); }}
      #floor {{ position:absolute; left:0; right:0; top:1440px; bottom:0; overflow:hidden; perspective:700px; perspective-origin:50% 0;
          background:linear-gradient(180deg,#2a0f45,#140b26); }}
      #grid {{ position:absolute; left:-1200px; right:-1200px; top:0; height:620px; transform-origin:50% 0;
          transform:rotateX(62deg);
          background-image:linear-gradient(rgba(127,227,255,.55) 3px,transparent 3px),
                           linear-gradient(90deg,rgba(127,227,255,.55) 3px,transparent 3px);
          background-size:120px 120px; }}
      #horizon {{ position:absolute; left:0; right:0; top:1434px; height:8px; background:#ffd0de;
          box-shadow:0 0 30px 10px rgba(255,93,143,.8); }}
      #vignette {{ position:absolute; inset:0; background:radial-gradient(90% 70% at 50% 45%,transparent 55%,rgba(8,3,20,.7)); }}
      .star {{ position:absolute; }}
      #bar {{ position:absolute; z-index:5; left:0; right:0; top:240px; display:flex; justify-content:center; gap:14px; }}
      .seg {{ width:150px; height:10px; border-radius:5px; background:rgba(255,255,255,.18); overflow:hidden; }}
      .seg-fill {{ width:100%; height:100%; transform-origin:0 50%; background:linear-gradient(90deg,var(--pink),var(--gold)); }}
      #note {{ position:absolute; left:0; right:0; top:180px; text-align:center; font:500 28px 'Outfit';
          color:rgba(255,255,255,.9); text-shadow:0 2px 0 rgba(10,4,24,.9),0 0 16px rgba(10,4,24,.95); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
      <div id="note" style="z-index:5">Giveaway rules at the link · Not affiliated with Rockstar Games</div>
      <div id="bar">{seg}</div>
{hosts}
{audio}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {seg_js}
      {('tl.fromTo("#note, #bar",{opacity:0},{opacity:1,duration:.3,ease:"power2.out"},' + str(OFF) + ');') if INTRO else ''}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(f"{OUT}/index.html", "w").write(index)
print("total", total, starts)
