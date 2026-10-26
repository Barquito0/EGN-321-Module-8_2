"""Four rubric cases explicitly linked to user's Module 1 workbook defects/tests."""
import math
import pytest
from capstone.tank_fill import calculate_tank_volume, calculate_from_units, total_run_volumes


def test_known_correct_workbook_r103():
    # Module 1 original workbook R-103: 10 ft x 6 ft x 12 in -> 448.8312 US gal.
    assert calculate_tank_volume(10, 6, 12) == pytest.approx(448.8312, abs=1e-8)


def test_second_correct_workbook_r116():
    # Other tank size from workbook: 12 ft x 5 ft x 22 in.
    assert calculate_tank_volume(12, 5, 22) == pytest.approx(822.8572, abs=1e-8)


def test_workbook_edge_case_r108_unit_regression():
    # Original field note for R-108 was 2.5 ft, copied incorrectly as 2.5 inches.
    wrong = calculate_tank_volume(10, 6, 2.5)
    corrected = calculate_from_units(10, 6, 2.5, 'ft')
    assert wrong == pytest.approx(93.5065, abs=1e-8)
    assert corrected['depth_inches_used'] == 30
    assert corrected['volume_gallons'] == pytest.approx(1122.078, abs=1e-8)
    assert corrected['volume_gallons'] - wrong == pytest.approx(1028.5715, abs=1e-8)


@pytest.mark.parametrize('kwargs', [
    {'length_ft': -1, 'width_ft': 6, 'fill_depth': 12, 'depth_unit': 'in'},
    {'length_ft': 0, 'width_ft': 6, 'fill_depth': 12, 'depth_unit': 'in'},
    {'length_ft': 10, 'width_ft': 0, 'fill_depth': 12, 'depth_unit': 'in'},
    {'length_ft': 10, 'width_ft': 6, 'fill_depth': -1, 'depth_unit': 'in'},
    {'length_ft': 10, 'width_ft': 6, 'fill_depth': 2.5, 'depth_unit': 'cm'},
    {'length_ft': 10, 'width_ft': 6, 'fill_depth': 2.5, 'depth_unit': None},
    {'length_ft': True, 'width_ft': 6, 'fill_depth': 12, 'depth_unit': 'in'},
    {'length_ft': 10, 'width_ft': 6, 'fill_depth': float('nan'), 'depth_unit': 'in'},
])
def test_invalid_input_refuses(kwargs):
    with pytest.raises(ValueError):
        calculate_from_units(**kwargs)


def test_student_created_total_all_runs_not_fixed_12_row_range():
    # Regression for inherited SUM(G6:G17) defect. Total every supplied run.
    runs=[{'run_id':f'R-{100+i}','length_ft':10,'width_ft':6,
           'fill_depth':12,'depth_unit':'in'} for i in range(1,19)]
    result=total_run_volumes(runs)
    assert result['run_count']==18
    assert result['total_gallons']==pytest.approx(18*448.8312)


def test_student_created_missing_or_duplicate_run_not_silently_excluded():
    row={'run_id':'R-103','length_ft':10,'width_ft':6,
         'fill_depth':12,'depth_unit':'in'}
    with pytest.raises(ValueError,match='duplicate'):
        total_run_volumes([row,row])
    with pytest.raises(ValueError,match='required field missing'):
        total_run_volumes([{'run_id':'R-106','length_ft':10,'width_ft':6,'fill_depth':12}])


def test_zero_depth_valid_empty_tank():
    assert calculate_from_units(10,6,0,'in')['volume_gallons']==0.0
