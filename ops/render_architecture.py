"""Generate the two ArchView documents and set readable diagram positions."""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "docs" / "architecture"
SKILL = Path.home() / ".codex" / "skills" / "archview" / "scripts"
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

LAYOUTS = {
    "arch-system": {
        "size": (1540, 720),
        "groups": {"g1": (20, 220, 330, 220), "g2": (20, 0, 330, 185),
                   "g3": (430, 0, 700, 630), "g4": (1180, 0, 300, 220),
                   "g5": (1180, 270, 300, 390)},
        "nodes": {"n1": (100, 315), "n2": (265, 315), "n3": (185, 85),
                  "n4": (540, 115), "n5": (540, 315), "n6": (755, 315),
                  "n7": (1010, 315), "n8": (665, 485), "n9": (995, 485),
                  "n10": (1330, 105), "n11": (1330, 370), "n12": (1330, 550)},
        "routes": {
            "e2": ([(225, 100), (300, 180), (300, 245), (265, 275)], (292, 203)),
            "e3": ([(305, 290), (400, 245), (500, 135)], (403, 200)),
            "e7": ([(985, 355), (985, 410), (665, 410), (665, 445)], (800, 400)),
            "e8": ([(1030, 355), (1030, 445)], (1080, 422)),
            "e9": ([(515, 355), (515, 600), (995, 600), (995, 525)], (745, 590)),
            "e10": ([(550, 355), (625, 465)], (574, 425)),
            "e11": ([(1050, 285), (1150, 155), (1290, 115)], (1130, 184)),
            "e12": ([(1050, 325), (1290, 370)], (1168, 341)),
            "e13": ([(1330, 510), (1330, 410)], (1395, 465)),
        },
    },
    "arch-assessment": {
        "size": (1480, 790),
        "groups": {"g1": (0, 0, 400, 495), "g2": (450, 0, 550, 720),
                   "g3": (1050, 0, 370, 720)},
        "nodes": {"n1": (100, 125), "n2": (100, 345), "n3": (285, 235),
                  "n4": (550, 110), "n5": (780, 110), "n6": (900, 305),
                  "n7": (550, 365), "n8": (780, 535), "n9": (1140, 130),
                  "n10": (1330, 305), "n11": (1140, 475), "n12": (1330, 625)},
        "routes": {"e8": ([(820, 535), (1025, 535), (1025, 130), (1100, 130)], (920, 525))},
        "labels": {"e5": (880, 230), "e7": (675, 480), "e9": (1305, 225),
                   "e10": (1185, 390), "e11": (1285, 575)},
    },
}


def border_point(start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    scale = 40 / max(abs(dx), abs(dy))
    return start[0] + dx * scale, start[1] + dy * scale


def render(name, layout):
    subprocess.run(["node", str(SKILL / "create-archview.js"),
                    str(VIEWS / (name + ".json")), str(VIEWS)], cwd=SKILL, check=True)
    target = VIEWS / (name + ".html")
    html = target.read_text(encoding="utf-8")
    match = re.search(r'<svg id="graph"[\s\S]*?</svg>', html)
    svg = ET.fromstring(match.group())
    graph = list(svg)[1]
    graph.set("transform", "translate(30,30)")
    svg.set("viewBox", f"0 0 {layout['size'][0]} {layout['size'][1]}")
    nodes, groups = layout["nodes"], layout["groups"]
    routes = dict(layout["routes"])
    for element in svg.iter():
        tag, identity = element.tag.rsplit("}", 1)[-1], element.get("id")
        if tag == "path" and element.get("source"):
            start, end = nodes[element.get("source")], nodes[element.get("target")]
            points, label = routes.get(identity, ([border_point(start, end), border_point(end, start)],
                                                   ((start[0]+end[0])/2, (start[1]+end[1])/2-12)))
            routes[identity] = (points, layout.get("labels", {}).get(identity, label))
            element.set("d", "M " + " L ".join(f"{x:g} {y:g}" for x, y in points))
        elif tag == "rect" and identity in groups:
            for key, value in zip(("x", "y", "width", "height"), groups[identity]):
                element.set(key, str(value))
        elif tag == "image" and identity in nodes:
            x, y = nodes[identity]
            element.set("x", str(x-40))
            element.set("y", str(y-40))
        elif tag == "text":
            index = int(element.get("index", 0))
            if identity in nodes:
                x, y = nodes[identity][0], nodes[identity][1] + 64 + index * 17
            elif identity in groups:
                x, y = groups[identity][0] + 10, groups[identity][1] + 28 + index * 18
            elif identity in routes:
                x, y = routes[identity][1]
            else:
                continue
            element.set("x", str(x))
            element.set("y", str(y))
    html = html[:match.start()] + ET.tostring(svg, encoding="unicode") + html[match.end():]
    nav = '<nav class="view-nav"><a href="arch-system.html">System</a><a href="arch-assessment.html">Assessment</a><a href="02_TECHNICAL_BLUEPRINT.md">Blueprint</a><span>Approved design | Not implemented</span></nav>'
    style = '<style>.view-nav{display:flex;gap:20px;align-items:center;padding:10px 18px;background:#edf3f8;font-size:14px}.view-nav a{color:#12476b}.view-nav span{margin-left:auto;color:#465467}.topbar{min-height:28px}p{font-size:14px;line-height:1.55;margin:8px 18px}h4{font-size:20px}#graph{max-width:1600px;margin:auto}.edge{stroke:#617487;stroke-width:1.4}svg text:not(.title){paint-order:stroke;stroke:white;stroke-width:2px;stroke-linejoin:round}@media(max-width:650px){.view-nav{gap:12px;flex-wrap:wrap}.view-nav span{margin-left:0}}</style><link rel="icon" href="data:,">'
    html = html.replace("</head>", style + "</head>", 1).replace('<div class="ss">', nav + '<div class="ss">', 1)
    target.write_text(html, encoding="utf-8")
    assert len(list(svg.iter("{http://www.w3.org/2000/svg}image"))) == len(nodes)
    print(f"Verified {name}: {len(nodes)} nodes, {len(routes)} edges")


if __name__ == "__main__":
    for name, layout in LAYOUTS.items():
        render(name, layout)
