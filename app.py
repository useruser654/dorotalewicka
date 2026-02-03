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
    speed = min(I * 4, 12)
    dot_count = int(min(I * 25, 30))

# =========================
# KROPKI PRĄDU
# =========================
dots_html = ""
for i in range(dot_count):
    delay = i * (1 / dot_count)
    dots_html += f"""
    <circle r="5" fill="yellow">
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
    width: 100%;
    height: 420px;
}}

path, line {{
    stroke: green;
    stroke-width: 4;
    fill: none;
}}

.label {{
    font-size: 13px;
    font-family: Arial;
}}
</style>
</head>

<body>
<svg viewBox="0 0 700 420">

    <!-- GŁÓWNY OBWÓD -->
    <path id="circuit" d="M160 70 H600 V340 H160 Z"/>

    <!-- ŹRÓDŁO NAPIĘCIA (SYMBOL DC) -->
    <!-- przewody -->
    <line x1="160" y1="180" x2="160" y2="220"/>

    <!-- kreski źródła -->
    <line x1="145" y1="185" x2="175" y2="185" stroke="black" stroke-width="4"/>
    <line x1="150" y1="215" x2="170" y2="215" stroke="black" stroke-width="4"/>

    <text x="110" y="175" class="label">Źródło</text>
    <text x="108" y="240" class="label">{U:.1f} V</text>

    <!-- ODBICIE DO WOLTOMIERZA -->
    <line x1="160" y1="130" x2="260" y2="130"/>
    <line x1="160" y1="290" x2="260" y2="290"/>

    <!-- WOLTOMIERZ (RÓWNOLEGLE) -->
    <circle cx="260" cy="210" r="20" fill="white" stroke="black"/>
    <text x="252" y="215" class="label">V</text>
    <text x="235" y="245" class="label">{U:.1f} V</text>

    <line x1="260" y1="130" x2="260" y2="190"/>
    <line x1="260" y1="230" x2="260" y2="290"/>

    <!-- REZYSTOR -->
    <rect x="580" y="190" width="40" height="80" fill="lightgray" stroke="black"/>
    <text x="582" y="180" class="label">R</text>
    <text x="570" y="290" class="label">{R:.0f} Ω</text>

    <!-- AMPEROMIERZ -->
    <circle cx="380" cy="70" r="20" fill="white" stroke="black"/>
    <text x="372" y="75" class="label">A</text>
    <text x="340" y="110" class="label">{I:.3f} A</text>

    <!-- KROPKI PRĄDU -->
    {dots_html}

</svg>
</body>
</html>
"""

components.html(html_code, height=440)

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
### Prawo Ohma
\[
I = \frac{U}{R}
\]
""")

# =========================
# SUWAKI – NA DOLE
# =========================
st.divider()
st.subheader("🎛 Regulacja parametrów")

U = st.slider("Napięcie U [V]", 0.0, 300.0, U, step=1.0, key="U")
R = st.slider("Opór R [Ω]", 1.0, 500.0, R, step=1.0, key="R")


