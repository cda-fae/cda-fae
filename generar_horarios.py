"""
Genera tablas de horario tipo Excel en las páginas de cada tutor.
Ejecutar desde la carpeta udp_cursos_site.
"""
import re, os

BASE = "docs/tutorias"
BLOCKS = [
    "8:30 – 9:50",
    "10:00 – 11:20",
    "11:30 – 12:50",
    "13:00 – 14:20",
    "14:30 – 15:50",
    "16:00 – 17:20",
    "17:30 – 18:50",
]
DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

P = "P"   # presencial
O = "O"   # online

# ── Construcción del grid (7 bloques × 5 días) ──────────────────────────────
def grid(spec: dict) -> list:
    """spec: {'L':[(bloque, tipo), ...], 'Ma':..., 'Mi':..., 'J':..., 'V':...}"""
    g = [[None]*5 for _ in range(7)]
    col = {"L": 0, "Ma": 1, "Mi": 2, "J": 3, "V": 4}
    for day, slots in spec.items():
        c = col[day]
        for (b, t) in slots:
            g[b][c] = t
    return g

# ── Definición de horarios ────────────────────────────────────────────────────

# A — Javiera Morgado
A = grid({"Ma": [(2,O),(3,O)], "Mi": [(5,P)], "J": [(2,O),(3,O)], "V": [(4,O)]})

# B — Marcela Robles
B = grid({
    "L":  [(1,P),(4,P),(5,P)],
    "Ma": [(3,P),(4,P),(5,P)],
    "Mi": [(4,P),(5,P)],
    "J":  [(3,P),(4,P),(5,P)],
    "V":  [(2,P),(3,P),(4,P),(5,P)],
})

# C — Abraham Huerta  (+nota online 19:00)
C = grid({
    "L":  [(0,P),(2,P),(3,P)],
    "Ma": [(0,P),(3,P),(4,P)],
    "J":  [(0,P),(3,P),(4,P)],
    "V":  [(0,P),(1,P),(2,P),(3,P)],
})

# D — Camila González
D = grid({
    "L":  [(2,P),(4,P)],
    "Ma": [(3,P)],
    "Mi": [(2,P)],
    "J":  [(4,P)],
    "V":  [(2,P),(3,P),(5,P)],
})

# E — Francisco Ulloa
E = grid({
    "L":  [(0,P),(3,P),(4,P),(6,P)],
    "Ma": [(5,P),(6,P)],
    "Mi": [(0,P),(3,P),(4,P),(5,P),(6,P)],
    "J":  [(3,P),(5,P)],
    "V":  [(0,P),(1,P),(3,P),(4,P),(5,P),(6,P)],
})

# F — Maximiliano Stuardo
F = grid({
    "L":  [(0,P),(1,P)],
    "Ma": [(0,P),(1,P),(4,P),(5,P)],
    "Mi": [(0,P),(5,P),(6,P)],
    "J":  [(0,P),(1,P),(3,P),(4,P),(5,P),(6,P)],
    "V":  [(0,P),(1,P),(2,P),(3,P),(4,P),(5,P)],
})

# G — Dhalmar Ovando
G = grid({
    "L":  [(0,P),(1,P),(3,P),(4,P),(6,P)],
    "Ma": [(5,P),(6,P)],
    "Mi": [(0,P),(1,P),(3,P)],
    "J":  [(3,P),(5,P)],
    "V":  [(0,P),(1,P),(3,P),(4,P),(5,P)],
})

# H — Antonia Soto
H = grid({
    "L":  [(1,P),(5,P)],
    "Ma": [(2,P),(5,P)],
    "Mi": [(1,P),(2,P)],
    "V":  [(1,P),(2,P),(3,P),(4,P)],
})

# I — Martina Ramirez  (+nota online 20:00)
I_ = grid({
    "L":  [(1,P),(2,P)],
    "Ma": [(4,P)],
    "Mi": [(2,P)],
    "J":  [(3,P)],
    "V":  [(2,P)],
})

# J — Catalina Martinez
J_ = grid({
    "L":  [(3,P),(5,P),(6,P)],
    "Ma": [(2,P),(3,P)],
    "Mi": [(3,P),(5,P)],
    "J":  [(2,P),(3,P)],
    "V":  [(2,P),(5,P)],
})

