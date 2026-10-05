"""Generate the README and static GitHub Pages catalog from data/projects.json.

Requires Python 3.10+ and only the standard library.
"""
import json, pathlib, html, collections, datetime
out = pathlib.Path(__file__).resolve().parents[1]
catalog = json.loads((out/'data'/'projects.json').read_text(encoding='utf-8'))
projects = catalog['projects']
featured_order = {name: index for index, name in enumerate(catalog.get('featured_order', []))}
featured_projects = sorted((p for p in projects if p['featured']), key=lambda p: featured_order.get(p['repository'], len(featured_order)))
groups = []
for p in projects:
    key = [p['degree'], p['year'], p['subject']]
    existing = next((g for g in groups if g[:3] == key), None)
    if existing is None:
        groups.append(key + [[p['repository']]])
    else:
        existing[3].append(p['repository'])
date = datetime.date.fromisoformat(catalog['updated'])
months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
formatted_date = f'{date.day} de {months[date.month-1]} de {date.year}'
def write(path,text):
 f=out/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf-8')
count=collections.Counter(p['degree'] for p in projects)
private=sum(p['visibility']=='private' for p in projects)
def repo_link(p):return '['+p['title']+']('+p['url']+')'+(' · 🔒 Privado' if p['visibility']=='private' else '')
lines=['<div align="center">','', '<img src="assets/banner.svg" alt="Marcos Caballero · Proyectos académicos · Ingeniería Informática e Inteligencia Artificial" width="100%" />','', '# Proyectos académicos','', '**Grado en Ingeniería Informática · UC3M**  ', '**Máster en Inteligencia Artificial · UNIR**','', '[Explorar la página](https://cabamarcos.github.io/academic-projects/) · [Mi perfil de GitHub](https://github.com/cabamarcos)','', f'**{len(projects)} entradas principales** · **{len(groups)} asignaturas, TFG y TFM** · **2 titulaciones**','', '</div>','', 'Una recopilación de mis prácticas, proyectos en equipo y trabajos de investigación: desde lógica digital, sistemas y desarrollo de software hasta aprendizaje automático, visión artificial y procesamiento del lenguaje natural.','', 'Cada entrada enlaza al repositorio que contiene el código, los cuadernos y la documentación. Las descripciones resumen el contenido de los proyectos; las prácticas conservan su contexto académico y su fase de desarrollo.','', '> 🔒 Los repositorios privados aparecen identificados y requieren acceso en GitHub. El catálogo reúne sus referencias, sin publicar su código.','', '## Proyectos destacados','', '| Proyecto | Qué encontrarás | Tecnologías |','| --- | --- | --- |']
for p in featured_projects:
 lines.append(f"| {repo_link(p)} | {p['description']} | {' · '.join(p['technologies'])} |")
lines+=['','## Índice','', '- [Grado en Ingeniería Informática · UC3M](#grado-uc3m)','  - [1.º curso](#uc3m-1) · [2.º curso](#uc3m-2) · [3.º curso](#uc3m-3) · [4.º curso y TFG](#uc3m-4)','- [Máster en Inteligencia Artificial · UNIR](#master-unir)','- [Repositorios alternativos y procedencia](#procedencia)','- [Pendiente de incorporar](#pendiente)','- [Cómo actualizar el catálogo](#actualizar)','', '<a id="grado-uc3m"></a>','## Grado en Ingeniería Informática · UC3M','', f'**Universidad Carlos III de Madrid** · {count["UC3M"]} entradas principales.','']
for year in range(1,5):
 lines +=[f'<a id="uc3m-{year}"></a>',f'### {year}.º curso'+(' y trabajo de fin de grado' if year==4 else ''),'']
 for degree,y,subject,names in groups:
  if degree!='UC3M' or y!=year:continue
  lines +=[f'#### {subject}','', '| Proyecto | Descripción | Tecnologías |','| --- | --- | --- |']
  for p in projects:
   if p['degree']==degree and p['year']==y and p['subject']==subject:
    note=' **'+p['note']+'**' if p.get('note') else ''
    lines.append(f"| {repo_link(p)} | {p['description']}{note} | {' · '.join(p['technologies'])} |")
  lines+=['']
