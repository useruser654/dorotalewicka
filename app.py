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
# SVG – OBWÓD (POWIĘKSZONY)
# =========================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
svg {{
    width: 100%;
    height: auto;
    display: block;
    margin: auto;
}}

path, line {{
    stroke: green;
    stroke-width: 5;
    fill: none;
}}

.label {{
    font-size: 15px;
    font-family: Arial;
}}

.symbol {{
    font-size: 18px;
    font-weight: bold;
    font-family: Arial;
}}
</style>
</head>

<body>
<svg viewBox="0 0 760 420">

    <!-- GŁÓWNY OBWÓD -->
    <path id="circuit" d="M160 70 H600 V350 H160 Z"/>

    <!-- ŹRÓDŁO NAPIĘCIA -->
    <line x1="160" y1="210" x2="160" y2="260"/>

    <line x1="138" y1="215" x2="182" y2="215" stroke="black" stroke-width="5"/>
    <line x1="146" y1="255" x2="174" y2="255" stroke="black" stroke-width="5"/>

    <text x="105" y="205" class="label">Źródło</text>
    <text x="102" y="285" class="label">{U:.1f} V</text>

    <!-- ODBICIE DO WOLTOMIERZA -->
    <line x1="160" y1="140" x2="300" y2="140"/>
    <line x1="160" y1="360" x2="300" y2="360"/>

    <!-- WOLTOMIERZ -->
    <circle cx="300" cy="250" r="26" fill="white" stroke="black"/>
    <text x="292" y="256" class="symbol">V</text>
    <text x="268" y="300" class="label">{U:.1f} V</text>

    <line x1="300" y1="140" x2="300" y2="224"/>
    <line x1="300" y1="276" x2="300" y2="360"/>

    <!-- REZYSTOR -->
    <rect x="600" y="220" width="56" height="110" fill="lightgray" stroke="black"/>
    <text x="620" y="210" class="symbol">R</text>
    <text x="598" y="360" class="label">{R:.0f} Ω</text>

    <!-- AMPEROMIERZ -->
    <circle cx="420" cy="70" r="26" fill="white" stroke="black"/>
    <text x="412" y="76" class="symbol">A</text>
    <text x="370" y="118" class="label">{I:.3f} A</text>

    <!-- KROPKI PRĄDU -->
    {dots_html}

</svg>
</body>
</html>
"""

# 👇 MNIEJSZY BOX, WIĘKSZA ANIMACJA
components.html(html_code, height=420)

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