# K — Joakina Quezada
K = grid({
    "L":  [(5,P)],
    "Ma": [(2,P),(3,P)],
    "Mi": [(4,P),(5,P)],
    "J":  [(4,P)],
    "V":  [(2,P),(3,P),(4,P),(5,P)],
})

# L — Luis Briceño
L_ = grid({
    "L":  [(3,P),(5,P)],
    "Ma": [(2,P)],
    "Mi": [(3,P),(5,P)],
    "J":  [(2,P),(3,P),(5,P)],
    "V":  [(3,P)],
})

# M — Camila Pasten  (todos los días después 11:30, menos miércoles)
M = grid({
    "L":  [(2,P),(3,P),(4,P),(5,P),(6,P)],
    "Ma": [(2,P),(3,P),(4,P),(5,P),(6,P)],
    "J":  [(2,P),(3,P),(4,P),(5,P),(6,P)],
    "V":  [(2,P),(3,P),(4,P),(5,P),(6,P)],
})

NOTE_19 = "\\* Disponible online a partir de las 19:00 hrs (todos los días)."
NOTE_20 = "\\* Disponible online a partir de las 20:00 hrs (todos los días)."

# ── Asignación archivo → (grid, nota) ────────────────────────────────────────
FILES = {
    "matematicas-1/tutores/tutor1.md": (A, None),
    "matematicas-1/tutores/tutor2.md": (B, None),
    "matematicas-1/tutores/tutor3.md": (C, NOTE_19),
    "matematicas-1/tutores/tutor4.md": (D, None),
    "matematicas-1/tutores/tutor6.md": (E, None),
    "matematicas-1/tutores/tutor9.md": (F, None),
    "matematicas-2/tutores/tutor1.md": (A, None),
    "matematicas-2/tutores/tutor2.md": (E, None),
    "matematicas-2/tutores/tutor3.md": (L_, None),
    "matematicas-2/tutores/tutor4.md": (D, None),
    "matematicas-2/tutores/tutor5.md": (G, None),
    "matematicas-2/tutores/tutor9.md": (H, None),
    "matematicas-3/tutores/tutor1.md": (G, None),
    "matematicas-3/tutores/tutor2.md": (L_, None),
    "matematicas-3/tutores/tutor3.md": (C, NOTE_19),
    "contabilidad-1/tutores/tutor1.md": (A, None),
    "contabilidad-1/tutores/tutor4.md": (M, None),
    "estadistica-1/tutores/tutor1.md":  (I_, NOTE_20),
    "estadistica-1/tutores/tutor3.md":  (D, None),
    "estadistica-2/tutores/tutor1.md":  (I_, NOTE_20),
    "estadistica-2/tutores/tutor2.md":  (C, NOTE_19),
    "estadistica-2/tutores/tutor3.md":  (J_, None),
    "finanzas-1/tutores/tutor2.md":     (L_, None),
    "macroeconomia-1/tutores/tutor3.md":(K, None),
    "macroeconomia-1/tutores/tutor5.md":(B, None),
    "macroeconomia-2/tutores/tutor3.md":(C, NOTE_19),
    "microeconomia-1/tutores/tutor1.md":(E, None),
    "microeconomia-1/tutores/tutor3.md":(K, None),
    "microeconomia-1/tutores/tutor4.md":(F, None),
    "microeconomia-2/tutores/tutor1.md":(L_, None),
    "microeconomia-2/tutores/tutor3.md":(F, None),
    "microeconomia-2/tutores/tutor4.md":(F, None),
    "programacion/tutores/tutor1.md":   (I_, NOTE_20),
    "programacion/tutores/tutor2.md":   (F, None),
    "programacion/tutores/tutor3.md":   (M, None),
}

