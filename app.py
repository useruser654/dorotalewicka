import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Prawo Ohma – symulacja", layout="centered")

st.title("⚡ Prawo Ohma – symulacja")
st.markdown("**Interaktywna symulacja przepływu prądu w zamkniętym obwodzie DC**")

# =========================
# DOMYŚLNE WARTOŚCI
# =========================
U = st.session_state.get("U", 20.0)
R = st.session_state.get("R", 150.0)

I = U / R if R != 0 else 0

# =========================
# PARAMETRY ANIMACJI
# =========================
speed = max(0.6, min(I * 5, 10))
dot_count = int(max(4, min(I * 30, 20)))

# =========================
# ANIMACJA – OBWÓD
# =========================
dots_html = ""
for i in range(dot_count):
    delay = i * (1 / dot_count)
    dots_html += f"""
    <circle r="5" class="dot">
        <animateMotion dur="{10/speed:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite">
            <mpath href="#circuit"/>
        </animateMotion>
    </circle>
    """

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
svg {{
    width: 100%;
    height: 320px;
}}

path {{
    stroke: green;
    stroke-width: 4;
    fill: none;
}}

.dot {{
    fill: yellow;
}}

.label {{
    font-size: 12px;
    font-family: Arial;
}}
</style>
</head>

<body>
<svg viewBox="0 0 600 320">

    <!-- Obwód -->
    <path id="circuit" d="M120 60 H500 V260 H120 Z"/>

    <!-- Źródło napięcia -->
    <line x1="120" y1="140" x2="120" y2="180" stroke="black" stroke-width="4"/>
    <text x="95" y="135" class="label">Źródło U</text>

    <!-- Woltomierz -->
    <circle cx="170" cy="160" r="18" fill="white" stroke="black"/>
    <text x="162" y="165" class="label">V</text>
    <text x="150" y="190" class="label">{U:.1f} V</text>

    <!-- Rezystor -->
    <rect x="480" y="130" width="40" height="60" fill="lightgray" stroke="black"/>
    <text x="483" y="125" class="label">R</text>

    <!-- Amperomierz -->
    <circle cx="310" cy="60" r="18" fill="white" stroke="black"/>
    <text x="302" y="65" class="label">A</text>
    <text x="280" y="90" class="label">{I:.3f} A</text>

    <!-- Kropki prądu -->
    {dots_html}

</svg>
</body>
</html>
"""

components.html(html_code, height=340)

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

U = st.slider("Napięcie U [V]", 0.0, 50.0, U, step=0.5, key="U")
R = st.slider("Opór R [Ω]", 1.0, 500.0, R, step=1.0, key="R")
