import os

import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

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
    results = {'in': {}, 'out': {}, 'total': {}}
    for path in paths:
        new_paths = [f.path for f in os.scandir(path) if f.is_dir()]
        for folder_path in new_paths:
            components = folder_path.split('\\')
            name = ''
            file = None
            for comp in components:
                if 'Linf' in comp:
                    attack = comp.split('_')[1] + '_'
                    name += attack
                elif 'crit' in comp:
                    mini_comp = comp.split('_')
                    for i, word in enumerate(mini_comp):
                        if word == 'factor':
                            temp = mini_comp[:i]
                            temp.remove('opt')
                            temp.remove('t')
                            temp.remove('crit')
                            if 'none' in temp:
                                temp.remove('none')
                                temp.append('regular')
                            loss = '_'.join(temp) + '_'
                            name += loss
                            break
                elif 'eps' in comp:
                    new_comp = ''
                    record = False
                    flag = False
                    for mini_comp in comp.split('_'):
                        if mini_comp == 'method':
                            record = True
                            continue
                        if mini_comp == 'momentum':
                            record = False
                            if flag:
                                new_comp += mini_comp + '_'
                            flag = ~flag
                        if mini_comp == '0.9':
                            record = True
                            continue
                        if record:
                            if len(mini_comp) == 0:
                                continue
                            if mini_comp == 'exp':
                                mini_comp = 'regular'
                            if mini_comp == 'apgd':
                                continue
                            new_comp += mini_comp + '_'
                    name += new_comp + '_'
                elif 'test' in comp:
                    file = int(comp.split('_')[1])
            name = name[:-2]
            if name == 'pgd_regular_signed_gradient_ascent':
                name = 'baseline'
            data = pd.read_csv(folder_path + '\\results_rms.csv')
            for key in results.keys():
                if name not in results[key].keys():
                    results[key][name] = {}
                for option in ['delta', 'ratio']:
                    if option not in results[key][name].keys():
                        results[key][name][option] = {}
                    if key == 'in':
                        folders = [i for i in range(5) if i != file]
                    elif key == 'out':
                        folders = [file]
                    else:
                        folders = [i for i in range(5)]
                    if option == 'ratio':
                        results[key][name][option][file] = {}
                        for i in range(8):
                            results[key][name][option][file][i] = calc_ratio_from_rms(data, folders,i)
                    else:
                        results[key][name][option][file] = {}
                        for i in range(8):
                            results[key][name][option][file][i] = calc_delta_from_rms(data, folders,i)
            # results['out'][file][name] = calc_ratio_from_rms(data,[int(file)])
            # results[file]['in'][name] = calc_ratio_from_rms(data,[i for i in range(5) if i != int(file)])
            # results[file]['total'][name] = calc_ratio_from_rms(data,[i for i in range(5)])
    return results


def calc_ratio_from_rms(data, folders,i):
    ratios = data[(data['frame_idx'] == i) & (data['dataset_name'].isin(folders))]['adv_ratio_rms']
    return ratios.tolist()


def calc_delta_from_rms(data, folders,i):
    deltas = data[(data['frame_idx'] == i) & (data['dataset_name'].isin(folders))]['adv_delta_rms']
    return deltas.to_list()


def get_ranking_of_runs_per_folder(results):
    final_dfs_in = []
    final_dfs_out = []
    final_dfs = []
    for key in results.keys():
        for key_2 in results[key].keys():
            ranking = [(key, value) for key, value in results[key][key_2].items()]
            ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
            final_df = pd.DataFrame(ranking)
            if key_2 == 'in':
                final_dfs_in.append(final_df)
            elif key_2 == 'out':
                final_dfs_out.append(final_df)
            else:
                final_dfs.append(final_df)
    return final_dfs_in, final_dfs_out, final_dfs


def method_stats(results, interest):
    df = pd.DataFrame(columns=['Algorithm', 'Mean_ratio', 'STD_ratio', 'Mean_delta', 'STD_delta'])
    for algo in results[interest].keys():
        row = {'Algorithm': algo}
        for option in results[interest][algo].keys():
            all = []
            for file in results[interest][algo][option].keys():
                for index,data in results[interest][algo][option][file].items():
                    if index != 7:
                        continue
                    all += data
            all = np.array(all)
            mean = all.mean()
            row['Mean_' + option] = mean
            std = all.std()
            row['STD_' + option] = std
        df = df.append(row, ignore_index=True)
    return df


def stats_over_trajectory(results, interest):
    plt.figure(figsize=(12, 8))
    res = {}
    for algo in results[interest].keys():
        res[algo] = []
        for option in results[interest][algo].keys():
            if option != 'ratio':
                continue
            for position in range(8):
                position_data = []
                for file in results[interest][algo][option].keys():
                    position_data += results[interest][algo][option][file][position]
                position_data = np.array(position_data)
                mean = position_data.mean()
                res[algo].append(mean)
    #for algo in ['baseline','pgd_regular_signed_adam','pgd_weighted_rms_signed_adam','pgd_reverse_weighted_rms_signed_adam']:
    for algo in res.keys():
        plt.plot(np.arange(8),np.array(res[algo])*100,label = algo)
    plt.xlabel('frame')
    plt.ylabel('Ratio in percentages (%)')
    plt.title('Algorithms mean performance of trajectories')
    plt.legend()
    plt.show()

def final_attack_eval(path):
    folder_paths = [f.path for f in os.scandir(path) if f.is_dir()]
    df = pd.DataFrame(columns=['Folder','Mean ratio','STD ratio','Mean delta','STD delta'])
    for folder_path in folder_paths:
        eval_folder = int(folder_path.split('_')[-1])
        row = {'Folder':eval_folder}
        data = pd.read_csv(folder_path +r'\results_rms.csv')
        eval_data = data[(data['dataset_name'] == eval_folder)&(data['frame_idx'] == 7)]
        row['Mean ratio'] = eval_data['adv_ratio_rms'].mean()
        row['STD ratio'] = eval_data['adv_ratio_rms'].std()
        row['Mean delta'] = eval_data['adv_delta_rms'].mean()
        row['STD delta'] = eval_data['adv_delta_rms'].std()
        df = df.append(row,ignore_index=True)
    df['Folder'] = df['Folder'].astype(int)
    return df
# paths = [r'C:\Users\yonip\Desktop\school_projects\semester_6\deep_learning\results']
# paths = compare_files(paths)
# results = extract_data_per_folder(paths)
# results_table = method_stats(results, 'out')
# stats_over_trajectory(results,'out')
final_attack_eval(r'C:\Users\yonip\Desktop\school_projects\semester_6\deep_learning\final_method')
