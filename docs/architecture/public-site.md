# Sitio público

El MVP usa Django Templates y una capa de vistas en `config.public`. Las rutas públicas consultan los modelos Django y solo exponen artículos con estado `published`.

Rutas principales:

- `/` portada editorial
- `/articulos/` archivo y buscador
- `/articulos/<slug>/` detalle
- `/categorias/` y `/categorias/<slug>/`
- `/tendencias/` y `/tendencias/<slug>/`
- `/rss.xml`, `/sitemap.xml`, `/robots.txt`, `/llms.txt`, `/llms-full.txt`

La capa visual puede reemplazarse posteriormente sin modificar los modelos ni la API de negocio.
