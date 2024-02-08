import pandas as pd
import numpy as np


def data_selector(reeds_df: pd.DataFrame, 
                  policy = None, 
                  state = None, 
                  scenario = None,
                  t = None,
                  results = 'capacity'):
    """
    Parameters
    ----------
    reeds_df : pd.DataFrame
        A dataframe containing results from a ReEDS run. ReEDS is a capacity expansion model
        from the National Renewable Energy Laboratory (NREL). The results from this model are
        viewable and downloadable at: https://scenarioviewer.nrel.gov/
    policy : str, or List[str], optional
        A string specifying which policy scenario to view.
    state : str, or List[str]
        A string specifying the state (United States) of interest using the two letter state
        code. E.g., Michigan --> `MI`.
    scenario : str, or List[str], optional
        A string specifying the specific model run (a.k.a. "case" or "scenario").
    t : int, or List[int], optional
        An optional parameter that further isolates a single year of interest in the ReEDS model
        time horizon. The default is `None` which results in a dataframe that reports all modeled
        years for each scenario.
    results : str, or List[str], optional
        An optional string indicating which kind of results to view. Currently supported options
        are: ['capacity', 'energy']. Default is `capacity`, which reports the capacity of each energy
        resource in each year.
        
    Returns
    -------
    results_df : pd.DataFrame
        The simplified dataframe based on the criteria provided.
    """
    
    params = locals()
    results_df = reeds_df.copy()
    category_cols = ['scenario','policy','t', 'state']
    categories = {col:reeds_df[col].unique() for col in category_cols}
    
    results_cols = []
    for i, col in enumerate(reeds_df.columns):
        if (results.lower() == 'capacity') and ('MW' in col) and not ('MWh' in col):
                results_cols.append(col)
        elif (results.lower() == 'energy') and ('MWh' in col):
                results_cols.append(col)
    
    for col in category_cols:
        if params[col]:
            if isinstance(params[col], list):
                results_df = results_df[results_df[col].isin(params[col])]
            else:
                results_df = results_df[results_df[col] == params[col]]
        
    results_df = results_df[category_cols+results_cols]
    results_df.reset_index(inplace=True, drop=True)

    return results_df