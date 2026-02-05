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

div[data-testid="stTextInput"] input {
    color: red;
    font-weight: 700;
}

div[data-testid="stTextInput"] {
    margin-top: -12px;
    margin-bottom: -8px;
}

div[data-testid="stSlider"] {
    margin-top: -6px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TYTUŁY I LEGENDA
# =========================
st.markdown("<h1 style='text-align:center; margin-bottom:4px;'>⚡ Prawo Ohma ⚡</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; font-weight:600; margin-top:0;'>"
    "Interaktywna symulacja przepływu prądu stałego w zamkniętym obwodzie DC</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:0.95rem; margin-top:-6px;'>"
    "<b>A</b> – amperomierz &nbsp;|&nbsp; "
    "<b>V</b> – woltomierz &nbsp;|&nbsp; "
    "<b>R</b> – rezystor</p>",
    unsafe_allow_html=True
)

# =========================
# SESSION STATE
# =========================
if "U" not in st.session_state: st.session_state.U = 20.0
if "R" not in st.session_state: st.session_state.R = 150.0
if "U_text" not in st.session_state: st.session_state.U_text = f"{st.session_state.U:.2f}"
if "R_text" not in st.session_state: st.session_state.R_text = f"{st.session_state.R:.2f}"

U = st.session_state.U
R = st.session_state.R
I = U / R if R != 0 else 0

# =========================
# KROPKI PRĄDU
# =========================
if U == 0 or I == 0:
    dot_count, speed = 0, 1
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
# PULS AMPEROMIERZA
# =========================
pulse_js = ""
if U != st.session_state.prev_U or R != st.session_state.prev_R:
    pulse_js = """
    const amp = document.getElementById("ampermeter");
    const fill = document.getElementById("amp-fill");
    amp.animate([{r:"20"},{r:"22"},{r:"20"}], {duration:1200});
    fill.animate([{opacity:0},{opacity:0.35},{opacity:0}], {duration:1200});
    """
st.session_state.prev_U = U
st.session_state.prev_R = R

# =========================
# SVG – OBWÓD
# =========================
html_code = f"""
<svg viewBox="48 26 544 291" style="width:100%; height:360px">
<path id="circuit" d="M140 60 H540 V300 H140 Z"
      stroke="green" stroke-width="4.5" fill="none"/>

<line x1="140" y1="160" x2="140" y2="200" stroke="black" stroke-width="4.5"/>
<line x1="120" y1="165" x2="160" y2="165" stroke="black" stroke-width="4.5"/>
<line x1="130" y1="195" x2="150" y2="195" stroke="black" stroke-width="4.5"/>

<line x1="140" y1="120" x2="220" y2="120" stroke="green" stroke-width="4.5"/>
<line x1="140" y1="240" x2="220" y2="240" stroke="green" stroke-width="4.5"/>

<circle cx="220" cy="180" r="20" fill="white" stroke="black"/>
<text x="212" y="186" font-weight="bold">V</text>
<text x="190" y="214">{U:.1f} V</text>
<line x1="220" y1="120" x2="220" y2="160" stroke="green" stroke-width="4.5"/>
<line x1="220" y1="200" x2="220" y2="240" stroke="green" stroke-width="4.5"/>

<rect x="520" y="145" width="45" height="75" fill="#ddd" stroke="black"/>
<text x="540" y="185" font-weight="bold">R</text>
<text x="512" y="240">{R:.0f} Ω</text>

<circle id="ampermeter" cx="340" cy="60" r="20" fill="white" stroke="black"/>
<circle id="amp-fill" cx="340" cy="60" r="15" fill="red" opacity="0"/>
<text x="332" y="66" font-weight="bold">A</text>
<text x="300" y="96">{I:.3f} A</text>

{dots_html}
<script>{pulse_js}</script>
</svg>
"""

components.html(html_code, height=360)

# =========================
# FUNKCJE SYNCHRONIZACJI
# =========================
def update_U_from_text():
    try:
        v = round(float(st.session_state.U_text.replace(",", ".")), 2)
        if 0 <= v <= 600:
            st.session_state.U = v
            st.session_state.U_text = f"{v:.2f}"
    except:
        pass

def update_R_from_text():
    try:
        v = round(float(st.session_state.R_text.replace(",", ".")), 2)
        if 1 <= v <= 500:
            st.session_state.R = v
            st.session_state.R_text = f"{v:.2f}"
    except:
        pass

def update_U_from_slider():
    st.session_state.U_text = f"{st.session_state.U:.2f}"

def update_R_from_slider():
    st.session_state.R_text = f"{st.session_state.R:.2f}"

# =========================
# PANEL STEROWANIA
# =========================
st.markdown("<h3 style='text-align:center;'>🎛️ Panel sterowania 🎛️</h3>", unsafe_allow_html=True)

# --- NAPIĘCIE ---
st.markdown("<div style='font-weight:700'>⚡ Napięcie U [V]</div>", unsafe_allow_html=True)

st.text_input(
    "",
    key="U_text",
    on_change=update_U_from_text
)

st.markdown(
    "<div style='text-align:right; font-size:0.8rem; color:black;'>"
    "przesuń suwak lub wprowadź wartość do dwóch miejsc po przecinku i zatwierdź enterem"
    "</div>",
    unsafe_allow_html=True
)

st.slider(
    "",
    0.0,
    600.0,
    key="U",
    step=0.01,
    on_change=update_U_from_slider
)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# --- OPÓR ---
st.markdown("<div style='font-weight:700'>🚧 Opór R [Ω]</div>", unsafe_allow_html=True)

st.text_input(
    "",
    key="R_text",
    on_change=update_R_from_text
)

st.markdown(
    "<div style='text-align:right; font-size:0.8rem; color:black;'>"
    "przesuń suwak lub wprowadź wartość do dwóch miejsc po przecinku i zatwierdź enterem"
    "</div>",
    unsafe_allow_html=True
)

st.slider(
    "",
    1.0,
    500.0,
    key="R",
    step=0.01,
    on_change=update_R_from_slider
)

# =========================
# WARTOŚCI
# =========================
st.markdown("<h3 style='text-align:center;'>📊 Wartości w obwodzie 📊</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("**Natężenie I**", f"{I:.3f} A")
c2.metric("Napięcie U", f"{U:.1f} V")
c3.metric("Opór R", f"{R:.0f} Ω")

# ========================= 
# PRAWO OHMA 
# ========================= 
st.markdown(""" 
<h3>Prawo Ohma</h3> 
<p style="white-space: nowrap;"> 
Natężenie prądu (I) jest wprost proporcjonalne do napięcia (U) oraz odwrotnie proporcjonalne do oporu (R). 
<br><b>Wzory:</b><br> 
I = U / R<br> 
U = I · R 
</p> 
""", unsafe_allow_html=True)
