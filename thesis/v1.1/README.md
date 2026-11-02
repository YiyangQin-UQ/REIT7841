# Thesis v1.1

**Collaborative Tangram in Shared Overhead VR: Shape Judgment and the Coordination of Construction**  
Yiyang Qin · REIT7841 · 2 November 2026

- [Read the thesis PDF](REIT7841_Thesis_v1.1.pdf)
- [Download the LaTeX source package](REIT7841_Thesis_v1.1_LaTeX.zip)
- [Source catalogue D01–D74](materials/README.md)

This version includes the revised figure placement, continuous case ordering, clearer schematic text and a single-page table of all 48 confirmed questionnaire responses. The manuscript has 7 chapters, 11 figures, 12 numbered tables and 20 references.

This repository copy preserves the manuscript and data. Appendix A's navigation explanation and external links point to the online source catalogue instead of the author's local file index. The signed consent forms, original recordings, private correspondence and full local archive are retained separately.

## Edit and compile

Edit `main.tex`, `frontmatter.tex`, `chapters/` and `appendices/`. References are in `references.bib`; the 11 required figure files are in `assets/figures/`.

Compile using Tectonic:

```sh
tectonic --keep-logs --keep-intermediates main.tex
```

Alternatively run XeLaTeX, BibTeX, then XeLaTeX twice. The source package contains all files needed to compile the manuscript. Source-catalogue links require an internet connection.