lines+=['<a id="master-unir"></a>','## Máster en Inteligencia Artificial · UNIR','',f'**Universidad Internacional de La Rioja** · {count["UNIR"]} entradas principales.','']
for degree,y,subject,names in groups:
 if degree!='UNIR':continue
 lines +=[f'### {subject}','','| Proyecto | Descripción | Tecnologías |','| --- | --- | --- |']
 for p in projects:
  if p['degree']==degree and p['subject']==subject:lines.append(f"| {repo_link(p)} | {p['description']} | {' · '.join(p['technologies'])} |")
 lines+=['']
lines +=['<a id="procedencia"></a>','## Repositorios alternativos y procedencia','', 'El índice usa una sola entrada para cada uno de los dos proyectos que tenían una copia pública y un fork privado. Los originales se conservan como referencia del trabajo en equipo.','', '| Entrada principal | Repositorio original | Motivo de la elección |','| --- | --- | --- |','| [FluidSimulator](https://github.com/cabamarcos/FluidSimulator) | [Proyecto_arqui](https://github.com/cabamarcos/Proyecto_arqui) · 🔒 Privado | Los 22 archivos de la copia pública coinciden con el fork. El original conserva también configuración de estilo y análisis estático. |','| [VideoFlix](https://github.com/cabamarcos/VideoFlix) | [P2_ubicuos](https://github.com/cabamarcos/P2_ubicuos) · 🔒 Privado | Versión pública posterior, con ajustes en la interfaz y el servidor; el fork conserva el desarrollo de equipo. |','', '[procesadores_lenguaje](https://github.com/cabamarcos/procesadores_lenguaje) reúne las prácticas de analizadores y el desarrollo del traductor; [CtoLisp](https://github.com/cabamarcos/CtoLisp) presenta por separado el proyecto final. Ambos tienen su propia entrada.','', 'Las autorías, licencias y créditos se consultan en cada repositorio original.','', '<a id="pendiente"></a>','## Pendiente de incorporar','', '| Titulación | Asignatura o trabajo | Próxima actualización |','| --- | --- | --- |']
for p in catalog['pending']:lines.append(f"| {p['degree']} | {p['subject']} | {p['description']} |")
lines+=['', '<a id="actualizar"></a>','## Cómo actualizar el catálogo','', 'El contenido del README y de la página nace de una única fuente: [`data/projects.json`](data/projects.json). Para añadir un proyecto o una entrega, o cambiar su enlace:','', '1. Editar los datos del proyecto en ese archivo.','2. Ejecutar `python scripts/generate.py`.','3. Revisar y subir los cambios; GitHub Pages publica el contenido de `docs/`.','', 'El generador solo necesita Python 3 y su biblioteca estándar. La página es estática y no requiere instalar dependencias.','', '---','', '**Marcos Caballero Cortés** · [@cabamarcos](https://github.com/cabamarcos)  ', f'Última revisión del catálogo: **{formatted_date}**.','']
write(pathlib.Path('README.md'),'\n'.join(lines))
write(pathlib.Path('assets/banner.svg'),f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="280" viewBox="0 0 1280 280" role="img" aria-label="Marcos Caballero: proyectos académicos de UC3M y UNIR"><rect width="1280" height="280" rx="18" fill="#081e36"/><path d="M44 228H1236" stroke="#35516c"/><rect x="44" y="38" width="6" height="139" fill="#37d4c3"/><g fill="#c0d6ea" font-family="Segoe UI,Arial,sans-serif"><text x="76" y="64" font-size="18" letter-spacing="4">MARCOS CABALLERO</text><text x="76" y="126" font-size="48" font-weight="700" fill="#ffffff">Proyectos académicos</text><text x="76" y="173" font-size="24">Ingeniería Informática · Inteligencia Artificial</text><text x="44" y="259" font-size="18">UC3M · Grado</text><text x="1236" y="259" text-anchor="end" font-size="18">UNIR · Máster</text></g><text x="1210" y="150" text-anchor="end" font-family="Segoe UI,Arial,sans-serif" font-size="80" font-weight="700" fill="#37d4c3">{len(projects)}</text></svg>''')
write(pathlib.Path('.gitignore'),'__pycache__/\n*.pyc\n.DS_Store\n')
write(pathlib.Path('docs/.nojekyll'),'')

def esc(value):
    return html.escape(str(value), quote=True)
def card(p):
    lock = '<span class="private">Privado</span>' if p['visibility'] == 'private' else ''
    tags = ''.join('<li>'+esc(t)+'</li>' for t in p['technologies'])
    note = '<p class="project-note">'+esc(p['note'])+'</p>' if p.get('note') else ''
    alts = ''.join('<p class="alternatives">Fork original: <a href="'+esc(a['url'])+'">'+esc(a['repository'])+'</a> · privado</p>' for a in p.get('alternatives',[]))
    searchable = ' '.join([p['title'],p['repository'],p['description'],p['subject'],*p['technologies']])
    return f'<article class="project" data-degree="{esc(p["degree"])}" data-year="{p["year"] or ""}" data-search="{esc(searchable)}"><p class="repo-name">{esc(p["repository"])}</p><h4><a href="{esc(p["url"])}">{esc(p["title"])}</a>{lock}</h4><p class="description">{esc(p["description"])}</p>{note}<ul class="tags" aria-label="Tecnologías">{tags}</ul>{alts}</article>'
sections = []
for degree, year in [('UC3M',1),('UC3M',2),('UC3M',3),('UC3M',4),('UNIR',None)]:
    selected = [p for p in projects if p['degree']==degree and p['year']==year]
    ident = 'unir' if degree=='UNIR' else f'uc3m-{year}'
    title = 'Máster en Inteligencia Artificial' if degree=='UNIR' else f'{year}.º curso'+(' y TFG' if year==4 else '')
    institution = 'UNIR' if degree=='UNIR' else 'UC3M · Ingeniería Informática'
    subjects = list(dict.fromkeys(p['subject'] for p in selected))
    pieces = []
    for subject in subjects:
        subject_cards = ''.join(card(p) for p in selected if p['subject']==subject)
        pieces.append('<section class="subject"><h3>'+esc(subject)+'</h3><div class="project-grid">'+subject_cards+'</div></section>')
    sections.append(f'<section class="course" id="{ident}"><div class="course-title"><h2>{esc(title)}</h2><span>{esc(institution)}</span></div>'+''.join(pieces)+'</section>')
featured = ''.join(f'<a class="feature" href="{esc(p["url"])}"><small>{esc(p["degree"])} · {"TFG" if p["repository"]=="SuperMask" else esc(p["subject"])}</small><h3>{esc(p["title"])}</h3><span>{esc(p["technologies"][0])}</span></a>' for p in featured_projects)
pending = ''.join('<article class="pending-item"><small>'+esc(p['degree'])+'</small><h3>'+esc(p['subject'])+'</h3><p>'+esc(p['description'])+'</p></article>' for p in catalog['pending'])
page = (out/'scripts'/'page-template.html').read_text(encoding='utf-8')
for key, value in {'TOTAL':len(projects),'SUBJECTS':len(groups),'PRIVATE':private,'FEATURED':featured,'ENTRIES':''.join(sections),'PENDING':pending,'UPDATED':formatted_date}.items():
    page = page.replace('{{'+key+'}}',str(value))
write(pathlib.Path('docs/index.html'), page)
print(f'Generated {len(projects)} catalog entries in README.md and docs/index.html.')
