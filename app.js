/* Ficha de admisión Hereford. Misma lógica que src/evaluacion.py. */

const TABLA_CE_PP = [
  [15, 17, 32.0, "15 a 17 meses", "Torito diente de leche Sur"],
  [18, 21, 34.5, "18 a 21 meses", "Diente de leche"],
  [22, 25, 35.5, "22 a 25 meses", "Dos dientes"],
  [26, 29, 36.5, "26 a 29 meses", "Cuatro dientes"],
  [30, 240, 36.5, "30 meses o más", "Seis dientes"],
];

const TABLA_CE_PR = {
  DL: [34.5, "Diente de leche"],
  "2D": [35.5, "Dos dientes"],
  "4D": [36.5, "Cuatro dientes"],
  "6D": [36.5, "Seis dientes"],
};

const TABLA_PESO_PR = {
  DL: { Macho: 360, Hembra: 250, referencia: "diente de leche, referencia 18 meses" },
  "2D": { Macho: 470, Hembra: 320, referencia: "dos dientes, referencia 24 meses" },
  "4D": { Macho: 580, Hembra: 390, referencia: "cuatro dientes, referencia 30 meses" },
};

const CONSECUENCIAS = {
  Admitido: "Queda habilitado y tiene que presentarse a premio. Si no sale a jura, no puede venderse (Art. 17).",
  "Admitido con observación": "Compite. La observación se informa por escrito al comisario (Art. 27).",
  Descalificado: "No entra en la jura. Puede salir a venta si queda identificado como descalificado (Art. 23).",
  Rechazado: "No compite y no sale a venta. Se aparta de los animales admitidos (Art. 23).",
};

