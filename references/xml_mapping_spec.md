# XML Mapping Spec

The Word execution layer uses Flat OPC XML, not Word 2003 XML and not ODF flat XML.

## Required Parts

- `/word/document.xml`
- `/word/styles.xml`
- `/word/_rels/document.xml.rels`
- `/word/settings.xml` when field refresh can be enabled

## Heading Detection

Detect heading styles with the same priority as the source project:

1. Paragraph styles with `w:outlineLvl` 0, 1, and 2 map to levels 1, 2, and 3.
2. Prefer names containing `Heading 1`, `Heading1`, `标题 1`, or `标题1`.
3. Prefer IDs containing `Heading1` or equal to the numeric level.
4. Fallback to the first outline-level style found.

## Section Mapping

Classify body nodes as:

- `heading`: level 1-3 body heading.
- `front_title`: 摘要, Abstract, 目录.
- `toc_title`: 插图目录, 表格目录.
- `back_title`: 致谢, 参考文献, 作者简介, 附录, 攻读期间发表.
- `paragraph`: normal body paragraph.
- `table`: `w:tbl`.
- `image_placeholder`: paragraph containing drawing/pict/VML shape.
- `equation`: paragraph containing OMML.
- `caption_figure` / `caption_table`: paragraph containing SEQ field.

## Writeback Behavior

- Preserve front matter and back matter.
- Preserve the template's TOC, list-of-tables, and list-of-figures field paragraphs. During front-matter cleanup, replace only Abstract/摘要 body text; do not delete the existing TOC/list field result paragraphs because Word will refresh them through `w:updateFields=true`. Mark field begins dirty so Word refreshes the cached TOC/list content on open or when fields are updated.
- Replace the body range from the first non-front level-1 heading up to the first back matter title or body `sectPr`.
- Clone paragraph prototypes from the template for heading, body, caption, and reference nodes; generate `[[TBL:...]]` as a real Word table rather than cloning stale template sample tables.
- Strip manual heading numbering before writing Word headings by default. This prevents numbered templates from producing duplicated headings such as `第五章 第5章 总结与展望`.
- Discard Markdown file headers such as `# 第5章 总结与展望`; they are not body content.
- Normalize Chinese/English spacing in body text while keeping spaces inside English phrases.
- Convert supported LaTeX-style formula tokens before Word writeback. Inline `[[SYM:...]]` and display `[[EQ:...]]` should emit OMML structures for superscript, subscript, and fraction nodes where possible; raw commands such as `\in` and `\times` should not remain visible in Word.
- Display `[[EQ:...]]` formula numbers as `(chapter.index)` with an ASCII period, for example `(3.1)`, unless `styleSettings.equationSeparator` is explicitly set for a different institution rule.
- Center figure placeholders, figure captions, and table captions with `w:jc w:val="center"`.
- Generate tables as three-line thesis tables matching the minimal template: table top border `single sz=12`, table bottom border `single sz=12`, first-row cell bottom border `single sz=4`, and left/right/insideH/insideV borders `none`. Set every table cell paragraph to `w:jc=center` and every cell to `w:vAlign=center`.
- When the reference prototype has `w:numPr`, preserve it and do not write explicit `[n]` text. The bundled template uses `numId=4`, `lvlText="[%1]"`, and paragraph indentation `left=425` / `hanging=425`; cloned entries should keep that automatic numbering and hanging indent. Body citations should use `REF bookmark \r \h` so Word resolves the paragraph number. Only use manual `[n]` labels as a fallback when no reference numbering exists in the template.
- Treat both standalone `w:sectPr` nodes and paragraph-contained `w:pPr/w:sectPr` nodes as protected section breaks. Never delete them while clearing TOC/list entries, replacing body content, or replacing reference entries, because they preserve the template's header/footer links and page-number restarts.
- When a header uses a `STYLEREF` field for the level-1 heading, update the cached field-result text to the current first chapter title so the header is reasonable before Word refreshes fields.
- Render `[[REF_FIG:...]]` and `[[REF_TBL:...]]` to chapter-local `图X-Y` and `表X-Y` text before creating paragraphs.
- Insert `w:updateFields w:val="true"` into settings so Word refreshes TOC/fields.
- Update header/footer STYLEREF fields to the detected level-1 heading style.
- Preserve XML intermediate files in `09_state/`.
