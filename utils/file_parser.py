import os
import re
from datetime import datetime

def parse_filename(file_name: str) -> dict:
    """
    Extract key information from a standardized file name.
    Expected pattern example:
    ID12345_RHW00_0CN_ACM0000_20250901_DCB2050_A000_P00_V01.xlsx

    Returns a dictionary with provider, dataset, year, month, and day.
    """

    try:
        # Remove extension and normalize case
        base_name = os.path.splitext(os.path.basename(file_name))[0].upper()

        # Split by underscore
        parts = base_name.split("_")

        # Default return values
        parsed = {
            "provider_code": None,
            "dataset_type": None,
            "year": None,
            "month": None,
            "day": None
        }

        # 1️⃣ Provider code extraction (e.g., RHW00 → RHW)
        provider_part = next((p for p in parts if re.match(r"^[A-Z]{3,5}0*$", p)), None)
        if provider_part:
            parsed["provider_code"] = re.sub(r"0+$", "", provider_part)

        # 2️⃣ Dataset type extraction (ACM, DRUGS, DEVICES etc.)
        dataset_part = next((p for p in parts if re.match(r"^[A-Z]{3,10}0*$", p) and not p.startswith("ID")), None)
        if dataset_part:
            parsed["dataset_type"] = re.sub(r"0+$", "", dataset_part)

        # 3️⃣ Extract date part (YYYYMMDD)
        date_match = re.search(r"(\d{8})", base_name)
        if date_match:
            date_str = date_match.group(1)
            parsed["year"] = int(date_str[:4])
            parsed["month"] = int(date_str[4:6])
            parsed["day"] = int(date_str[6:8])

        return parsed

    except Exception as e:
        raise RuntimeError(f"Error parsing file name '{file_name}': {e}")


def get_financial_month_from_filename(file_name: str) -> int:
    """
    Derive the logical 'data month' based on filename date.
    If providers submit 1 month later, subtract 1 month from the date part.
    """
    try:
        parsed = parse_filename(file_name)
        if not parsed.get("year") or not parsed.get("month"):
            raise ValueError("No date information found in filename.")

        date = datetime(parsed["year"], parsed["month"], 1)

        # Subtract one month since submission is one month late
        prev_month = (date.month - 1) or 12
        prev_year = date.year if date.month > 1 else date.year - 1

        return prev_month, prev_year

    except Exception as e:
        raise RuntimeError(f"Error deriving financial month: {e}")