const MARCAS = [
  ["exceso_blanco", "Pelaje", "Exceso de blanco fuera de la línea inferior, el pecho y el calzado", "observacion", "Reglamento PR, art. 5.2.6", "La distribución de manchas tiene que mantener la identidad racial. El exceso de blanco queda a criterio del jurado."],
  ["exceso_tapado", "Pelaje", "Animal tapado: falta blanco de línea inferior, calzado o penacho", "observacion", "Reglamento PR, art. 5.2.6", "El exceso de tapado no es, por sí solo, un rechazo automático de la exposición."],
  ["mancha_negra", "Pelaje", "Mancha negra o color ajeno al colorado y al blanco", "causal", "Reglamento PR, art. 5.2.6", "No se aceptan manchas negras ni colores ajenos para calificar PR o VIP. En la exposición el jurado elige rechazo o descalificación."],
  ["piel_negra", "Pelaje", "Piel pigmentada negra", "causal", "Reglamento PR, art. 5.2.6", "La piel pigmentada negra impide la calificación PR o VIP. En pista, el jurado define rechazo o descalificación."],
  ["adulteracion", "Pelaje", "Adulteración de forma o pelaje, o cirugía para ocultar un defecto o simular la raza", "causal", "Art. 18.c, Reglamento de Exposiciones 2026", "Hay que constatar que no se usaron químicos ni cirugías para ocultar defectos o simular el Hereford."],
  ["embellecimiento", "Pelaje", "Producto de embellecimiento distinto de agua, jabón, detergente, champú, crema de enjuague o sopladora", "rechazo", "Art. 19.13, Reglamento de Exposiciones 2026", "El reproductor queda excluido. La suspensión de la cabaña la comunica el comisario."],
  ["prognatismo", "Cabeza", "Prognatismo (mandíbulas de distinta longitud)", "causal", "Art. 19.2, Reglamento de Exposiciones 2026", "Causal de rechazo o descalificación."],
  ["criptorquidia", "Reproducción", "Criptorquidia, monorquidia o hipoplasia testicular", "causal", "Art. 19.3, Reglamento de Exposiciones 2026", "La corrección quirúrgica no se admite como eximente.", ["Macho"]],
  ["lesion_reproductiva", "Reproducción", "Lesión o anomalía que impide o compromete la función reproductiva", "causal", "Art. 19.1, Reglamento de Exposiciones 2026", "El jurado puede rechazar o descalificar."],
  ["anormalidad_genital", "Reproducción", "Anormalidad genital palpable, congénita o adquirida", "causal", "Art. 19.4 y Art. 25, Reglamento de Exposiciones 2026", "Desde el año de edad, el dictamen del jurado es el que vale."],
  ["enfermedad_aguda", "Reproducción", "Enfermedad infectocontagiosa en etapa aguda", "causal", "Art. 19.6, Reglamento de Exposiciones 2026", "Aunque el animal esté en tratamiento."],
  ["asimetria", "Estructura", "Asimetría o desviación, aunque sea parcial", "causal", "Art. 19.5, Reglamento de Exposiciones 2026", "Alcanza desviaciones parciales de la conformación."],
  ["aplomos", "Estructura", "Aplomos con desviación del eje", "observacion", "Reglamento PR, art. 5.2.2", "Descalifica en la inspección de marcación PR. En pista se cruza con el Art. 19.5."],
  ["pezunas", "Estructura", "Pezuñas con crecimiento defectuoso, callos o limax", "observacion", "Reglamento PR, art. 5.2.2", "Motivo de descalificación en la marcación PR."],
  ["dorso", "Estructura", "Lordosis, xifosis o paletas defectuosas", "observacion", "Reglamento PR, art. 5.2.2", "Motivo de descalificación en la marcación PR."],
  ["cola", "Estructura", "Cola de implantación defectuosa o torcida", "observacion", "Reglamento PR, art. 5.2.2", "Motivo de descalificación en la marcación PR."],
  ["prepucio", "Estructura", "Prepucio u ombligo con desarrollo excesivo", "observacion", "Reglamento PR, art. 5.2.2", "Si además compromete la reproducción, marcá la lesión reproductiva."],
  ["doble_musculo", "Estructura", "Doble músculo en el cuarto, sin terminación de grasa", "observacion", "Reglamento PR, art. 5.2.5", "Descalifica como productor de carne en la inspección PR."],
  ["poca_musculatura", "Estructura", "Falta de musculatura, tipo cuarterón o biotipo lechero", "observacion", "Reglamento PR, art. 5.2.5", "Descalifica en la inspección PR."],
  ["falta_desarrollo", "Presentación", "Falta de desarrollo, mal estado o indocilidad manifiesta", "rechazo", "Art. 19.12, Reglamento de Exposiciones 2026", "Esos reproductores serán rechazados."],
  ["id_no_coincide", "Presentación", "RP, HBA o fecha de nacimiento no coinciden con la planilla", "rechazo", "Art. 19.7 y 19.8, Reglamento de Exposiciones 2026", "La individualización que no cierra es causal de rechazo."],
  ["sin_tatuaje", "Presentación", "Sin tatuaje de plantel (Puro Registrado o VIP)", "rechazo", "Art. 19.7, Reglamento de Exposiciones 2026", "El PR o VIP sin tatuaje obligatorio de plantel será rechazado.", null, ["PR", "VIP"]],
  ["cirugia_sin_nota", "Presentación", "Cirugía o accidente previo sin nota ni certificado al comisario", "observacion", "Art. 21, Reglamento de Exposiciones 2026", "Tiene que informarse por nota, con certificación veterinaria."],
];

const TOMAS = [
  ["frente", "Cabeza de frente", "Cara, ojos, anteojeras, orejas, morro y mucosa."],
  ["perfil", "Cabeza de perfil", "Mandíbulas, poll, cuernos o tocos."],
  ["lateral", "Cuerpo de costado", "Color de fondo, línea inferior, dorso, prepucio u ombligo."],
  ["posterior", "Grupa y cola", "Marca de registro, cola y penacho."],
  ["miembros", "Miembros", "Calzado, aplomos y pezuñas."],
];

function alerta(codigo, nivel, titulo, detalle, norma) {
  return { codigo, nivel, titulo, detalle, norma };
}

function marcaPorId(id) {
  return MARCAS.find((m) => m[0] === id);
}

function alertaMarca(id) {
  const m = marcaPorId(id);
  return alerta(m[0], m[3], m[2], m[5], m[4]);
}

