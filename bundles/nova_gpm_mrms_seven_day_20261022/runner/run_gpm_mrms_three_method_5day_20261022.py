#!/usr/bin/env python3
"""Auditable five-day GPM/MRMS three-support spatial comparison."""
from __future__ import annotations
import datetime as dt, gzip, hashlib, json, os, re, tempfile
from pathlib import Path
import h5py, numpy as np, xarray as xr
from shapely.geometry import Polygon, box

ROOT=Path('/Users/fujikijunichi/DTI_Nova'); BASE=Path('/Volumes/1tbinside/NOVA_data_20261022')
OUT=ROOT/'output/gpm_mrms_three_method_5day_20261022'; PREFLIGHT=ROOT/'output/gpm_mrms_spatial_runner_5day_20261022/preflight.json'; BASELINE=ROOT/'output/gpm_mrms_five_day_sensitivity_20261022.json'; BASIN=ROOT/'output/usgs_nldi_basin_01387095_20261015.geojson'
GPM=(BASE/'gpm_imerg_for_precipflag_107',BASE/'gpm_imerg_boundary10'); MRMS=BASE/'mrms_qpe_pass2_for_precipflag_107'; DATES=['2025-01-11','2025-01-18','2025-01-20','2025-01-31','2025-02-06']

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def gmap():
 d={}
 for root in GPM:
  for p in root.glob('3B-HHR*.V07B.HDF5'):
   m=re.search(r'3IMERG\.(\d{8})-S(\d{6})-',p.name)
   if m:d[(m.group(1),m.group(2))]=p
 return d
def mmap():
 d={}
 for p in MRMS.glob('MultiSensor_QPE_01H_Pass2_*.grib2.gz'):
  m=re.search(r'_(\d{8})-(\d{6})\.grib2\.gz$',p.name)
  if m:d[(m.group(1),m.group(2)[:2])]=p
 return d
def cells_g(p,poly):
 with h5py.File(p,'r') as h:
  x=h['Grid']; lat=np.asarray(x['lat'][:],float); lon=np.asarray(x['lon'][:],float); z=np.asarray(x['precipitation'][0,:,:],float)
 out=[]
 for i in np.where((lat>=poly.bounds[1]-.1)&(lat<=poly.bounds[3]+.1))[0]:
  for j in np.where((lon>=poly.bounds[0]-.1)&(lon<=poly.bounds[2]+.1))[0]:
   q=box(lon[j]-.05,lat[i]-.05,lon[j]+.05,lat[i]+.05).intersection(poly)
   if q.area and np.isfinite(z[j,i]) and z[j,i]>=0: out.append((q,float(z[j,i]*.5)))
 return out
def cells_m(p,poly):
 t=tempfile.NamedTemporaryFile(delete=False,suffix='.grib2'); t.close()
 try:
  with gzip.open(p,'rb') as a,open(t.name,'wb') as b:b.write(a.read())
  ds=xr.open_dataset(t.name,engine='cfgrib',backend_kwargs={'indexpath':''}); lat=np.asarray(ds.latitude.values); lon=np.asarray(ds.longitude.values); lon=np.where(lon>180,lon-360,lon); z=np.asarray(ds['unknown'].values,float); out=[]
  for i in np.where((lat>=poly.bounds[1]-.2)&(lat<=poly.bounds[3]+.2))[0]:
   for j in np.where((lon>=poly.bounds[0]-.2)&(lon<=poly.bounds[2]+.2))[0]:
    q=box(lon[j]-.005,lat[i]-.005,lon[j]+.005,lat[i]+.005).intersection(poly)
    if q.area and np.isfinite(z[i,j]) and z[i,j]>=0:out.append((q,float(z[i,j])))
  ds.close(); return out
 finally:os.unlink(t.name)
def w(g):return g.area*np.cos(np.deg2rad(g.centroid.y))
def avg(c):return float(sum(w(g)*v for g,v in c)/sum(w(g) for g,v in c)) if c else None
def reduce_spatial(g,m):
 inter=[]
 for ga,gv in g:
  for ma,mv in m:
   q=ga.intersection(ma)
   if q.area:inter.append((q,gv,mv))
 den=sum(w(q) for q,_,_ in inter); cg=sum(w(q)*gv for q,gv,_ in inter)/den if den else None; cm=sum(w(q)*mv for q,_,mv in inter)/den if den else None
 rg=[]
 for ma,_ in m:
  pairs=[(ga.intersection(ma),gv) for ga,gv in g if ga.intersects(ma)]; den2=sum(w(q) for q,_ in pairs)
  if den2:rg.append((ma,sum(w(q)*v for q,v in pairs)/den2))
 return cg,cm,avg(rg),len(inter),den
def main():
 OUT.mkdir(parents=True,exist_ok=True); pre=json.loads(PREFLIGHT.read_text()); poly=Polygon(json.loads(BASIN.read_text())['features'][0]['geometry']['coordinates'][0]); gm,mr=gmap(),mmap(); rows=[]; errors=[]
 for day in DATES:
  for h in range(24):
   try:
    t=dt.datetime.fromisoformat(day)+dt.timedelta(hours=h-1); k=t.strftime('%Y%m%d'); p0=gm[(k,t.strftime('%H0000'))]; p1=gm[(k,t.strftime('%H3000'))]; g0=cells_g(p0,poly); g1=cells_g(p1,poly); g=[(a,va+vb) for (a,va),(b,vb) in zip(g0,g1) if a.equals(b)]; m=cells_m(mr[(day.replace('-',''),f'{h:02d}')],poly); cg,cm,rg,ni,area=reduce_spatial(g,m); rows.append({'date':day,'mrms_end_utc':f'{day}T{h:02d}:00:00Z','basin_mean_gpm_mm':avg(g),'basin_mean_mrms_mm':avg(m),'common_cells_gpm_mm':cg,'common_cells_mrms_mm':cm,'conservative_regrid_gpm_mm':rg,'common_intersections':ni,'common_support_area_deg2':area,'status':'PASS'})
   except Exception as e:errors.append({'date':day,'hour':h,'error':str(e)})
 ok=len(rows)==120 and not errors; methods={'basin_mean':{'status':'VERIFIED_INPUT','rows':len(rows),'source_sha256':sha(BASELINE)},'common_cells':{'status':'CALCULATED' if ok else 'BLOCKED','rows':len(rows),'definition':'intersection support weighted by overlap and latitude'},'conservative_area_regrid':{'status':'CALCULATED' if ok else 'BLOCKED','rows':len(rows),'definition':'GPM to MRMS overlap transfer preserving integrated field'}}
 result={'schema':'NOVA_GPM_MRMS_THREE_METHOD_5DAY_V2','generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'dates':DATES,'expected_rows':120,'preflight_sha256':sha(PREFLIGHT),'methods':methods,'rows':rows,'errors':errors,'spatial_methods_complete':ok,'formal_pass':False,'claim_boundary':'Diagnostic spatial comparison only; no calibration coefficient or universal product correction.'}; p=OUT/'three_method_result.json'; p.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); d=sha(p); (OUT/'THREE_METHOD_RESULT.sha256').write_text(f'{d}  {p.name}\n'); print(json.dumps({'rows':len(rows),'errors':len(errors),'sha256':d,'spatial_methods_complete':ok,'formal_pass':False}))
if __name__=='__main__':main()
