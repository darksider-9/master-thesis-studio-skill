# Master Thesis Studio Skill

面向东南大学的中文硕士论文写作与 Word 自动生成的 Codex Skill，默认适配东南大学风格硕士论文 Word 模板。它把论文创作流程拆成两层：先通过对话确认题目、章节、资产和写作边界，再通过内置 Python 脚本把 Markdown 内容安全写入 Word 模板，生成新的 `.docx` 文件，打开时出现任何弹窗都点击是即可。

## 模板来源
 - 模板修改自https://seuthesis-word.github.io/ ，目前在图表目录和封面上尚未完全完成，请勿直接使用模板带封面的word，修改后的模板文件已存放在examples/中，可以在完成后再额外添加封面等摘要之前的内容。
## 主要能力

- 初始化论文项目工作区，创建章节、图表、代码、数据、参考文献、状态文件和输出目录。
- 引导用户确认题目、研究方向、当前完成度、已有资产、章节框架和写作模式。
- 支持从零生成初稿、边做边写、续写已有论文、根据代码和数据转写论文、格式整理与 Word 输出。
- 使用 manifest 管理参考文献、图、表、代码、数据、公式和待补材料。
- 将确认后的 Markdown 写入 Flat OPC XML，再构建新的 Word 文档，不覆盖原始模板。
- 支持图题、表题、三线表、公式编号、参考文献、交叉引用、页眉页脚和目录字段刷新。

## 适用场景

- 只有论文题目或方向，希望先生成一个可修改的完整初稿。
- 已经写了一部分论文，希望继续补写或重写薄弱章节。
- 已有代码、数据、实验记录、图表，希望转写成论文方法和实验章节。
- 已有 Word 模板，希望自动化写入章节、图表、公式和参考文献。
- 需要基于东南大学风格模板生成安全、可追溯的新 Word 副本。

## 目录结构

```text
master-thesis-studio-skill/
├─ SKILL.md
├─ assets/
│  └─ project_state.schema.json
├─ examples/
│  └─ Template.docx
├─ references/
│  ├─ writing_workflow.md
│  ├─ xml_mapping_spec.md
│  ├─ placeholders.md
│  └─ reference_rules.md
├─ scripts/
│  ├─ init_thesis_workspace.py
│  ├─ flat_opc_converter.py
│  ├─ parse_template_xml.py
│  ├─ generate_planning_files.py
│  ├─ apply_markdown_to_xml.py
│  ├─ build_new_docx.py
│  ├─ embed_figures_docx.py
│  ├─ validate_xml_docx.py
│  ├─ reference_tools.py
│  └─ word_xml_core.py
└─ templates/
   ├─ project_manifest.md
   ├─ thesis_master_index.md
   ├─ figures_manifest.md
   ├─ tables_manifest.md
   ├─ code_manifest.md
   └─ data_manifest.md
```

## 环境要求

- Python 3.10 或更高版本。
- Python 依赖：`lxml`。
- 一个 `.docx` 论文模板或已有论文草稿。
- 如需在 Word 中看到目录、表格目录、插图目录和交叉引用的最终页码，打开 Word 后可全选并按 `F9` 刷新域。

安装依赖：

```bash
pip install lxml
```