function minimoCE(registro, sexo, edad, denticion) {
  if (sexo !== "Macho") return [null, "La circunferencia escrotal se exige a los machos (Art. 26)."];
  if (registro === "PP") {
    if (edad == null) return [null, "Falta la edad en meses para el cuadro de Pedigree."];
    if (edad < 15) return [null, "El cuadro del Art. 26 empieza a los 15 meses. Esta edad no tiene mínimo en ese cuadro."];
    for (const [desde, hasta, minimo, texto] of TABLA_CE_PP) {
      if (edad >= desde && edad <= hasta) return [minimo, texto];
    }
    return [null, "Edad fuera del cuadro del Art. 26."];
  }
  if (registro === "PR" || registro === "VIP") {
    const fila = TABLA_CE_PR[denticion];
    if (!fila) {
      if (denticion === "8D") return [null, "Ocho dientes no tiene categoría PR ni VIP (Art. 19.9)."];
      return [null, "Elegí la dentición para aplicar el mínimo de Puro Registrado."];
    }
    return fila;
  }
  return [null, "Registro sin cuadro de circunferencia."];
}

function bajo(medida, minimo) {
  return Math.round(medida * 10) < Math.round(minimo * 10);
}

function variedad(sexo, inscripta, constatada) {
  const out = [];
  const norma = "Art. 18.b, Reglamento de Exposiciones 2026, y art. 5.3 del Reglamento PR";
  if (constatada === "Tocos adheridos al cuero" && sexo === "Hembra") {
    out.push(alerta("variedad_hembra_tocos", "observacion", "Hembra con tocos: no califica como mocha", "En hembras no se aceptan formaciones córneas inhibidas. Corresponde dejarla como astada. En el catálogo vale la variedad que constate el jurado.", norma));
  } else if (constatada === "Tocos adheridos al cuero" && sexo === "Macho" && inscripta === "Mocho") {
    out.push(alerta("variedad_macho_tocos", "info", "Macho mocho con tocos adheridos al cuero", "Se aceptan en el macho si están adheridos al cuero y mantienen la cabeza típica del Polled Hereford. Si la deforman, es astado.", "Reglamento PR, art. 5.3.a"));
  }
  if (inscripta === "Mocho" && constatada === "Astado") {
    out.push(alerta("variedad_pasa_a_astado", "observacion", "Inscripto mocho y constatado astado", "Se corrige la variedad del catálogo. No es, por sí solo, un rechazo.", norma));
  }
  if (inscripta === "Astado" && constatada === "Mocho limpio") {
    out.push(alerta("variedad_pasa_a_mocho", "observacion", "Inscripto astado y constatado mocho", "Se corrige la variedad del catálogo. No es, por sí solo, un rechazo.", norma));
  }
  if (inscripta === "Astado" && sexo === "Macho" && constatada === "Tocos adheridos al cuero") {
    out.push(alerta("variedad_astado_con_tocos", "observacion", "Inscripto astado, con tocos", "Si los tocos cumplen el art. 5.3.a puede recategorizarse mocho. Si exceden, sigue astado. Vale lo que constate el jurado.", norma));
  }
  return out;
}

function prenez(sexo, exigida, constatada) {
  const alertas = [];
  const incompleto = [];
  if (sexo !== "Hembra" || exigida === "No corresponde") {
    if (sexo === "Hembra" && constatada === "Anormalidad genital palpable") alertas.push(alertaMarca("anormalidad_genital"));
    return [alertas, incompleto];
  }
  if (constatada === "No constatada") {
    incompleto.push("Falta palpar preñez y genitales (Art. 24 y Art. 25).");
    return [alertas, incompleto];
  }
  const vacia = new Set(["Vacía, genitales normales", "Preñada de menos de 60 días", "Anormalidad genital palpable"]);
  if (exigida === "Vacía normal o preñada") {
    if (constatada === "Anormalidad genital palpable") alertas.push(alertaMarca("anormalidad_genital"));
    return [alertas, incompleto];
  }
  if ((exigida === "Preñez de 60 días o más" || exigida === "Preñada o parida") && vacia.has(constatada)) {
    alertas.push(alerta("prenez_insuficiente", "rechazo", "No cumple la preñez que exige la categoría", "Si la categoría exige preñez, la hembra vacía, con menos de 60 días o con anormalidad genital palpable será rechazada. El dictamen del jurado prevalece sobre el certificado.", "Art. 19.11 y Art. 25, Reglamento de Exposiciones 2026"));
    return [alertas, incompleto];
  }
  if (exigida === "Preñez de 60 días o más" && constatada === "Parida con cría") {
    alertas.push(alerta("parida_en_categoria_preniez", "observacion", "Está parida y la categoría pide preñez", "Puede corresponder a la subdivisión de paridas (Art. 25). Definilo con el comisario antes de rechazarla.", "Art. 25, Reglamento de Exposiciones 2026"));
  }
  if (exigida === "Parida con cría al pie" && constatada !== "Parida con cría") {
    if (constatada === "Anormalidad genital palpable") alertas.push(alertaMarca("anormalidad_genital"));
    alertas.push(alerta("sin_cria", "observacion", "La categoría es con cría al pie y no se constató la cría", "Puede no encuadrar en esa categoría. El pase de categoría lo define el comisario, no un rechazo automático.", "Art. 25 y Art. 30, Reglamento de Exposiciones 2026"));
  }
  return [alertas, incompleto];
}

