# Submission: University Data Integration

This folder contains all submission artifacts for the university data integration assignment.

Contents
- `university_data_integration_plan.md` — full plan and recommendations
- `university_data_integration_plan.pdf` — rendered PDF of the full plan
- `sql/ddl_core_tables.sql` — DDLs for canonical ODS schema
- `er_diagram.puml` — PlantUML ER diagram
- `er_diagram.svg` — placeholder or rendered SVG of the ER diagram
- `onepager.md` — one-page brief for leadership
- `onepager.pdf` — rendered one-page PDF
- `examples/` — contains example connector code and DAGs
- `vendor_connectors.md` — connector guidance for common SIS/LMS/HR/Library systems
- `submission_university_integration.zip` — zip archive (located at repo root)

How to regenerate the PDF locally
1. Ensure `pandoc` and a TeX engine (xelatex) are installed.
2. From this folder run:

```powershell
pandoc "university_data_integration_plan.md" -o "university_data_integration_plan.pdf" --pdf-engine=xelatex -V geometry:margin=20mm -V fontsize=11pt
```

How to render the PlantUML diagram
1. If you have PlantUML installed with Graphviz, run:

```powershell
plantuml er_diagram.puml
```

2. Or use the online PlantUML server /VSCode PlantUML extension to preview and export as SVG/PNG.

Notes
- Sensitive secrets or connection strings are not included. Replace placeholders in example files before use.
- If `er_diagram.svg` is a placeholder (it indicates PlantUML isn't available in this environment), render it locally or ask me to produce an SVG if you enable PlantUML.
# Submission: University Data Integration

This folder contains all submission artifacts for the university data integration assignment.

Contents
- `university_data_integration_plan.md` — full plan and recommendations
- `sql/ddl_core_tables.sql` — SQL DDLs for canonical ODS schema
- `er_diagram.puml` — PlantUML ER diagram
- `onepager.md` — one-page brief for leadership
- `examples/` — contains example connector code and DAGs (added below)
- `university_data_integration_plan.pdf` — rendered PDF of the full plan (generated)

How to regenerate the PDF locally
1. Ensure `pandoc` and a TeX engine (xelatex) are installed.
2. From this folder run:

```powershell
pandoc "university_data_integration_plan.md" -o "university_data_integration_plan.pdf" --pdf-engine=xelatex -V geometry:margin=20mm -V fontsize=11pt
```

How to render the PlantUML diagram
1. If you have PlantUML installed with Graphviz, run:

```powershell
plantuml er_diagram.puml
```

2. Or use the online PlantUML server / VSCode PlantUML extension to preview and export as SVG/PNG.

Notes
- Sensitive secrets or connection strings are not included. Replace placeholders in example files before use.
