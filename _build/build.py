#!/usr/bin/env python3
"""Genera las páginas estáticas de ipca.cl con header/footer compartidos.

Uso (desde la carpeta del sitio):  python3 _build/build.py
Edita los textos aquí y vuelve a ejecutar; sobrescribe los .html generados.
"""
import json
import re
from datetime import date
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ipca.cl"
PHONE_DISPLAY = "+56 9 3331 2344"
PHONE_WA = "56933312344"
EMAIL = "contacto@ipca.cl"
WA = f"https://wa.me/{PHONE_WA}?text=Hola%2C%20quisiera%20agendar%20una%20reuni%C3%B3n%20con%20IPCA%20Consultores."
OG = f"{SITE}/assets/ipca_opengraph.png"

SERVICES = [
    ("/consultoria-financiera/", "Consultoría financiera", "Presupuestos, flujo de caja y decisiones con números claros."),
    ("/contabilidad-pymes/", "Contabilidad para pymes", "Contabilidad mensual, estados financieros y asesoría permanente."),
    ("/sociedades-de-profesionales/", "Sociedades de profesionales", "Cuándo conviene, requisitos y constitución."),
]


def head(title, desc, path, extra=""):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">

  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{OG}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="icon" type="image/png" href="/assets/ipca_favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Lato:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
{extra}</head>
<body>
"""


def header(current="", over=False):
    def a(href, label):
        cur = ' aria-current="page"' if current == href else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    links = "\n        ".join([
        a("/", "Inicio"),
        a("/consultoria-financiera/", "Consultoría financiera"),
        a("/contabilidad-pymes/", "Contabilidad"),
        a("/sociedades-de-profesionales/", "Sociedades"),
    ])
    return f"""  <a class="skip-link" href="#main">Saltar al contenido</a>
  <header class="site-header{' over' if over else ''}">
    <div class="container nav">
      <a class="logo" href="/" aria-label="IPCA Consultores, ir al inicio"><img src="/assets/logo.svg" alt="IPCA Consultores" width="150" height="46"></a>
      <button class="hamburger" id="hamburger" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks"><span></span><span></span><span></span></button>
      <ul class="nav-links" id="navLinks">
        {links}
        <li class="nav-cta"><a class="btn btn-primary" href="/contacto/">Comunícate con nosotros</a></li>
      </ul>
    </div>
  </header>
"""


FOOTER = f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <img src="/assets/logo_blanco.svg" alt="IPCA Consultores" width="150" height="54">
          <p>Consultoría financiera y contable para empresas y profesionales independientes.</p>
        </div>
        <div>
          <h2>Servicios</h2>
          <ul>
            {''.join(f'<li><a href="{u}">{n}</a></li>' for u, n, _ in SERVICES)}
          </ul>
        </div>
        <div>
          <h2>Contacto</h2>
          <ul>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><a href="{WA}">WhatsApp {PHONE_DISPLAY}</a></li>
            <li>Villa Alemana y alrededores · atención online</li>
            <li>Lunes a viernes, 9:00 a 18:00</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">© 2026 IPCA Consultores · Todos los derechos reservados · <a href="/privacidad/">Política de privacidad</a></div>
    </div>
  </footer>

  <script>
    var hb = document.getElementById('hamburger'), nl = document.getElementById('navLinks');
    hb.addEventListener('click', function () {{
      var open = nl.classList.toggle('open');
      hb.setAttribute('aria-expanded', open);
    }});
    var hd = document.querySelector('.site-header.over');
    if (hd) {{
      var stick = function () {{ hd.classList.toggle('is-stuck', window.scrollY > 80); }};
      stick(); addEventListener('scroll', stick, {{ passive: true }});
    }}
  </script>
</body>
</html>
"""


def faq_html(items):
    out = '<div class="faq">\n'
    for q, ans in items:
        out += f"  <details><summary>{q}</summary><p>{ans}</p></details>\n"
    return out + "</div>"


def faq_ld(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}
    return f'  <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def breadcrumb_ld(name, path):
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}
    return f'  <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def service_ld(name, desc, path):
    data = {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "url": SITE + path, "serviceType": name,
            "provider": {"@type": "ProfessionalService", "name": "IPCA Consultores", "url": SITE},
            "areaServed": ["Región de Valparaíso", "Santiago", "Chile (online)"]}
    return f'  <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def cta_band(title="Conversemos sobre la estructura que tu organización necesita",
             text="Cuéntanos en qué etapa está tu empresa y te decimos cómo podemos ayudarte. Respondemos en horario hábil."):
    return f"""    <section class="cta-band">
      <div class="container">
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="btn-row">
          <a class="btn btn-gold" href="/contacto/">Comunícate con nosotros</a>
          <a class="btn btn-ghost-light" href="{WA}">Escribir por WhatsApp</a>
        </div>
      </div>
    </section>
"""


