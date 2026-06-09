import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os
import io
import base64

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MotoGP AI Coach",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# MASTER STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,300&family=Orbitron:wght@400;500;600;700;800;900&family=Share+Tech+Mono&display=swap');

/* ── tokens ── */
:root {
  --bg:     #080C10;
  --bg1:    #0C1118;
  --bg2:    #101820;
  --bg3:    #141F28;
  --bg4:    #1A2535;
  --glass:  rgba(16,24,32,0.85);
  --border: rgba(255,255,255,0.06);
  --border2:rgba(255,255,255,0.10);
  --red:    #FF0033;
  --red-d:  #B80024;
  --red-g:  rgba(255,0,51,0.18);
  --red-g2: rgba(255,0,51,0.08);
  --cyan:   #00F5FF;
  --cyan-d: #00B8C4;
  --cyan-g: rgba(0,245,255,0.12);
  --amber:  #FFB800;
  --amb-g:  rgba(255,184,0,0.12);
  --green:  #00FF85;
  --grn-g:  rgba(0,255,133,0.10);
  --purple: #9D4EDD;
  --txt:    #E8EDF2;
  --txt2:   #7A8899;
  --txt3:   #3D5060;
  --txt4:   #2A3A48;
  --shadow: 0 8px 32px rgba(0,0,0,0.5);
  --shadow2:0 2px 12px rgba(0,0,0,0.4);
  --r4: 4px; --r6: 6px; --r8: 8px;
}

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, [class*="css"] {
  font-family: 'Exo 2', sans-serif;
  background: var(--bg);
  color: var(--txt);
  font-size: 15px;
}
.stApp { background: var(--bg); }
.main .block-container { padding: 20px 28px 60px; max-width: 100%; }

/* ── scanline overlay on main ── */
.main::before {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.03) 2px,
    rgba(0,0,0,0.03) 4px
  );
  pointer-events: none;
  z-index: 0;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #070B0F 0%, #0A1018 60%, #0C1420 100%);
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebarContent"] { padding: 0; }

/* ── radio nav ── */
.stRadio > div { gap: 2px; }
.stRadio > div > label {
  font-family: 'Exo 2', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  color: var(--txt2) !important;
  padding: 9px 14px !important;
  border-radius: var(--r4) !important;
  transition: all 0.15s !important;
  cursor: pointer !important;
}
.stRadio > div > label:hover { color: var(--cyan) !important; background: var(--cyan-g) !important; }
[data-testid="stRadio"] { margin: 0; }

/* ── inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r4) !important;
  color: var(--txt) !important;
  font-family: 'Exo 2', sans-serif !important;
  font-size: 14px !important;
  transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 1px rgba(0,245,255,0.25) !important;
}

/* ── selectbox ── */
.stSelectbox > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r4) !important;
  color: var(--txt) !important;
  font-family: 'Exo 2', sans-serif !important;
}

/* ── slider ── */
div[data-baseweb="slider"] > div > div:first-child { background: var(--bg4) !important; }
.stSlider > div > div > div > div { background: var(--red) !important; }

/* ── buttons ── */
.stButton > button {
  font-family: 'Orbitron', monospace !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 2.5px !important;
  text-transform: uppercase !important;
  background: linear-gradient(135deg, var(--red-d) 0%, var(--red) 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r4) !important;
  padding: 11px 26px !important;
  transition: all 0.2s !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, transparent 100%);
  pointer-events: none;
}
.stButton > button:hover {
  box-shadow: 0 0 24px var(--red-g), 0 4px 16px rgba(0,0,0,0.4) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── checkbox ── */
.stCheckbox > label {
  font-family: 'Exo 2', sans-serif !important;
  font-size: 13px !important;
  color: var(--txt2) !important;
}

/* ── progress bars ── */
div[data-testid="stProgress"] > div {
  background: var(--bg4) !important;
  border-radius: 3px !important;
}
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--red-d), var(--red)) !important;
  border-radius: 3px !important;
}

/* ── native metric ── */
[data-testid="stMetric"] {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r6);
  padding: 14px 18px;
}
[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  color: var(--red) !important;
}

/* ── charts ── */
[data-testid="stArrowVegaLiteChart"] { background: transparent !important; }
.js-plotly-plot { background: transparent !important; }

/* ── spinner ── */
[data-testid="stSpinner"] { color: var(--cyan) !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border2); }