function denticionAlertas(registro, denticion) {
  const alertas = [];
  const incompleto = [];
  if (registro !== "PR" && registro !== "VIP") return [alertas, incompleto];
  if (!denticion || denticion === "No examinada") {
    incompleto.push("En PR y VIP la dentición define la categoría (Art. 18.d).");
    return [alertas, incompleto];
  }
  if (denticion === "8D") {
    alertas.push(alerta("ocho_dientes", "rechazo", "Ocho dientes: no encuadra en las categorías PR o VIP", "Quien por su dentición no entra en diente de leche, dos, cuatro o seis dientes será rechazado. El ejemplo del reglamento es la boca llena.", "Art. 19.9, Reglamento de Exposiciones 2026"));
  }
  return [alertas, incompleto];
}

function pesoAlerta(registro, sexo, denticion, peso) {
  if (registro !== "PR" || peso == null || !denticion) return [];
  const fila = TABLA_PESO_PR[denticion];
  if (!fila || fila[sexo] == null) return [];
  if (peso < fila[sexo]) {
    return [alerta("peso_pr", "observacion", `Peso por debajo del mínimo de marcación PR (${fila[sexo]} kg)`, `${fila.referencia}. Ese mínimo es de la inspección de Puro Registrado, no un rechazo automático de la exposición.`, "Reglamento PR, art. 5.2.1")];
  }
  return [];
}

function sugerir(alertas) {
  const niveles = new Set(alertas.map((a) => a.nivel));
  if (niveles.has("rechazo") || niveles.has("causal")) return "Rechazado";
  if (niveles.has("observacion")) return "Admitido con observación";
  return "Admitido";
}

function evaluar(datos, marcas) {
  const set = new Set(marcas);
  let alertas = [];
  const incompleto = [];
  for (const m of MARCAS) {
    if (!set.has(m[0])) continue;
    const sexos = m[6] || ["Macho", "Hembra"];
    if (!sexos.includes(datos.sexo)) continue;
    if (m[7] && !m[7].includes(datos.registro)) continue;
    alertas.push(alertaMarca(m[0]));
  }
  alertas = alertas.concat(variedad(datos.sexo, datos.variedad_inscripta, datos.variedad_constatada));
  const [dA, dF] = denticionAlertas(datos.registro, datos.denticion);
  alertas = alertas.concat(dA);
  incompleto.push(...dF);
  const [pA, pF] = prenez(datos.sexo, datos.prenez_exigida, datos.prenez_constatada);
  alertas = alertas.concat(pA);
  incompleto.push(...pF);
  const [ceMin, ceRef] = minimoCE(datos.registro, datos.sexo, datos.edad_meses, datos.denticion);
  if (datos.sexo === "Macho" && datos.registro === "PP" && datos.edad_meses == null) {
    incompleto.push("Falta la edad en meses del toro de pedigree (Art. 26).");
  }
  if (ceMin != null && datos.ce_cm == null) {
    incompleto.push(`Falta la circunferencia escrotal. Mínimo de esta fila: ${ceMin.toFixed(1)} cm.`);
  } else if (ceMin != null && datos.ce_cm != null && bajo(datos.ce_cm, ceMin)) {
    alertas.push(alerta("ce_baja", "rechazo", `Circunferencia escrotal ${datos.ce_cm.toFixed(1)} cm, bajo el mínimo de ${ceMin.toFixed(1)} cm`, `Fila aplicada: ${ceRef}. Sin excepciones, el que no llega al mínimo será rechazado.`, "Art. 19.10 y Art. 26, Reglamento de Exposiciones 2026"));
  }
  alertas = alertas.concat(pesoAlerta(datos.registro, datos.sexo, datos.denticion, datos.peso_kg));
  const vistos = new Set();
  const unicas = [];
  for (const a of alertas) {
    if (vistos.has(a.codigo)) continue;
    vistos.add(a.codigo);
    unicas.push(a);
  }
  return { alertas: unicas, sugerido: sugerir(unicas), ce_minimo: ceMin, ce_referencia: ceRef, incompleto };
}