def related(exclude):
    cards = "".join(
        f'<a href="{u}"><strong>{n}</strong><span>{d}</span></a>' for u, n, d in SERVICES if u != exclude)
    return f"""    <section>
      <div class="container">
        <h2>Otros servicios</h2>
        <div class="related">{cards}</div>
      </div>
    </section>
"""


ICONS = {
    "Consultoría financiera que se traduce en decisiones": "chart-line",
    "Consultoría financiera para pymes": "building-2",
    "Asesoría financiera para profesionales independientes": "briefcase",
    "Dirección financiera externa (CFO externo)": "compass",
    "Contador para pymes: contabilidad ordenada y al día": "calculator",
    "Contabilidad para emprendedores": "rocket",
    "Contabilidad online": "laptop",
    "Contador en Villa Alemana": "map-pin",
}


def lucide(name):
    import re
    svg = (ROOT / "_build" / "icons" / f"{name}.svg").read_text(encoding="utf-8")
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    inner = re.sub(r"\s+", " ", inner).strip()
    return (f'<svg class="icon" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')


def add_icons(html):
    import re
    def rep(m):
        ic = ICONS.get(m.group(1))
        return f'<h2>{lucide(ic)}{m.group(1)}</h2>' if ic else m.group(0)
    return re.sub(r"<h2>(.*?)</h2>", rep, html)


def service_page(path, title, desc, name, h1, lead, body, faq, aside_title, aside_text, hero_img=None, aside_html=None, cards=None, cards_heading='', intro=None):
    body = add_icons(body)
    aside_html = add_icons(aside_html) if aside_html else aside_html
    default_aside = f'''<h3>{aside_title}</h3>
          <p>{aside_text}</p>
          <a class="btn btn-primary" href="/contacto/">Comunícate con nosotros</a>
          <p style="margin-top:1rem;margin-bottom:0">O escríbenos a <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''
    if intro:
        ititle, itext, chips = intro
        chips_html = "".join(f'<li class="concept"><span class="badge">{lucide(ic)}</span><span class="label">{label}</span></li>' for ic, label in chips)
        main_html = f'''    <section>
      <div class="container">
        <div class="intro-center">
          <h2>{ititle}</h2>
          <p>{itext}</p>
          <ul class="concepts">{chips_html}</ul>
        </div>
      </div>
    </section>'''
        left, _, right = (aside_html or "").partition('<div class="callout">')
        right = '<div class="callout">' + right if right else ""
        after_cards = f'''    <section class="section-cream">
      <div class="container split split-center">
        <div class="prose">{left}</div>
        <div>{right}</div>
      </div>
    </section>
''' if aside_html else ""
    else:
        main_html = f'''    <section>
      <div class="container split split-aside">
        <div class="prose">
{body}
        </div>
        <aside class="aside-card{' aside-info' if aside_html else ''}">
          {aside_html if aside_html else default_aside}
        </aside>
      </div>
    </section>'''
        after_cards = ""
    cards_html = ""
    if cards:
        items = "".join(
            f'<article class="svc-card"><h3>{t}</h3>{txt}</article>' for t, txt in cards)
        cards_html = f'''    <section class="svc-section">
      <div class="container">
        <h2>{cards_heading}</h2>
        <div class="svc-grid">{items}</div>
      </div>
    </section>
