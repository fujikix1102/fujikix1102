#!/usr/bin/env python3
import argparse, csv, hashlib, json, math
from datetime import datetime, timezone
from pathlib import Path


def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(description='Verify NOVA NLR CMP22 bundle using standard library only.')
 ap.add_argument('--bundle', required=True, type=Path, help='Bundle metadata JSON')
 ap.add_argument('--output', required=True, type=Path, help='Verification output JSON')
 args=ap.parse_args()
 BUNDLE=args.bundle; OUT=args.output
 b=json.loads(BUNDLE.read_text())
 a=b['artifacts']; data=Path(a['bms_primary_data']['path'])
 checks={}
 checks['bundle_exists']=BUNDLE.is_file()
 checks['input_sha_matches']=sha(data)==a['bms_primary_data']['sha256']
 rows=[]; values=[]; invalid=0
 with data.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f); fields=r.fieldnames or []
  checks['primary_field_present']='Global CMP22 (vent/cor) [W/m^2]' in fields
  for row in r:
   rows.append(row)
   try:
    v=float(row['Global CMP22 (vent/cor) [W/m^2]'])
    if not math.isfinite(v): raise ValueError
    values.append(v)
   except (ValueError,TypeError,KeyError): invalid+=1
 dates={(x.get('Year',''),x.get('DOY','')) for x in rows}
 checks.update({'rows_43200':len(rows)==43200,'unique_days_30':len(dates)==30,'finite_all_rows':len(values)==len(rows),'invalid_zero':invalid==0,'calibration_ledger_hash_matches':sha(Path(a['calibration_ledger']['path']))==a['calibration_ledger']['sha256'],'cosine_sensitivity_hash_matches':sha(Path(a['cosine_response_sensitivity']['path']))==a['cosine_response_sensitivity']['sha256']})
 rec={'schema':'NOVA_NLR_CMP22_INDEPENDENT_REPRODUCTION_VERIFICATION_V1','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'runner':'standalone standard-library verifier','bundle':str(BUNDLE),'bundle_sha256':sha(BUNDLE),'checks':checks,'rows':len(rows),'finite_values':len(values),'negative_values':sum(v<0 for v in values),'status':'INDEPENDENT_REPRODUCTION_VERIFIED' if all(checks.values()) else 'INDEPENDENT_REPRODUCTION_FAILED','formal_pass':False,'claim_boundary':'Independent file/hash/schema reproduction succeeded; this does not establish an independent physical calibration or complete field uncertainty budget.'}
 rec['record_sha256']=hashlib.sha256(json.dumps(rec,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 OUT.parent.mkdir(parents=True, exist_ok=True)
 OUT.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'output':str(OUT),'status':rec['status'],'record_sha256':rec['record_sha256'],'formal_pass':False},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
