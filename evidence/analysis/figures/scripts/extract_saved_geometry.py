from portable_metadata import dumps as portable_json
from pathlib import Path
import json,re,hashlib
B=Path(__file__).resolve().parent.parent
scene=B/'inputs/geometry/TangramMultiplayer.unity'
text=scene.read_text()
chunks={m.group(2):(m.group(1),m.group(3)) for m in re.finditer(r'^--- !u!(\d+) &(\d+)[^\n]*\n(.*?)(?=^--- !u!|\Z)',text,re.M|re.S)}
transforms={re.search(r'm_GameObject: \{fileID: (\d+)\}',b).group(1):(i,b) for i,(t,b) in chunks.items() if t=='4' and 'm_GameObject:' in b}
geo={}
for i,(t,b) in chunks.items():
    if '  footprintVertices:' not in b:continue
    game=re.search(r'm_GameObject: \{fileID: (\d+)\}',b).group(1)
    name=re.search(r'^  m_Name: (.*)$',chunks[game][1],re.M).group(1)
    points=[[float(v) for v in xyz] for xyz in re.findall(r'^  - \{x: ([^,]+), y: ([^,]+), z: ([^}]+)\}',b.split('  footprintVertices:',1)[1].split('  placementArea:',1)[0],re.M)]
    scale=1.;tid=transforms[game][0]
    while tid in chunks:
        tb=chunks[tid][1]
        m=re.search(r'm_LocalScale: \{x: ([^,]+), y: ([^,]+), z: ([^}]+)',tb)
        sc=[float(v) for v in m.groups()];assert max(sc)-min(sc)<1e-9;scale*=sc[0]
        tid=re.search(r'm_Father: \{fileID: (\d+)\}',tb).group(1)
    geo['S'+name[-1]]={'name':name,'points':points,'scale':scale}

archived=json.loads((B/'inputs/geometry/geometry_from_backup.json').read_text())
assert geo==archived['geometry']
assert hashlib.sha256(scene.read_bytes()).hexdigest()==archived['sha256']
output={'source':'inputs/geometry/TangramMultiplayer.unity','sha256':archived['sha256'],'geometry':geo,'limit':archived['limit']}
(B/'generated/audit/geometry_extracted_from_scene.json').write_text(portable_json(output,ensure_ascii=False,indent=2))
print('Saved Unity scene: all seven piece vertex arrays and scales match the archived geometry exactly')
