# Placeholder Protocol

The Markdown layer uses explicit tags so the XML layer can write deterministic Word nodes.

## Tags

- `[[FIG:description]]`: insert image placeholder paragraph plus caption. XML output uses `图 X-Y`.
- `[[TBL:description]]`: insert table caption and a real Word `w:tbl` generated from structured rows or a known experiment-table description. XML output uses `表 X-Y`; generated tables must be thesis three-line tables.
- `[[EQ:formula]]`: insert display formula. XML output uses OMML text with chapter-local numbering in `(chapter.index)` form, for example `(3.1)`.
- `[[SYM:formula]]`: insert inline math symbol with OMML.
- `[[REF:n]]`: insert numbered bibliography cross-reference as a superscript field.
- `[[REF:KEYWORD_PLACEHOLDER: terms]]`: unresolved reference that can be normalized into a numeric ID.
- `[[REF_FIG:description]]`: render a Markdown figure reference.
- `[[REF_TBL:description]]`: render a Markdown table reference.
- `[[CODE:path-or-description]]`: track code asset needs in Markdown.
- `[[DATA:path-or-description]]`: track data asset needs in Markdown.

## Rules

- Do not remove or rewrite placeholders during polishing.
- Do not hard-code figure/table numbers in prose.
- Write figure references as `如图[[REF_FIG:description]]所示` or `见[[REF_FIG:description]]`; write table references as `如表[[REF_TBL:description]]所示` or `见[[REF_TBL:description]]`. The writer renders them as `图X-Y` and `表X-Y`.
- Multiple references must be split as `[[REF:1]][[REF:2]]`, not `[[REF:1,2]]`.
- Descriptions should be stable because figure/table references are matched by description.

## Formula Syntax

- Use a limited LaTeX-style syntax inside `[[SYM:...]]` and `[[EQ:...]]`.
- Prefer `\mathbb{R}` for real-number spaces, for example `[[SYM:X\in\mathbb{R}^{H\times W\times C}]]`.
- Supported conversions include `\in`, `\times`, `\cap`, `\cup`, `\otimes`, `\sigma`, `\lambda`, `\frac{...}{...}`, `^{...}`, and `_{...}`.
- The writer must convert supported LaTeX tokens to Word OMML structures or math symbols before XML writeback; raw backslash commands should not appear in the final Word body.
- Display formula numbering must use an ASCII period between chapter and formula number, for example `(3.1)`, not `(3-1)` or `(3－1)`.