function fundamento(alertas, sugerido) {
  if (!alertas.length) return "Sin causales marcadas. Pelaje, identificación y controles reproductivos dentro de lo examinado.";
  const lineas = [`Sugerencia de la ficha: ${sugerido}.`, ""];
  for (const a of alertas) {
    if (a.nivel === "info") continue;
    lineas.push(`- ${a.titulo}. ${a.norma}.`);
  }
  lineas.push("", "El dictamen lo firma el jurado de admisión.");
  return lineas.join("\n");
}

function informe(datos, resultado, dictamen, texto, fotos) {
  let ce = datos.ce_cm == null ? "sin medir" : `${datos.ce_cm.toFixed(1)} cm`;
  if (resultado.ce_minimo != null) ce += ` (mínimo ${resultado.ce_minimo.toFixed(1)} cm, ${resultado.ce_referencia})`;
  return [
    "INFORME DE ADMISIÓN — HEREFORD",
    "Herramienta de apoyo. El dictamen es del jurado de admisión (Art. 27).",
    "Sociedad Rural de San Luis",
    "",
    `Exposición: ${datos.exposicion || "—"}`,
    `Veterinario: ${datos.veterinario || "—"}`,
    `RP / caravana: ${datos.rp || "—"}`,
    `Cabaña: ${datos.cabana || "—"}`,
    `Sexo: ${datos.sexo || "—"}   Registro: ${datos.registro || "—"}`,
    `Variedad inscripta: ${datos.variedad_inscripta || "—"}`,
    `Variedad constatada: ${datos.variedad_constatada || "—"}`,
    `Dentición: ${datos.denticion || "—"}   Edad (meses): ${datos.edad_meses == null ? "—" : datos.edad_meses}`,
    `Circunferencia escrotal: ${ce}`,
    `Peso: ${datos.peso_kg == null ? "—" : datos.peso_kg} kg`,
    `Preñez exigida: ${datos.prenez_exigida || "—"}`,
    `Preñez constatada: ${datos.prenez_constatada || "—"}`,
    `Fotos: ${fotos.length ? fotos.join(", ") : "sin fotos"}`,
    "",
    `DICTAMEN: ${dictamen}`,
    `Sugerencia de la ficha (no vinculante): ${resultado.sugerido}`,
    "",
    "FUNDAMENTO",
    (texto || "").trim() || "—",
    "",
    "Norma de base: Reglamento General de Exposiciones 2026 (AACH, archivo de agosto de 2026)",
    "y Reglamento del Puro Registrado (vigencia 23 de octubre de 2023).",
  ].join("\n");
}

const HIST = "manga-hereford-informes";

function leerHistorial() {
  try { return JSON.parse(localStorage.getItem(HIST) || "[]"); } catch { return []; }
}

function guardarHistorial(item) {
  const lista = leerHistorial();
  lista.unshift(item);
  localStorage.setItem(HIST, JSON.stringify(lista.slice(0, 80)));
}

