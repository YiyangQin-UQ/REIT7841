#!/usr/bin/env python3
"""Rebuild the 11 published figure families. Outputs remain within this package."""
from pathlib import Path
import subprocess,sys
B=Path(__file__).resolve().parent
for d in ['generated/figures','generated/audit']:(B/d).mkdir(parents=True,exist_ok=True)
for name in ['extract_saved_geometry.py','build_geometry.py','plot_timeline.py','plot_self_revision.py','plot_goose.py','build_auxiliary_figures.py','draw_method_figures.py','redraw_final_schematics.py']:
    print('Building',name,flush=True)
    subprocess.run([sys.executable,str(B/'scripts'/name)],check=True,cwd=B)
subprocess.run([sys.executable,str(B/'validate.py')],check=True,cwd=B)
