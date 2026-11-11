# ipca_demo

Prototipo del sitio de **IPCA Consultores** (Villa Alemana, Chile), una consultora financiera y contable. Es una demo para revisión: no es la versión en vivo de ipca.cl.

Los enlaces, estilos e imágenes usan rutas relativas, para que la demo funcione al publicarla en GitHub Pages (`/ipca_demo/`). Las direcciones de SEO (canonical, Open Graph y datos estructurados) siguen apuntando a `https://ipca.cl`.

Páginas incluidas: inicio, consultoría financiera, contabilidad para pymes, sociedades de profesionales, contacto, política de privacidad y páginas de error (404, 500, 502, 503 y 504).

## Checklist SEO

Estado al 10/11/2026. `[x]` = verificado en el código de este repositorio. `[ ]` = pendiente. Entre paréntesis, quién lo resuelve cuando no depende solo del sitio.

### 1. Rastreo e indexación

- [x] `robots.txt` permite todo y enlaza el sitemap
- [x] `sitemap.xml` con 6 URLs (inicio, 3 servicios, contacto y privacidad) y fecha `lastmod`
- [x] Páginas de error con `noindex` y fuera del sitemap
- [x] Canonical con URL absoluta en todas las páginas
- [x] Una URL por servicio, sin una URL por keyword
- [x] `lang="es"` en todas las páginas
- [ ] Forzar HTTPS y una sola versión del dominio (con o sin `www`) con redirección 301 (hosting)
- [ ] Configurar en el hosting qué archivo sirve cada error y confirmar que la 404 responde con estado 404 real (hosting)
- [ ] Enviar el sitemap a Google Search Console
- [ ] Solicitar indexación de las 4 páginas clave

### 2. On-page por página

| Página | Title (máx. 60) | Meta (140 a 155) | H1 único | Estado |
|---|---|---|---|---|
| `/` | 52 | 139 | sí | [x] |
| `/consultoria-financiera/` | 58 | 150 | sí | [x] |
| `/contabilidad-pymes/` | 59 | 145 | sí | [x] |
| `/sociedades-de-profesionales/` | 49 | 134 | sí | [x] |
| `/contacto/` | 47 | 119 | sí | [ ] meta corta |
| `/privacidad/` | 41 | 148 | sí | [x] |

- [x] Todos los title de 60 caracteres o menos
- [x] Open Graph y Twitter card en todas las páginas
- [ ] Alargar la meta de `/contacto/` a 140 caracteres o más
- [x] Title, H1 y H2 de cada servicio contrastados con el mapa de keywords (10/11/2026). Resultado en la tabla de abajo
- [ ] Sumar al texto las variantes del mapa que todavía no aparecen (ver tabla)

Contraste con el mapa de keywords (frases exactas, sin distinguir tildes; las variantes incluyen frases sin datos de volumen):

| Página | Keyword principal del mapa | En title y H1 | Keywords del mapa en el texto |
|---|---|---|---|
| `/consultoria-financiera/` | consultoría financiera | sí | 16 de 23 |
| `/contabilidad-pymes/` | contador para pymes | sí (title) y la variante "contabilidad para pymes" (H1) | 4 de 24 |
| `/sociedades-de-profesionales/` | sociedad de profesionales | sí | 4 de 11 |

- Lo que falta son variantes y preguntas del mapa, por ejemplo: "contador villa alemana" y "contabilidad mensual para pymes" (contabilidad), "requisitos de una sociedad de profesionales" y "boleta de honorarios o sociedad" (sociedades), y, en consultoría, "cuánto cuesta un contador en Chile" y "asesoría financiera para profesionales independientes en Chile".
- Las keywords de emprendedores y de inicio de actividades no se agregan por ahora: el cliente busca empresas consolidadas en crecimiento, y eso se decide para la entrega final.

Otros pendientes de esta sección:

- [ ] Explicar IFRS y SII la primera vez que aparecen en cada página
- [ ] Imagen Open Graph distinta por servicio (opcional)

### 3. Enlaces internos

- [x] Menú principal con inicio y los 3 servicios, más botón hacia contacto
- [x] Cada página de servicio enlaza a las otras dos
- [x] Migas de pan en servicios, contacto y privacidad
- [x] Pie con los 3 servicios, contacto y política de privacidad
- [ ] Enlace propio a `/contacto/` en el pie
- [ ] Enlaces dentro del texto con la keyword (por ejemplo, contabilidad hacia consultoría)
- [ ] Revisar enlaces rotos antes de publicar

### 4. Datos estructurados (schema.org)

- [x] `ProfessionalService` y `WebSite` en la home
- [x] `Service` y `FAQPage` en los 3 servicios, con el mismo texto que las preguntas visibles
- [x] `BreadcrumbList` en servicios, contacto y privacidad
- [ ] `Person` de quien atiende, junto con el bloque "Quién te atiende"
- [ ] `sameAs` con LinkedIn y Google Business Profile, cuando existan
- [ ] `ContactPage` o `ContactPoint` en contacto
- [ ] Validar todo con la Prueba de resultados enriquecidos de Google

