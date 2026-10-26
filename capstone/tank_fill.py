"""Workbook-traceable rectangular tank fill calculation, US gallons.

Inherited source: Barquito0/EGN-321-Module-1/original/TANK_FILL_rev4.xlsx
This module deliberately separates input units from the calculation so a value
labeled 2.5 feet cannot be silently treated as 2.5 inches (R-108 defect).
"""
from __future__ import annotations

import math
from numbers import Real

GALLONS_PER_CUBIC_FOOT = 7.48052
INCHES_PER_FOOT = 12.0


def numeric(name: str, value) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return value


def calculate_tank_volume(length_ft, width_ft, depth_in) -> float:
    """Return liquid volume in US gal for a rectangular tank.

    ft x ft x (in / 12) gives ft^3, multiplied by 7.48052 gives gal.
    Depth 0 is a valid empty tank. Tank height is unknown, so no fill-depth
    vs physical height safety guarantee is made.
    """
    length = numeric('length_ft', length_ft)
    width = numeric('width_ft', width_ft)
    depth = numeric('depth_in', depth_in)
    if length <= 0:
        raise ValueError('length_ft must be greater than zero')
    if width <= 0:
        raise ValueError('width_ft must be greater than zero')
    if depth < 0:
        raise ValueError('depth_in cannot be negative')
    return length * width * (depth / INCHES_PER_FOOT) * GALLONS_PER_CUBIC_FOOT


def calculate_from_units(length_ft, width_ft, fill_depth, depth_unit):
    """Require an *explicit* depth unit to prevent the R-108 silent unit mix-up."""
    if depth_unit not in ('in', 'ft'):
        raise ValueError("depth_unit must be 'in' or 'ft'; no unit is assumed")
    depth = numeric('fill_depth', fill_depth)
    depth_in = depth if depth_unit == 'in' else depth * INCHES_PER_FOOT
    gallons = calculate_tank_volume(length_ft, width_ft, depth_in)
    return {'volume_gallons': gallons, 'depth_inches_used': depth_in,
            'depth_unit_supplied': depth_unit, 'method': 'rectangular tank volume'}


def total_run_volumes(runs):
    """Sum *every* provided run (no fixed spreadsheet SUM range).

    Every run must carry length_ft, width_ft, fill_depth, depth_unit.
    Any invalid row refuses the entire total; no silent omission.
    """
    if not isinstance(runs, list) or not runs:
        raise ValueError('runs must be a nonempty list')
    seen = set()
    total = 0.0
    details = []
    for index, row in enumerate(runs, 1):
        if not isinstance(row, dict):
            raise ValueError(f'run {index}: expected an object')
        identifier = row.get('run_id')
        if not identifier or not isinstance(identifier, str):
            raise ValueError(f'run {index}: run_id is required')
        if identifier in seen:
            raise ValueError(f'run {index}: duplicate run_id {identifier}')
        seen.add(identifier)
        try:
            result = calculate_from_units(row['length_ft'], row['width_ft'],
                                           row['fill_depth'], row['depth_unit'])
        except KeyError as exc:
            raise ValueError(f'run {index}: required field missing: {exc.args[0]}') from exc
        except ValueError as exc:
            raise ValueError(f'run {index} ({identifier}): {exc}') from exc
        total += result['volume_gallons']
        details.append({'run_id': identifier, **result})
    return {'total_gallons': total, 'run_count': len(details), 'runs': details}
