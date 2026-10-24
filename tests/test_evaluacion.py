"""Casos del cuadro del Art. 26 y de las causales del Art. 19."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.evaluacion import evaluar, minimo_circunferencia


def datos(**kwargs):
    base = {
        "sexo": "Macho",
        "registro": "PP",
        "variedad_inscripta": "Mocho",
        "variedad_constatada": "Mocho limpio",
        "denticion": "No examinada",
        "edad_meses": 20,
        "ce_cm": 36.0,
        "prenez_exigida": "No corresponde",
        "prenez_constatada": "No constatada",
        "peso_kg": None,
    }
    base.update(kwargs)
    return base


def codigos(resultado):
    return {a.codigo for a in resultado.alertas}


def test_ce_pedigree():
    assert minimo_circunferencia("PP", "Macho", 16, None)[0] == 32.0
    assert minimo_circunferencia("PP", "Macho", 20, None)[0] == 34.5
    assert minimo_circunferencia("PP", "Macho", 24, None)[0] == 35.5
    assert minimo_circunferencia("PP", "Macho", 28, None)[0] == 36.5
    assert minimo_circunferencia("PP", "Macho", 40, None)[0] == 36.5
    assert minimo_circunferencia("PP", "Macho", 12, None)[0] is None
    justo = evaluar(datos(edad_meses=20, ce_cm=34.5), [])
    assert "ce_baja" not in codigos(justo)
    assert justo.sugerido == "Admitido"
    bajo = evaluar(datos(edad_meses=20, ce_cm=34.4), [])
    assert "ce_baja" in codigos(bajo)
    assert bajo.sugerido == "Rechazado"


def test_ce_pr_por_denticion():
    assert minimo_circunferencia("PR", "Macho", None, "DL")[0] == 34.5
    assert minimo_circunferencia("PR", "Macho", None, "2D")[0] == 35.5
    bajo = evaluar(
        datos(registro="PR", denticion="2D", ce_cm=35.0, edad_meses=None),
        [],
    )
    assert "ce_baja" in codigos(bajo)
    boca = evaluar(
        datos(registro="PR", denticion="8D", ce_cm=40, edad_meses=None),
        [],
    )
    assert "ocho_dientes" in codigos(boca)
    pedigree_boca = evaluar(datos(registro="PP", denticion="8D", ce_cm=37, edad_meses=32), [])
    assert "ocho_dientes" not in codigos(pedigree_boca)


def test_ce_faltante_no_rechaza_solo():
    falta = evaluar(datos(ce_cm=None), [])
    assert "ce_baja" not in codigos(falta)
    assert falta.incompleto


def test_hembra_preniez_y_variedad():
    vacia = evaluar(
        datos(
            sexo="Hembra",
            registro="PR",
            denticion="2D",
            edad_meses=24,
            ce_cm=None,
            prenez_exigida="Preñez de 60 días o más",
            prenez_constatada="Vacía, genitales normales",
            variedad_inscripta="Mocho",
            variedad_constatada="Tocos adheridos al cuero",
        ),
        [],
    )
    assert "prenez_insuficiente" in codigos(vacia)
    assert "variedad_hembra_tocos" in codigos(vacia)
    assert vacia.sugerido == "Rechazado"

    parida = evaluar(
        datos(
            sexo="Hembra",
            registro="PP",
            prenez_exigida="Preñada o parida",
            prenez_constatada="Parida con cría",
            variedad_constatada="Astado",
            variedad_inscripta="Astado",
        ),
        [],
    )
    assert parida.sugerido == "Admitido"


def test_causal_de_pelaje_no_pisa_un_rechazo_explicito():
    solo_mancha = evaluar(datos(), ["mancha_negra"])
    assert solo_mancha.sugerido == "Rechazado"
    assert any(a.nivel == "causal" for a in solo_mancha.alertas)
    assert not any(a.nivel == "rechazo" for a in solo_mancha.alertas)


def test_prognatismo_y_desarrollo():
    caso = evaluar(datos(), ["prognatismo", "falta_desarrollo"])
    niveles = {a.codigo: a.nivel for a in caso.alertas}
    assert niveles["prognatismo"] == "causal"
    assert niveles["falta_desarrollo"] == "rechazo"
    assert caso.sugerido == "Rechazado"


if __name__ == "__main__":
    test_ce_pedigree()
    test_ce_pr_por_denticion()
    test_ce_faltante_no_rechaza_solo()
    test_hembra_preniez_y_variedad()
    test_causal_de_pelaje_no_pisa_un_rechazo_explicito()
    test_prognatismo_y_desarrollo()
    print("ok")
