from pathlib import Path
import os
import sys
from glob import glob
import pandas as pd
import argparse


file_dir = Path(os.path.dirname(os.path.abspath(__file__)))

reeds_dir = Path("C:/Users/sdotson/OneDrive - Union of Concerned Scientists/Documents/Analysis/2024_reeds_reproduction/reeds_results")


if __name__ == "__main__":

    files = glob(str(reeds_dir/"*"/"outputs"/"*.csv"))
    
    scenario_files = [f.split('\\')[-3:] for f in files]
    
    cols = ['scenario','outputs','file_name']
    
    df = pd.DataFrame(scenario_files, columns=cols)

    scenarios = df.scenario.unique()
    file_names = df.file_name.unique()
    
    output_folder = (file_dir/"../combined_results/").resolve()
    Path.mkdir(output_folder, exist_ok=True)
    print(output_folder)
    
    for fname in file_names:
        frames = []
        for scene in scenarios:
            file_path = reeds_dir/scene/"outputs"/fname
            try:
                df = pd.read_csv(str(file_path))
                df['scenario'] = scene
                frames.append(df)
                print(f"[SUCCESS] {file_path}")
            except FileNotFoundError:
                print(f'[FILE NOT FOUND] {file_path}')
                continue
        combined_df = pd.concat(frames, axis=0)
        combined_df.to_csv(str(output_folder/fname))
        
        
        