# Manga Hereford

Ficha de admisión para el médico veterinario que trabaja en la manga, antes de que el reproductor Hereford salga a jura en una exposición rural.

En el celular se abre como el Campo Gemelo, por el enlace público:

https://jose2026-market.github.io/manga-hereford/

No hace falta estar en la misma WiFi que la notebook. El informe queda guardado en ese celular.

La foto documenta cabeza, cuerpo, grupa y miembros. La ficha no diagnostica la imagen: cruza lo que el jurado marca con el Reglamento General de Exposiciones 2026 de la Asociación Argentina Criadores de Hereford y con el Reglamento del Puro Registrado (vigencia 23 de octubre de 2023). El dictamen lo confirma el veterinario.

## Cómo abrirla

Doble clic en `run.bat`, o:

```powershell
cd MangaHereford
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0
```

- En la notebook: http://localhost:8501
- En el celular de cada jurado, con la misma WiFi: la dirección Network que imprime Streamlit, por ejemplo `http://192.168.0.12:8501`

La notebook tiene que seguir encendida. Si Windows pregunta, permití Python en la red privada.

Los informes y las fotos quedan en `data/`, en esa computadora.
