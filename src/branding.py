"""Pantalla de manga: letra grande, pocos colores, usable al sol y en el celular."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
LOGO_RURAL = ASSETS / "logo-sociedad-rural-san-luis.png"

CSS = """
.block-container {
  padding-top: 0.6rem;
  padding-bottom: 2.4rem;
  max-width: 760px;
}
div.stButton > button {
  min-height: 3rem;
  font-weight: 700;
}
/* Logo de la Sociedad Rural, margen izquierdo superior, también con la barra cerrada. */
[data-testid="stSidebarHeader"] img,
[data-testid="stHeader"] img,
[data-testid="stLogo"] img {
  height: 52px !important;
  width: 52px !important;
  object-fit: contain;
}
@media (max-width: 700px) {
  .block-container {
    padding-left: 0.7rem;
    padding-right: 0.7rem;
  }
  [data-testid="stSidebarHeader"] img,
  [data-testid="stHeader"] img,
  [data-testid="stLogo"] img {
    height: 44px !important;
    width: 44px !important;
  }
}
"""


def inyectar_css(st) -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
