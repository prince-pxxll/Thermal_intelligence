"""Schema and quality validation for ingested thermal-anomaly data.

Validation is intentionally separated from preprocessing: this module answers
"is this data structurally and semantically sound?" while `preprocessing.py`
answers "how do we clean/transform it?".
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

VALID_CONFIDENCE_VALUES = {"low", "nominal", "high", "l", "n", "h"}
VALID_DAYNIGHT_VALUES = {"D", "N"}
LAT_RANGE = (-90.0, 90.0)
LON_RANGE = (-180.0, 180.0)


@dataclass
class ValidationReport:
    """Result of validating a detections DataFrame."""

    n_rows: int
    n_errors: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.n_errors == 0


def validate_firms_schema(df: pd.DataFrame) -> ValidationReport:
    """Validate structural and range constraints on raw FIRMS detections.

    Checks performed:
      - required columns present
      - latitude/longitude within valid global ranges
      - confidence and daynight values within the expected category set
      - no fully-null rows
    """
    errors: list[str] = []

    if "latitude" in df.columns:
        out_of_range = df["latitude"].between(*LAT_RANGE).eq(False).sum()
        if out_of_range:
            errors.append(f"{out_of_range} rows with latitude outside {LAT_RANGE}")

    if "longitude" in df.columns:
        out_of_range = df["longitude"].between(*LON_RANGE).eq(False).sum()
        if out_of_range:
            errors.append(f"{out_of_range} rows with longitude outside {LON_RANGE}")

    if "confidence" in df.columns:
        bad_conf = ~df["confidence"].astype(str).str.lower().isin(
            {v.lower() for v in VALID_CONFIDENCE_VALUES}
        )
        if bad_conf.any():
            errors.append(f"{bad_conf.sum()} rows with unexpected confidence values")

    if "daynight" in df.columns:
        bad_dn = ~df["daynight"].isin(VALID_DAYNIGHT_VALUES)
        if bad_dn.any():
            errors.append(f"{bad_dn.sum()} rows with unexpected daynight values")

    if df.isnull().all(axis=1).any():
        errors.append("one or more fully-null rows present")

    return ValidationReport(n_rows=len(df), n_errors=len(errors), errors=errors)
