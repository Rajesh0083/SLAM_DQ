import os
import pandas as pd
from io import BytesIO

def load_file(file_obj, file_name=None):
    # ... (same as before) ...
    try:
        if isinstance(file_obj, str):
            ext = os.path.splitext(file_obj)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(file_obj)
            elif ext in [".xls", ".xlsx"]:
                df = pd.read_excel(file_obj, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            return df

        elif hasattr(file_obj, "read"):
            if not file_name and hasattr(file_obj, "name"):
                file_name = file_obj.name
            ext = os.path.splitext(file_name)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(file_obj)
            elif ext in [".xls", ".xlsx"]:
                file_bytes = BytesIO(file_obj.read())
                df = pd.read_excel(file_bytes, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported uploaded file type: {ext}")
            return df

        else:
            raise ValueError("Invalid file input provided.")

    except Exception as e:
        raise RuntimeError(f"Error loading file: {e}")


def save_output(df, output_folder, input_filename, suffix="_DQ_Report"):
    """
    Save the DataFrame as an Excel file to the user-specified folder.

    Parameters:
        df : pandas DataFrame
        output_folder : str path to folder
        input_filename : original input filename (used to generate output name)
        suffix : string to append before file extension (default: '_DQ_Report')
    """
    try:
        os.makedirs(output_folder, exist_ok=True)

        base_name, ext = os.path.splitext(os.path.basename(input_filename))
        output_filename = f"{base_name}{suffix}{ext}"
        output_path = os.path.join(output_folder, output_filename)

        df.to_excel(output_path, index=False, engine="openpyxl")
        return output_path

    except Exception as e:
        raise RuntimeError(f"Error saving output file: {e}")
