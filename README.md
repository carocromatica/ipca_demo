# ipca_demo

Prototipo del sitio de **IPCA Consultores** (Villa Alemana, Chile). Es una demo para revisión: no es la versión en vivo de ipca.cl.

## Qué contiene

- Sitio estático (HTML y CSS), sin cookies ni herramientas de medición.
- Páginas: inicio, `/consultoria-financiera/`, `/contabilidad-pymes/`, `/sociedades-de-profesionales/`, `/contacto/`, `/privacidad/` y páginas de error (404, 500, 502, 503, 504).
- SEO técnico: title y meta por página, canonical, sitemap con `lastmod`, `robots.txt` y datos estructurados (schema.org).

## Cómo se genera

Las páginas se generan con un script. Para cambiar textos, edita `_build/build.py` y vuelve a ejecutarlo; sobrescribe los `.html`.

```bash
python3 _build/build.py
```

## Cómo verlo en local

```bash
python3 -m http.server 8099
```

Luego abre `http://localhost:8099`.

## Estado

- Accesibilidad: en proceso.
- Pendientes de contenido: retrato de quien atiende, términos y condiciones, y revisión de la política de privacidad.
- Pendiente para la versión final: aviso de cookies y criterios de la Ley N° 21.719 de protección de datos personales.
