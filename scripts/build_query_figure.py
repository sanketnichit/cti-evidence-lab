"""Render the minimal non-identifiable graph pair; optional ReportLab dependency."""
from pathlib import Path


def drawing():
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
    from reportlab.lib.colors import HexColor
    d = Drawing(495, 234)
    ink, accent = HexColor("#183b4c"), HexColor("#156276")
    def text(x, y, value, size=9, bold=False):
        d.add(String(x, y, value, fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=size, fillColor=ink, textAnchor="middle"))
    def node(x, y, value):
        d.add(Rect(x-24, y-11, 48, 22, rx=4, fillColor=HexColor("#eef4f6"), strokeColor=accent))
        text(x, y-3, value)
    def arrow(x1, y, x2):
        d.add(Line(x1+25, y, x2-28, y, strokeColor=accent))
        d.add(Polygon([x2-25, y, x2-31, y+3, x2-31, y-3], fillColor=accent, strokeColor=accent))
    text(116, 219, "Disconnected occurrences", 10, True)
    text(375, 219, "Connected occurrences", 10, True)
    for x, y, label in [(48,184,"u : A"),(185,184,"v : B"),(48,140,"w : B"),(185,140,"x : C"),
                         (294,184,"u : A"),(375,184,"v : B"),(456,184,"x : C"),(375,140,"w : B")]:
        node(x,y,label)
    arrow(48,184,185); arrow(48,140,185)
    arrow(294,184,375); arrow(375,184,456)
    text(375,119,"isolated occurrence",8)
    text(116,96,"Connected A,B,C query: NO",9,True)
    text(375,96,"Connected A,B,C query: YES",9,True)
    d.add(Line(247, 90, 247, 224, strokeColor=HexColor("#ccd8de")))
    text(247,67,"Both project to the same technique graph",10,True)
    for x, label in [(166,"A"),(247,"B"),(328,"C")]:
        node(x,43,label)
    arrow(166,43,247); arrow(247,43,328)
    text(247,10,"All arrows are supplied BEFORE edges. Identical technique labels do not establish identical occurrences.",8)
    return d


if __name__ == "__main__":
    from reportlab.graphics import renderSVG
    path = Path(__file__).resolve().parents[1] / "research/experiments/query_fidelity_v0.1/sequence_counterexample.svg"
    renderSVG.drawToFile(drawing(), str(path))
    print("Written:", path.name)
