import os

import pandas as pd


def compare_files(paths):
    more_files = True
    final_files = []
    while more_files:
        new_paths = []
        for path in paths:
            os.scandir(path)
            new_paths += [f.path for f in os.scandir(path) if f.is_dir()]
        paths = []
        for path in new_paths:
            if '40' in path:
                final_files.append(path)
            else:
                paths.append(path)
        if len(paths) == 0:
            more_files = False
    return final_files

def extract_data_per_folder(paths):
    results = {'0':{},'1':{},'2':{}}
    for path in paths:
        new_paths = [f.path for f in os.scandir(path) if f.is_dir()]
        for folder_path in new_paths:
            data = pd.read_csv(folder_path+'\\results_rms.csv')
            vo = data[data['frame_idx'] == 7]['adv_delta_rms'].sum()
            components = folder_path.split('\\')
            name = ''
            file = None
            for comp in components:
                if 'Linf' in comp:
                    attack = comp.split('_')[1]+'_'
                    name += attack
                elif 'crit' in comp:
                    mini_comp = comp.split('_')
                    for i,word in enumerate(mini_comp):
                        if word == 'factor':
                            loss = '_'.join(mini_comp[:i])+'_'
                            name += loss
                            break
                elif 'eps' in comp:
                    name += comp +'_'
                elif 'test' in comp:
                    file = comp.split('_')[1]
            results[file][name] = vo
    return results


def get_ranking_of_runs_per_folder(results):
    final_dfs = []
    for key in results.keys():
        ranking = [(key,value) for key,value in results[key].items()]
        ranking = sorted(ranking,key = lambda x:x[1],reverse=True)
        final_df = pd.DataFrame(ranking)
        final_dfs.append(final_df)
    return final_dfs

lr = 1
for i in range(40):
    lr *=0.95
    print(lr)
paths = [r'C:\Users\yonip\Desktop\school_projects\semester_6\deep_learning\results']
paths = compare_files(paths)
results = extract_data_per_folder(paths)
dfs = get_ranking_of_runs_per_folder(results)


