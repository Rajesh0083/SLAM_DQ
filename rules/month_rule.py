import pandas as pd
from rules.base_rule import BaseRule

class FinancialMonthRule(BaseRule):
    """
    Validates the 'Financial Month' column in a dataset.
    """

    def __init__(self, column_name: str, current_file_month: int, **kwargs):
        super().__init__(column_name, **kwargs)
        self.current_file_month = int(current_file_month)

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate that financial month is numeric, 1–12, and <= file month.
        Returns DataFrame with _Result and _Reason columns.
        """
        # ✅ 0. Column type validation
        if not pd.api.types.is_numeric_dtype(df[self.column_name]):
            print(
                f"⚠️ Column '{self.column_name}' is not numeric type "
                f"({df[self.column_name].dtype}). Values may need conversion."
            )
        results, reasons = [], []

        for idx, val in enumerate(df[self.column_name]):
            reason_list = []
            val_str = str(val).strip() if not pd.isna(val) else ""

            # 1️⃣ Mandatory check
            if val_str == "":
                reason_list.append("Blank - mandatory field.")
                results.append("FAIL")
                reasons.append("; ".join(reason_list))
                continue

            # 2️⃣ Numeric check
            if not val_str.isdigit():
                reason_list.append("Not numeric.")

            # 3️⃣ Length check
            if len(val_str) > 2:
                reason_list.append("More than 2 digits.")

            # 4️⃣ Range check
            try:
                num = int(val_str)
                if num < 1 or num > 12:
                    reason_list.append("Invalid month (must be 1–12).")
            except ValueError:
                reason_list.append("Not convertible to integer.")

            # 5️⃣ Logical check
            if val_str.isdigit():
                num = int(val_str)
                if num > self.current_file_month:
                    reason_list.append(f"Month {num} exceeds current file month ({self.current_file_month}).")

            # Finalize results
            if reason_list:
                results.append("FAIL")
                reasons.append("; ".join(reason_list))
            else:
                results.append("PASS")
                reasons.append("")

        df[f"{self.column_name}_Result"] = results
        df[f"{self.column_name}_Reason"] = reasons
        return df
