# Convert English digits to Persian digits
"""
core/number_utils.py

Small, dependency-free helper for converting Western Arabic digits (0-9) to
Eastern Arabic-Indic / Persian digits (۰-۹), used whenever the UI is in
Persian mode.
"""

_EN_TO_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def en_to_fa_num(value) -> str:
    """Convert every digit found in `value` (str, int, etc.) to its Persian
    digit equivalent."""
    return str(value).translate(_EN_TO_FA_DIGITS)