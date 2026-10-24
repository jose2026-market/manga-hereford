"""SQLite local. Las fotos no salen de la computadora."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "admision_hereford.db"
FOTOS_DIR = DATA_DIR / "fotos"


def conectar() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FOTOS_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    con = conectar()
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS examenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creado TEXT NOT NULL,
            exposicion TEXT,
            veterinario TEXT,
            rp TEXT NOT NULL,
            cabana TEXT,
            sexo TEXT,
            registro TEXT,
            variedad_inscripta TEXT,
            variedad_constatada TEXT,
            denticion TEXT,
            edad_meses INTEGER,
            ce_cm REAL,
            ce_minimo REAL,
            prenez_exigida TEXT,
            prenez_constatada TEXT,
            peso_kg REAL,
            marcas TEXT,
            sugerido TEXT,
            dictamen TEXT,
            fundamento TEXT,
            informe TEXT,
            fotos TEXT
        )
        """
    )
    con.commit()
    con.close()


def guardar_foto(examen_clave: str, toma: str, contenido: bytes) -> str:
    FOTOS_DIR.mkdir(parents=True, exist_ok=True)
    destino = FOTOS_DIR / f"{examen_clave}_{toma}.jpg"
    destino.write_bytes(contenido)
    return str(destino)


def guardar_examen(datos: dict, informe: str, fotos: str) -> int:
    con = conectar()
    cur = con.execute(
        """
        INSERT INTO examenes (
            creado, exposicion, veterinario, rp, cabana, sexo, registro,
            variedad_inscripta, variedad_constatada, denticion, edad_meses,
            ce_cm, ce_minimo, prenez_exigida, prenez_constatada, peso_kg,
            marcas, sugerido, dictamen, fundamento, informe, fotos
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(timespec="seconds"),
            datos.get("exposicion"),
            datos.get("veterinario"),
            datos.get("rp"),
            datos.get("cabana"),
            datos.get("sexo"),
            datos.get("registro"),
            datos.get("variedad_inscripta"),
            datos.get("variedad_constatada"),
            datos.get("denticion"),
            datos.get("edad_meses"),
            datos.get("ce_cm"),
            datos.get("ce_minimo"),
            datos.get("prenez_exigida"),
            datos.get("prenez_constatada"),
            datos.get("peso_kg"),
            datos.get("marcas"),
            datos.get("sugerido"),
            datos.get("dictamen"),
            datos.get("fundamento"),
            informe,
            fotos,
        ),
    )
    con.commit()
    examen_id = int(cur.lastrowid)
    con.close()
    return examen_id


def listar() -> pd.DataFrame:
    con = conectar()
    frame = pd.read_sql_query(
        """
        SELECT id, creado, rp, cabana, sexo, registro, dictamen, sugerido, exposicion
        FROM examenes
        ORDER BY id DESC
        """,
        con,
    )
    con.close()
    return frame


def obtener(examen_id: int) -> sqlite3.Row | None:
    con = conectar()
    row = con.execute("SELECT * FROM examenes WHERE id = ?", (examen_id,)).fetchone()
    con.close()
    return row
