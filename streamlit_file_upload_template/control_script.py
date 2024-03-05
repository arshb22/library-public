import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
pandas2ri.activate()


def run_r_script_v1(script_path):
    with open(script_path, 'r') as file:
        r_script = file.read()
    
    ro.r(r_script)
    
    r_df = ro.r('df')
    py_df = pandas2ri.ri2py_dataframe(r_df)
    
    return py_df

py_df = run_r_script('path_to_your_script.R')
print(py_df)


def run_r_script_gpt(script_path):
    # Activate the automatic conversion of rpy2 objects to pandas objects
    pandas2ri.activate()
    
    # Load the R script
    robjects.r.source(script_path)
    
    # Assume the R script saves the results in a variable named 'results'
    # If your R script uses a different variable name, change it here
    r_results = robjects.r['results']
    
    # Convert the R data.frame to a pandas DataFrame
    with localconverter(robjects.default_converter + pandas2ri.converter):
        pd_results = robjects.conversion.rpy2py(r_results)
    
    # Deactivate the pandas conversion
    pandas2ri.deactivate()
    
    return pd_results
