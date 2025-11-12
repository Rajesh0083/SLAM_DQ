import pandas as pd
from abc import ABC, abstractmethod

class BaseRule(ABC):
    """
    Base class for all data quality rules.
    Each specific rule (e.g., FinancialMonthRule, DateFormatRule) will inherit from this.
    """

    def __init__(self, column_name: str, rule_name: str = None, **kwargs):
        self.column_name = column_name
        self.rule_name = rule_name or self.__class__.__name__
        self.params = kwargs  # Additional rule parameters
        self.results = None   # Store results DataFrame after validation

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to be implemented by all child rules.
        Each rule must take a DataFrame and return a DataFrame with validation results.
        """
        pass

    def _mark_fail(self, reason: str) -> dict:
        """
        Utility to standardize failure reporting.
        """
        return {"Result": "FAIL", "Reason": reason}

    def _mark_pass(self) -> dict:
        """
        Utility to standardize pass reporting.
        """
        return {"Result": "PASS", "Reason": ""}

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Wrapper method to execute the rule and handle exceptions.
        Adds Result and Reason columns to the DataFrame.
        """
        try:
            validated_df = self.validate(df)
            self.results = validated_df
            return validated_df
        except Exception as e:
            print(f"❌ Error in rule '{self.rule_name}' for column '{self.column_name}': {e}")
            df[f"{self.column_name}_Result"] = "ERROR"
            df[f"{self.column_name}_Reason"] = str(e)
            self.results = df
            return df

    def summary(self) -> pd.DataFrame:
        """
        Returns a simple summary DataFrame (count of PASS/FAIL/Error).
        """
        if self.results is None:
            return pd.DataFrame(columns=["Rule", "PASS", "FAIL", "ERROR"])

        summary = {
            "Rule": [self.rule_name],
            "PASS": [(self.results.filter(like="_Result") == "PASS").sum().sum()],
            "FAIL": [(self.results.filter(like="_Result") == "FAIL").sum().sum()],
            "ERROR": [(self.results.filter(like="_Result") == "ERROR").sum().sum()]
        }

        return pd.DataFrame(summary)
