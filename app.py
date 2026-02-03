import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Prawo Ohma – symulacja", layout="centered")

st.title("⚡ Prawo Ohma – symulacja")
st.markdown("**Interaktywna symulacja przepływu prądu w zamkniętym obwodzie DC**")

# =========================
# PARAMETRY (SESSION)
# =========================
U = st.session_state.get("U", 20.0)
R = st.session_state.get("R", 150.0)

I = U / R if R != 0 else 0

# =========================
# PARAMETRY ANIMACJI
# =========================
speed = max(0.6, min(I * 4, 12))
dot_count = int(max(5, min(I * 25, 25)))

# =========================
# KROPKI PRĄDU
# =========================
dots_html = ""
for i in range(dot_count):
    delay = i * (1 / dot_count)
    dots_html += f"""
    <circle r="4.5" fill="yellow">
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
    height: 340px;
}}

path, line {{
    stroke: green;
    stroke-width: 4;
    fill: none;
}}

.label {{
    font-size: 12px;
    font-family: Arial;
}}
</style>
</head>

<body>
<svg viewBox="0 0 640 340">

    <!-- GŁÓWNY OBWÓD -->
    <path id="circuit" d="M140 60 H540 V280 H140 Z"/>

    <!-- ŹRÓDŁO NAPIĘCIA -->
    <line x1="140" y1="150" x2="140" y2="190" stroke="black"/>
    <text x="100" y="145" class="label">Źródło U</text>

    <!-- ODBICIE DO WOLTOMIERZA (RÓWNOLEGLE) -->
    <line x1="140" y1="110" x2="220" y2="110"/>
    <line x1="140" y1="230" x2="220" y2="230"/>

    <!-- WOLTOMIERZ -->
    <circle cx="220" cy="170" r="18" fill="white" stroke="black"/>
    <text x="213" y="175" class="label">V</text>
    <text x="198" y="200" class="label">{U:.1f} V</text>

    <!-- POŁĄCZENIE POWROTNE -->
    <line x1="220" y1="110" x2="220" y2="152"/>
    <line x1="220" y1="188" x2="220" y2="230"/>

    <!-- REZYSTOR -->
    <rect x="520" y="150" width="40" height="60" fill="lightgray" stroke="black"/>
    <text x="523" y="145" class="label">R</text>

    <!-- AMPEROMIERZ -->
    <circle cx="340" cy="60" r="18" fill="white" stroke="black"/>
    <text x="332" y="65" class="label">A</text>
    <text x="305" y="90" class="label">{I:.3f} A</text>

    <!-- KROPKI PRĄDU -->
    {dots_html}

</svg>
</body>
</html>
"""

components.html(html_code, height=360)

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

