"""Normas vigentes usadas por la ficha de admisión Hereford.

Fuentes leídas para armar esta ficha (agosto 2026):
- Asociación Argentina Criadores de Hereford, Reglamento General de Exposiciones 2026,
  archivo publicado en agosto de 2026.
- Asociación Argentina Criadores de Hereford, Reglamento del Puro Registrado,
  vigencia 23 de octubre de 2023, archivo publicado en el sitio en agosto de 2025.

No es una transcripción de esos reglamentos. Si una exposición adopta un anexo
propio, manda el anexo de esa muestra.
"""

from __future__ import annotations

FUENTE_EXPO = (
    "Reglamento General de Exposiciones 2026, Asociación Argentina Criadores de Hereford "
    "(archivo de agosto de 2026)"
)
FUENTE_EXPO_URL = (
    "https://www.hereford.org.ar/web/wp-content/uploads/2026/08/"
    "REGLAMENTO-GENERAL-DE-EXPOSICIONES-2026.pdf"
)
FUENTE_PR = (
    "Reglamento del Puro Registrado, vigencia 23 de octubre de 2023, "
    "Asociación Argentina Criadores de Hereford"
)
FUENTE_PR_URL = (
    "https://www.hereford.org.ar/web/wp-content/uploads/2025/08/"
    "Reglamento-Puro-Registrado-Actualizado.pdf"
)

# Cuadro del Art. 26, página 12. La columna de edad es Puro de Pedigree.
# La de categoría es Puro Registrado. Comparten el mínimo de esa fila.
# (desde, hasta, mínimo cm, edad pedigree, categoría PR de la misma fila del cuadro)
TABLA_CE_PEDIGREE = (
    (15, 17, 32.0, "15 a 17 meses", "Torito diente de leche Sur"),
    (18, 21, 34.5, "18 a 21 meses", "Diente de leche"),
    (22, 25, 35.5, "22 a 25 meses", "Dos dientes"),
    (26, 29, 36.5, "26 a 29 meses", "Cuatro dientes"),
    (30, 240, 36.5, "30 meses o más", "Seis dientes"),
)

TABLA_CE_PR = {
    "DL": (34.5, "Diente de leche"),
    "2D": (35.5, "Dos dientes"),
    "4D": (36.5, "Cuatro dientes"),
    "6D": (36.5, "Seis dientes"),
}

# Mínimos de marcación PR, art. 5.2.1. No son causal automática de rechazo en pista.
TABLA_PESO_PR = {
    "DL": {"Macho": 360, "Hembra": 250, "referencia": "diente de leche, referencia 18 meses"},
    "2D": {"Macho": 470, "Hembra": 320, "referencia": "dos dientes, referencia 24 meses"},
    "4D": {"Macho": 580, "Hembra": 390, "referencia": "cuatro dientes, referencia 30 meses"},
}

TOMAS = (
    ("frente", "Cabeza de frente", "Cara, ojos, anteojeras, orejas, morro y mucosa."),
    ("perfil", "Cabeza de perfil", "Mandíbulas, poll, cuernos o tocos."),
    ("lateral", "Cuerpo de costado", "Color de fondo, línea inferior, dorso, prepucio u ombligo."),
    ("posterior", "Grupa y cola", "Marca de registro, cola y penacho."),
    ("miembros", "Miembros", "Calzado, aplomos y pezuñas."),
)

