"""Traduce lo que constata el veterinario a un dictamen sugerido.

El sugerido no se guarda solo. El jurado lo confirma.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.normativa import MARCAS, TABLA_CE_PEDIGREE, TABLA_CE_PR, TABLA_PESO_PR

NIVEL_QUE_SUGIERE_RECHAZO = {"rechazo", "causal"}


@dataclass(frozen=True)
class Alerta:
    codigo: str
    nivel: str
    titulo: str
    detalle: str
    norma: str


@dataclass(frozen=True)
class Resultado:
    alertas: tuple[Alerta, ...]
    sugerido: str
    ce_minimo: float | None
    ce_referencia: str
    incompleto: tuple[str, ...]


def _marca(codigo: str) -> dict:
    for item in MARCAS:
        if item["id"] == codigo:
            return item
    raise KeyError(codigo)


def _alerta_marca(codigo: str) -> Alerta:
    item = _marca(codigo)
    return Alerta(item["id"], item["nivel"], item["etiqueta"], item["detalle"], item["norma"])


def minimo_circunferencia(
    registro: str,
    sexo: str,
    edad_meses: int | None,
    denticion: str | None,
) -> tuple[float | None, str]:
    """Devuelve (mínimo en cm, texto de la fila). None si esa categoría no tiene mínimo."""
    if sexo != "Macho":
        return None, "La circunferencia escrotal se exige a los machos (Art. 26)."
    if registro == "PP":
        if edad_meses is None:
            return None, "Falta la edad en meses para el cuadro de Pedigree."
        if edad_meses < 15:
            return None, "El cuadro del Art. 26 empieza a los 15 meses. Esta edad no tiene mínimo en ese cuadro."
        for desde, hasta, minimo, texto, _categoria_pr in TABLA_CE_PEDIGREE:
            if desde <= edad_meses <= hasta:
                return minimo, texto
        return None, "Edad fuera del cuadro del Art. 26."
    if registro in {"PR", "VIP"}:
        fila = TABLA_CE_PR.get(denticion or "")
        if fila is None:
            if denticion == "8D":
                return None, "Ocho dientes no tiene categoría PR ni VIP (Art. 19.9)."
            return None, "Elegí la dentición para aplicar el mínimo de Puro Registrado."
        minimo, texto = fila
        return minimo, texto
    return None, "Registro sin cuadro de circunferencia."


def _bajo(medida: float, minimo: float) -> bool:
    return round(medida, 1) < round(minimo, 1)


def _variedad(sexo: str, inscripta: str, constatada: str) -> list[Alerta]:
    alertas: list[Alerta] = []
    norma = "Art. 18.b, Reglamento de Exposiciones 2026, y art. 5.3 del Reglamento PR"
    if constatada == "Tocos adheridos al cuero" and sexo == "Hembra":
        alertas.append(
            Alerta(
                "variedad_hembra_tocos",
                "observacion",
                "Hembra con tocos: no califica como mocha",
                "En hembras no se aceptan formaciones córneas inhibidas. Corresponde dejarla como astada. En el catálogo vale la variedad que constate el jurado.",
                norma,
            )
        )
    elif constatada == "Tocos adheridos al cuero" and sexo == "Macho" and inscripta == "Mocho":
        alertas.append(
            Alerta(
                "variedad_macho_tocos",
                "info",
                "Macho mocho con tocos adheridos al cuero",
                "Se aceptan en el macho si están adheridos al cuero y mantienen la cabeza típica del Polled Hereford. Si la deforman, es astado.",
                "Reglamento PR, art. 5.3.a",
            )
        )
    if inscripta == "Mocho" and constatada == "Astado":
        alertas.append(
            Alerta(
                "variedad_pasa_a_astado",
                "observacion",
                "Inscripto mocho y constatado astado",
                "Se corrige la variedad del catálogo. No es, por sí solo, un rechazo.",
                norma,
            )
        )
    if inscripta == "Astado" and constatada == "Mocho limpio":
        alertas.append(
            Alerta(
                "variedad_pasa_a_mocho",
                "observacion",
                "Inscripto astado y constatado mocho",
                "Se corrige la variedad del catálogo. No es, por sí solo, un rechazo.",
                norma,
            )
        )
    if inscripta == "Astado" and sexo == "Macho" and constatada == "Tocos adheridos al cuero":
        alertas.append(
            Alerta(
                "variedad_astado_con_tocos",
                "observacion",
                "Inscripto astado, con tocos",
                "Si los tocos cumplen el art. 5.3.a puede recategorizarse mocho. Si exceden, sigue astado. Vale lo que constate el jurado.",
                norma,
            )
        )
    return alertas


def _prenez(sexo: str, exigida: str, constatada: str) -> tuple[list[Alerta], list[str]]:
    alertas: list[Alerta] = []
    incompleto: list[str] = []
    if sexo != "Hembra" or exigida == "No corresponde":
        if sexo == "Hembra" and constatada == "Anormalidad genital palpable":
            alertas.append(_alerta_marca("anormalidad_genital"))
        return alertas, incompleto
    if constatada == "No constatada":
        incompleto.append("Falta palpar preñez y genitales (Art. 24 y Art. 25).")
        return alertas, incompleto

    vacia_o_corta = {
        "Vacía, genitales normales",
        "Preñada de menos de 60 días",
        "Anormalidad genital palpable",
    }
    if exigida == "Vacía normal o preñada":
        if constatada == "Anormalidad genital palpable":
            alertas.append(_alerta_marca("anormalidad_genital"))
        return alertas, incompleto

    if exigida in {"Preñez de 60 días o más", "Preñada o parida"} and constatada in vacia_o_corta:
        alertas.append(
            Alerta(
                "prenez_insuficiente",
                "rechazo",
                "No cumple la preñez que exige la categoría",
                "Si la categoría exige preñez, la hembra vacía, con menos de 60 días o con anormalidad genital palpable será rechazada. El dictamen del jurado prevalece sobre el certificado.",
                "Art. 19.11 y Art. 25, Reglamento de Exposiciones 2026",
            )
        )
        return alertas, incompleto

    if exigida == "Preñez de 60 días o más" and constatada == "Parida con cría":
        alertas.append(
            Alerta(
                "parida_en_categoria_preniez",
                "observacion",
                "Está parida y la categoría pide preñez",
                "Puede corresponder a la subdivisión de paridas (Art. 25). Definilo con el comisario antes de rechazarla.",
                "Art. 25, Reglamento de Exposiciones 2026",
            )
        )
    if exigida == "Parida con cría al pie" and constatada != "Parida con cría":
        if constatada == "Anormalidad genital palpable":
            alertas.append(_alerta_marca("anormalidad_genital"))
        alertas.append(
            Alerta(
                "sin_cria",
                "observacion",
                "La categoría es con cría al pie y no se constató la cría",
                "Puede no encuadrar en esa categoría. El pase de categoría lo define el comisario, no un rechazo automático.",
                "Art. 25 y Art. 30, Reglamento de Exposiciones 2026",
            )
        )
    return alertas, incompleto


def _denticion(registro: str, denticion: str | None) -> tuple[list[Alerta], list[str]]:
    alertas: list[Alerta] = []
    incompleto: list[str] = []
    if registro not in {"PR", "VIP"}:
        return alertas, incompleto
    if not denticion or denticion == "No examinada":
        incompleto.append("En PR y VIP la dentición define la categoría (Art. 18.d).")
        return alertas, incompleto
    if denticion == "8D":
        alertas.append(
            Alerta(
                "ocho_dientes",
                "rechazo",
                "Ocho dientes: no encuadra en las categorías PR o VIP",
                "Quien por su dentición no entra en diente de leche, dos, cuatro o seis dientes será rechazado. El ejemplo del reglamento es la boca llena.",
                "Art. 19.9, Reglamento de Exposiciones 2026",
            )
        )
    return alertas, incompleto


def _peso(registro: str, sexo: str, denticion: str | None, peso_kg: float | None) -> list[Alerta]:
    if registro != "PR" or peso_kg is None or not denticion:
        return []
    fila = TABLA_PESO_PR.get(denticion)
    if fila is None or sexo not in fila:
        return []
    minimo = fila[sexo]
    if peso_kg < minimo:
        return [
            Alerta(
                "peso_pr",
                "observacion",
                f"Peso por debajo del mínimo de marcación PR ({minimo} kg)",
                f"{fila['referencia']}. Ese mínimo es de la inspección de Puro Registrado, no un rechazo automático de la exposición.",
                "Reglamento PR, art. 5.2.1",
            )
        ]
    return []


def sugerir(alertas: tuple[Alerta, ...] | list[Alerta]) -> str:
    niveles = {a.nivel for a in alertas}
    if "rechazo" in niveles or "causal" in niveles:
        return "Rechazado"
    if "observacion" in niveles:
        return "Admitido con observación"
    return "Admitido"


def evaluar(datos: dict, marcas: set[str] | list[str]) -> Resultado:
    sexo = datos.get("sexo") or ""
    registro = datos.get("registro") or ""
    denticion = datos.get("denticion") or "No examinada"
    edad = datos.get("edad_meses")
    ce = datos.get("ce_cm")
    marcas_set = set(marcas)

    alertas: list[Alerta] = []
    incompleto: list[str] = []

    for item in MARCAS:
        if item["id"] not in marcas_set:
            continue
        if sexo not in item["sexos"]:
            continue
        registros = item.get("registros")
        if registros and registro not in registros:
            continue
        alertas.append(_alerta_marca(item["id"]))

    alertas.extend(
        _variedad(
            sexo,
            datos.get("variedad_inscripta") or "",
            datos.get("variedad_constatada") or "",
        )
    )

    extra, falta = _denticion(registro, denticion)
    alertas.extend(extra)
    incompleto.extend(falta)

    extra, falta = _prenez(
        sexo,
        datos.get("prenez_exigida") or "No corresponde",
        datos.get("prenez_constatada") or "No constatada",
    )
    alertas.extend(extra)
    incompleto.extend(falta)

    ce_minimo, ce_referencia = minimo_circunferencia(registro, sexo, edad, denticion)
    if sexo == "Macho" and registro == "PP" and edad is None:
        incompleto.append("Falta la edad en meses del toro de pedigree (Art. 26).")
    if ce_minimo is not None and ce is None:
        incompleto.append(f"Falta la circunferencia escrotal. Mínimo de esta fila: {ce_minimo:.1f} cm.")
    elif ce_minimo is not None and ce is not None and _bajo(float(ce), ce_minimo):
        alertas.append(
            Alerta(
                "ce_baja",
                "rechazo",
                f"Circunferencia escrotal {float(ce):.1f} cm, bajo el mínimo de {ce_minimo:.1f} cm",
                f"Fila aplicada: {ce_referencia}. Sin excepciones, el que no llega al mínimo será rechazado.",
                "Art. 19.10 y Art. 26, Reglamento de Exposiciones 2026",
            )
        )

    alertas.extend(_peso(registro, sexo, denticion, datos.get("peso_kg")))

    # Una misma causal no debe repetirse si la preñez ya la incorporó.
    vistos: set[str] = set()
    unicas: list[Alerta] = []
    for alerta in alertas:
        if alerta.codigo in vistos:
            continue
        vistos.add(alerta.codigo)
        unicas.append(alerta)

    return Resultado(
        alertas=tuple(unicas),
        sugerido=sugerir(unicas),
        ce_minimo=ce_minimo,
        ce_referencia=ce_referencia,
        incompleto=tuple(incompleto),
    )


def fundamento(alertas: tuple[Alerta, ...] | list[Alerta], sugerido: str) -> str:
    if not alertas:
        return "Sin causales marcadas. Pelaje, identificación y controles reproductivos dentro de lo examinado."
    lineas = [f"Sugerencia de la ficha: {sugerido}.", ""]
    for alerta in alertas:
        if alerta.nivel == "info":
            continue
        lineas.append(f"- {alerta.titulo}. {alerta.norma}.")
    lineas.append("")
    lineas.append("El dictamen lo firma el jurado de admisión.")
    return "\n".join(lineas)


def informe(datos: dict, resultado: Resultado, dictamen: str, texto_fundamento: str, fotos: list[str]) -> str:
    ce = datos.get("ce_cm")
    ce_txt = "sin medir" if ce is None else f"{float(ce):.1f} cm"
    if resultado.ce_minimo is not None:
        ce_txt += f" (mínimo {resultado.ce_minimo:.1f} cm, {resultado.ce_referencia})"
    tomas = ", ".join(fotos) if fotos else "sin fotos"
    lineas = [
        "INFORME DE ADMISIÓN — HEREFORD",
        "Herramienta de apoyo. El dictamen es del jurado de admisión (Art. 27).",
        "",
        f"Exposición: {datos.get('exposicion') or '—'}",
        f"Veterinario: {datos.get('veterinario') or '—'}",
        f"RP / caravana: {datos.get('rp') or '—'}",
        f"Cabaña: {datos.get('cabana') or '—'}",
        f"Sexo: {datos.get('sexo') or '—'}   Registro: {datos.get('registro') or '—'}",
        f"Variedad inscripta: {datos.get('variedad_inscripta') or '—'}",
        f"Variedad constatada: {datos.get('variedad_constatada') or '—'}",
        f"Dentición: {datos.get('denticion') or '—'}   Edad (meses): {datos.get('edad_meses') if datos.get('edad_meses') is not None else '—'}",
        f"Circunferencia escrotal: {ce_txt}",
        f"Peso: {datos.get('peso_kg') if datos.get('peso_kg') is not None else '—'} kg",
        f"Preñez exigida: {datos.get('prenez_exigida') or '—'}",
        f"Preñez constatada: {datos.get('prenez_constatada') or '—'}",
        f"Fotos: {tomas}",
        "",
        f"DICTAMEN: {dictamen}",
        f"Sugerencia de la ficha (no vinculante): {resultado.sugerido}",
        "",
        "FUNDAMENTO",
        texto_fundamento.strip() or "—",
        "",
        "Norma de base: Reglamento General de Exposiciones 2026 (AACH, archivo de agosto de 2026)",
        "y Reglamento del Puro Registrado (vigencia 23 de octubre de 2023).",
    ]
    return "\n".join(lineas)
