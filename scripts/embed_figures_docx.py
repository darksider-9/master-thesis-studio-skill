from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import zipfile

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

NS = {"w": W_NS, "r": R_NS, "rel": REL_NS, "wp": WP_NS, "a": A_NS, "pic": PIC_NS, "ct": CT_NS}


def qn(ns: str, local: str) -> str:
    return f"{{{ns}}}{local}"


def para_text(p: etree._Element) -> str:
    return "".join(t.text or "" for t in p.findall(".//w:t", namespaces=NS)).strip()


def next_rid(rels_root: etree._Element) -> str:
    max_id = 0
    for rel in rels_root.findall("rel:Relationship", namespaces=NS):
        rid = rel.get("Id") or ""
        if rid.startswith("rId"):
            try:
                max_id = max(max_id, int(rid[3:]))
            except ValueError:
                pass
    return f"rId{max_id + 1}"


def ensure_svg_content_type(types_root: etree._Element) -> None:
    for node in types_root.findall("ct:Default", namespaces=NS):
        if node.get("Extension") == "svg":
            return
    default = etree.SubElement(types_root, qn(CT_NS, "Default"))
    default.set("Extension", "svg")
    default.set("ContentType", "image/svg+xml")


def drawing_para(rel_id: str, name: str, cx: int = 4800000, cy: int = 2700000) -> etree._Element:
    return etree.fromstring(f'''<w:p xmlns:w="{W_NS}" xmlns:r="{R_NS}" xmlns:wp="{WP_NS}" xmlns:a="{A_NS}" xmlns:pic="{PIC_NS}">
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="1" name="{name}"/>
        <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr><pic:cNvPr id="0" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''.encode("utf-8"))


def is_image_placeholder_text(text: str) -> bool:
    compact = (text or "").replace(" ", "")
    return "\u63d2\u5165\u56fe\u7247" in compact or "\u63d2\u5165\u56fe" in compact


def embed_figures(input_docx: Path, output_docx: Path, figures: list[Path]) -> None:
    work = output_docx.with_suffix(".embed_tmp")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    with zipfile.ZipFile(input_docx, "r") as zf:
        zf.extractall(work)

    doc_path = work / "word" / "document.xml"
    rels_path = work / "word" / "_rels" / "document.xml.rels"
    ct_path = work / "[Content_Types].xml"
    media_dir = work / "word" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    parser = etree.XMLParser(remove_blank_text=False, recover=True)
    doc_tree = etree.parse(str(doc_path), parser)
    rels_tree = etree.parse(str(rels_path), parser)
    ct_tree = etree.parse(str(ct_path), parser)
    doc_root = doc_tree.getroot()
    rels_root = rels_tree.getroot()
    ensure_svg_content_type(ct_tree.getroot())

    placeholders = [p for p in doc_root.findall(".//w:p", namespaces=NS) if is_image_placeholder_text(para_text(p))]
    count = min(len(placeholders), len(figures))
    for i in range(count):
        fig = figures[i].resolve()
        target_name = f"generated_fig_{i + 1}{fig.suffix.lower()}"
        shutil.copy(fig, media_dir / target_name)
        rid = next_rid(rels_root)
        rel = etree.SubElement(rels_root, qn(REL_NS, "Relationship"))
        rel.set("Id", rid)
        rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
        rel.set("Target", f"media/{target_name}")
        para = placeholders[i]
        parent = para.getparent()
        parent.replace(para, drawing_para(rid, target_name))

    doc_tree.write(str(doc_path), encoding="UTF-8", xml_declaration=True, standalone=True)
    rels_tree.write(str(rels_path), encoding="UTF-8", xml_declaration=True, standalone=True)
    ct_tree.write(str(ct_path), encoding="UTF-8", xml_declaration=True, standalone=True)

    if output_docx.exists():
        output_docx.unlink()
    with zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in work.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(work).as_posix())
    shutil.rmtree(work)
    print(output_docx)


def main() -> int:
    ap = argparse.ArgumentParser(description="Replace Word image placeholders with generated SVG figure files.")
    ap.add_argument("input_docx")
    ap.add_argument("output_docx")
    ap.add_argument("figures", nargs="+")
    args = ap.parse_args()
    embed_figures(Path(args.input_docx), Path(args.output_docx), [Path(p) for p in args.figures])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
