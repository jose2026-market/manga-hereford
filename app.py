"""Manga Hereford: ficha de admisión para el jurado veterinario."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from src.branding import LOGO_RURAL, inyectar_css
from src.database import guardar_examen, guardar_foto, init_db, listar, obtener
from src.evaluacion import evaluar, fundamento, informe
from src.normativa import (
    CONSECUENCIAS,
    FUENTE_EXPO,
    FUENTE_EXPO_URL,
    FUENTE_PR,
    FUENTE_PR_URL,
    GRUPOS,
    MARCAS,
    MEDIA_RACIAL,
    TABLA_CE_PEDIGREE,
    TABLA_CE_PR,
    TOMAS,
)

st.set_page_config(
    page_title="Manga Hereford | Admisión",
    page_icon=":material/pets:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

init_db()
inyectar_css(st)
if LOGO_RURAL.exists():
    st.logo(str(LOGO_RURAL), size="large")

if "ficha" not in st.session_state:
    st.session_state.ficha = 1

FICHA = st.session_state.ficha


def clave(nombre: str) -> str:
    return f"{FICHA}_{nombre}"


st.title("Manga Hereford")
st.caption(
    "Admisión de vacas y toros en la manga, antes de la jura. "
    "Las fotos documentan lo que ves. El dictamen lo firmás vos."
)

with st.sidebar:
    st.subheader("Jurado")
    veterinario = st.text_input("Médico veterinario", placeholder="Nombre y matrícula")
    exposicion = st.text_input("Exposición", placeholder="Rural, fecha, localidad")
    st.caption("Los datos quedan en esta computadora.")

tab_manga, tab_norma, tab_informe = st.tabs(
    ["Manga", "Norma Hereford", "Informes"]
)

with tab_norma:
    st.subheader("Qué mira el jurado")
    st.markdown(
        "La admisión de las exposiciones Hereford la rige el **Reglamento General "
        "de Exposiciones 2026** de la Asociación Argentina Criadores de Hereford. "
        "El patrón de pelaje, estructura y diferencia mocho/astado que usa la "
        "inspección de registro está en el **Reglamento del Puro Registrado** "
        "(vigencia 23 de octubre de 2023)."
    )
    st.caption(FUENTE_EXPO)
    st.caption(FUENTE_EXPO_URL)
    st.caption(FUENTE_PR)
    st.caption(FUENTE_PR_URL)

    st.markdown("**Circunferencia escrotal mínima (Art. 26)**")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Edad Puro de Pedigree": texto,
                    "Mínimo (cm)": minimo,
                    "Categoría Puro Registrado en la misma fila": categoria,
                }
                for _desde, _hasta, minimo, texto, categoria in TABLA_CE_PEDIGREE
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "En Puro Registrado y VIP el mínimo se aplica por dentición, "
        "como en el anexo de categorías: diente de leche 34,5 cm; dos dientes 35,5 cm; "
        "cuatro y seis dientes 36,5 cm. El cuadro de pedigree empieza a los 15 meses."
    )
    ce_pr = pd.DataFrame(
        [
            {"Dentición": texto, "Mínimo (cm)": minimo}
            for minimo, texto in TABLA_CE_PR.values()
        ]
    )
    st.dataframe(ce_pr, hide_index=True, width="stretch")

    st.markdown("**Pelaje y cabeza**")
    st.write(MEDIA_RACIAL)
    st.markdown(
        "- **Mocho (Polled Hereford).** En el macho se aceptan tocos adheridos al cuero "
        "si no cambian la forma de la cabeza. En la hembra no se aceptan. "
        "Lo que exceda se marca astado (Reglamento PR, art. 5.3).\n"
        "- En los PR, si la variedad inscripta no coincide, vale la que constate "
        "el jurado de admisión (Art. 18.b).\n"
        "- Mancha negra, color ajeno y piel negra impiden la calificación PR o VIP "
        "(art. 5.2.6). En la exposición no están redactados como rechazo automático: "
        "el jurado elige rechazo o descalificación.\n"
        "- Prognatismo, fallas reproductivas, asimetría y enfermedad aguda son "
        "causales del Art. 19, puntos 1 a 6."
    )
    st.markdown("**Rechazo y descalificación (Art. 23)**")
    st.markdown(
        "- **Rechazado:** no compite y no sale a venta. Se aparta de los admitidos.\n"
        "- **Descalificado:** puede quedar en el corral, identificado, y salir a venta.\n"
        "- Serán rechazados, con esa palabra en el reglamento, los de identificación "
        "que no cierra, ocho dientes en PR o VIP, circunferencia escrotal bajo el mínimo, "
        "hembras que debían estar preñadas y están vacías o con anormalidad, "
        "falta de desarrollo, mal estado o indocilidad, y el uso de productos "
        "de embellecimiento no permitidos (Art. 19.7 a 19.13)."
    )
    st.markdown("**Preñez**")
    st.write(
        "Cuando la categoría la exige, al ingreso no puede tener menos de 60 días. "
        "El certificado veterinario previo no reemplaza la palpación del jurado (Art. 25)."
    )

with tab_informe:
    st.subheader("Informes de esta computadora")
    historial = listar()
    if historial.empty:
        st.caption("Todavía no hay admisiones guardadas.")
    else:
        st.dataframe(historial, hide_index=True, width="stretch")
        elegido = st.selectbox(
            "Ver informe",
            historial["id"].tolist(),
            format_func=lambda i: f"#{i} · {historial.loc[historial['id'] == i, 'rp'].iloc[0]} · {historial.loc[historial['id'] == i, 'dictamen'].iloc[0]}",
        )
        fila = obtener(int(elegido))
        if fila is not None:
            st.code(fila["informe"], language=None)
            st.download_button(
                "Descargar este informe",
                data=fila["informe"],
                file_name=f"admision-hereford-{fila['id']}-{fila['rp']}.txt",
                mime="text/plain",
            )
        csv = historial.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar listado CSV",
            data=csv,
            file_name="admisiones-hereford.csv",
            mime="text/csv",
        )

with tab_manga:
    st.subheader("Animal en la manga")
    c1, c2 = st.columns(2)
    with c1:
        rp = st.text_input("RP o caravana", key=clave("rp"), placeholder="Número de catálogo")
        cabana = st.text_input("Cabaña", key=clave("cabana"))
        sexo = st.radio("Sexo", ["Macho", "Hembra"], horizontal=True, key=clave("sexo"))
    with c2:
        registros = ["PP", "PR"] if sexo == "Macho" else ["PP", "PR", "VIP"]
        registro = st.radio(
            "Registro",
            registros,
            horizontal=True,
            key=clave(f"registro_{sexo}"),
        )
        variedad_inscripta = st.radio(
            "Variedad inscripta",
            ["Mocho", "Astado"],
            horizontal=True,
            key=clave("var_in"),
        )
        variedad_constatada = st.selectbox(
            "Variedad que constatás",
            ["Mocho limpio", "Tocos adheridos al cuero", "Astado"],
            key=clave("var_ok"),
        )

    d1, d2, d3 = st.columns(3)
    with d1:
        denticion = st.selectbox(
            "Dentición",
            ["No examinada", "DL", "2D", "4D", "6D", "8D"],
            format_func=lambda x: {
                "No examinada": "No examinada",
                "DL": "Diente de leche",
                "2D": "Dos dientes",
                "4D": "Cuatro dientes",
                "6D": "Seis dientes",
                "8D": "Ocho dientes",
            }[x],
            key=clave("dientes"),
            help="Diente nacido es el que ya cortó encía (Art. 18.d).",
        )
    with d2:
        edad = st.number_input(
            "Edad (meses)",
            min_value=0,
            max_value=240,
            value=None,
            step=1,
            key=clave("edad"),
            placeholder="Ej. 22",
        )
    with d3:
        peso = st.number_input(
            "Peso (kg)",
            min_value=0.0,
            max_value=1600.0,
            value=None,
            step=1.0,
            key=clave("peso"),
            placeholder="Opcional",
        )

    if sexo == "Macho":
        ce = st.number_input(
            "Circunferencia escrotal (cm)",
            min_value=0.0,
            max_value=60.0,
            value=None,
            step=0.1,
            format="%.1f",
            key=clave("ce"),
            placeholder="Medida en la manga",
        )
        prenez_exigida = "No corresponde"
        prenez_constatada = "No constatada"
    else:
        ce = None
        e1, e2 = st.columns(2)
        with e1:
            prenez_exigida = st.selectbox(
                "Qué pide la categoría",
                [
                    "No corresponde",
                    "Vacía normal o preñada",
                    "Preñez de 60 días o más",
                    "Preñada o parida",
                    "Parida con cría al pie",
                ],
                key=clave("exige"),
            )
        with e2:
            prenez_constatada = st.selectbox(
                "Qué palpás",
                [
                    "No constatada",
                    "Vacía, genitales normales",
                    "Preñada de 60 días o más",
                    "Preñada de menos de 60 días",
                    "Parida con cría",
                    "Anormalidad genital palpable",
                ],
                key=clave("palpa"),
            )

    st.subheader("Fotos de lo que estás mirando")
    st.caption(
        "Sacá una foto por región. La ficha no clasifica la imagen: "
        "deja constancia y te muestra qué confrontar con la norma."
    )
    fotos: dict[str, bytes] = {}
    for toma, titulo, ayuda in TOMAS:
        with st.expander(titulo):
            st.caption(ayuda)
            camara = st.camera_input("Tomar foto", key=clave(f"cam_{toma}"))
            archivo = st.file_uploader(
                "O elegir de la galería",
                type=["jpg", "jpeg", "png", "webp"],
                key=clave(f"file_{toma}"),
            )
            elegido = archivo or camara
            if elegido is not None:
                fotos[toma] = elegido.getvalue()

    st.subheader("Lo que constatás")
    st.caption("Marcá solo lo que ves. Lo que no marques queda como no observado en esa causal.")
    marcas: list[str] = []
    for grupo in GRUPOS:
        items = [
            item
            for item in MARCAS
            if item["grupo"] == grupo
            and sexo in item["sexos"]
            and (not item.get("registros") or registro in item["registros"])
        ]
        if not items:
            continue
        st.markdown(f"**{grupo}**")
        for item in items:
            if st.checkbox(item["etiqueta"], key=clave(item["id"])):
                marcas.append(item["id"])

    datos = {
        "exposicion": exposicion.strip(),
        "veterinario": veterinario.strip(),
        "rp": rp.strip(),
        "cabana": cabana.strip(),
        "sexo": sexo,
        "registro": registro,
        "variedad_inscripta": variedad_inscripta,
        "variedad_constatada": variedad_constatada,
        "denticion": denticion,
        "edad_meses": None if edad is None else int(edad),
        "ce_cm": None if ce is None else float(ce),
        "prenez_exigida": prenez_exigida,
        "prenez_constatada": prenez_constatada,
        "peso_kg": None if peso is None else float(peso),
    }
    resultado = evaluar(datos, marcas)

    st.subheader("Dictamen")
    if resultado.ce_minimo is not None:
        st.metric(
            "Mínimo de circunferencia para esta fila",
            f"{resultado.ce_minimo:.1f} cm",
            help=resultado.ce_referencia,
        )
    elif sexo == "Macho":
        st.caption(resultado.ce_referencia)

    st.info(f"Sugerencia de la ficha: **{resultado.sugerido}**. {CONSECUENCIAS[resultado.sugerido]}")
    if resultado.sugerido == "Rechazado" and any(a.nivel == "causal" for a in resultado.alertas) and not any(
        a.nivel == "rechazo" for a in resultado.alertas
    ):
        st.caption(
            "Esta sugerencia sale de una causal en la que el reglamento te deja "
            "rechazar o descalificar. Podés cambiar el dictamen."
        )

    for alerta in resultado.alertas:
        texto = f"**{alerta.titulo}.** {alerta.detalle} _{alerta.norma}_"
        if alerta.nivel == "rechazo":
            st.error(texto)
        elif alerta.nivel == "causal":
            st.warning(texto)
        elif alerta.nivel == "observacion":
            st.warning(texto)
        else:
            st.caption(texto)

    if resultado.incompleto:
        st.caption("Antes de guardar: " + " ".join(resultado.incompleto))

    borrador = fundamento(resultado.alertas, resultado.sugerido)
    if st.session_state.get(clave("base")) != borrador:
        st.session_state[clave("base")] = borrador
        st.session_state[clave("fundamento")] = borrador

    texto = st.text_area(
        "Fundamento para el comisario (Art. 27)",
        key=clave("fundamento"),
        height=180,
    )
    dictamen = st.radio(
        "Dictamen del jurado",
        list(CONSECUENCIAS),
        key=clave("dictamen"),
        index=None,
    )
    if dictamen:
        st.caption(CONSECUENCIAS[dictamen])
    confirmo = st.checkbox(
        "Confirmo que este dictamen es el del jurado de admisión",
        key=clave("confirmo"),
    )

    if st.button("Guardar admisión", type="primary", key=clave("guardar")):
        if not rp.strip():
            st.error("Falta el RP o la caravana.")
        elif resultado.incompleto:
            st.error("Completá las mediciones que el reglamento pide antes de cerrar.")
        elif dictamen is None:
            st.error("Elegí el dictamen.")
        elif not confirmo:
            st.error("Confirmá el dictamen para dejar constancia.")
        else:
            sello = f"{FICHA}_{rp.strip()}"
            rutas = []
            for toma, contenido in fotos.items():
                rutas.append(guardar_foto(sello, toma, contenido))
            datos_guardar = {
                **datos,
                "ce_minimo": resultado.ce_minimo,
                "marcas": ", ".join(marcas),
                "sugerido": resultado.sugerido,
                "dictamen": dictamen,
                "fundamento": texto,
            }
            texto_informe = informe(
                datos,
                resultado,
                dictamen,
                texto,
                list(fotos),
            )
            examen_id = guardar_examen(datos_guardar, texto_informe, " | ".join(rutas))
            st.session_state["ultimo_informe"] = texto_informe
            st.session_state["ultimo_id"] = examen_id
            st.success(f"Admisión #{examen_id} guardada: {dictamen}.")

    if st.session_state.get("ultimo_informe") and st.session_state.get("ultimo_id"):
        st.download_button(
            "Descargar informe",
            data=st.session_state["ultimo_informe"],
            file_name=f"admision-hereford-{st.session_state['ultimo_id']}.txt",
            mime="text/plain",
            key=clave("descarga"),
        )

    if st.button("Otro animal", key=clave("otro")):
        st.session_state.ficha += 1
        st.session_state.pop("ultimo_informe", None)
        st.session_state.pop("ultimo_id", None)
        st.rerun()
