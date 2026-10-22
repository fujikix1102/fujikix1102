#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path('/Users/fujikijunichi/DTI_Nova'); BASE=ROOT/'output/gpm_mrms_three_method_5day_20261022'; IN2=ROOT/'output/gpm_mrms_independent_20240201_three_method_20261022/result.json'; IN1=ROOT/'output/gpm_mrms_independent_20240107_three_method_20261022/result.json'; OUT=ROOT/'output/gpm_mrms_seven_day_integrated_audit_20261022';OUT.mkdir(parents=True,exist_ok=True)
def ci(x,seed):
 x=np.asarray(x,float); rng=np.random.default_rng(seed); b=rng.choice(x,(10000,len(x)),replace=True).mean(1); return {'n':len(x),'mean':float(x.mean()),'ci95':[float(np.quantile(b,.025)),float(np.quantile(b,.975))]}
def add(rows,r,date):
 for x in r['rows']: rows.append({'date':date,'v':{'basin_mean':x['gpm_basin_mm'],'common_cells':x['common_gpm_mm'],'conservative_area_regrid':x['conservative_gpm_mm']},'m':x['mrms_basin_mm']})
def main():
 rows=[]; five=json.loads((BASE/'three_method_result.json').read_text())
 for x in five['rows']:rows.append({'date':x['date'],'v':{'basin_mean':x['basin_mean_gpm_mm'],'common_cells':x['common_cells_gpm_mm'],'conservative_area_regrid':x['conservative_regrid_gpm_mm']},'m':x['basin_mean_mrms_mm']})
 add(rows,json.loads(IN2.read_text()),'2024-02-01');add(rows,json.loads(IN1.read_text()),'2024-01-07'); summary={}
 for i,k in enumerate(['basin_mean','common_cells','conservative_area_regrid']):
  dif=[x['v'][k]-x['m'] for x in rows if x['v'][k] is not None and x['m'] is not None]; lodo=[]
  for day in sorted(set(x['date'] for x in rows)):
   z=[x['v'][k]-x['m'] for x in rows if x['date']!=day and x['v'][k] is not None and x['m'] is not None];lodo.append({'excluded_date':day,'mean_difference_mm':float(np.mean(z)) if z else None})
  summary[k]={'bootstrap':ci(dif,20261022+i),'lodo':lodo}
 out={'schema':'NOVA_GPM_MRMS_SEVEN_DAY_INTEGRATED_AUDIT_V1','source_sha256':{'five_day':hashlib.sha256((BASE/'three_method_result.json').read_bytes()).hexdigest(),'20240107':hashlib.sha256(IN1.read_bytes()).hexdigest(),'20240201':hashlib.sha256(IN2.read_bytes()).hexdigest()},'dates':sorted(set(x['date'] for x in rows)),'rows':len(rows),'methods':summary,'formal_pass':False,'claim_boundary':'Seven-day independent diagnostic comparison only; no calibration coefficient or universal product correction.'};p=OUT/'integrated.json';p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');h=hashlib.sha256(p.read_bytes()).hexdigest();(OUT/'INTEGRATED.sha256').write_text(f'{h}  {p.name}\n');print(json.dumps({'rows':len(rows),'dates':out['dates'],'sha256':h,'formal_pass':False}))
if __name__=='__main__':main()
