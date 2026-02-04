import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Prawo Ohma – symulacja", layout="centered")

# =========================
# GLOBALNE STYLIZACJE
# =========================
st.markdown("""
<style>
.block-container { padding-top: 1.4rem !important; }
span[data-testid="stSliderValue"] { display: none; }
.bold-metric { font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# =========================
# TYTUŁY I LEGENDA
# =========================
st.markdown("<h1 style='text-align:center; margin-bottom:4px;'>⚡ Prawo Ohma ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:600; margin-top:0;'>Interaktywna symulacja przepływu prądu stałego w zamkniętym obwodzie DC</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:0.95rem; margin-top:-6px;'><b>A</b> – amperomierz &nbsp;&nbsp;|&nbsp;&nbsp; <b>V</b> – woltomierz &nbsp;&nbsp;|&nbsp;&nbsp; <b>R</b> – rezystor</p>", unsafe_allow_html=True)

# =========================
# DOMYŚLNE WARTOŚCI / SESSION_STATE
# =========================
if "U" not in st.session_state: st.session_state.U = 20.0
if "R" not in st.session_state: st.session_state.R = 150.0
if "prev_U" not in st.session_state: st.session_state.prev_U = st.session_state.U
if "prev_R" not in st.session_state: st.session_state.prev_R = st.session_state.R

U = st.session_state.U
R = st.session_state.R
I = U / R if R != 0 else 0

# =========================
# PARAMETRY DOTÓW PRĄDU
# =========================
if U == 0 or I == 0:
    dot_count = 0
    speed = 1
else:
    speed = min(I * 4, 12)
    dot_count = int(min(I * 25, 25))

dots_html = ""
for i in range(dot_count):
    delay = i * (1 / dot_count)
    dots_html += f"""
    <circle r="5.5" fill="yellow">
        <animateMotion dur="{10/speed:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite">
            <mpath href="#circuit"/>
        </animateMotion>
    </circle>
    """

# =========================
# PULSOWANIE AMPEROMIERZA I "TĘTNO PRĄDU"
# =========================
pulse_js = ""
if U != st.session_state.prev_U or R != st.session_state.prev_R:
    pulse_js = """
    const amp = document.getElementById("ampermeter");
    const fill = document.getElementById("amp-fill");
    amp.animate([
        { r: "20" },
        { r: "22" },
        { r: "20" },
        { r: "22" },
        { r: "20" }
    ], {
        duration: 2000,
        iterations: 1,
        easing: "ease-in-out"
    });
    fill.animate([
        { opacity: 0 },
        { opacity: 0.35 },
        { opacity: 0 },
        { opacity: 0.35 },
        { opacity: 0 }
    ], {
        duration: 2000,
        iterations: 1,
        easing: "ease-in-out"
    });
    """
st.session_state.prev_U = U
st.session_state.prev_R = R

# =========================
# SVG – OBWÓD Z AMPEROMIERZEM I TĘTNEM
# =========================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
svg {{ width: 100%; height: 360px; }}
path, line {{ stroke: green; stroke-width: 4.5; fill: none; }}
.label {{ font-size: 14px; font-family: Arial; }}
.symbol {{ font-size: 15px; font-family: Arial; font-weight: bold; }}
</style>
</head>

<body>
<svg viewBox="48 26 544 291">

    <path id="circuit" d="M140 60 H540 V300 H140 Z"/>

    <line x1="140" y1="160" x2="140" y2="200" stroke="black"/>
    <line x1="120" y1="165" x2="160" y2="165" stroke="black" stroke-width="4.5"/>
    <line x1="130" y1="195" x2="150" y2="195" stroke="black" stroke-width="4.5"/>
    <text x="90" y="155" class="label">Źródło</text>

    <line x1="140" y1="120" x2="220" y2="120"/>
    <line x1="140" y1="240" x2="220" y2="240"/>

    <!-- Woltomierz -->
    <circle cx="220" cy="180" r="20" fill="white" stroke="black"/>
    <text x="212" y="186" class="symbol">V</text>
    <text x="190" y="214" class="label">{U:.1f} V</text>
    <line x1="220" y1="120" x2="220" y2="160"/>
    <line x1="220" y1="200" x2="220" y2="240"/>

    <!-- Rezystor -->
    <rect x="520" y="145" width="45" height="75" fill="lightgray" stroke="black"/>
    <text x="540" y="185" class="symbol">R</text>
    <text x="512" y="240" class="label">{R:.0f} Ω</text>

    <!-- Amperomierz -->
    <circle id="ampermeter" cx="340" cy="60" r="20" fill="white" stroke="black"/>
    <circle id="amp-fill" cx="340" cy="60" r="15" fill="red" opacity="0"/>
    <text x="332" y="66" class="symbol">A</text>
    <text x="300" y="96" class="label">{I:.3f} A</text>

    {dots_html}

</svg>
<script>
{pulse_js}
</script>
</body>
</html>
"""

# =========================
# ANIMACJA
# =========================
components.html(html_code, height=360)

# =========================
# PANEL STEROWANIA POD ANIMACJĄ
# =========================
st.markdown("<h3 style='text-align:center; margin-top:6px;'>🎛️ Panel sterowania 🎛️</h3>", unsafe_allow_html=True)

# Napięcie U
st.markdown("**⚡ Napięcie U [V]**")
st.markdown(f"<div style='color:red; font-weight:700; margin-top:-6px;'>{U:.1f} V</div>", unsafe_allow_html=True)
U = st.slider("", 0.0, 600.0, U, step=1.0, key="U")

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# Opór R - suwaki podniesione bliżej wartości
st.markdown("**Opór R [Ω]**")
st.markdown(f"<div style='color:red; font-weight:700; margin-top:-17px; margin-bottom:-16px;'>{R:.0f} Ω</div>", unsafe_allow_html=True)
R = st.slider("", 1.0, 500.0, R, step=1.0, key="R")

# =========================
# WYNIKI – wyśrodkowany nagłówek i pogrubiony tylko napis "Natężenie I"
# =========================
st.markdown("<h3 style='text-align:center; margin-top:10px;'>📊 Wartości w obwodzie 📊</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("**Natężenie I**", f"{I:.3f} A")  # tylko napis pogrubiony
col2.metric("Napięcie U", f"{U:.1f} V")
col3.metric("Opór R", f"{R:.0f} Ω")

# =========================
# WZORY PRAWA OHMA
# =========================
st.markdown("""
<h3>Prawo Ohma</h3>
<p style="white-space: nowrap;">
Natężenie prądu (I) jest wprost proporcjonalne do napięcia (U) oraz odwrotnie proporcjonalne do oporu (R).
</p>
<p><b>Wzory:</b><br>
I = U / R<br>
U = I · R
</p>
""", unsafe_allow_html=True)