# ── Generación del HTML de la tabla ──────────────────────────────────────────
C_HEAD  = "background-color:#D71920;color:#fff;padding:9px 8px;border:1px solid #a00;font-weight:700;text-align:center;"
C_LABEL = "background-color:#d9d9d9;font-weight:700;color:#222;border:1px solid #999;padding:6px 10px;white-space:nowrap;text-align:left;"
C_P     = "background-color:#70ad47;color:#fff;font-weight:700;border:1px solid #4e7c32;text-align:center;padding:6px;font-size:1rem;"
C_O     = "background-color:#2e75b6;color:#fff;font-weight:700;border:1px solid #1f527f;text-align:center;padding:6px;font-size:1rem;"
C_FREE  = "background-color:#fff;color:#ccc;border:1px solid #ddd;text-align:center;padding:6px;"
C_FREE2 = "background-color:#f5f5f5;color:#ccc;border:1px solid #ddd;text-align:center;padding:6px;"

def make_table(g: list, note) -> str:
    lines = []
    lines.append("Horarios disponibles para solicitar círculos:")
    lines.append("")
    lines.append(f'<table style="width:100%;border-collapse:collapse;border:2px solid #888;'
                 f'box-shadow:3px 3px 8px rgba(0,0,0,0.15);font-size:0.82rem;margin-top:0.5rem;">')
    lines.append("  <thead><tr>")
    lines.append(f'    <th style="{C_HEAD}">Horario</th>')
    for d in DAYS:
        lines.append(f'    <th style="{C_HEAD}">{d}</th>')
    lines.append("  </tr></thead>")
    lines.append("  <tbody>")
    for bi, block in enumerate(BLOCKS):
        even = bi % 2 == 1
        lines.append("    <tr>")
        lines.append(f'      <td style="{C_LABEL}">{block}</td>')
        for di in range(5):
            val = g[bi][di]
            if val == P:
                lines.append(f'      <td style="{C_P}">✓</td>')
            elif val == O:
                lines.append(f'      <td style="{C_O}">🌐</td>')
            else:
                c = C_FREE2 if even else C_FREE
                lines.append(f'      <td style="{c}">—</td>')
        lines.append("    </tr>")
    lines.append("  </tbody>")
    lines.append("</table>")
    lines.append("")
    # Leyenda
    lines.append('<div style="display:flex;gap:1rem;margin-top:0.5rem;font-size:0.78rem;flex-wrap:wrap;align-items:center;">')
    lines.append('  <span style="display:inline-flex;align-items:center;gap:6px;">'
                 '<span style="display:inline-block;width:16px;height:16px;background:#70ad47;border-radius:2px;border:1px solid #4e7c32;"></span>'
                 ' Disponible presencial</span>')
    lines.append('  <span style="display:inline-flex;align-items:center;gap:6px;">'
                 '<span style="display:inline-block;width:16px;height:16px;background:#2e75b6;border-radius:2px;border:1px solid #1f527f;"></span>'
                 ' Disponible online</span>')
    lines.append('  <span style="display:inline-flex;align-items:center;gap:6px;">'
                 '<span style="display:inline-block;width:16px;height:16px;background:#fff;border-radius:2px;border:1px solid #bbb;"></span>'
                 ' No disponible</span>')
    lines.append('</div>')
    if note:
        lines.append("")
        lines.append(note)
    return "\n".join(lines)

# ── Procesamiento de archivos ─────────────────────────────────────────────────
SCHEDULE_PATTERN = re.compile(
    r'((?:(?:Mis\s+)?[Hh]orarios?\s+(?:disponibles?|libres?)[^\n]*|[Tt]odo\s+los\s+d[ií]as[^\n]*|[Dd]isponibles?[^\n]*))\n.*?(?=\n##\s)',
    re.DOTALL
)

def process(rel_path: str, g: list, note):
    path = os.path.join(BASE, rel_path)
    if not os.path.exists(path):
        print(f"  ⚠ No encontrado: {path}")
        return False
    content = open(path, encoding="utf-8").read()
    table_html = make_table(g, note)
    new_content = SCHEDULE_PATTERN.sub(table_html, content)
    if new_content == content:
        print(f"  ⚠ Sin cambios (revisar patrón): {rel_path}")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  ✓ {rel_path}")
    return True

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ok = err = 0
    for rel, (g, note) in FILES.items():
        if process(rel, g, note):
            ok += 1
        else:
            err += 1
    print(f"\nResultado: {ok} actualizados, {err} con problemas.")