/* ── divider ── */
hr { border-color: var(--border) !important; margin: 18px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# COMPONENT LIBRARY
# ─────────────────────────────────────────────────────────────────────────────
def H(html: str):
    st.markdown(html, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    sub_html = f'<div class="ph-sub">{subtitle}</div>' if subtitle else ""
    H(f"""
    <div style="
      position:relative;overflow:hidden;
      background:linear-gradient(135deg,rgba(255,0,51,0.07) 0%,rgba(0,0,0,0) 60%),
                 linear-gradient(90deg,#0C1118,#0E1620);
      border:1px solid rgba(255,255,255,0.06);
      border-left:3px solid #FF0033;
      border-radius:0 6px 6px 0;
      padding:20px 24px 18px;
      margin-bottom:24px;
    ">
      <div style="position:absolute;right:-10px;top:-10px;width:180px;height:180px;
        background:radial-gradient(circle,rgba(255,0,51,0.06) 0%,transparent 70%);
        pointer-events:none;"></div>
      <div style="
        font-family:'Orbitron',monospace;font-size:20px;font-weight:800;
        letter-spacing:3px;color:#fff;text-transform:uppercase;line-height:1.1;
      ">{icon} {title}</div>
      <div style="
        font-family:'Share Tech Mono',monospace;font-size:11px;
        color:#00F5FF;letter-spacing:2.5px;margin-top:6px;opacity:0.75;
      ">{subtitle}</div>
    </div>
    """)


def mode_badge(m: str):
    palettes = {
        "🛠️ Manual":  ("#FFB800", "rgba(255,184,0,0.10)"),
        "🤖 AI":       ("#00F5FF", "rgba(0,245,255,0.10)"),
        "🔥 Hybrid":   ("#FF0033", "rgba(255,0,51,0.12)"),
    }
    color, bg = palettes.get(m, ("#7A8899", "rgba(122,136,153,0.08)"))
    labels = {"🛠️ Manual": "MANUAL ENGINE", "🤖 AI": "AI ENGINE", "🔥 Hybrid": "HYBRID ENGINE"}
    lbl = labels.get(m, m)
    H(f"""
    <div style="
      display:inline-flex;align-items:center;gap:9px;
      background:{bg};border:1px solid {color};
      border-radius:4px;padding:6px 16px;margin-bottom:18px;
    ">
      <span style="width:8px;height:8px;background:{color};border-radius:50%;
        box-shadow:0 0 10px {color};display:inline-block;flex-shrink:0;"></span>
      <span style="font-family:'Orbitron',monospace;font-size:10px;font-weight:700;
        letter-spacing:2.5px;color:{color};">{lbl} ACTIVE</span>
    </div>
    """)


def metric_card(value: str, label: str, color: str = "#FF0033", icon: str = ""):
    H(f"""
    <div style="
      background:linear-gradient(145deg,#101820,#0E1520);
      border:1px solid rgba(255,255,255,0.07);
      border-top:2px solid {color};
      border-radius:6px;padding:16px 14px 14px;
      text-align:center;
      box-shadow:0 4px 20px rgba(0,0,0,0.35);
      position:relative;overflow:hidden;
    ">
      <div style="position:absolute;bottom:-20px;right:-10px;width:80px;height:80px;
        background:radial-gradient(circle,{color}18 0%,transparent 70%);pointer-events:none;"></div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:9px;
        color:rgba(255,255,255,0.3);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">{label}</div>
      <div style="font-family:'Orbitron',monospace;font-size:24px;font-weight:700;
        color:{color};line-height:1;letter-spacing:1px;">{icon}{value}</div>
    </div>
    """)


def skill_bar(label: str, value: float, max_val: float = 100, color: str = "#FF0033"):
    pct = min(100, max(0, value / max_val * 100))
    H(f"""
    <div style="margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;align-items:center;
        margin-bottom:5px;">
        <span style="font-family:'Exo 2',sans-serif;font-size:12px;font-weight:600;
          color:#7A8899;letter-spacing:1px;text-transform:uppercase;">{label}</span>
        <span style="font-family:'Orbitron',monospace;font-size:12px;
          color:{color};font-weight:600;">{value:.1f}</span>
      </div>
      <div style="background:#1A2535;border-radius:3px;height:6px;overflow:hidden;
        box-shadow:inset 0 1px 3px rgba(0,0,0,0.4);">
        <div style="width:{pct}%;height:100%;border-radius:3px;
          background:linear-gradient(90deg,{color}cc,{color});
          box-shadow:0 0 8px {color}66;
          transition:width 0.6s ease;"></div>
      </div>
    </div>
    """)


def radio_line(text: str, color: str = "#00F5FF"):
    H(f"""
    <div style="
      display:flex;align-items:flex-start;gap:10px;
      background:linear-gradient(90deg,rgba(255,255,255,0.03),transparent);
      border-left:2px solid {color};
      padding:10px 14px;margin:4px 0;border-radius:0 4px 4px 0;
    ">
      <span style="color:#FF0033;font-size:10px;margin-top:2px;flex-shrink:0;">▶</span>
      <span style="font-family:'Share Tech Mono',monospace;font-size:12px;
        color:{color};line-height:1.7;">{text}</span>
    </div>
    """)


def alert(text: str, kind: str = "warn"):
    styles = {
        "warn":   ("#FFB800", "rgba(255,184,0,0.08)",   "⚠"),
        "danger": ("#FF0033", "rgba(255,0,51,0.10)",    "🔴"),
        "safe":   ("#00FF85", "rgba(0,255,133,0.08)",   "✅"),
        "info":   ("#00F5FF", "rgba(0,245,255,0.08)",   "◈"),
    }
    c, bg, ico = styles.get(kind, styles["warn"])
    H(f"""
    <div style="
      background:{bg};border:1px solid {c}44;border-left:3px solid {c};
      border-radius:0 6px 6px 0;padding:12px 16px;margin:12px 0;
      display:flex;gap:10px;align-items:flex-start;
    ">
      <span style="font-size:14px;flex-shrink:0;margin-top:1px;">{ico}</span>
      <span style="font-family:'Share Tech Mono',monospace;font-size:12px;
        color:{c};line-height:1.7;">{text}</span>
    </div>
    """)


def engineer_feed(content: str, title: str = "ENGINEER RADIO FEED"):
    H(f"""
    <div style="
      background:linear-gradient(135deg,#080E16,#0A1522);
      border:1px solid rgba(0,245,255,0.15);
      border-top:2px solid #00F5FF;
      border-radius:6px;padding:20px 22px;margin:16px 0;
      box-shadow:0 4px 24px rgba(0,0,0,0.4),
                 inset 0 1px 0 rgba(0,245,255,0.08);
      position:relative;overflow:hidden;
    ">
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
        background:linear-gradient(90deg,transparent,#00F5FF44,transparent);"></div>
      <div style="
        font-family:'Orbitron',monospace;font-size:9px;font-weight:700;
        letter-spacing:3px;color:#00F5FF;text-transform:uppercase;
        margin-bottom:14px;opacity:0.8;display:flex;align-items:center;gap:8px;
      ">
        <span style="width:6px;height:6px;background:#00F5FF;border-radius:50%;
          box-shadow:0 0 8px #00F5FF;display:inline-block;"></span>
        📡 {title}
      </div>
      <div style="
        font-family:'Share Tech Mono',monospace;font-size:13px;
        color:#C8D8E8;line-height:1.9;white-space:pre-wrap;
        border-top:1px solid rgba(0,245,255,0.08);padding-top:14px;
      ">{content}</div>
    </div>
    """)


def hybrid_report(manual: str, ai_text: str):
    H(f"""
    <div style="
      background:linear-gradient(135deg,#0C0814,#0A1018);
      border:1px solid rgba(255,0,51,0.2);
      border-top:2px solid #FF0033;
      border-radius:6px;padding:20px 22px;margin:16px 0;
      box-shadow:0 4px 24px rgba(0,0,0,0.4);
    ">
      <div style="font-family:'Orbitron',monospace;font-size:9px;font-weight:700;
        letter-spacing:3px;color:#FF0033;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
        <span style="width:6px;height:6px;background:#FF0033;border-radius:50%;
          box-shadow:0 0 8px #FF0033;display:inline-block;"></span>
        🔥 HYBRID ANALYSIS REPORT
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;
        color:#FFB800;letter-spacing:2px;margin-bottom:10px;opacity:0.8;">
        ── COMPUTED ENGINE ──
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:12px;
        color:#B0C4D8;line-height:1.85;margin-bottom:18px;white-space:pre-wrap;
        background:rgba(255,255,255,0.02);border-radius:4px;padding:12px 14px;
      ">{manual}</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;
        color:#00F5FF;letter-spacing:2px;margin-bottom:10px;opacity:0.8;">
        ── AI ENHANCEMENT ──
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:12px;
        color:#C8D8E8;line-height:1.9;white-space:pre-wrap;
        background:rgba(0,245,255,0.03);border-radius:4px;padding:12px 14px;
      ">{ai_text}</div>
    </div>
    """)


def section_label(text: str):
    H(f"""<div style="font-family:'Share Tech Mono',monospace;font-size:9px;
      color:#3D5060;letter-spacing:3px;text-transform:uppercase;
      margin-bottom:10px;padding-bottom:6px;
      border-bottom:1px solid rgba(255,255,255,0.04);">{text}</div>""")


def divider():
    H('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.07),transparent);margin:18px 0;"></div>')


def lap_row(lap_n: int, action: str, color: str):
    H(f"""
    <div style="display:flex;align-items:center;gap:0;
      background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);
      border-radius:4px;padding:6px 12px;margin-bottom:3px;overflow:hidden;
      border-left:2px solid {color};">
      <span style="font-family:'Orbitron',monospace;font-size:11px;
        color:#FF0033;width:46px;flex-shrink:0;font-weight:700;">L{lap_n:02d}</span>
      <span style="font-family:'Share Tech Mono',monospace;font-size:12px;
        color:{color};letter-spacing:0.5px;">{action}</span>
    </div>
    """)


# ─────────────────────────────────────────────────────────────────────────────
# VOICE ENGINE  (Web Speech API — zero dependencies, works on Streamlit Cloud)
# ─────────────────────────────────────────────────────────────────────────────
def _clean_for_speech(text: str) -> str:
    """Strip markdown / special chars that confuse TTS."""
    import re
    text = re.sub(r"[*_`#►▶◉●•·\-–—]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()[:600]


def voice_button(text: str, key: str):
    """
    Renders a speak button that uses the browser's built-in SpeechSynthesis API.
    No Python packages, no network calls, works on every modern browser and
    Streamlit Cloud out of the box.
    """
    safe_text = _clean_for_speech(text).replace("'", "\\'").replace("\n", " ")

    # Unique container id so multiple buttons on same page don't clash
    uid = key.replace("-", "_")

    H(f"""
    <div style="margin-top:10px;">
      <button
        id="vbtn_{uid}"
        onclick="(function(){{
          var btn  = document.getElementById('vbtn_{uid}');
          var stop = document.getElementById('vstop_{uid}');
          if (window.speechSynthesis.speaking) {{
            window.speechSynthesis.cancel();
            btn.innerHTML  = '🎤 SPEAK REPORT';
            btn.style.background = 'linear-gradient(135deg,#1a2535,#243040)';
            stop.style.display = 'none';
            return;
          }}
          var msg = new SpeechSynthesisUtterance('{safe_text}');
          msg.rate   = 0.92;
          msg.pitch  = 0.88;
          msg.volume = 1.0;
          var voices = window.speechSynthesis.getVoices();
          var eng = voices.find(function(v){{
            return v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Daniel') || v.name.includes('Alex'));
          }}) || voices.find(function(v){{ return v.lang.startsWith('en'); }});
          if (eng) msg.voice = eng;
          msg.onstart = function(){{
            btn.innerHTML  = '⏹ STOP SPEAKING';
            btn.style.background = 'linear-gradient(135deg,#800018,#FF0033)';
            stop.style.display = 'inline-block';
          }};
          msg.onend = function(){{
            btn.innerHTML  = '🎤 SPEAK REPORT';
            btn.style.background = 'linear-gradient(135deg,#1a2535,#243040)';
            stop.style.display = 'none';
          }};
          window.speechSynthesis.speak(msg);
        }})()"
        style="
          font-family:'Orbitron',monospace;
          font-size:10px;font-weight:700;
          letter-spacing:2px;text-transform:uppercase;
          background:linear-gradient(135deg,#1a2535,#243040);
          color:#00F5FF;
          border:1px solid rgba(0,245,255,0.35);
          border-radius:4px;
          padding:9px 20px;
          cursor:pointer;
          transition:all 0.2s;
          margin-right:8px;
        "
        onmouseover="this.style.boxShadow='0 0 14px rgba(0,245,255,0.3)'"
        onmouseout="this.style.boxShadow='none'"
      >🎤 SPEAK REPORT</button>

      <span id="vstop_{uid}"
        style="
          display:none;
          font-family:'Share Tech Mono',monospace;
          font-size:10px;color:#FF0033;
          letter-spacing:1px;
          animation: pulse_{uid} 1.2s infinite;
        "
      >● BROADCASTING</span>

      <style>
        @keyframes pulse_{uid} {{
          0%,100% {{ opacity:1; }}
          50%      {{ opacity:0.3; }}
        }}
      </style>
    </div>
    """)


# ─────────────────────────────────────────────────────────────────────────────
# AI ENGINE
# ─────────────────────────────────────────────────────────────────────────────
_ENGINEER_PERSONA = (
    "You are a world-class MotoGP factory race engineer with 20+ years experience at Ducati, Honda, and Yamaha. "
    "Respond with sharp technical precision. Always use telemetry language: "
    "'Telemetry indicates…', 'Corner exit is suboptimal…', 'Recommended adjustment for next session…', "
    "'Elite riders typically gain…'. Be concise (under 180 words), professional, actionable. "
    "Structure your response as clear observations followed by specific recommendations."
)


def ai_response(prompt: str) -> str:
    k_oai = st.session_state.get("k_oai", "") or os.getenv("OPENAI_API_KEY", "")
    k_cld = st.session_state.get("k_cld", "") or os.getenv("CLAUDE_API_KEY", "")

    if k_oai:
        try:
            from openai import OpenAI
            r = OpenAI(api_key=k_oai).chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": _ENGINEER_PERSONA},
                    {"role": "user",   "content": prompt},
                ],
                max_tokens=420,
            )
            return r.choices[0].message.content
        except Exception as e:
            return f"[API Error: {str(e)[:80]}]\n\n" + _simulate(prompt)

    if k_cld:
        try:
            import anthropic
            r = anthropic.Anthropic(api_key=k_cld).messages.create(
                model="claude-opus-4-6",
                max_tokens=420,
                system=_ENGINEER_PERSONA,
                messages=[{"role": "user", "content": prompt}],
            )
            return r.content[0].text
        except Exception as e:
            return f"[API Error: {str(e)[:80]}]\n\n" + _simulate(prompt)

    return _simulate(prompt)


def _simulate(p: str) -> str:
    p = p.lower()
    if any(x in p for x in ["telemetry", "performance", "lap", "speed", "sector", "braking", "cornering"]):
        return (
            "Telemetry indicates suboptimal corner-exit velocity across S2 and S3.\n\n"
            "Observations:\n"
            "• Braking trace shows late threshold engagement — shift brake point 8m earlier into T7\n"
            "• Throttle application lacks decisiveness post-apex; elite riders gain +0.4s here\n"
            "• Corner entry speed is within range but mid-corner balance is disrupting drive phase\n\n"
            "Recommended adjustments:\n"
            "• Increase rear preload 2mm to improve corner entry stability\n"
            "• Trial earlier apex geometry in the stadium section\n"
            "• Consistency index is acceptable — focus on replicating best-lap sector splits"
        )
    if any(x in p for x in ["strategy", "pit", "tire", "tyre", "fuel", "race"]):
        return (
            "Pit wall telemetry confirms rear compound entering critical thermal window by lap 14.\n\n"
            "Observations:\n"
            "• Rear deg tracking 12% above nominal — compound approaching cliff\n"
            "• Gap to P3 at 4.2s — undercut window is viable\n"
            "• Weather radar confirms dry conditions holding for full race distance\n\n"
            "Recommended strategy:\n"
            "• Box window: lap 12–13 for maximum undercut benefit\n"
            "• Switch to medium compound — projected 1:48.x pace is sufficient\n"
            "• Fuel delta: +0.8s margin available — push without lift-and-coast until lap 18"
        )
    if any(x in p for x in ["setup", "suspension", "bike", "machine", "gear", "pressure"]):
        return (
            "Machine data indicates front-end understeer in slow-speed technical sections.\n\n"
            "Observations:\n"
            "• Chassis pitch angle 1.2° beyond optimal at corner entry\n"
            "• TC intervention 18% above session average — rear setup too stiff for tarmac temp\n"
            "• Front pressure slightly above optimal window for current conditions\n\n"
            "Recommended adjustments:\n"
            "• Reduce front compression damping 2 clicks\n"
            "• Soften rear spring rate and lower ride height 3mm\n"
            "• Trial 0.05 bar lower front pressure — improved feedback reported by similar builds"
        )
    if any(x in p for x in ["crash", "risk", "safety", "danger", "fatigue"]):
        return (
            "Safety radar flags elevated risk signature across current input parameters.\n\n"
            "Observations:\n"
            "• Aggression index above safe operational threshold\n"
            "• Tire envelope degraded — 73% correlation with high-side incidents at T1\n"
            "• Fatigue profile indicates reduced reaction margin in fast sections\n\n"
            "Immediate actions required:\n"
            "• Reduce corner entry speed 12km/h in negative-camber sectors\n"
            "• Extend following distance until fresh rubber fitted\n"
            "• Prioritize corner exit over maximum entry — margin management is championship driving"
        )
    if any(x in p for x in ["reaction", "reflex", "response time"]):
        return (
            "Neural response data indicates a developing competitive reflex profile.\n\n"
            "Observations:\n"
            "• MotoGP race-start benchmark is <220ms gate-to-throttle\n"
            "• Current profile projects to 240ms range within structured training\n\n"
            "Recommended programme:\n"
            "• 3 sessions/week of visual-trigger response training\n"
            "• Focus on reactive vs. anticipatory response patterns\n"
            "• Elite starters average 195ms — achievable in 6–8 weeks with discipline"
        )
    if any(x in p for x in ["track", "circuit", "corner", "racing line", "braking zone"]):
        return (
            "Circuit analysis complete. Primary time loss at mid-speed chicane and final hairpin.\n\n"
            "Observations:\n"
            "• Top-5 qualifiers show consistent 150m board engagement at T7\n"
            "• Geometric late apex required through main chicane — excess entry speed kills drive\n"
            "• Kerb usage at exit is suboptimal — 0.1s available through better apex geometry\n\n"
            "Recommended approach:\n"
            "• Trail-brake deeper into apex, maintain lean through exit kerb\n"
            "• Prioritize drive for the following straight over maximum corner entry\n"
            "• Elite riders typically gain 0.6s per lap through disciplined execution of this sector"
        )
    if any(x in p for x in ["rider", "profile", "biography", "career"]):
        return (
            "Rider profile assessment complete.\n\n"
            "Observations:\n"
            "• Technical riding style with notable strength in braking stability and corner approach\n"
            "• Performance DNA optimal for cool, high-grip circuits with demanding braking zones\n"
            "• Year-on-year consistency improvement noted — positive development trajectory\n\n"
            "Development targets:\n"
            "• Corner-exit throttle application currently 18% below elite benchmark\n"
            "• Mental pressure management under championship conditions needs work\n"
            "• Projected ceiling: podium contention within 2 full seasons at current improvement rate"
        )
    return (
        "Telemetry analysis complete. Input parameters processed through race engineering algorithms.\n\n"
        "Observations:\n"
        "• Targeted improvement areas identified across multiple performance vectors\n"
        "• Current profile shows competitive baseline with clear development pathway\n\n"
        "Recommended focus:\n"
        "• Address weakest metric identified in computed analysis first\n"
        "• Precision, consistency, and incremental improvement define championship performance\n"
        "• Schedule structured data review session after next track outing"
    )


# ─────────────────────────────────────────────────────────────────────────────
# MANUAL COMPUTATION ENGINES
# ─────────────────────────────────────────────────────────────────────────────
def calc_performance(speed, lap, consistency, braking):
    speed_s = min(100, (speed - 100) / 270 * 100)
    time_s  = max(0, 100 - (lap - 60) / 1.4)
    score   = round(0.25*speed_s + 0.30*time_s + 0.25*consistency + 0.20*braking, 1)
    return score, round(speed_s, 1), round(time_s, 1)


def calc_risk(speed, fatigue, agg, weather_idx, tire_wear, familiarity):
    weather_mult = [1.0, 1.25, 1.65, 2.15, 1.9]
    r = (
        (speed - 60) / 300 * 40
        + fatigue * 5
        + agg * 5.5
        + (weather_mult[weather_idx] - 1) * 30
        + tire_wear * 0.3
        + (10 - familiarity) * 2.5
    )
    return round(min(97, max(3, r)), 1)


def calc_setup(weight, style, terrain):
    spring = 78 + (weight - 65) * 0.85
    if terrain == "High-Speed":    spring += 5
    if terrain == "Bumpy Street":  spring -= 8
    adj = {"Aggressive Entry": 3, "Late Braking": 2, "Smooth Arc": -2, "Throttle-First": 1, "Balanced": 0}
    comp = round(8 + adj.get(style, 0) + random.uniform(-0.3, 0.3), 1)
    reb  = round(9.2 + random.uniform(-0.3, 0.3), 1)
    fp   = round(2.02 + (weight - 65) * 0.004, 2)
    rp   = round(1.89 + (weight - 65) * 0.003, 2)
    return round(spring, 1), comp, reb, fp, rp


def calc_pit_strategy(tire, weather):
    windows = {"New": 18, "Good": 14, "Worn": 9, "Critical": 5}
    pw = windows.get(tire, 12)
    if weather in ["Wet", "Mixed"]:
        pw = max(3, pw - 4)
    second = "Hard" if tire in ["New", "Good"] else "Medium"
    return pw, second


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo block
    H("""
    <div style="
      padding:22px 18px 18px;
      border-bottom:1px solid rgba(255,255,255,0.06);
      margin-bottom:6px;
      background:linear-gradient(135deg,rgba(255,0,51,0.04),transparent);
    ">
      <div style="
        font-family:'Orbitron',monospace;font-size:22px;font-weight:900;
        letter-spacing:4px;color:#fff;line-height:1;
      ">MOTO<span style="color:#FF0033;">GP</span></div>
      <div style="
        font-family:'Share Tech Mono',monospace;font-size:9px;
        letter-spacing:2.5px;color:#00F5FF;margin-top:5px;opacity:0.7;
      ">ELITE INTELLIGENCE SYSTEM</div>
      <div style="display:flex;align-items:center;gap:8px;margin-top:12px;">
        <span style="width:7px;height:7px;background:#00FF85;border-radius:50%;
          box-shadow:0 0 8px #00FF85;display:inline-block;"></span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:10px;
          color:#00FF85;letter-spacing:1.5px;">SYSTEM ONLINE</span>
      </div>
    </div>
    """)

    H('<div style="padding:12px 10px 6px;font-family:\'Share Tech Mono\',monospace;font-size:9px;color:#3D5060;letter-spacing:3px;">MODULES</div>')

    module = st.radio("_nav", [
        "📡 Live Telemetry",
        "🧠 Performance Analyzer",
        "🏁 Pit Wall Strategy",
        "🏍️ Machine Setup",
        "⚡ Reaction Simulator",
        "⚠️ Safety Radar",
        "📈 Sector Timing",
        "🧾 Rider Profile",
        "🏆 Track Mastery",
    ], label_visibility="collapsed")

    H('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);margin:10px 0;"></div>')
    H('<div style="padding:8px 10px 6px;font-family:\'Share Tech Mono\',monospace;font-size:9px;color:#3D5060;letter-spacing:3px;">ENGINE MODE</div>')

    mode = st.radio("_mode", ["🛠️ Manual", "🤖 AI", "🔥 Hybrid"], index=2, label_visibility="collapsed")

    H('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);margin:10px 0;"></div>')
    H('<div style="padding:8px 10px 6px;font-family:\'Share Tech Mono\',monospace;font-size:9px;color:#3D5060;letter-spacing:3px;">API KEYS</div>')

    k1 = st.text_input("_oai", type="password", placeholder="OpenAI key (sk-…)", label_visibility="collapsed")
    k2 = st.text_input("_cld", type="password", placeholder="Claude key (sk-ant-…)", label_visibility="collapsed")
    if k1: st.session_state["k_oai"] = k1
    if k2: st.session_state["k_cld"] = k2

    # Status panel
    H("""
    <div style="
      margin-top:12px;padding:12px 14px;
      background:rgba(0,0,0,0.3);
      border:1px solid rgba(255,255,255,0.05);
      border-radius:6px;
      font-family:'Share Tech Mono',monospace;font-size:10px;
      color:#3D5060;line-height:2.3;
    ">
      <span style="color:#455060;">SESSION</span> QUALIFYING<br>
      <span style="color:#455060;">TRACK TEMP</span> 28°C<br>
      <span style="color:#455060;">GRIP</span> NOMINAL<br>
      <span style="color:#455060;">WIND</span> 12km/h NW<br>
      <span style="color:#455060;">VERSION</span> 4.1.0
    </div>
    """)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: LIVE TELEMETRY
# ─────────────────────────────────────────────────────────────────────────────
if "Live Telemetry" in module:
    page_header("📡", "Live Telemetry", "REAL-TIME PIT WALL FEED · SIMULATED RACE DATA STREAM")

    alert("SIMULATION MODE — Pit wall data refreshes every 1.5 s. Press START to activate the live feed.", "info")

    btn_col1, btn_col2, _ = st.columns([1, 1, 4])
    with btn_col1:
        start = st.button("▶ START FEED", key="lt_start")
    with btn_col2:
        stop  = st.button("■ STOP", key="lt_stop")

    if "live_on" not in st.session_state:
        st.session_state.live_on = False
    if start: st.session_state.live_on = True
    if stop:  st.session_state.live_on = False

    ph_cards  = st.empty()
    ph_chart  = st.empty()
    ph_gauges = st.empty()
    ph_log    = st.empty()

    if st.session_state.live_on:
        spd_h, lt_h, rk_h, lbl_h = [], [], [], []
        lap_n = 1

        for tick in range(80):
            if not st.session_state.live_on:
                break

            spd  = round(270 + random.uniform(-18, 24) - (tick % 9) * 0.4, 1)
            lt   = round(102.4 + random.uniform(-0.6, 1.4) - (tick % 14) * 0.06, 2)
            rsk  = round(random.uniform(18, 78), 1)
            rpm  = random.randint(11000, 14900)
            gear = random.randint(3, 6)
            thr  = round(random.uniform(38, 100), 1)
            brk  = round(random.uniform(0, 82), 1)
            lean = round(random.uniform(28, 61), 1)

            if tick % 9 == 0 and tick > 0:
                lap_n += 1

            spd_h.append(spd); lt_h.append(lt)
            rk_h.append(rsk);  lbl_h.append(f"T{tick+1}")

            rsk_color = "#FF0033" if rsk > 60 else ("#FFB800" if rsk > 35 else "#00FF85")

            with ph_cards.container():
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                with c1: metric_card(f"{spd:.0f}", "SPEED km/h",  "#00F5FF")
                with c2: metric_card(f"{lt:.2f}s", "LAP TIME",    "#FF0033")
                with c3: metric_card(f"{rsk:.0f}%","RISK INDEX",  rsk_color)
                with c4: metric_card(f"{rpm:,}",   "ENGINE RPM",  "#00FF85")
                with c5: metric_card(f"{thr:.0f}%","THROTTLE",    "#00FF85")
                with c6: metric_card(f"G{gear}",   "GEAR",        "#7A8899")

            with ph_chart.container():
                df = pd.DataFrame({
                    "Speed (/10)": [s / 10 for s in spd_h[-30:]],
                    "Lap Time":    lt_h[-30:],
                    "Risk (/10)":  [r / 10  for r in rk_h[-30:]],
                }, index=lbl_h[-30:])
                st.line_chart(df, color=["#00F5FF", "#FF0033", "#FFB800"], height=220)

            with ph_gauges.container():
                g1, g2, g3 = st.columns(3)
                with g1:
                    H('<div style="font-family:\'Share Tech Mono\',monospace;font-size:10px;color:#3D5060;letter-spacing:2px;margin-bottom:4px;">THROTTLE</div>')
                    st.progress(int(thr))
                with g2:
                    H('<div style="font-family:\'Share Tech Mono\',monospace;font-size:10px;color:#3D5060;letter-spacing:2px;margin-bottom:4px;">BRAKE</div>')
                    st.progress(int(brk))
                with g3:
                    H('<div style="font-family:\'Share Tech Mono\',monospace;font-size:10px;color:#3D5060;letter-spacing:2px;margin-bottom:4px;">LEAN ANGLE</div>')
                    st.progress(int(lean / 65 * 100))

            with ph_log.container():
                H(f"""
                <div style="
                  background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.05);
                  border-left:2px solid #00FF85;border-radius:0 4px 4px 0;
                  padding:10px 16px;font-family:'Share Tech Mono',monospace;font-size:12px;
                  display:flex;gap:20px;flex-wrap:wrap;
                ">
                  <span><span style="color:#FF0033;">◉ LAP {lap_n}</span></span>
                  <span>SPD <span style="color:#00F5FF;">{spd}kph</span></span>
                  <span>LEAN <span style="color:#FFB800;">{lean:.1f}°</span></span>
                  <span>BRAKE <span style="color:#FF0033;">{brk:.0f}%</span></span>
                  <span>THROTTLE <span style="color:#00FF85;">{thr:.0f}%</span></span>
                  <span>RPM <span style="color:#7A8899;">{rpm:,}</span></span>
                </div>
                """)
            time.sleep(1.5)
    else:
        H("""
        <div style="
          display:flex;flex-direction:column;align-items:center;justify-content:center;
          height:380px;opacity:0.2;
        ">
          <div style="font-size:48px;margin-bottom:16px;">📡</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:12px;
            letter-spacing:4px;color:#3D5060;">FEED INACTIVE — PRESS START</div>
        </div>
        """)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: PERFORMANCE ANALYZER
# ─────────────────────────────────────────────────────────────────────────────
elif "Performance" in module:
    page_header("🧠", "Performance Analyzer", "MULTI-AXIS TELEMETRY INTELLIGENCE · REAL-TIME SCORING ENGINE")
    mode_badge(mode)

    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        section_label("INPUT PARAMETERS")
        speed    = st.slider("Top Speed (km/h)",    100, 370, 292, key="pa_spd")
        lap_t    = st.slider("Best Lap (seconds)",   60, 200, 103, key="pa_lap")
        cons     = st.slider("Consistency (%)",       0, 100,  73, key="pa_con")
        braking  = st.slider("Braking Skill",         0, 100,  67, key="pa_brk")
        cornering= st.slider("Cornering Skill",       0, 100,  72, key="pa_cor")
        throttle = st.slider("Throttle Control",      0, 100,  65, key="pa_thr")
        run_btn  = st.button("▶ RUN ANALYSIS", key="pa_run")

    with col_out:
        if run_btn:
            score, ss, ts = calc_performance(speed, lap_t, cons, braking)
            overall = round(np.mean([ss, ts, cons, braking, cornering, throttle]), 1)
            tier = "ELITE" if overall >= 80 else ("COMPETITIVE" if overall >= 60 else "DEVELOPING")
            tier_c = "#00FF85" if overall >= 80 else ("#FFB800" if overall >= 60 else "#FF0033")

            c1, c2, c3, c4 = st.columns(4)
            with c1: metric_card(f"{overall:.0f}", "OVERALL INDEX", "#FF0033")
            with c2: metric_card(f"{lap_t}s",      "BEST LAP",     "#00F5FF")
            with c3: metric_card(f"{cons}%",       "CONSISTENCY",  "#00FF85")
            with c4: metric_card(f"{speed}kph",    "TOP SPEED",    "#FFB800")

            divider()

            if mode in ["🛠️ Manual", "🔥 Hybrid"]:
                section_label("SKILL BREAKDOWN")
                skill_bar("Braking Zone",     braking,    color="#FF0033")
                skill_bar("Cornering Speed",  cornering,  color="#00F5FF")
                skill_bar("Throttle Control", throttle,   color="#FFB800")
                skill_bar("Lap Consistency",  cons,       color="#00FF85")
                skill_bar("Speed Score",      ss,         color="#9D4EDD")
                skill_bar("Lap Time Score",   ts,         color="#FF6699")

                weakest = min(
                    [("BRAKING", braking), ("CORNERING", cornering), ("THROTTLE", throttle)],
                    key=lambda x: x[1]
                )
                alert(f"Primary deficit identified: <strong>{weakest[0]}</strong> at {weakest[1]:.0f}/100 — focus next session here.", "warn")

            if mode == "🤖 AI":
                with st.spinner("Race engineer analyzing telemetry…"):
                    resp = ai_response(
                        f"Analyze rider telemetry: speed={speed}kph, best_lap={lap_t}s, "
                        f"consistency={cons}%, braking={braking}/100, cornering={cornering}/100, "
                        f"throttle={throttle}/100, overall_index={overall}/100."
                    )
                engineer_feed(resp)
                voice_button(resp, "pa_voice")

            if mode == "🔥 Hybrid":
                weakest = min(
                    [("BRAKING", braking), ("CORNERING", cornering), ("THROTTLE", throttle)],
                    key=lambda x: x[1]
                )
                manual_txt = (
                    f"Performance Index: {overall:.1f}/100\n"
                    f"Tier classification: {tier}\n"
                    f"Primary deficit: {weakest[0]} ({weakest[1]:.0f}/100)\n"
                    f"Consistency: {cons}% — {'within target' if cons >= 70 else 'below threshold'}\n"
                    f"Speed score: {ss:.1f} | Lap time score: {ts:.1f}"
                )
                with st.spinner("Fusing AI enhancement layer…"):
                    ai_txt = ai_response(
                        f"Enhance this performance report with engineering insight: "
                        f"overall={overall:.1f}/100, tier={tier}, "
                        f"braking={braking}, cornering={cornering}, throttle={throttle}, "
                        f"consistency={cons}%, speed={speed}kph, lap={lap_t}s. "
                        f"Primary gap: {weakest[0]}."
                    )
                hybrid_report(manual_txt, ai_txt)
                voice_button(ai_txt, "pa_hv")

            divider()
            chart_df = pd.DataFrame(
                {"Score": [braking, cornering, throttle, cons, ss, ts]},
                index=["Braking", "Cornering", "Throttle", "Consistency", "Speed", "Lap Time"],
            )
            st.bar_chart(chart_df, color="#FF0033", height=200)
        else:
            H("""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:300px;opacity:0.18;"><div style="font-size:40px;margin-bottom:12px;">🧠</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:4px;
            color:#3D5060;">AWAITING DATA INPUT</div></div>""")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: PIT WALL STRATEGY
# ─────────────────────────────────────────────────────────────────────────────
elif "Pit Wall" in module:
    page_header("🏁", "Pit Wall Strategy", "ADAPTIVE RACE STRATEGY ENGINE · TIRE & FUEL MANAGEMENT")
    mode_badge(mode)

    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        section_label("RACE PARAMETERS")
        track_type = st.selectbox("Track Type",      ["High-Speed", "Technical", "Mixed", "Street Circuit", "Flowing Curves"])
        weather    = st.selectbox("Conditions",      ["Dry – Hot", "Dry – Cool", "Overcast", "Mixed", "Wet"])
        bike_class = st.selectbox("Bike Class",      ["MotoGP Prototype", "Superbike", "Supersport"])
        tire_start = st.selectbox("Starting Tire",   ["New", "Good", "Worn", "Critical"])
        num_laps   = st.slider("Race Laps",          10, 30, 22)
        grid_pos   = st.number_input("Grid Position", 1, 24,  5)
        run_btn    = st.button("▶ BUILD STRATEGY", key="pw_run")

    with col_out:
        if run_btn:
            w_idx = ["Dry – Hot", "Dry – Cool", "Overcast", "Mixed", "Wet"].index(weather)
            pit_lap, sec_compound = calc_pit_strategy(tire_start, weather)
            target_pos = max(1, grid_pos - random.randint(1, 4))
            risk_idx   = min(98, 40 + w_idx * 12 - (num_laps - pit_lap))

            c1, c2, c3, c4 = st.columns(4)
            with c1: metric_card(f"LAP {pit_lap}",          "PIT WINDOW",    "#FF0033")
            with c2: metric_card(sec_compound.upper(),       "2ND COMPOUND",  "#00F5FF")
            with c3: metric_card(f"P{target_pos}",          "TARGET FINISH", "#00FF85")
            with c4: metric_card(f"{risk_idx:.0f}%",        "RISK INDEX",    "#FFB800")

            divider()

            if mode in ["🛠️ Manual", "🔥 Hybrid"]:
                section_label("LAP-BY-LAP RACE SCRIPT")
                overtake_laps = sorted(random.sample(range(2, min(pit_lap, num_laps)), min(3, pit_lap - 2)))
                col_a, col_b  = st.columns(2)
                for i in range(1, num_laps + 1):
                    if   i == 1:              ac, lc = "LAUNCH — HOLD POSITION",       "#FFB800"
                    elif i in overtake_laps:  ac, lc = f"OVERTAKE WINDOW · L{i}",      "#00F5FF"
                    elif i == pit_lap:        ac, lc = f"⏩ BOX → {sec_compound.upper()}", "#FF0033"
                    elif pit_lap < i <= pit_lap + 2: ac, lc = "TIRE WARM-UP — HOLD",   "#3D5060"
                    elif i >= num_laps - 3:   ac, lc = "FINAL PUSH — FULL ATTACK",     "#00FF85"
                    else:
                        ac = ["MANAGE GAP", "PUSH PACE", "FUEL DELTA"][i % 3]
                        lc = "#3D5060"
                    with (col_a if i % 2 else col_b):
                        lap_row(i, ac, lc)

            if mode == "🤖 AI":
                with st.spinner("Pit wall engineer building race plan…"):
                    resp = ai_response(
                        f"Build a complete MotoGP race strategy: track={track_type}, "
                        f"weather={weather}, starting_tire={tire_start}, "
                        f"total_laps={num_laps}, grid_pos={grid_pos}, bike={bike_class}. "
                        "Cover pit timing, compound choices, overtaking windows, fuel delta, risk assessment."
                    )
                engineer_feed(resp, "PIT WALL STRATEGY FEED")
                voice_button(resp, "pw_voice")

            if mode == "🔥 Hybrid":
                manual_txt = (
                    f"Pit window: LAP {pit_lap}\n"
                    f"Second compound: {sec_compound}\n"
                    f"Target finish: P{target_pos}\n"
                    f"Weather factor: {weather} — {'elevated deg risk' if w_idx >= 3 else 'nominal conditions'}\n"
                    f"Risk index: {risk_idx:.0f}%"
                )
                with st.spinner("AI enhancing race strategy…"):
                    ai_txt = ai_response(
                        f"Enhance this race strategy with expert race engineering: "
                        f"pit_lap={pit_lap}, second_compound={sec_compound}, "
                        f"track={track_type}, weather={weather}, grid_pos={grid_pos}, laps={num_laps}. "
                        "Add psychology cues, tire management phases, fuel delta targets."
                    )
                hybrid_report(manual_txt, ai_txt)
                voice_button(ai_txt, "pw_hv")
        else:
            H("""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:300px;opacity:0.18;"><div style="font-size:40px;margin-bottom:12px;">🏁</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:4px;
            color:#3D5060;">CONFIGURE RACE PARAMETERS</div></div>""")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: MACHINE SETUP
# ─────────────────────────────────────────────────────────────────────────────
elif "Machine" in module:
    page_header("🏍️", "Machine Setup", "SUSPENSION · TIRE PRESSURE · GEARING · AERO CONFIGURATION")
    mode_badge(mode)

    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        section_label("MACHINE PARAMETERS")
        rider_wt = st.slider("Rider Weight (kg)",    50, 105,  68)
        ride_sty = st.selectbox("Riding Style", ["Aggressive Entry", "Late Braking", "Smooth Arc", "Throttle-First", "Balanced"])
        terrain  = st.selectbox("Track Type",   ["High-Speed", "Technical", "Mixed", "Bumpy Street", "Smooth Tarmac"])
        amb_temp = st.slider("Ambient Temp (°C)",     5,  50,  24)
        run_btn  = st.button("▶ GENERATE SETUP", key="ms_run")

    with col_out:
        if run_btn:
            spring, comp, reb, fp, rp = calc_setup(rider_wt, ride_sty, terrain)
            temp_adj = (amb_temp - 20) * 0.008
            fp = round(fp + temp_adj,       2)
            rp = round(rp + temp_adj * 0.8, 2)

            c1, c2, c3, c4 = st.columns(4)
            with c1: metric_card(f"{spring:.1f}",   "SPRING RATE", "#FF0033")
            with c2: metric_card(f"{comp:.1f}",     "COMPRESSION", "#00F5FF")
            with c3: metric_card(f"{fp} bar",       "FRONT PRESS", "#00FF85")
            with c4: metric_card(f"{rp} bar",       "REAR PRESS",  "#FFB800")

            divider()

            if mode in ["🛠️ Manual", "🔥 Hybrid"]:
                section_label("SUSPENSION PROFILE")
                skill_bar("Front Spring",    spring,      120, "#00F5FF")
                skill_bar("Rear Spring",     spring*1.08, 120, "#FF0033")
                skill_bar("Compression",     comp,         20, "#FFB800")
                skill_bar("Rebound",         reb,          20, "#00FF85")

                divider()
                gear_map = {
                    "High-Speed":    "Primary 2.80 · Final 2.35 — max Vmax ratio",
                    "Technical":     "Primary 3.10 · Final 2.70 — short exit drive",
                    "Mixed":         "Primary 2.95 · Final 2.52 — balanced compromise",
                    "Bumpy Street":  "Primary 3.00 · Final 2.60 — smooth power delivery",
                    "Smooth Tarmac": "Primary 2.85 · Final 2.42 — high-speed bias",
                }
                aero_map = {
                    "Aggressive Entry": "Front wing +2° for additional entry stability",
                    "Late Braking":     "Ride height +3mm front — improved pitch control",
                    "Smooth Arc":       "Factory neutral aero — standard spec",
                    "Throttle-First":   "Rear ride height -2mm — maximize exit traction",
                    "Balanced":         "Minor front downforce trim from factory baseline",
                }
                section_label("DRIVETRAIN & AERO")
                radio_line(f"GEARING: {gear_map.get(terrain, 'Standard')}",  "#FFB800")
                radio_line(f"AERO:    {aero_map.get(ride_sty, 'Factory')}",  "#00F5FF")
                radio_line(f"TC LEVEL: {'4' if 'Agg' in ride_sty else '6'} · EC: {'3' if 'Late' in ride_sty else '4'} · WC: Standard", "#00FF85")

            if mode == "🤖 AI":
                with st.spinner("Machine engineer computing setup…"):
                    resp = ai_response(
                        f"Generate complete MotoGP bike setup: rider_weight={rider_wt}kg, "
                        f"style={ride_sty}, track={terrain}, ambient_temp={amb_temp}°C. "
                        "Provide specific suspension values, tire pressures, gearing, and aero adjustments."
                    )
                engineer_feed(resp, "MACHINE SETUP FEED")
                voice_button(resp, "ms_voice")

            if mode == "🔥 Hybrid":
                manual_txt = (
                    f"Spring rate:   F={spring:.1f} · R={spring*1.08:.1f}\n"
                    f"Damping:       Comp={comp:.1f} clicks · Reb={reb:.1f} clicks\n"
                    f"Tire pressure: F={fp}bar · R={rp}bar\n"
                    f"Gearing:       {gear_map.get(terrain, 'Standard')}\n"
                    f"Aero:          {aero_map.get(ride_sty, 'Factory spec')}"
                )
                with st.spinner("AI enhancing machine setup…"):
                    ai_txt = ai_response(
                        f"Enhance this bike setup with engineering detail: "
                        f"spring={spring:.1f}, comp={comp:.1f}, reb={reb:.1f}, "
                        f"FP={fp}bar, RP={rp}bar, rider={rider_wt}kg, style={ride_sty}, track={terrain}."
                    )
                hybrid_report(manual_txt, ai_txt)
                voice_button(ai_txt, "ms_hv")
        else:
            H("""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:300px;opacity:0.18;"><div style="font-size:40px;margin-bottom:12px;">🏍️</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:4px;
            color:#3D5060;">CONFIGURE MACHINE PARAMETERS</div></div>""")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: REACTION SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────
elif "Reaction" in module:
    page_header("⚡", "Reaction Simulator", "NEURAL RESPONSE CALIBRATION · MotoGP REFLEX BENCHMARK")
    mode_badge(mode)

    # Init session state
    defaults = [("rx_state","idle"),("rx_go_time",0.0),("rx_t0",0.0),
                ("rx_times",[]),("rx_last",0.0),("rx_count",0)]
    for k, v in defaults:
        if k not in st.session_state:
            st.session_state[k] = v

    col_game, col_stats = st.columns([2, 1], gap="large")

    with col_game:
        state = st.session_state.rx_state

        if state == "idle":
            H("""
            <div style="
              background:linear-gradient(135deg,#0C1118,#101820);
              border:1px solid rgba(255,255,255,0.06);
              border-radius:8px;padding:60px 20px;text-align:center;
            ">
              <div style="font-size:36px;margin-bottom:16px;">⚡</div>
              <div style="font-family:'Orbitron',monospace;font-size:13px;
                letter-spacing:4px;color:#3D5060;">REACTION TEST READY</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                color:#2A3A48;margin-top:8px;">PRESS START TO BEGIN</div>
            </div>
            """)
            if st.button("▶ START SESSION", key="rx_start"):
                st.session_state.rx_state    = "waiting"
                st.session_state.rx_go_time  = time.time() + random.uniform(1.5, 4.5)
                st.rerun()

        elif state == "waiting":
            if time.time() >= st.session_state.rx_go_time:
                st.session_state.rx_state = "go"
                st.session_state.rx_t0    = time.time()
                st.rerun()

            H("""
            <div style="
              background:linear-gradient(135deg,#120900,#1A0E00);
              border:2px solid #FFB800;border-radius:8px;
              padding:60px 20px;text-align:center;
              box-shadow:0 0 30px rgba(255,184,0,0.12);
            ">
              <div style="font-family:'Orbitron',monospace;font-size:20px;
                letter-spacing:6px;color:#FFB800;">⏸ WAIT…</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                color:#5A4000;margin-top:10px;">DO NOT REACT YET</div>
            </div>
            """)
            if st.button("FALSE START ⚡", key="rx_false"):
                st.session_state.rx_times.append(999)
                st.session_state.rx_last  = 999
                st.session_state.rx_count += 1
                st.session_state.rx_state = "result"
                st.rerun()
            time.sleep(0.12)
            st.rerun()

        elif state == "go":
            H("""
            <div style="
              background:linear-gradient(135deg,#001A07,#002010);
              border:2px solid #00FF85;border-radius:8px;
              padding:60px 20px;text-align:center;
              box-shadow:0 0 40px rgba(0,255,133,0.2);
            ">
              <div style="font-family:'Orbitron',monospace;font-size:24px;
                letter-spacing:6px;color:#00FF85;">🟢 GO! GO! GO!</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:12px;
                color:#005530;margin-top:10px;">REACT NOW!</div>
            </div>
            """)
            if st.button("⚡ TAP NOW!", key="rx_tap"):
                rt = (time.time() - st.session_state.rx_t0) * 1000
                st.session_state.rx_times.append(rt)
                st.session_state.rx_last   = rt
                st.session_state.rx_count += 1
                st.session_state.rx_state  = "result"
                st.rerun()

        elif state == "result":
            rt = st.session_state.rx_last
            if   rt == 999: rating, color = "FALSE START",   "#FF0033"
            elif rt < 200:  rating, color = "SUPERHUMAN",    "#00FF85"
            elif rt < 270:  rating, color = "MotoGP LEVEL",  "#00F5FF"
            elif rt < 360:  rating, color = "COMPETITIVE",   "#FFB800"
            else:           rating, color = "DEVELOPING",    "#FF0033"

            display = "FALSE" if rt == 999 else f"{rt:.0f}ms"
            H(f"""
            <div style="
              background:linear-gradient(135deg,#0A0E14,#0E1520);
              border:2px solid {color};border-radius:8px;
              padding:40px 20px;text-align:center;
              box-shadow:0 0 40px {color}22;
            ">
              <div style="font-family:'Orbitron',monospace;font-size:48px;
                font-weight:700;color:{color};line-height:1;
                text-shadow:0 0 20px {color}66;">{display}</div>
              <div style="font-family:'Orbitron',monospace;font-size:12px;
                font-weight:700;letter-spacing:4px;color:{color};
                margin-top:10px;opacity:0.9;">{rating}</div>
            </div>
            """)

            msg_map = {
                "FALSE START":  "Anticipatory trigger detected — train reactive, not predictive response.",
                "SUPERHUMAN":   "Elite-tier neural response confirmed. MotoGP race-start benchmark achieved.",
                "MotoGP LEVEL": "Professional race-start window confirmed. Top 10% competitive profile.",
                "COMPETITIVE":  "Solid profile. Sub-270ms achievable with 4 weeks of structured drills.",
                "DEVELOPING":   "200 reps/session of visual-trigger training required to reach benchmark.",
            }

            if mode in ["🤖 AI", "🔥 Hybrid"]:
                with st.spinner("Analyzing reflex profile…"):
                    resp = ai_response(
                        f"Reaction time recorded: {rt:.0f}ms, classification: {rating}. "
                        "Provide coaching feedback with specific reflex improvement drills."
                    )
                engineer_feed(resp, "REFLEX COACHING FEED")
                voice_button(resp, "rx_voice")
            else:
                alert(msg_map[rating], "safe" if rt < 360 and rt != 999 else "warn")

            btn_a, btn_b = st.columns(2)
            with btn_a:
                if st.button("▶ NEXT ROUND", key="rx_next"):
                    st.session_state.rx_state   = "waiting"
                    st.session_state.rx_go_time = time.time() + random.uniform(1.5, 4.5)
                    st.rerun()
            with btn_b:
                if st.button("↺ RESET SESSION", key="rx_reset"):
                    for k, v in [("rx_state","idle"),("rx_times",[]),("rx_last",0.0),("rx_count",0)]:
                        st.session_state[k] = v
                    st.rerun()

    with col_stats:
        section_label("SESSION STATS")
        valid = [t for t in st.session_state.rx_times if t != 999]

        metric_card(str(st.session_state.rx_count), "ROUNDS", "#FF0033")

        if valid:
            H("<br>")
            metric_card(f"{min(valid):.0f}ms",       "PERSONAL BEST",  "#00FF85")
            H("<br>")
            metric_card(f"{np.mean(valid):.0f}ms",   "AVG REACTION",   "#00F5FF")
            H("<br>")
            rt_df = pd.DataFrame({"Reaction (ms)": valid}, index=range(1, len(valid)+1))
            st.line_chart(rt_df, color="#FF0033", height=160)

        H("""
        <div style="
          background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.05);
          border-radius:6px;padding:14px 16px;
          font-family:'Share Tech Mono',monospace;font-size:10px;
          line-height:2.5;margin-top:14px;
        ">
          <div style="color:#3D5060;letter-spacing:2px;font-size:9px;margin-bottom:6px;">BENCHMARK REFERENCE</div>
          <div><span style="color:#00FF85;">●</span> <span style="color:#455060;">MotoGP ELITE</span>  &lt;200ms</div>
          <div><span style="color:#00F5FF;">●</span> <span style="color:#455060;">PROFESSIONAL</span>  &lt;270ms</div>
          <div><span style="color:#FFB800;">●</span> <span style="color:#455060;">COMPETITIVE</span>   &lt;360ms</div>
          <div><span style="color:#FF0033;">●</span> <span style="color:#455060;">DEVELOPING</span>    &gt;360ms</div>
        </div>
        """)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: SAFETY RADAR
# ─────────────────────────────────────────────────────────────────────────────
elif "Safety" in module:
    page_header("⚠️", "Safety Radar", "CRASH RISK PREDICTION · INCIDENT PREVENTION · SAFETY INTELLIGENCE")
    mode_badge(mode)

    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        section_label("RISK PARAMETERS")
        entry_spd = st.slider("Entry Speed (km/h)",      60, 350, 190)
        fatigue   = st.slider("Fatigue Level (0=Fresh)",  0,  10,   5)
        agg       = st.slider("Aggression Index (0–10)",  0,  10,   6)
        conditions= st.selectbox("Track Conditions", ["Dry – Optimal","Dry – Dusty","Damp","Wet","Mixed"])
        tire_wear = st.slider("Tire Wear (%)",            0, 100,  50)
        familiarity=st.slider("Track Familiarity (0–10)", 0,  10,   6)
        run_btn   = st.button("▶ ASSESS RISK", key="sr_run")

    with col_out:
        if run_btn:
            w_idx   = ["Dry – Optimal","Dry – Dusty","Damp","Wet","Mixed"].index(conditions)
            risk    = calc_risk(entry_spd, fatigue, agg, w_idx, tire_wear, familiarity)
            margin  = round(max(0, 100 - risk), 1)
            level   = "CRITICAL" if risk > 70 else ("HIGH" if risk > 50 else ("MODERATE" if risk > 30 else "LOW"))
            lv_col  = "#FF0033" if risk > 70 else ("#FFB800" if risk > 50 else ("#00F5FF" if risk > 30 else "#00FF85"))

            c1, c2, c3 = st.columns(3)
            with c1: metric_card(f"{risk:.0f}%",   "CRASH RISK",    "#FF0033" if risk > 50 else "#FFB800")
            with c2: metric_card(level,             "RISK LEVEL",    lv_col)
            with c3: metric_card(f"{margin:.0f}%",  "SAFETY MARGIN", "#00FF85")

            divider()

            if mode in ["🛠️ Manual", "🔥 Hybrid"]:
                section_label("FACTOR CONTRIBUTION")
                wm = [1.0, 1.25, 1.65, 2.15, 1.9]
                skill_bar("Speed Vector",        (entry_spd-60)/300*40, 40, "#FF0033")
                skill_bar("Fatigue Impact",       fatigue * 5,          50, "#FFB800")
                skill_bar("Aggression Factor",    agg * 5.5,            55, "#FF6633")
                skill_bar("Weather Multiplier",   (wm[w_idx]-1)*30,     33, "#00F5FF")
                skill_bar("Tire Degradation",     tire_wear * 0.3,      30, "#9D4EDD")
                skill_bar("Track Unfamiliarity",  (10-familiarity)*2.5, 25, "#3D5060")

                divider()
                if   risk > 70: alert(f"CRITICAL RISK — {risk:.0f}% crash probability. Pit immediately. Reduce entry speed, lower aggression, change tires.", "danger")
                elif risk > 50: alert(f"HIGH RISK — {risk:.0f}%. Reduce corner entry speed and manage fatigue over next stint.", "warn")
                elif risk > 30: alert(f"MODERATE RISK — {risk:.0f}%. Monitor tire wear closely. Reduce lean angle in negative-camber sections.", "info")
                else:           alert(f"LOW RISK — {risk:.0f}%. All parameters within safe operational window. Proceed at race pace.", "safe")

            if mode == "🤖 AI":
                with st.spinner("Safety systems analyzing risk profile…"):
                    resp = ai_response(
                        f"Safety assessment: entry_speed={entry_spd}kph, fatigue={fatigue}/10, "
                        f"aggression={agg}/10, conditions={conditions}, tire_wear={tire_wear}%, "
                        f"track_familiarity={familiarity}/10. Computed risk: {risk:.0f}%. "
                        "Provide immediate and session-level safety recommendations."
                    )
                engineer_feed(resp, "SAFETY ENGINEER FEED")
                voice_button(resp, "sr_voice")

            if mode == "🔥 Hybrid":
                wm = [1.0, 1.25, 1.65, 2.15, 1.9]
                manual_txt = (
                    f"Risk Index:     {risk:.0f}% — Level: {level}\n"
                    f"Safety Margin:  {margin:.0f}%\n"
                    f"Top factors:    Speed contribution={((entry_spd-60)/300*40):.1f}, "
                    f"Aggression={agg*5.5:.1f}, Fatigue={fatigue*5:.1f}\n"
                    f"Conditions:     {conditions} (multiplier {wm[w_idx]:.2f}x)\n"
                    f"Tire wear:      {tire_wear}%"
                )
                with st.spinner("AI safety analysis in progress…"):
                    ai_txt = ai_response(
                        f"Enhance safety analysis: risk={risk:.0f}%, entry_speed={entry_spd}kph, "
                        f"fatigue={fatigue}, aggression={agg}, conditions={conditions}, tire_wear={tire_wear}%."
                    )
                hybrid_report(manual_txt, ai_txt)
                voice_button(ai_txt, "sr_hv")
        else:
            H("""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:300px;opacity:0.18;"><div style="font-size:40px;margin-bottom:12px;">⚠️</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:4px;
            color:#3D5060;">INPUT RISK PARAMETERS</div></div>""")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: SECTOR TIMING
# ─────────────────────────────────────────────────────────────────────────────
elif "Sector" in module:
    page_header("📈", "Sector Timing", "LAP TIME INTELLIGENCE · TREND ANALYSIS · CONSISTENCY ENGINE")
    mode_badge(mode)

    num_laps = st.slider("Session Laps", 3, 25, 12)
    input_cols = st.columns(min(num_laps, 6))
    lap_values = []
    for i in range(num_laps):
        with input_cols[i % 6]:
            v = st.number_input(
                f"L{i+1}",
                value=round(97 + random.uniform(-2, 5) - i * 0.1, 2),
                step=0.01, format="%.2f", key=f"st_lap_{i}",
            )
            lap_values.append(v)

    run_btn = st.button("▶ ANALYZE SESSION", key="st_run")

    if run_btn:
        best  = min(lap_values)
        worst = max(lap_values)
        avg   = np.mean(lap_values)
        std   = np.std(lap_values)
        cons  = max(0, round(100 - std * 15, 1))
        trend = np.polyfit(range(len(lap_values)), lap_values, 1)[0]
        pred_best = round(best - abs(trend) * 2 if trend < 0 else best - 0.25, 2)

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: metric_card(f"{best:.2f}s",     "BEST LAP",       "#00FF85")
        with c2: metric_card(f"{avg:.2f}s",      "SESSION AVG",    "#00F5FF")
        with c3: metric_card(f"{cons:.0f}%",     "CONSISTENCY",    "#FFB800")
        with c4: metric_card(f"{std:.3f}s",      "STD DEVIATION",  "#FF0033")
        with c5: metric_card(f"{pred_best:.2f}s","PREDICTED BEST", "#9D4EDD")

        divider()
        lap_df = pd.DataFrame({"Lap Time (s)": lap_values}, index=range(1, len(lap_values) + 1))
        st.line_chart(lap_df, color="#FF0033", height=230)

        if mode in ["🛠️ Manual", "🔥 Hybrid"]:
            divider()
            section_label("TELEMETRY ANALYSIS")
            trend_label = "IMPROVING" if trend < -0.05 else ("DEGRADING" if trend > 0.10 else "STABLE")
            trend_color = "#00FF85"   if trend < -0.05 else ("#FF0033" if trend > 0.10 else "#FFB800")
            radio_line(f"TREND: {trend_label} ({trend:+.3f}s/lap)", trend_color)
            radio_line(f"BEST→WORST DELTA: {worst-best:.2f}s — {'acceptable' if worst-best < 2 else 'high variance — investigate setup'}", "#7A8899")
            radio_line(f"STD DEV {std:.3f}s — {'elite repeatability' if std < 0.5 else ('competitive' if std < 1.0 else 'inconsistent — focus on braking repeatability')}", "#00F5FF")

        if mode == "🤖 AI":
            with st.spinner("Race engineer analyzing session data…"):
                resp = ai_response(
                    f"Analyze session: best_lap={best:.2f}s, avg={avg:.2f}s, "
                    f"std_dev={std:.3f}s, consistency={cons:.0f}%, "
                    f"trend={trend:+.3f}s/lap, total_laps={num_laps}."
                )
            engineer_feed(resp, "LAP ANALYSIS FEED")
            voice_button(resp, "st_voice")

        if mode == "🔥 Hybrid":
            manual_txt = (
                f"Best lap:      {best:.2f}s\n"
                f"Session avg:   {avg:.2f}s\n"
                f"Consistency:   {cons:.0f}%\n"
                f"Std deviation: {std:.3f}s\n"
                f"Trend:         {trend:+.3f}s/lap\n"
                f"Predicted best:{pred_best:.2f}s"
            )
            with st.spinner("AI fusion analysis…"):
                ai_txt = ai_response(
                    f"Analyze and prescribe improvements for this session: "
                    f"best={best:.2f}s, std={std:.3f}s, trend={trend:+.3f}/lap, "
                    f"consistency={cons:.0f}%, laps={num_laps}."
                )
            hybrid_report(manual_txt, ai_txt)
            voice_button(ai_txt, "st_hv")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: RIDER PROFILE
# ─────────────────────────────────────────────────────────────────────────────
elif "Rider" in module:
    page_header("🧾", "Rider Profile", "MotoGP-STYLE RIDER CARD · PERFORMANCE DNA · AI BIOGRAPHY")
    mode_badge(mode)

    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        section_label("RIDER DATA")
        r_name = st.text_input("Full Name",    "Marco Veltri")
        r_num  = st.number_input("Race No.",    1, 99, 33)
        r_nat  = st.text_input("Nationality",  "Italian")
        r_age  = st.number_input("Age",        16, 45, 24)
        r_exp  = st.number_input("Years Exp",   0, 25,  5)
        r_sp   = st.slider("Speed",         0, 100, 78)
        r_br   = st.slider("Braking",       0, 100, 72)
        r_co   = st.slider("Cornering",     0, 100, 74)
        r_cs   = st.slider("Consistency",   0, 100, 70)
        r_mn   = st.slider("Mental Str.",   0, 100, 67)
        run_btn= st.button("▶ GENERATE PROFILE", key="rp_run")

    with col_out:
        if run_btn:
            overall = round(np.mean([r_sp, r_br, r_co, r_cs, r_mn]), 1)
            tier = (
                "LEGEND"       if overall >= 88 else
                "ELITE"        if overall >= 75 else
                "PRO"          if overall >= 60 else
                "INTERMEDIATE" if overall >= 45 else
                "ROOKIE"
            )
            tier_colors = {
                "LEGEND":       "#00F5FF",
                "ELITE":        "#00F5FF",
                "PRO":          "#00FF85",
                "INTERMEDIATE": "#FFB800",
                "ROOKIE":       "#FF0033",
            }
            tc = tier_colors[tier]

            # Rider card
            H(f"""
            <div style="
              background:linear-gradient(135deg,#0C1420 0%,#101A28 50%,#140C1A 100%);
              border:1px solid rgba(255,255,255,0.08);
              border-top:3px solid #FF0033;
              border-radius:8px;
              padding:26px 30px;
              position:relative;overflow:hidden;
              margin-bottom:20px;
              box-shadow:0 8px 40px rgba(0,0,0,0.5);
            ">
              <div style="position:absolute;right:20px;top:14px;
                font-family:'Orbitron',monospace;font-size:72px;font-weight:900;
                color:rgba(255,0,51,0.06);line-height:1;">#{r_num}</div>
              <div style="position:absolute;bottom:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,transparent,rgba(0,245,255,0.2),transparent);"></div>

              <div style="font-family:'Orbitron',monospace;font-size:26px;font-weight:900;
                color:#fff;letter-spacing:2px;text-transform:uppercase;line-height:1;">
                {r_name}
              </div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                color:#3D5060;letter-spacing:2.5px;margin-top:6px;">
                {r_nat.upper()} · AGE {r_age} · {r_exp} YRS EXPERIENCE
              </div>

              <div style="display:flex;align-items:center;gap:14px;margin-top:18px;">
                <div style="
                  font-family:'Orbitron',monospace;font-size:10px;font-weight:700;
                  letter-spacing:2.5px;color:{tc};
                  background:{tc}18;border:1px solid {tc}55;
                  border-radius:4px;padding:4px 12px;
                ">{tier}</div>
                <div style="font-family:'Orbitron',monospace;font-size:26px;
                  color:{tc};font-weight:700;letter-spacing:1px;">
                  {overall:.0f}
                  <span style="font-size:12px;color:#3D5060;font-weight:400;">/100</span>
                </div>
              </div>
            </div>
            """)

            if mode in ["🛠️ Manual", "🔥 Hybrid"]:
                section_label("PERFORMANCE DNA")
                skill_bar("Speed",            r_sp, color="#FF0033")
                skill_bar("Braking",          r_br, color="#00F5FF")
                skill_bar("Cornering",        r_co, color="#FFB800")
                skill_bar("Consistency",      r_cs, color="#00FF85")
                skill_bar("Mental Strength",  r_mn, color="#9D4EDD")

            if mode == "🤖 AI":
                with st.spinner("Generating rider biography…"):
                    resp = ai_response(
                        f"Write a professional MotoGP rider biography: "
                        f"name={r_name}, nationality={r_nat}, age={r_age}, "
                        f"experience={r_exp}yrs, overall_rating={overall:.0f}/100, tier={tier}. "
                        f"Speed={r_sp}, Braking={r_br}, Cornering={r_co}. Max 150 words, journalist tone."
                    )
                engineer_feed(resp, "RIDER BIOGRAPHY FEED")
                voice_button(resp, "rp_voice")

            if mode == "🔥 Hybrid":
                manual_txt = (
                    f"Rider:       {r_name} #{r_num} ({r_nat})\n"
                    f"Tier:        {tier} | Overall: {overall:.0f}/100\n"
                    f"Speed: {r_sp} · Braking: {r_br} · Cornering: {r_co}\n"
                    f"Consistency: {r_cs} · Mental Strength: {r_mn}"
                )
                with st.spinner("AI generating biography…"):
                    ai_txt = ai_response(
                        f"Write a concise professional MotoGP biography for {r_name} "
                        f"({r_nat}, age {r_age}), rated {overall:.0f}/100, tier {tier}. "
                        f"Strongest: {'speed' if r_sp == max(r_sp,r_br,r_co) else 'braking' if r_br == max(r_sp,r_br,r_co) else 'cornering'}."
                    )
                hybrid_report(manual_txt, ai_txt)
                voice_button(ai_txt, "rp_hv")
        else:
            H("""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:300px;opacity:0.18;"><div style="font-size:40px;margin-bottom:12px;">🧾</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:4px;
            color:#3D5060;">ENTER RIDER DATA</div></div>""")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE: TRACK MASTERY
# ─────────────────────────────────────────────────────────────────────────────
elif "Track" in module:
    page_header("🏆", "Track Mastery", "CIRCUIT INTELLIGENCE · RACING LINE · BRAKING ZONES · SECTOR COACHING")
    mode_badge(mode)

    col_in, col_out = st.columns([1, 2], gap="large")

    with col_in:
        section_label("CIRCUIT PARAMETERS")
        circuit_name = st.text_input("Circuit Name",  "Mugello")
        circuit_type = st.selectbox("Track Character", [
            "High-Speed Power", "Technical/Slow", "Mixed Layout",
            "Street Circuit",   "Flowing High-Speed",
        ])
        circuit_len  = st.slider("Circuit Length (km)", 2.5, 7.0, 5.2, 0.1)
        num_corners  = st.slider("Number of Corners",     8,  22,  15)
        num_sectors  = st.slider("Sectors",                2,   6,   3)
        run_btn      = st.button("▶ GENERATE CIRCUIT BRIEF", key="tm_run")

    with col_out:
        if run_btn:
            est_lap = round(circuit_len * 21.5 + random.uniform(-4, 4), 1)

            c1, c2, c3, c4 = st.columns(4)
            with c1: metric_card(f"{circuit_len:.1f}km", "CIRCUIT LEN",  "#FF0033")
            with c2: metric_card(str(num_corners),        "CORNERS",      "#00F5FF")
            with c3: metric_card(str(num_sectors),        "SECTORS",      "#00FF85")
            with c4: metric_card(f"{est_lap:.0f}s",       "EST LAP TIME", "#FFB800")

            divider()

            knowledge = {
                "High-Speed Power": {
                    "line":   "Late apex at every corner — maximize exit drive velocity. Sacrifice entry to gain straight-line advantage.",
                    "braking":"200m/150m/100m marker discipline is non-negotiable. Trail brake into T1 complex. Full commitment on chicane braking.",
                    "corner": "Smooth, connected arcs at high lean angles. Body position aerodynamically optimized through fast sequences.",
                    "focus":  "Raw exit velocity and top-end speed — no braking timidity allowed.",
                },
                "Technical/Slow": {
                    "line":   "Early apex on hairpins to maximize drive out. Chicane geometry: late apex on second element for exit advantage.",
                    "braking":"Aggressive threshold braking into slow corners. Trail brake deep — weight transfer creates crucial rotation.",
                    "corner": "Short, sharp directional changes. Rear rotation on entry. Drive aggressively from every apex.",
                    "focus":  "Corner exit traction and acceleration — every tenth on following straight counts.",
                },
                "Mixed Layout": {
                    "line":   "Adapt technique per sector: late apex in fast sections, early rotation in slow corners.",
                    "braking":"Variable demands per zone — pre-brief each braking point with specific markers.",
                    "corner": "Highest mental workload circuit type. Data analysis between sessions is critical for optimization.",
                    "focus":  "Holistic circuit knowledge — no single sector defines the lap time.",
                },
                "Street Circuit": {
                    "line":   "Maximize curb usage and build pace methodically. Walls are unforgiving — build confidence progressively.",
                    "braking":"Add 12–15m to normal brake points in first session. Surface contamination increases stopping distances.",
                    "corner": "Reduced grip at track edges. Center of circuit offers cleaner rubber. Maintain 10% safety margin.",
                    "focus":  "Risk management first — no single lap justifies a wall contact.",
                },
                "Flowing High-Speed": {
                    "line":   "Connected arcs — flow state is everything. Each corner directly sets up the next. Rhythm defines lap time.",
                    "braking":"Minimal hard braking — smooth deceleration preserves momentum. Never disrupt the rhythm.",
                    "corner": "Maximum commitment and lean angle throughout. Bravery and fluidity directly translate to lap time.",
                    "focus":  "Rhythm, flow, and commitment — this circuit punishes hesitation.",
                },
            }
            intel = knowledge[circuit_type]

            if mode in ["🛠️ Manual", "🔥 Hybrid"]:
                section_label("CIRCUIT INTELLIGENCE")
                radio_line(f"RACING LINE:   {intel['line']}",    "#00F5FF")
                radio_line(f"BRAKING ZONES: {intel['braking']}", "#FF0033")
                radio_line(f"CORNERING:     {intel['corner']}",  "#FFB800")
                radio_line(f"SESSION FOCUS: {intel['focus']}",   "#00FF85")

                divider()
                section_label("SECTOR TIME TARGETS")
                sector_df = pd.DataFrame(
                    {"Target (s)": [round(est_lap / num_sectors + random.uniform(-2, 2), 1) for _ in range(num_sectors)]},
                    index=[f"Sector {i+1}" for i in range(num_sectors)],
                )
                st.bar_chart(sector_df, color="#00F5FF", height=200)

            if mode == "🤖 AI":
                with st.spinner("Circuit engineer analyzing…"):
                    resp = ai_response(
                        f"Provide advanced circuit coaching for {circuit_name}: "
                        f"type={circuit_type}, length={circuit_len}km, corners={num_corners}. "
                        "Include optimal racing line strategy, braking zone markers, cornering technique, "
                        "sector-specific coaching, and mental preparation cues."
                    )
                engineer_feed(resp, "CIRCUIT COACHING FEED")
                voice_button(resp, "tm_voice")

            if mode == "🔥 Hybrid":
                manual_txt = (
                    f"Circuit:     {circuit_name} ({circuit_len:.1f}km · {num_corners} corners)\n"
                    f"Type:        {circuit_type}\n"
                    f"Est. lap:    {est_lap:.0f}s\n"
                    f"Racing line: {intel['line']}\n"
                    f"Braking:     {intel['braking']}\n"
                    f"Focus:       {intel['focus']}"
                )
                with st.spinner("AI enhancing circuit brief…"):
                    ai_txt = ai_response(
                        f"Enhance circuit brief for {circuit_name}: type={circuit_type}, "
                        f"corners={num_corners}, length={circuit_len}km. "
                        "Add advanced engineering detail, mental preparation, setup correlation."
                    )
                hybrid_report(manual_txt, ai_txt)
                voice_button(ai_txt, "tm_hv")
        else:
            H("""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:300px;opacity:0.18;"><div style="font-size:40px;margin-bottom:12px;">🏆</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:4px;
            color:#3D5060;">ENTER CIRCUIT DETAILS</div></div>""")