# nivel: rechazo = el artículo dice que serán rechazados o excluidos
#        causal  = el jurado puede rechazar o descalificar
#        observacion = se informa y no cierra la admisión por sí sola
MARCAS = (
    {
        "id": "exceso_blanco",
        "grupo": "Pelaje",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Exceso de blanco fuera de la línea inferior, el pecho y el calzado",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.6",
        "detalle": (
            "La distribución de manchas tiene que mantener la identidad racial. "
            "El exceso de blanco se aparta de la media y queda a criterio del jurado."
        ),
    },
    {
        "id": "exceso_tapado",
        "grupo": "Pelaje",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Animal tapado: falta blanco de línea inferior, calzado o penacho",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.6",
        "detalle": (
            "El mismo artículo alcanza al exceso de tapado. "
            "No es, por sí solo, un rechazo automático de la exposición."
        ),
    },
    {
        "id": "mancha_negra",
        "grupo": "Pelaje",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Mancha negra o color ajeno al colorado y al blanco",
        "nivel": "causal",
        "norma": "Reglamento PR, art. 5.2.6",
        "detalle": (
            "No se aceptan manchas negras ni colores ajenos para calificar PR o VIP. "
            "En la exposición el Art. 19 no la lista como rechazo automático: "
            "el jurado elige rechazo o descalificación."
        ),
    },
    {
        "id": "piel_negra",
        "grupo": "Pelaje",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Piel pigmentada negra",
        "nivel": "causal",
        "norma": "Reglamento PR, art. 5.2.6",
        "detalle": (
            "La piel pigmentada negra impide la calificación PR o VIP. "
            "En pista, el jurado define rechazo o descalificación."
        ),
    },
    {
        "id": "adulteracion",
        "grupo": "Pelaje",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Adulteración de forma o pelaje, o cirugía para ocultar un defecto o simular la raza",
        "nivel": "causal",
        "norma": "Art. 18.c, Reglamento de Exposiciones 2026",
        "detalle": (
            "Hay que constatar que no se usaron químicos ni cirugías para ocultar "
            "defectos o simular el Hereford. El jurado rechaza o descalifica."
        ),
    },
    {
        "id": "embellecimiento",
        "grupo": "Pelaje",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Producto de embellecimiento distinto de agua, jabón, detergente, champú, crema de enjuague o sopladora",
        "nivel": "rechazo",
        "norma": "Art. 19.13, Reglamento de Exposiciones 2026",
        "detalle": (
            "El reproductor queda excluido de la exposición. "
            "La norma también prevé un año de suspensión de la cabaña en esa muestra: "
            "lo comunica el comisario, no esta ficha."
        ),
    },
    {
        "id": "prognatismo",
        "grupo": "Cabeza",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Prognatismo (mandíbulas de distinta longitud)",
        "nivel": "causal",
        "norma": "Art. 19.2, Reglamento de Exposiciones 2026",
        "detalle": "Causal de rechazo o descalificación. No depende del pelaje.",
    },
    {
        "id": "criptorquidia",
        "grupo": "Reproducción",
        "sexos": ("Macho",),
        "etiqueta": "Criptorquidia, monorquidia o hipoplasia testicular",
        "nivel": "causal",
        "norma": "Art. 19.3, Reglamento de Exposiciones 2026",
        "detalle": "La corrección quirúrgica no se admite como eximente.",
    },
    {
        "id": "lesion_reproductiva",
        "grupo": "Reproducción",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Lesión o anomalía que impide o compromete la función reproductiva",
        "nivel": "causal",
        "norma": "Art. 19.1, Reglamento de Exposiciones 2026",
        "detalle": "El jurado puede rechazar o descalificar.",
    },
    {
        "id": "anormalidad_genital",
        "grupo": "Reproducción",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Anormalidad genital palpable, congénita o adquirida",
        "nivel": "causal",
        "norma": "Art. 19.4 y Art. 25, Reglamento de Exposiciones 2026",
        "detalle": (
            "Desde el año de edad, la normalidad genital la constata el jurado "
            "y ese dictamen es el que vale, aunque haya certificado previo."
        ),
    },
    {
        "id": "enfermedad_aguda",
        "grupo": "Reproducción",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Enfermedad infectocontagiosa en etapa aguda",
        "nivel": "causal",
        "norma": "Art. 19.6, Reglamento de Exposiciones 2026",
        "detalle": "Aunque el animal esté en tratamiento.",
    },
    {
        "id": "asimetria",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Asimetría o desviación, aunque sea parcial",
        "nivel": "causal",
        "norma": "Art. 19.5, Reglamento de Exposiciones 2026",
        "detalle": "Alcanza desviaciones parciales de la conformación.",
    },
    {
        "id": "aplomos",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Aplomos con desviación del eje",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.2",
        "detalle": "Descalifica en la inspección de marcación PR. En pista se cruza con el Art. 19.5.",
    },
    {
        "id": "pezunas",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Pezuñas con crecimiento defectuoso, callos o limax",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.2",
        "detalle": "Motivo de descalificación en la marcación PR.",
    },
    {
        "id": "dorso",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Lordosis, xifosis o paletas defectuosas",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.2",
        "detalle": "Motivo de descalificación en la marcación PR.",
    },
    {
        "id": "cola",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Cola de implantación defectuosa o torcida",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.2",
        "detalle": "Motivo de descalificación en la marcación PR.",
    },
    {
        "id": "prepucio",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Prepucio u ombligo con desarrollo excesivo",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.2",
        "detalle": "Si además compromete la reproducción, marcá la lesión reproductiva.",
    },
    {
        "id": "doble_musculo",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Doble músculo en el cuarto, sin terminación de grasa",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.5",
        "detalle": "Descalifica como productor de carne en la inspección PR.",
    },
    {
        "id": "poca_musculatura",
        "grupo": "Estructura",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Falta de musculatura, tipo cuarterón o biotipo lechero",
        "nivel": "observacion",
        "norma": "Reglamento PR, art. 5.2.5",
        "detalle": "Descalifica en la inspección PR.",
    },
    {
        "id": "falta_desarrollo",
        "grupo": "Presentación",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Falta de desarrollo, mal estado o indocilidad manifiesta",
        "nivel": "rechazo",
        "norma": "Art. 19.12, Reglamento de Exposiciones 2026",
        "detalle": "Esos reproductores serán rechazados.",
    },
    {
        "id": "id_no_coincide",
        "grupo": "Presentación",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "RP, HBA o fecha de nacimiento no coinciden con la planilla",
        "nivel": "rechazo",
        "norma": "Art. 19.7 y 19.8, Reglamento de Exposiciones 2026",
        "detalle": "La individualización que no cierra con el reglamento es causal de rechazo.",
    },
    {
        "id": "sin_tatuaje",
        "grupo": "Presentación",
        "sexos": ("Macho", "Hembra"),
        "registros": ("PR", "VIP"),
        "etiqueta": "Sin tatuaje de plantel (Puro Registrado o VIP)",
        "nivel": "rechazo",
        "norma": "Art. 19.7, Reglamento de Exposiciones 2026",
        "detalle": "El PR o VIP sin tatuaje obligatorio de plantel será rechazado.",
    },
    {
        "id": "cirugia_sin_nota",
        "grupo": "Presentación",
        "sexos": ("Macho", "Hembra"),
        "etiqueta": "Cirugía o accidente previo sin nota ni certificado al comisario",
        "nivel": "observacion",
        "norma": "Art. 21, Reglamento de Exposiciones 2026",
        "detalle": "Tiene que informarse por nota, con certificación veterinaria identificada.",
    },
)

GRUPOS = ("Pelaje", "Cabeza", "Reproducción", "Estructura", "Presentación")

CONSECUENCIAS = {
    "Admitido": "Queda habilitado y tiene que presentarse a premio. Si no sale a jura, no puede venderse (Art. 17).",
    "Admitido con observación": "Compite. La observación se informa por escrito al comisario (Art. 27).",
    "Descalificado": "No entra en la jura. Puede salir a venta si queda identificado como descalificado (Art. 23).",
    "Rechazado": "No compite y no sale a venta. Se aparta de los animales admitidos (Art. 23).",
}

MEDIA_RACIAL = (
    "La media que usa la inspección, descrita en la bibliografía técnica argentina "
    "y acotada por el art. 5.2.6 del Reglamento PR, es esta: cuerpo colorado "
    "(rojo cereza a abayado), cara blanca, orejas coloradas, blanco en pecho, "
    "vientre, ingle y extremos de los miembros, penacho blanco. Las anteojeras "
    "coloradas se admiten. Las mucosas son rosadas. Esa descripción orienta la foto; "
    "el rechazo automático de pista sale del Reglamento de Exposiciones, no de esta guía."
)