function num(id) {
  const v = document.getElementById(id).value.trim();
  if (v === "") return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function val(id) {
  return document.getElementById(id).value;
}

function radio(name) {
  const el = document.querySelector(`input[name="${name}"]:checked`);
  return el ? el.value : "";
}

function leerDatos() {
  const sexo = radio("sexo");
  return {
    exposicion: val("exposicion").trim(),
    veterinario: val("veterinario").trim(),
    rp: val("rp").trim(),
    cabana: val("cabana").trim(),
    sexo,
    registro: radio("registro"),
    variedad_inscripta: radio("variedad"),
    variedad_constatada: val("constatada"),
    denticion: val("denticion"),
    edad_meses: num("edad") == null ? null : Math.trunc(num("edad")),
    ce_cm: sexo === "Macho" ? num("ce") : null,
    prenez_exigida: sexo === "Hembra" ? val("exige") : "No corresponde",
    prenez_constatada: sexo === "Hembra" ? val("palpa") : "No constatada",
    peso_kg: num("peso"),
  };
}

function marcasMarcadas() {
  return [...document.querySelectorAll("#marcas input:checked")].map((el) => el.value);
}

function fotosTomadas() {
  return [...document.querySelectorAll("#fotos input[type=file]")]
    .filter((el) => el.files && el.files.length)
    .map((el) => el.dataset.toma);
}

let editandoFundamento = false;

function pintar() {
  const datos = leerDatos();
  const macho = datos.sexo === "Macho";
  document.getElementById("bloque-ce").hidden = !macho;
  document.getElementById("bloque-prenez").hidden = macho;
  document.querySelectorAll("#registros-vip").forEach((el) => { el.hidden = macho; });
  if (macho && radio("registro") === "VIP") {
    document.querySelector('input[name="registro"][value="PP"]').checked = true;
    datos.registro = "PP";
  }
  document.querySelectorAll("#marcas label").forEach((lab) => {
    const sexos = (lab.dataset.sexos || "Macho,Hembra").split(",");
    const regs = lab.dataset.regs;
    const visible = sexos.includes(datos.sexo) && (!regs || regs.split(",").includes(datos.registro));
    lab.hidden = !visible;
  });
  const resultado = evaluar(datos, marcasMarcadas());
  const sug = document.getElementById("sugerencia");
  sug.textContent = `Sugerencia: ${resultado.sugerido}. ${CONSECUENCIAS[resultado.sugerido]}`;
  const min = document.getElementById("minimo");
  if (resultado.ce_minimo != null) min.textContent = `Mínimo de esta fila: ${resultado.ce_minimo.toFixed(1)} cm (${resultado.ce_referencia}).`;
  else min.textContent = macho ? resultado.ce_referencia : "";
  const caja = document.getElementById("alertas");
  caja.innerHTML = "";
  for (const a of resultado.alertas) {
    const p = document.createElement("p");
    p.className = a.nivel === "info" ? "info" : a.nivel === "observacion" ? "obs" : "mal";
    p.innerHTML = `<b>${a.titulo}.</b> ${a.detalle} <i>${a.norma}</i>`;
    caja.appendChild(p);
  }
  if (resultado.incompleto.length) {
    const p = document.createElement("p");
    p.className = "falta";
    p.textContent = "Antes de guardar: " + resultado.incompleto.join(" ");
    caja.appendChild(p);
  }
  const nota = document.getElementById("nota-causal");
  nota.hidden = !(resultado.sugerido === "Rechazado" && resultado.alertas.some((a) => a.nivel === "causal") && !resultado.alertas.some((a) => a.nivel === "rechazo"));
  const fund = document.getElementById("fundamento");
  if (!editandoFundamento) fund.value = fundamento(resultado.alertas, resultado.sugerido);
  document.getElementById("efecto").textContent = radio("dictamen") ? CONSECUENCIAS[radio("dictamen")] : "";
  window.__resultado = resultado;
  window.__datos = datos;
}

function armarMarcas() {
  const root = document.getElementById("marcas");
  let grupo = "";
  for (const m of MARCAS) {
    if (m[1] !== grupo) {
      grupo = m[1];
      const h = document.createElement("h3");
      h.textContent = grupo;
      root.appendChild(h);
    }
    const lab = document.createElement("label");
    lab.className = "check";
    lab.dataset.sexos = (m[6] || ["Macho", "Hembra"]).join(",");
    if (m[7]) lab.dataset.regs = m[7].join(",");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.value = m[0];
    lab.append(input, document.createTextNode(" " + m[2]));
    root.appendChild(lab);
  }
}

function armarFotos() {
  const root = document.getElementById("fotos");
  for (const [id, titulo, ayuda] of TOMAS) {
    const det = document.createElement("details");
    const sum = document.createElement("summary");
    sum.textContent = titulo;
    const p = document.createElement("p");
    p.className = "ayuda";
    p.textContent = ayuda;
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.capture = "environment";
    input.dataset.toma = id;
    det.append(sum, p, input);
    root.appendChild(det);
  }
}

function pintarHistorial() {
  const root = document.getElementById("lista");
  const lista = leerHistorial();
  root.innerHTML = lista.length ? "" : "<p class='ayuda'>Todavía no hay admisiones en este celular.</p>";
  for (const item of lista) {
    const art = document.createElement("article");
    const h = document.createElement("h3");
    h.textContent = `${item.rp} · ${item.dictamen}`;
    const pre = document.createElement("pre");
    pre.textContent = item.informe;
    const a = document.createElement("a");
    a.textContent = "Descargar informe";
    a.download = `admision-hereford-${item.rp}.txt`;
    a.href = URL.createObjectURL(new Blob([item.informe], { type: "text/plain" }));
    art.append(h, pre, a);
    root.appendChild(art);
  }
}

function mostrar(tab) {
  document.querySelectorAll(".panel").forEach((p) => { p.hidden = p.id !== tab; });
  document.querySelectorAll(".tabs button").forEach((b) => { b.classList.toggle("on", b.dataset.tab === tab); });
  if (tab === "informes") pintarHistorial();
}

document.addEventListener("DOMContentLoaded", () => {
  armarMarcas();
  armarFotos();
  document.body.addEventListener("input", (ev) => {
    if (ev.target.id === "fundamento") editandoFundamento = true;
    pintar();
  });
  document.body.addEventListener("change", pintar);
  document.querySelector(".tabs").addEventListener("click", (ev) => {
    const b = ev.target.closest("button");
    if (b) mostrar(b.dataset.tab);
  });
  document.getElementById("guardar").addEventListener("click", () => {
    const datos = window.__datos;
    const resultado = window.__resultado;
    const msg = document.getElementById("mensaje");
    if (!datos.rp) { msg.textContent = "Falta el RP o la caravana."; return; }
    if (resultado.incompleto.length) { msg.textContent = "Completá las mediciones que el reglamento pide antes de cerrar."; return; }
    const dictamen = radio("dictamen");
    if (!dictamen) { msg.textContent = "Elegí el dictamen."; return; }
    if (!document.getElementById("confirmo").checked) { msg.textContent = "Confirmá el dictamen para dejar constancia."; return; }
    const texto = informe(datos, resultado, dictamen, val("fundamento"), fotosTomadas());
    guardarHistorial({ rp: datos.rp, dictamen, informe: texto, creado: new Date().toISOString() });
    msg.textContent = `Guardado en este celular: ${dictamen}.`;
    const a = document.getElementById("descarga");
    a.hidden = false;
    a.download = `admision-hereford-${datos.rp}.txt`;
    a.href = URL.createObjectURL(new Blob([texto], { type: "text/plain" }));
  });
  document.getElementById("otro").addEventListener("click", () => {
    document.getElementById("rp").value = "";
    document.getElementById("cabana").value = "";
    document.getElementById("edad").value = "";
    document.getElementById("peso").value = "";
    document.getElementById("ce").value = "";
    document.querySelectorAll("#marcas input, #fotos input").forEach((el) => {
      if (el.type === "checkbox") el.checked = false;
      if (el.type === "file") el.value = "";
    });
    document.getElementById("confirmo").checked = false;
    document.querySelectorAll('input[name="dictamen"]').forEach((el) => { el.checked = false; });
    document.getElementById("mensaje").textContent = "";
    document.getElementById("descarga").hidden = true;
    editandoFundamento = false;
    pintar();
    window.scrollTo(0, 0);
  });
  pintar();
});
