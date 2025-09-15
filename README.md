
# udp-cursos

Plantilla rápida para publicar un sitio con **MkDocs (Material)** en **GitHub Pages**.

## Requisitos locales (opcional)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve  # http://127.0.0.1:8000
```

## Estructura
```
.
├── .github/workflows/deploy.yml   # CI para publicar el sitio
├── docs/                          # Contenido del sitio
│   ├── index.md
│   ├── about.md
│   └── ramos/
│       ├── econometria.md
│       ├── microeconomia.md
│       └── macroeconomia.md
├── mkdocs.yml                     # Configuración del sitio
├── requirements.txt
└── .gitignore
```

## Publicación
Al hacer *push* a la rama `main`, GitHub Actions construye el sitio y lo publica en la rama `gh-pages`.
Activa **Settings → Pages → Build and deployment → Source: GitHub Actions** si no queda activado automáticamente.
