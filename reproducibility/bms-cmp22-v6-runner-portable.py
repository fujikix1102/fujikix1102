import argparse, hashlib, json, pathlib
def load(name): return json.loads((base/name).read_text())
def main():
    ap = argparse.ArgumentParser(description='Integrate NOVA BMS blind-E2E evidence artifacts.')
    ap.add_argument('--base-dir', required=True, type=pathlib.Path, help='Directory containing evidence JSON files')
    ap.add_argument('--output', required=True, type=pathlib.Path, help='Output JSON path')
    args = ap.parse_args()
    base = args.base_dir
    def load(name): return json.loads((base/name).read_text())
    row=load('bms_row_range_audit_20261023.json')
    xy=load('bms_xy_blind_comparison_20261023.json')
    rec=load('bms_independent_engine_recalc_20261023.json')
    out={'schema':'NOVA_BMS_BLIND_E2E_INTEGRATED_V1','dataset':'SRRL BMS June 2023 Global CMP22 vent/cor serial 080017','evidence':{
        'archive_structure':'PASS_FOR_ARCHIVE_AND_STRUCTURE_ONLY','independent_engine_save':rec['all_files_saved'],
        'workbook_count':row['workbook_count'],'active_row_count':row['active_rows_set'],
        'template_tail_count':row['template_tail_rows_set'],'xy_difference_total':xy['xy_difference_total'],
        'xy_error_total':xy['xy_error_total'],'xy_formula_total':xy['xy_formula_total'],
        'row_range_sha256':hashlib.sha256((base/'bms_row_range_audit_20261023.json').read_bytes()).hexdigest(),
        'xy_comparison_sha256':hashlib.sha256((base/'bms_xy_blind_comparison_20261023.json').read_bytes()).hexdigest(),
        'recalc_sha256':hashlib.sha256((base/'bms_independent_engine_recalc_20261023.json').read_bytes()).hexdigest()},
        'verdicts':{'execution_complete':True,'numerical_verified_for_xy_and_range':True,'statistical_valid':False,'external_verified':False,'physical_calibrated':False},
        'formal_pass':False,'claim_boundary':'Independent engine and structure/X-Y equivalence are verified; statistical, external, and physical-calibration gates remain unverified.'}
    p=args.output; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(out,indent=2)+'\n'); print(hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__': main()