### 5. Imágenes y rendimiento

- [x] Todas las imágenes con `alt` (las decorativas con `alt` vacío) y con `width` y `height`
- [x] Imágenes principales en webp, con la del primer pantallazo en prioridad alta
- [x] Fuentes con `display=swap`
- [ ] `loading="lazy"` en las imágenes que no son del primer pantallazo
- [ ] `srcset` para móvil en las imágenes grandes
- [ ] Reducir o quitar el PNG de respaldo del hero (1,9 MB)
- [ ] Autoalojar o precargar las fuentes
- [x] PageSpeed Insights de la home (10/11/2026): en celulares, rendimiento 96 y accesibilidad, recomendaciones y SEO en 100; en escritorio, 100 en las cuatro categorías
- [ ] Medir en PageSpeed Insights los 3 servicios y comparar antes y después

### 6. Accesibilidad (en proceso)

- [x] Medición automática de accesibilidad en la home: 100 en celulares y escritorio (no reemplaza la revisión manual de abajo)
- [ ] Corregir el contraste del texto dorado de la página 404 (2,8:1; el mínimo es 4,5:1)
- [ ] Botones y enlaces de al menos 44 px de alto
- [ ] Foco visible y menú que cierra con la tecla Escape
- [ ] Orden de encabezados y etiqueta `<main>` en todas las páginas
- [ ] Revisar el H2 de contabilidad, que lleva un ícono dentro, y confirmar que el texto se lee limpio

### 7. Favicon e identidad

- [x] `/favicon.ico` en la raíz, ícono de 32 px y `apple-touch-icon`
- [x] Logo con `alt` "IPCA Consultores"

### 8. Contenido y confianza

- [x] El servicio de CFO externo está confirmado por el cliente
- [x] Sin testimonios, cifras ni clientes inventados
- [x] Horario, zona de atención, WhatsApp y correo visibles en el pie
- [ ] Bloque "Quién te atiende" con el contador auditor del cliente
- [ ] Retrato real en lugar de la foto referencial (cliente)
- [ ] Reseñas y casos reales con permiso, cuando existan
- [ ] Primer artículo del blog sobre flujo de caja (fase 2)

### 9. Privacidad y legal

- [x] `/privacidad/` creada y enlazada desde el pie
- [x] Casilla de consentimiento obligatoria en el formulario
- [x] El sitio no usa cookies ni herramientas de medición
- [ ] Plazo de conservación de datos definido por el cliente (cliente)
- [ ] Revisión de `/privacidad/` (cliente)
- [ ] Términos y condiciones, a redactar con el cliente
- [ ] Versión final: aviso de cookies y criterios de la Ley N° 21.719 de protección de datos personales
- [ ] Si se vuelve a usar Google Tag Manager: aviso de cookies y actualizar la política
- [ ] Anuncios: revisar el aviso de certificación de productos y servicios financieros de Google Ads (ver si aplica a la consultoría antes de publicar anuncios)

### 10. SEO local

- [x] Datos de contacto coherentes entre sitio y schema
- [ ] Ficha de Google Business Profile como negocio sin local, con zona de servicio y dirección oculta (cliente)
- [ ] Mismos datos (nombre, teléfono y zona) en la ficha, el sitio y el schema
- [ ] Primeras reseñas de clientes reales
- [ ] Directorios locales serios, con los mismos datos

### 11. Despliegue

- [x] Prototipo subido a GitHub para revisión, sin tocar el sitio en vivo
- [x] Este repositorio no incluye versiones antiguas, borradores ni Google Tag Manager
- [ ] Quitar del despliegue los archivos sobrantes del sitio en vivo
- [ ] Si la página antigua `ipca_consultores.html` está indexada en el sitio en vivo, redirigirla con 301 a la home
- [ ] Revisar las 6 páginas en el navegador, escritorio y móvil

### 12. Medición y seguimiento

- [ ] Verificar la propiedad en Google Search Console
- [ ] Registrar las posiciones iniciales de las keywords del mapa
- [ ] Definir cómo medir clics en WhatsApp y envíos del formulario
- [ ] Revisar indexación a las 2 semanas y posiciones y clics cada mes
- [ ] Decidir con datos si algún satélite merece URL propia

### 13. Primera consulta con costo

- [x] Decidido por el cliente: la primera consulta tiene costo
- [ ] Definir cómo se comunica (hoy se menciona en contacto y en las preguntas frecuentes de consultoría y contabilidad, no en la home)
- [ ] Decidir si se publica el valor

## Estado general

Listo: la base técnica (indexación, title y meta, datos estructurados, imágenes y privacidad básica). Pendiente: accesibilidad, rendimiento fino, la configuración del hosting, Google Search Console, la ficha de Google Business Profile y la información que debe entregar el cliente.
