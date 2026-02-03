import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Prawo Ohma – symulacja", layout="centered")

st.title("⚡ Prawo Ohma – symulacja")
st.markdown("**Interaktywna symulacja przepływu prądu w zamkniętym obwodzie DC**")

# =========================
# PARAMETRY
# =========================
U = st.session_state.get("U", 20.0)
R = st.session_state.get("R", 150.0)

I = U / R if R != 0 else 0

# =========================
# PARAMETRY ANIMACJI
# =========================
if U == 0 or I == 0:
    dot_count = 0
    speed = 1
else:
    speed = min(I * 4, 14)
    dot_count = int(min(I * 30, 36))

# =========================
# KROPKI PRĄDU
# =========================
dots_html = ""
for i in range(dot_count):
    delay = i * (1 / dot_count)
    dots_html += f"""
    <circle r="6" fill="yellow">
        <animateMotion dur="{10/speed:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite">
            <mpath href="#circuit"/>
        </animateMotion>
    </circle>
    """

# =========================
# SVG – OBWÓD
# =========================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
svg {{
    width: 95%;
    height: 480px;
    display: block;
    margin: auto;
}}

path, line {{
    stroke: green;
    stroke-width: 4;
    fill: none;
}}

.label {{
    font-size: 14px;
    font-family: Arial;
}}

.symbol {{
    font-size: 16px;
    font-weight: bold;
    font-family: Arial;
}}
</style>
</head>

<body>
<svg viewBox="0 0 760 480">

    <!-- GŁÓWNY OBWÓD -->
    <path id="circuit" d="M180 80 H660 V380 H180 Z"/>

    <!-- ŹRÓDŁO NAPIĘCIA -->
    <line x1="180" y1="220" x2="180" y2="260"/>

    <!-- kreski źródła -->
    <line x1="160" y1="225" x2="200" y2="225" stroke="black" stroke-width="4"/>
    <line x1="168" y1="255" x2="192" y2="255" stroke="black" stroke-width="4"/>

    <text x="120" y="215" class="label">Źródło</text>
    <text x="118" y="285" class="label">{U:.1f} V</text>

    <!-- ODBICIE DO WOLTOMIERZA -->
    <line x1="180" y1="150" x2="300" y2="150"/>
    <line x1="180" y1="350" x2="300" y2="350"/>

    <!-- WOLTOMIERZ -->
    <circle cx="300" cy="250" r="24" fill="white" stroke="black"/>
    <text x="292" y="256" class="symbol">V</text>
    <text x="272" y="292" class="label">{U:.1f} V</text>

    <line x1="300" y1="150" x2="300" y2="226"/>
    <line x1="300" y1="274" x2="300" y2="350"/>

    <!-- REZYSTOR -->
    <rect x="640" y="230" width="48" height="100" fill="lightgray" stroke="black"/>
    <text x="652" y="220" class="symbol">R</text>
    <text x="630" y="350" class="label">{R:.0f} Ω</text>

    <!-- AMPEROMIERZ -->
    <circle cx="420" cy="80" r="24" fill="white" stroke="black"/>
    <text x="412" y="86" class="symbol">A</text>
    <text x="372" y="122" class="label">{I:.3f} A</text>

    <!-- KROPKI PRĄDU -->
    {dots_html}

</svg>
</body>
</html>
"""

components.html(html_code, height=500)

# =========================
# WYNIKI
# =========================
st.divider()
st.subheader("📊 Wartości w obwodzie")

col1, col2, col3 = st.columns(3)
col1.metric("Napięcie U", f"{U:.1f} V")
col2.metric("Opór R", f"{R:.0f} Ω")
col3.metric("Natężenie I", f"{I:.3f} A")

st.markdown(r"""
### Ω Prawo Ohma
Natężenie prądu (I) płynącego przez przewodnik jest wprost proporcjonalne do napięcia przyłożonego do jego końców oraz odwrotnie proporcjonalne do jego oporu.  Wzór: I = U / R  lub  U = I x R
""")

# =========================
# SUWAKI – NA DOLE
# =========================
st.divider()
st.subheader("🎛 Regulacja parametrów")

U = st.slider("Napięcie U [V]", 0.0, 300.0, U, step=1.0, key="U")
R = st.slider("Opór R [Ω]", 1.0, 500.0, R, step=1.0, key="R")



