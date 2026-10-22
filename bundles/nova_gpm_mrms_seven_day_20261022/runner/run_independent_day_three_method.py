#!/usr/bin/env python3
import gzip,json,hashlib,tempfile,os,sys
from pathlib import Path
import numpy as np,xarray as xr
sys.path.insert(0,'/Users/fujikijunichi/DTI_Nova/tools')
import run_gpm_mrms_three_method_5day_20261022 as base

ROOT=Path('/Users/fujikijunichi/DTI_Nova'); DAY=os.environ.get('NOVA_DAY','2024-02-01'); TOKEN=DAY.replace('-',''); G=Path(f'/Volumes/1tbinside/NOVA_data_20261022/gpm_independent_{TOKEN}'); M=Path(f'/Volumes/1tbinside/NOVA_data_20261022/mrms_independent_{TOKEN}_pass2'); OUT=ROOT/f'output/gpm_mrms_independent_{TOKEN}_three_method_20261022'; OUT.mkdir(parents=True,exist_ok=True)
poly=base.Polygon(__import__('json').loads((ROOT/'output/usgs_nldi_basin_01387095_20261015.geojson').read_text())['features'][0]['geometry']['coordinates'][0]); mrfiles=sorted(M.glob('*.grib2.gz')); inspect=[]
for p in mrfiles:
 t=tempfile.NamedTemporaryFile(delete=False,suffix='.grib2');t.close()
 try:
  with gzip.open(p,'rb') as a,open(t.name,'wb') as b:b.write(a.read())
  ds=xr.open_dataset(t.name,engine='cfgrib',backend_kwargs={'indexpath':''}); lat=np.asarray(ds.latitude.values);lon=np.asarray(ds.longitude.values);lon=np.where(lon>180,lon-360,lon);z=np.asarray(ds['unknown'].values,float); finite=np.isfinite(z); inside=(lat[:,None]>=poly.bounds[1]-.2)&(lat[:,None]<=poly.bounds[3]+.2)&(lon[None,:]>=poly.bounds[0]-.2)&(lon[None,:]<=poly.bounds[2]+.2); valid=inside&finite&(z>=0); inspect.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'valid_time':str(ds.valid_time.values),'shape':list(z.shape),'inside_cells':int(inside.sum()),'valid_cells':int(valid.sum()),'negative_cells':int((inside&finite&(z<0)).sum()),'nonfinite_cells':int((inside&~finite).sum())}); ds.close()
 except Exception as e: inspect.append({'file':p.name,'error':str(e)})
 finally:os.unlink(t.name)
 gm={};
 import re
 for p in G.glob('*.HDF5'):
  if p.name.startswith('._'): continue
  m=re.search(rf'{TOKEN}-S(\d{{6}})-',p.name)
  if m:gm[m.group(1)]=p
 rows=[]; errors=[]
 try:
  for h in range(24):
   p0=gm[f'{h:02d}0000'];p1=gm[f'{h:02d}3000'];g0=base.cells_g(p0,poly);g1=base.cells_g(p1,poly);g=[(a,va+vb) for (a,va),(b,vb) in zip(g0,g1) if a.equals(b)];m=base.cells_m(M/f'MultiSensor_QPE_01H_Pass2_00.00_{TOKEN}-{h:02d}0000.grib2.gz',poly);cg,cm,rg,ni,area=base.reduce_spatial(g,m);rows.append({'hour':h,'gpm_basin_mm':base.avg(g),'mrms_basin_mm':base.avg(m),'common_gpm_mm':cg,'common_mrms_mm':cm,'conservative_gpm_mm':rg,'common_intersections':ni,'support_area_deg2':area})
 except Exception as e:errors.append(str(e))
 result={'schema':'NOVA_GPM_MRMS_INDEPENDENT_DAY_THREE_METHOD_V1','date':DAY,'mrms_inspection':inspect,'rows':rows,'errors':errors,'complete':len(inspect)==24 and all('error' not in x for x in inspect) and len(rows)==24 and not errors,'formal_pass':False,'claim_boundary':'Independent-day diagnostic comparison only; no calibration or product correction claim.'}; p=OUT/'result.json';p.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');h=hashlib.sha256(p.read_bytes()).hexdigest();(OUT/'RESULT.sha256').write_text(f'{h}  {p.name}\n');print(json.dumps({'mrms_files':len(inspect),'rows':len(rows),'errors':len(errors),'complete':result['complete'],'sha256':h,'formal_pass':False}))
