"""Deterministic documented capstone verification, without claiming live sensor activity."""
import json
from datetime import datetime,timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from capstone.tank_fill import calculate_from_units, total_run_volumes
ROOT=Path(__file__).resolve().parents[1]

def main():
    cases=[]
    for label,length,width,depth,unit,expected in [
       ('Workbook R-103',10,6,12,'in',448.8312),
       ('Workbook R-116',12,5,22,'in',822.8572),
       ('Workbook R-108 corrected source feet',10,6,2.5,'ft',1122.078),
    ]:
        data=calculate_from_units(length,width,depth,unit)
        actual=data['volume_gallons']
        passed=abs(actual-expected)<1e-8
        cases.append({'case':label,'expected_gal':expected,'actual_gal':actual,'pass':passed,
                      'inputs':{'length_ft':length,'width_ft':width,'depth':depth,'depth_unit':unit}})
    refusal=None
    try:calculate_from_units(10,6,-1,'in')
    except ValueError as e:refusal=str(e)
    assert refusal and all(x['pass'] for x in cases)
    total=total_run_volumes([{'run_id':f'R-{i}','length_ft':10,'width_ft':6,'fill_depth':12,'depth_unit':'in'} for i in range(101,119)])
    assert total['run_count']==18
    result={'verified_utc':datetime.now(timezone.utc).isoformat(),
            'source_of_expectations':'Module 1 source tests + DEFECTS.md (links in README)',
            'workbook_cases':cases,'invalid_case_error':refusal,
            'student_created_total':{'run_count':total['run_count'],'total_gallons':total['total_gallons'],
                                     'note':'Synthetic identical-depth test runs, not original workbook aggregate'},
            'all_passed':True}
    out=ROOT/'evidence'/'workbook_verification.json'
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
