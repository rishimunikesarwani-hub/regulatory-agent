"""Create the separate diagrams.net architecture with the installed skill."""
from pathlib import Path
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "docs" / "architecture"
BASE = VIEWS / "arch-regulatory-agent-component-v1"
SKILL = Path.home() / ".codex" / "skills" / "architecture-diagrams" / "scripts"
sys.path.insert(0, str(SKILL))
import generate_diagram
from lib.icon_catalog import CATALOG

# Resolve symbols against the installed draw.io library before rendering.
# The retrieval provider is undecided, so its server symbol is vendor-neutral.
CATALOG.update({
    "aws/general/Client": "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.client;",
    "neutral/Service": "shape=mxgraph.networks.server;html=1;aspect=fixed;verticalLabelPosition=bottom;verticalAlign=top;",
})
CATALOG["aws/storage/S3"] = CATALOG["aws/storage/S3"].replace("simple_storage_service_s3", "s3")
CATALOG["aws/integration/SQS"] = CATALOG["aws/integration/SQS"].replace("simple_queue_service", "sqs")


def add_text(root, identity, text, x, y, width, height, size=14):
    cell = ET.SubElement(root, "mxCell", {
        "id": identity, "value": text, "vertex": "1", "parent": "1",
        "style": f"text;html=0;whiteSpace=wrap;align=left;verticalAlign=top;fontColor=#142537;fontSize={size};",
    })
    ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(width),
                                      "height": str(height), "as": "geometry"})


def main():
    spec = json.loads(BASE.with_suffix(".json").read_text(encoding="utf-8"))
    generate_diagram.main(["--spec", str(BASE.with_suffix(".json")), "--out", str(BASE.with_suffix(".drawio"))])
    tree = ET.parse(BASE.with_suffix(".drawio"))
    model = tree.find(".//mxGraphModel")
    root = model.find("root")
    model.set("pageHeight", "1160")
    nodes = {node["id"]: node for node in spec["nodes"]}
    zones = {zone["id"] for zone in spec["zones"]}
    title_rows = 0
    real_edges = [cell for cell in root.findall("mxCell") if cell.get("edge") == "1" and cell.get("parent") == "1"]
    edge_specs = {cell.get("id"): source for cell, source in zip(real_edges, spec["edges"])}
    for cell in root.findall("mxCell"):
        identity = cell.get("id")
        geometry = cell.find("mxGeometry")
        if identity == "titleblock":
            geometry.set("width", "1840")
            geometry.set("height", "76")
        if cell.get("parent") == "titleblock":
            title_rows += 1
            geometry.set("width", "1816")
            if title_rows == 1:
                cell.set("style", cell.get("style") + "fontSize=24;")
            elif title_rows == 2:
                geometry.set("y", "37")
                cell.set("style", cell.get("style") + "fontSize=12;")
            else:
                cell.set("value", "Approved design. Not implemented. Reviewer: " + spec["reviewer"])
                geometry.set("y", "58")
                cell.set("style", cell.get("style") + "fontSize=11;")
        if identity in zones:
            cell.set("style", cell.get("style") + "fontColor=#142537;spacingTop=8;fontSize=16;arcSize=5;")
        if identity in nodes:
            cell.set("style", cell.get("style") + "fontColor=#142537;fontSize=14;labelWidth=190;whiteSpace=wrap;spacingTop=10;")
        if "edgeLabel" in cell.get("style", ""):
            cell.set("style", cell.get("style") + "fontColor=#142537;fontSize=12;spacing=4;")
            offset = edge_specs.get(cell.get("parent"), {}).get("label_offset")
            if offset:
                point = geometry.find("mxPoint")
                point.set("x", str(offset[0]))
                point.set("y", str(offset[1]))
    add_text(root, "source-note", "Source: docs/architecture/02_TECHNICAL_BLUEPRINT.md | Security: docs/security/03_SECURITY_ACCESS.md | D20 and D21", 40, 1115, 1840, 25, 12)
    add_text(root, "design-note", "ASSESSMENT CONTROLS\nRefresh sources before selection. Verify selected versions at worker start.\nFailed verification or changed versions stops the assessment.\nUse one bounded agent. Keep 24 model calls and a 600-second deadline.\nStore exact evidence versions. Save human review decisions separately.\nNo crawler. No independent reviewer role.", 40, 840, 670, 220)
    add_text(root, "boundary-note", "DESIGN LIMITS\nAll names identify planned roles. No deployed resource names exist.\nTLS: Transport Layer Security. PKCE protects the sign-in code exchange.\nIAM: AWS Identity and Access Management. API: application interface.\nHTTPS/443 is intended transport. Live connections remain unverified.\nZones show responsibility and trust. They do not specify VPCs or subnets.\nAWS SAM defines deployment. Local adapters use the same application logic.", 1230, 840, 650, 235)
    add_text(root, "model-note", "Profile: in.openai.gpt-5.6-luna\nAllow Mumbai and Hyderabad only.\nVerify destinations, access, and quality\nbefore private uploads.", 1590, 645, 260, 105, 12)
    add_text(root, "provider-note", "Public regulatory queries only.\nAllow configured HTTPS endpoints.\nVerify authority, versions, and freshness.\nProvider credentials stay server-side.", 1590, 300, 260, 70, 12)
    add_text(root, "data-note", "Private bank files and records | encryption required | owner-scoped access\nRegulatory S3 copies are evidence. They do not establish current coverage.", 430, 765, 1000, 30, 12)
    for cell in list(root.findall("mxCell")):
        if cell.get("vertex") != "1":
            continue
        identity = cell.attrib.pop("id")
        label = cell.attrib.pop("value", "")
        tooltip = nodes.get(identity, {}).get("description", label or "Diagram annotation")
        wrapper = ET.Element("UserObject", {"id": identity, "label": label, "tooltip": tooltip})
        if identity in nodes:
            wrapper.set("component_id", identity)
            wrapper.set("status", "planned")
        index = list(root).index(cell)
        root.remove(cell)
        wrapper.append(cell)
        root.insert(index, wrapper)
    ET.indent(tree, space="  ")
    tree.write(BASE.with_suffix(".drawio"), encoding="utf-8", xml_declaration=True)
    subprocess.run([sys.executable, str(SKILL / "export_to_svg.py"), str(BASE.with_suffix(".drawio"))], check=True)


if __name__ == "__main__":
    main()
