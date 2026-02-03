import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Prawo Ohma – symulacja", layout="centered")

st.title("⚡ Prawo Ohma – symulacja")
st.markdown("Interaktywna symulacja przepływu prądu w zamkniętym obwodzie (DC)")

# --- SUWAKI ---
U = st.slider("Napięcie U [V]", 0.0, 50.0, 20.0, step=0.5)
R = st.slider("Opór R [Ω]", 1.0, 500.0, 150.0, step=1.0)

# --- OBLICZENIA ---
I = U / R if R != 0 else 0

st.divider()

st.subheader("🔌 Amperomierz")
st.metric("Natężenie prądu I", f"{I:.3f} A")

st.markdown(r"""
### Prawo Ohma
\[
I = \frac{U}{R}
\]
""")

# --- PARAMETR ANIMACJI ---
# Im większy prąd, tym szybszy ruch
speed = max(0.5, min(I * 5, 10))

# --- ANIMACJA HTML + SVG ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
svg {{
    width: 100%;
    height: 300px;
}}

.dot {{
    fill: yellow;
    animation: flow {10/speed:.2f}s linear infinite;
}}

@keyframes flow {{
    0%   {{ offset-distance: 0%; }}
    100% {{ offset-distance: 100%; }}
}}

path {{
    stroke: green;
    stroke-width: 4;
    fill: none;
}}
</style>
</head>

<body>
<svg viewBox="0 0 600 300">

    <!-- Obwód -->
    <path id="circuit" d="M100 50 H500 V250 H100 Z"/>

    <!-- Rezystor -->
    <rect x="480" y="120" width="40" height="60" fill="lightgray" stroke="black"/>
    <text x="485" y="115" font-size="12">R</text>

    <!-- Źródło -->
    <line x1="100" y1="130" x2="100" y2="170" stroke="black" stroke-width="4"/>
    <text x="85" y="125" font-size="12">U</text>

    <!-- Amperomierz -->
    <circle cx="300" cy="50" r="20" fill="white" stroke="black"/>
    <text x="292" y="55" font-size="12">A</text>

    <!-- Kropki prądu -->
    <circle r="5" class="dot">
        <animateMotion dur="{10/speed:.2f}s" repeatCount="indefinite">
            <mpath href="#circuit"/>
        </animateMotion>
    </circle>

    <circle r="5" class="dot">
        <animateMotion dur="{10/speed:.2f}s" begin="0.5s" repeatCount="indefinite">
            <mpath href="#circuit"/>
        </animateMotion>
    </circle>

</svg>

<p><b>U = {U:.1f} V | R = {R:.0f} Ω | I = {I:.3f} A</b></p>
</body>
</html>
"""

components.html(html_code, height=350)