'''
    extra = breadcrumb_ld(name, path) + service_ld(name, desc, path) + faq_ld(faq)
    html = head(title, desc, path, extra) + header(path)
    img_html = ""
    grid_cls = ""
    if hero_img:
        src, alt = hero_img
        grid_cls = " hero-grid"
        img_html = f'<div class="hero-image"><img src="{src}" alt="{alt}" width="1536" height="1024" fetchpriority="high"></div>'
    html += f"""
  <main id="main">
    <div class="page-hero">
      <div class="container{grid_cls}">
        <div>
        <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / {name}</nav>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="/contacto/">Agendar reunión</a>
          <a class="btn btn-outline" href="{WA}">Escribir por WhatsApp</a>
        </div>
        </div>
        {img_html}
      </div>
    </div>

{main_html}
{cards_html}{after_cards}    <section class="section-alt">
      <div class="container">
        <h2>Preguntas frecuentes</h2>
        {faq_html(faq)}
      </div>
    </section>

{cta_band()}
{related(path)}  </main>
"""
    return html + FOOTER


ASIDE_CONTADOR = '''<h2>¿Contador o asesor financiero?</h2>
          <p>El contador registra y declara lo que ya pasó, y cumple con la normativa. El asesor financiero mira hacia adelante: cuánto necesitas, cuándo y cómo financiarlo. Cuando una empresa escala, suele necesitar ambos. En IPCA podemos hacer las dos cosas y coordinarlas con tu contador actual si prefieres mantenerlo.</p>
          <div class="callout"><p>¿No sabes cuál necesitas? Conversemos: en la primera reunión revisamos tu situación y te orientamos con honestidad.</p></div>'''


# ───────────────────────── Páginas ─────────────────────────

def home():
    ld = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "IPCA Consultores",
        "url": SITE, "logo": f"{SITE}/assets/logo.png", "image": OG, "email": EMAIL, "telephone": "+56933312344",
        "description": "Consultoría financiera y contable para empresas y profesionales independientes.",
        "areaServed": ["Región de Valparaíso", "Santiago", "Chile (online)"],
        "address": {"@type": "PostalAddress", "addressLocality": "Villa Alemana", "addressCountry": "CL"},
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                      "opens": "09:00", "closes": "18:00"},
    }
    ws = {"@context": "https://schema.org", "@type": "WebSite", "name": "IPCA Consultores", "url": SITE + "/", "inLanguage": "es-CL"}
    extra = (f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
             f'  <script type="application/ld+json">{json.dumps(ws, ensure_ascii=False)}</script>\n')
    h = head("IPCA Consultores | Consultoría financiera y contable",
             "Consultoría financiera, contabilidad para pymes y sociedades de profesionales en Villa Alemana y online. Agenda una reunión de diagnóstico.",
             "/", extra) + header("/", over=True)
    icons = ["finanzas", "contabilidad", "pilar"]
    bullets = [
        ["Presupuestos y proyecciones", "Flujo de caja y control de gestión", "Dirección financiera externa"],
        ["Contabilidad mensual", "Estados financieros bajo IFRS", "Asesoría contable permanente"],
        ["¿Conviene crear una sociedad?", "Requisitos ante el SII", "Constitución y puesta en marcha"],
    ]
    blurbs = [
        "Información financiera clara y oportuna para decidir con respaldo, sin tecnicismos.",
        "Orden, cumplimiento y continuidad para tu empresa, con un equipo que entiende de negocio.",
        "Te explicamos cuándo tiene sentido esta figura y te acompañamos en el proceso.",
    ]
    lic = ["chart-line", "calculator", "users", "file-search"]
    arts = []
    for (u, n, _), ic, bl, bu in zip(SERVICES, lic, blurbs, bullets):
        arts.append((u, n, ic, bl, "".join(f"<li>{b}</li>" for b in bu)))
    arts.append(("/contacto/", "Auditoría y optimización de procesos", lic[3],
                 "Revisamos riesgos y procesos para que tu empresa opere con más control.",
                 "<li>Auditoría y evaluación de riesgos</li><li>Optimización de procesos financieros y administrativos</li>"))

    def svc_row(a):
        u, n, ic, bl, lis = a
        return f"""
          <a class="svc-row" href="{u}">
            <div class="svc-head"><span class="svc-icon">{lucide(ic)}</span><h3>{n}</h3></div>
            <p>{bl}</p>
            <ul>{lis}</ul>
            <span class="svc-go">{lucide("arrow-right")}</span>
          </a>"""

    pillars = "".join(svc_row(a) for a in arts)
    h += f"""
  <main id="main">
    <div class="hero hero-split">
      <div class="container hero-grid">
        <div class="hero-copy">
          <h1>Estructura <em>financiera</em> para decisiones sólidas</h1>
          <p class="lead">Consultora de finanzas y contabilidad. Construimos bases financieras estables para empresas y profesionales independientes en crecimiento.</p>
          <div class="btn-row">
            <a class="btn btn-primary" href="/contacto/">Agendar reunión</a>
            <a class="btn btn-outline" href="{WA}">Escribir por WhatsApp</a>
          </div>
        </div>
        <div class="hero-image">
          <div class="hero-photo">
            <picture>
              <source srcset="/assets/hero-pilares.webp" type="image/webp">
              <img src="/assets/hero-pilares.png" alt="Columnas griegas que representan estructura y estabilidad" width="941" height="1672" fetchpriority="high">
            </picture>
          </div>
          <a class="hero-cta" href="/contacto/">
            <img class="hero-cta-mark" src="/assets/pilar.svg" alt="" width="52" height="39">
            <span class="hero-cta-text">Conversemos sobre tu empresa.</span>
            <span class="hero-cta-go">Agendar reunión {lucide("arrow-right")}</span>
          </a>
        </div>
      </div>
    </div>

    <div class="trust">
      <div class="container">
        <ul>
          <li><strong>Finanzas corporativas</strong>amplia experiencia</li>
          <li><strong>Grandes firmas de auditoría</strong>formación y práctica</li>
          <li><strong>Control interno</strong>procesos con trazabilidad</li>
          <li><strong>Mentalidad gerencial</strong>números que sirven para decidir</li>
        </ul>
      </div>
    </div>

    <section id="servicios">
      <div class="container">
        <div class="section-head">
          <h2>Cuatro áreas para ordenar y hacer crecer tu empresa</h2>
          <p class="lead">Trabajamos con empresas medianas, pymes en crecimiento y profesionales independientes.</p>
        </div>
        <div class="svc-list">{pillars}
        </div>
      </div>
    </section>

    <section class="section-alt">
      <div class="container path-layout">
        <div class="section-head">
          <h2>Cercanos, claros y sin letra chica</h2>
        </div>
        <ol class="path">
          <li><h3>Conversamos</h3><p>Nos cuentas cómo funciona tu negocio y qué necesitas resolver. Atendemos presencial, por videollamada, WhatsApp o correo.</p></li>
          <li><h3>Ordenamos el panorama</h3><p>Revisamos tu situación contable y financiera y te proponemos un plan simple, con prioridades claras.</p></li>
          <li><h3>Te acompañamos</h3><p>Implementamos junto a ti y damos seguimiento en el tiempo, para que cada decisión tenga respaldo.</p></li>
        </ol>
      </div>
    </section>

    <section class="statement">
      <div class="container">
        <h2>Cuando tu negocio crece, la contabilidad sola ya no basta</h2>
        <div class="statement-body">
          <p>Muchas empresas cambian de contador porque lo que necesitan en realidad es un asesor financiero que complemente la contabilidad. Ahí entramos nosotros.</p>
          <ul class="profiles">
            <li>Empresas medianas que necesitan estructura y control en su gestión.</li>
            <li>Pymes que crecieron y requieren estados financieros más profundos.</li>
            <li>Profesionales independientes con facturación sostenida.</li>
            <li>Emprendedores que inician actividades y quieren partir ordenados.</li>
          </ul>
        </div>
      </div>
    </section>

{cta_band()}  </main>
"""
    return h + FOOTER


def consultoria():
    body = ""
    faq = [
        ("¿Cuánto cuesta una asesoría financiera para empresas?",
         "Depende del tamaño de la empresa, la complejidad y si el trabajo es puntual o recurrente. Después de la primera reunión te enviamos una propuesta con alcance y valor definidos. La primera consulta tiene costo."),
        ("¿Cuál es la diferencia entre un contador y un asesor financiero?",
         "El contador se ocupa del registro contable y el cumplimiento tributario. El asesor financiero usa esa información para proyectar, planificar y recomendar decisiones."),
        ("¿Trabajan con empresas fuera de Villa Alemana?",
         "Sí. Atendemos en la región de Valparaíso y Santiago, y online al resto del país por videollamada, WhatsApp y correo."),
        ("¿Qué necesito para partir?",
         "Tus estados financieros o registros más recientes, si los tienes, y una idea de lo que quieres resolver. Si no tienes todo ordenado, también te ayudamos a partir de ahí."),
    ]
    return service_page(
        "/consultoria-financiera/",
        "IPCA - Consultoría financiera para empresas en crecimiento",
        "Consultoría y asesoría financiera para empresas y pymes: presupuestos, flujo de caja y control de gestión. Villa Alemana y online. Agenda una reunión.",
        "Consultoría financiera",
        "Consultoría y asesoría financiera para empresas",
        "Información financiera clara para decidir con respaldo: presupuestos, flujo de caja y control de gestión, con una mirada gerencial.",
        body, faq, "Hablemos de tus números", "Cuéntanos qué necesitas resolver y te orientamos en la primera reunión.",
        aside_html=ASIDE_CONTADOR,
        intro=("Finanzas claras que se traducen en decisiones",
               "Ordenamos la información de tu empresa para que sepas dónde estás parado, cuánta caja tendrás y qué decisiones conviene tomar primero. Trabajamos con lenguaje simple y con foco en lo que mueve tu negocio.",
               [("chart-column", "Presupuestos y proyecciones financieras"),
                ("banknote", "Flujo de caja y control de gestión"),
                ("landmark", "Gestión operativa de tesorería"),
                ("users", "Acompañamiento a equipos en el orden de procesos internos"),
                ("file-search", "Apoyo en compra de empresas (due diligence)")]),
        cards_heading="Nuestros servicios están para ayudarte",
        cards=[
            ("Consultoría financiera para pymes", "<p>Si tu pyme ya factura de manera estable, pero las decisiones se toman “a ojo”, una consultoría financiera te da un tablero claro: márgenes, necesidades de capital y escenarios. No necesitas un área de finanzas completa para partir.</p>"),
            # Confirmado con el cliente (2026-11-10): sí ofrece dirección financiera externa recurrente.
            ("Dirección financiera externa (CFO externo)", "<p>Para empresas que necesitan una mirada gerencial en finanzas, pero no justifican un gerente financiero de jornada completa: nos hacemos cargo de la planificación, el seguimiento de indicadores y el apoyo en decisiones, de forma recurrente.</p>"),
            ("Asesoría financiera para profesionales independientes", '<p>Es la consulta que más nos hacen: profesionales que facturan sobre los 5 millones mensuales y quieren ordenar impuestos, estructura y proyección. Revisamos tu caso y te decimos si te conviene seguir como persona natural o dar el paso a una sociedad (<a href="/sociedades-de-profesionales/">lee más sobre sociedades de profesionales</a>).</p>'),
        ],
        hero_img=("/assets/consultoria-pymes.webp", "Dos personas revisando gráficos financieros impresos en una reunión de consultoría"))


def contabilidad():
    body = """
          <h2>Contador para pymes: contabilidad ordenada y al día</h2>
          <p>Nos encargamos de que tu contabilidad cumpla con la normativa y, además, te sirva para gestionar. Para empresas en crecimiento combinamos contabilidad con asesoría financiera, algo que los servicios básicos de bajo costo no incluyen.</p>
          <ul class="checklist">
            <li>Contabilidad mensual.</li>
            <li>Estados financieros bajo IFRS.</li>
            <li>Asesoría contable permanente.</li>
            <li>Remuneraciones y apoyo básico en recursos humanos.</li>
            <li>Acompañamiento en trámites presenciales (notaría, SII).</li>
          </ul>
          <div class="callout"><p>Atención de lunes a viernes, de 9:00 a 18:00. Presencial, videollamada, WhatsApp y correo.</p></div>
"""
    faq = [
        ("¿Cuánto cobra un contador por una pyme?",
         "El valor depende de la cantidad de movimientos, empleados y el nivel de asesoría que necesites. Te enviamos una cotización por escrito después de conocer tu caso; la primera consulta tiene costo."),
        ("¿Pueden llevar mi contabilidad si la atiendo desde otra ciudad?",
         "Sí, trabajamos online con empresas de todo el país."),
        ("¿Qué diferencia hay entre un servicio de contabilidad básico y el de IPCA?",
         "Además de mantener tu contabilidad al día, te ayudamos a interpretar los números y planificar. Cuando tu empresa lo necesita, sumamos consultoría financiera."),
        ("¿Pueden ayudarme a iniciar actividades?",
         "Sí. Te orientamos en el inicio de actividades y en dejar tu contabilidad configurada desde el comienzo."),
    ]
    return service_page(
        "/contabilidad-pymes/",
        "Contador para pymes y emprendedores en Villa Alemana | IPCA",
        "Contabilidad mensual, estados financieros y asesoría contable para pymes y emprendedores. Contador en Villa Alemana y online. Agenda una reunión.",
        "Contabilidad para pymes",
        "Contabilidad para pymes y emprendedores",
        "Contabilidad mensual, estados financieros y asesoría permanente para empresas que quieren crecer con orden, en Villa Alemana y online.",
        body, faq, "¿Necesitas un contador?", "Cuéntanos sobre tu empresa y te enviamos una propuesta clara.",
        cards_heading="Contabilidad a tu medida",
        cards=[
            ("Contabilidad para emprendedores", "<p>Si estás iniciando actividades, te ayudamos a partir con el pie derecho: elegir bien el régimen, dejar tu contabilidad al día desde el primer mes y evitar errores que después cuesta corregir.</p>"),
            ("Contabilidad online", "<p>Trabajamos 100 % a distancia si lo prefieres: videollamadas, WhatsApp y correo, con la misma atención personalizada. Atendemos empresas de todo Chile.</p>"),
            ("Contador en Villa Alemana", "<p>Somos un equipo con base en Villa Alemana y atendemos en la región de Valparaíso, Santiago y Salamanca, con visitas presenciales cuando se necesitan. Si buscas un contador cercano que además entienda de finanzas, escríbenos.</p>"),
        ])


def sociedades():
    body = """
          <h2>¿Qué es una sociedad de profesionales?</h2>
          <p>Es una forma de organizar la actividad de profesionales que prestan servicios de su especialidad a través de una sociedad, en lugar de hacerlo como personas naturales con boleta de honorarios. Tiene reglas propias ante el SII, y no sirve para cualquier independiente.</p>

          <h2>¿Cuándo conviene crear una sociedad de profesionales?</h2>
          <p>Suele evaluarse cuando la facturación es alta y sostenida, cuando hay varios socios o cuando se busca ordenar impuestos y la proyección del negocio. No es una decisión automática: depende de tu situación tributaria y de tus objetivos.</p>

          <h2>Requisitos y registro ante el SII</h2>
          <p>El SII establece condiciones específicas, por ejemplo respecto de quiénes pueden ser socios y de las actividades que la sociedad puede realizar. Revisamos tu caso antes de iniciar cualquier trámite para evitar que luego la figura no sea aceptada.</p>

          <h2>¿Persona natural o sociedad?</h2>
          <p>Boleta de honorarios y sociedad son caminos distintos, con ventajas y costos distintos. Comparamos ambos escenarios con tus cifras reales y te recomendamos el que más te conviene, incluso si es seguir como estás.</p>

          <h2>Constitución de sociedades</h2>
          <p>Si decides avanzar, te acompañamos en la constitución, el inicio de actividades y la puesta en marcha de la contabilidad. Atendemos en la región de Valparaíso y Santiago, y online.</p>
          <div class="callout"><p>Esta página es informativa y no reemplaza una evaluación de tu caso. Agenda una reunión y revisamos si la figura aplica para ti.</p></div>
"""
    faq = [
        ("¿Cualquier profesional independiente puede formar una sociedad de profesionales?",
         "No. La figura tiene requisitos específicos ante el SII. Revisamos tu situación antes de recomendarla."),
        ("¿Ustedes se encargan de la constitución?",
         "Sí, te acompañamos en el proceso de constitución y en la puesta en marcha contable de la sociedad."),
        ("¿Cuánto demora y cuánto cuesta?",
         "Depende del tipo de sociedad y de tu caso. Tras la primera reunión te enviamos una propuesta con plazos y valores."),
        ("¿Puedo atenderme online?",
         "Sí. Podemos hacer el proceso por videollamada, correo y WhatsApp, con acompañamiento presencial si hace falta."),
    ]
    return service_page(
        "/sociedades-de-profesionales/",
        "Sociedad de profesionales: cuándo conviene | IPCA",
        "Qué es una sociedad de profesionales, cuándo conviene, requisitos ante el SII y cómo constituirla. Asesoría en Villa Alemana y online.",
        "Sociedades de profesionales",
        "Sociedad de profesionales: cuándo conviene y cómo constituirla",
        "Te explicamos qué es, qué requisitos exige el SII y si tiene sentido para tu caso. Si avanzas, te acompañamos en la constitución.",
        body, [(q, a) for q, a in faq], "¿Te conviene una sociedad?", "Comparamos tus cifras como persona natural y como sociedad.")


def contacto():
    path = "/contacto/"
    h = head("Contacto: agenda una reunión | IPCA Consultores",
             "Agenda una reunión con IPCA Consultores. Escríbenos por formulario, WhatsApp o correo. Villa Alemana y atención online.",
             path, breadcrumb_ld("Contacto", path)) + header(path)
    h += f"""
  <main id="main">
    <div class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / Contacto</nav>
        <h1>Conversemos sobre tu empresa</h1>
        <p class="lead">Cuéntanos qué necesitas y te respondemos a la brevedad, en horario hábil. La primera consulta es una reunión de diagnóstico con costo.</p>
      </div>
    </div>

    <section>
      <div class="container contact-grid">
        <form class="form" action="https://api.web3forms.com/submit" method="POST">
          <input type="hidden" name="access_key" value="acc18df3-3e96-453a-aa84-b144d0ee0dfc">
          <input type="hidden" name="subject" value="Nuevo mensaje desde ipca.cl">
          <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
          <div class="field"><label for="name">Nombre</label><input id="name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="email">Correo electrónico</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="phone">Teléfono (opcional)</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="service">¿Qué te interesa?</label>
            <select id="service" name="service">
              <option>Consultoría financiera</option>
              <option>Contabilidad para pymes</option>
              <option>Sociedad de profesionales</option>
              <option>Otro / no estoy seguro</option>
            </select>
          </div>
          <div class="field"><label for="message">Mensaje</label><textarea id="message" name="message" required></textarea></div>
          <div class="consent">
            <input id="consent" name="consent" type="checkbox" value="Acepto la política de privacidad" required>
            <label for="consent">He leído la <a href="/privacidad/">política de privacidad</a> y acepto que IPCA use mis datos para responder esta consulta.</label>
          </div>
          <button class="btn btn-primary" type="submit">Enviar mensaje</button>
        </form>

        <div>
          <h2>Otras formas de contactarnos</h2>
          <ul class="contact-list">
            <li><strong>WhatsApp</strong><a href="{WA}">{PHONE_DISPLAY}</a></li>
            <li><strong>Correo</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><strong>Horario</strong>Lunes a viernes, 9:00 a 18:00</li>
            <li><strong>Dónde atendemos</strong>Villa Alemana y alrededores, región de Valparaíso, Santiago y Salamanca. Online al resto del país.</li>
          </ul>
        </div>
      </div>
    </section>
  </main>
"""
    return h + FOOTER


def privacidad():
    path = "/privacidad/"
    h = head("Política de privacidad | IPCA Consultores",
             "Cómo IPCA Consultores usa los datos que envías por el formulario, WhatsApp o correo: qué recibimos, para qué, con quién y cómo pedir su eliminación.",
             path, breadcrumb_ld("Política de privacidad", path)) + header(path)
    h += f"""
  <main id="main">
    <div class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / Política de privacidad</nav>
        <h1>Política de privacidad</h1>
        <p class="lead">Aquí te explicamos, en simple, qué datos recibimos cuando nos escribes, para qué los usamos y cómo puedes pedir que los corrijamos o eliminemos.</p>
      </div>
    </div>

    <section>
      <div class="container">
        <div class="prose">
          <p><small>Última actualización: noviembre de 2026.</small></p>

          <h2>Quién es responsable</h2>
          <p>IPCA Consultores, con base en Villa Alemana, Chile. Puedes escribirnos a <a href="mailto:{EMAIL}">{EMAIL}</a> para cualquier consulta sobre tus datos.</p>

          <h2>Qué datos recibimos</h2>
          <p>Solo los que tú nos entregas al contactarnos:</p>
          <ul>
            <li>Por el formulario del sitio: nombre, correo electrónico, teléfono (opcional), el servicio que te interesa y tu mensaje.</li>
            <li>Por WhatsApp o correo: tu número o dirección de correo y lo que nos cuentes en la conversación.</li>
          </ul>
          <p>Te pedimos que no incluyas en el mensaje datos sensibles ni información bancaria. Si hace falta compartir documentos de tu empresa, lo coordinamos después, por un canal adecuado.</p>

          <h2>Para qué los usamos</h2>
          <ul>
            <li>Responder tu consulta y coordinar una reunión.</li>
            <li>Enviarte una propuesta de trabajo, si la pides.</li>
          </ul>
          <p>No usamos tus datos para enviarte publicidad masiva ni los vendemos a terceros.</p>

          <h2>Con quién se comparten</h2>
          <ul>
            <li><strong>Web3Forms:</strong> servicio externo que recibe lo que escribes en el formulario y lo entrega a nuestro correo. Sus servidores pueden estar fuera de Chile.</li>
            <li><strong>WhatsApp (Meta):</strong> si nos escribes por ahí, la conversación se rige también por las condiciones de WhatsApp.</li>
            <li><strong>Tu proveedor de correo y el nuestro:</strong> por donde viajan los correos.</li>
            <li><strong>Google Fonts:</strong> el sitio carga sus tipografías desde Google, por lo que Google recibe tu dirección IP al abrir una página.</li>
          </ul>
          <p>Fuera de eso, solo compartiríamos tus datos si una autoridad competente nos lo exige.</p>

          <h2>Cookies y herramientas de seguimiento</h2>
          <p>Este sitio no usa cookies propias ni herramientas de analítica o publicidad. Si esto cambia, actualizaremos esta página y te lo informaremos con un aviso en el sitio.</p>

          <h2>Cuánto tiempo los guardamos</h2>
          <p>El tiempo necesario para atender tu consulta y, si pasas a ser cliente, durante la relación de trabajo y los plazos que exija la ley. Si no se concreta un trabajo, puedes pedir que eliminemos tu mensaje en cualquier momento.</p>

          <h2>Tus derechos</h2>
          <p>Puedes pedirnos acceder a tus datos, corregirlos, eliminarlos u oponerte a que los usemos. Escríbenos a <a href="mailto:{EMAIL}">{EMAIL}</a> indicando qué necesitas; respondemos en un plazo razonable, en horario hábil.</p>

          <h2>Cambios en esta política</h2>
          <p>Si cambiamos algo importante, actualizaremos la fecha de arriba y el contenido de esta página.</p>

          <div class="callout"><p>¿Dudas sobre tus datos? Escríbenos a <a href="mailto:{EMAIL}">{EMAIL}</a> o por <a href="{WA}">WhatsApp</a>.</p></div>
        </div>
      </div>
    </section>
  </main>
"""
    return h + FOOTER


def not_found():
    h = head("Página no encontrada | IPCA Consultores", "La página que buscas no existe.", "/404.html",
             '  <meta name="robots" content="noindex">\n').replace(
        '<meta name="robots" content="index, follow">\n', "")
    h += header() + f"""
  <main id="main">
    <div class="container error-page">
      <div class="code">404</div>
      <h1>No encontramos esa página</h1>
      <p class="lead" style="margin-inline:auto">Puede que el enlace haya cambiado. Desde aquí puedes volver al inicio o ir directo a un servicio.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/">Volver al inicio</a>
        <a class="btn btn-outline" href="/contacto/">Contacto</a>
      </div>
    </div>
  </main>
"""
    return h + FOOTER


# Páginas de error del servidor: una sola plantilla, cambia el código y el mensaje.
ERRORS = {
    "500": ("Algo falló de nuestro lado", "Error interno del servidor",
            "Tuvimos un problema al cargar la página. Prueba de nuevo en unos minutos; si sigue pasando, escríbenos y lo revisamos."),
    "502": ("No pudimos conectar con el servidor", "Mala puerta de enlace",
            "La conexión con el servidor falló por un momento. Intenta recargar en unos minutos; si sigue igual, escríbenos."),
    "503": ("Estamos en mantenimiento", "Servicio no disponible",
            "El sitio no está disponible por ahora, quizás por mantenimiento. Vuelve en unos minutos. Mientras tanto, puedes escribirnos."),
    "504": ("El servidor tardó demasiado en responder", "Tiempo de espera agotado",
            "La página demoró más de lo normal en responder. Intenta de nuevo en unos minutos o escríbenos."),
}


def server_error(code):
    h1, meta_title, lead = ERRORS[code]
    h = head(f"Error {code}: {meta_title} | IPCA Consultores", lead, f"/{code}.html",
             '  <meta name="robots" content="noindex">\n').replace(
        '<meta name="robots" content="index, follow">\n', "")
    h += header() + f"""
  <main id="main">
    <div class="container error-page">
      <div class="code">{code}</div>
      <h1>{h1}</h1>
      <p class="lead" style="margin-inline:auto">{lead}</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/">Volver al inicio</a>
        <a class="btn btn-outline" href="{WA}">Escribir por WhatsApp</a>
      </div>
      <p class="error-note">También puedes escribirnos a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
  </main>
"""
    return h + FOOTER


def relativize(html, rel):
    """Convierte rutas que empiezan con / en rutas relativas a la página.

    Así la demo funciona también en GitHub Pages, donde el sitio vive en
    /ipca_demo/ y no en la raíz del dominio. No toca URLs absolutas (https://).
    """
    prefix = "../" * rel.count("/") or "./"

    def fix(u):
        u = u.strip()
        return prefix + u[1:] if u.startswith("/") and not u.startswith("//") else u

    def attr(m):
        name, val = m.group(1), m.group(2)
        if name == "srcset":
            val = ", ".join(" ".join([fix(parts[0])] + parts[1:]) for parts in (p.split() for p in val.split(",") if p.strip()))
        else:
            val = fix(val)
        return f'{name}="{val}"'

    return re.sub(r'\b(href|src|srcset)="([^"]*)"', attr, html)


def write(rel, content):
    if rel.endswith(".html"):
        content = relativize(content, rel)
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("escrito", rel)


def sitemap():
    urls = ["/", "/consultoria-financiera/", "/contabilidad-pymes/", "/sociedades-de-profesionales/", "/contacto/", "/privacidad/"]
    prio = {"/": "1.0", "/contacto/": "0.5", "/privacidad/": "0.3"}
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        x += f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{date.today().isoformat()}</lastmod>\n    <priority>{prio.get(u, '0.8')}</priority>\n  </url>\n"
    return x + "</urlset>\n"


if __name__ == "__main__":
    write("index.html", home())
    write("consultoria-financiera/index.html", consultoria())
    write("contabilidad-pymes/index.html", contabilidad())
    write("sociedades-de-profesionales/index.html", sociedades())
    write("contacto/index.html", contacto())
    write("privacidad/index.html", privacidad())
    write("404.html", not_found())
    for code in ERRORS:
        write(f"{code}.html", server_error(code))
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n") if not (ROOT / "robots.txt").exists() else None
