# Universal-Patch-Adverserial-Attacks-Project
### Structure of folder:  

In src there is one folder called Universal-Patch-Adverserial-Attacks-Project.
Inside  Universal-Patch-Adverserial-Attacks-Project folder there are 2 folders:  
* code- contains all the relevent code for the project.
* data- empty folder. Should add the data (unprocessed or processed) to this folder.  
<!-- -->
Inside the code folder:  
  
**Directories:**  
* Attacks
* Datasets
* Docker
* Evaluator
* Models
* Network
<!-- -->
**Files:** 
* loss.py
* run_attacks.py
* run_attacks_cross_train_eval.py
* TartanVO.py
* Tartanvo_node.py
* utils.py
<!-- -->  
Those are the additions we made to the original code in terms of code structure.
1.	New file called run_attacks_cross_train_eval.py used to run the final model as described in our report.
2.	In the code/attacks folder there is a new file called apgd.py which is used to run apgd attacks.
<!-- -->
All the other changes were done to the existing code and were integrated into it. 
  
**Note worty changes:**  
  
Added the following methods to Attack in attacks/attack.py:
* gradient_ascent_step_with_adam_optimizer - gradient ascent with adam optimizer.
* gradient_ascent_step_with_simple_momentum - gradient ascent with momentum.
* gradient_ascent_step_with_apgd_momentum - gradient ascent as decribed in the apgd paper.
* gradient_ascent_step_with_apgd_adam - gradient ascent which combines adam and apgd.
<!-- -->
Added the following methods to VOCriterion in loss.py:
* calc_weighted_cumul_poses_t - calculates weighted rms.
* calc_reverse_weighted_cumul_poses_t - calculates reverse weighted rms.  
<!-- -->
The implementation for adam optimizer is in attacks/attack.py.  
New arguments in utils.py:
* anneal_method - String. schedular. Can be exp for original schedular or cosine schedular in apgd.
* momentum- Float. controls momentum variable (for momentum, Adam etc).
* sign - Boolean. Sign or unsigned gradient ascent.
* gradient_ascent_method - String. Controls the gradient ascent method. Can be: gradient_ascent,momentum,adam,apgd_momentum,apgd_adam.
* p_1 - Float. Controls checkpoints generation in apgd.
* rho - Float. Hyper paramter for apgd.
<!-- -->
### Reproduce results
#### Final model
In order to reproduce our final chosen model, run the following:  
srun -c 2 --gres=gpu:1 --pty python code/run_attacks_cross_train_eval.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 100 --attack apgd --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_momentum --sign --anneal_method exp --save_best_pert  
  
The perturbation we chose will be located in the path: 
  
results/kitti_custom/tartanvo_1914/VO_adv_project_train_dataset_8_frames/train_attack/universal_attack/gradient_ascent/attack_apgd_norm_Linf/opt_whole_trajectory/opt_t_crit_none_factor_1_0_rot_crit_none_flow_crit_none_target_t_crit_none/eval_rms/eps_1_attack_iter_100_alpha_0_05_optimization_method__signed_apgd_momentum_momentum_0.9_anneal_exp/eval_4/adv_best_pert  
  
The folder of results will be created when the script runs.    
  
In order to run the script there needs to be a folder of data under the folder    
  
Its also possible to run the same script with the flag --preprocessed_data in case the folder VO_adv_project_train_dataset_8_frames_processed exists in the data folder to save run time.  
#### Experiment results
In order to reproduce our experiment results run run_attacks.py with the parameters you wish.  
  
The results will be save at results depending on the hyperparameters you chose as a csv file. 
  
**Note:** The model is tested on all the data during the cross validation, but the results we showed were after filtering according to the testing folder.  
The commends we used were:   
  
srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack pgd  --model-name tartanvo_1914.pkl --gradient_ascent_method gradient_ascent --sign;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack pgd  --model-name tartanvo_1914.pkl --gradient_ascent_method gradient_ascent;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack pgd  --model-name tartanvo_1914.pkl --gradient_ascent_method momentum --sign;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack pgd  --model-name tartanvo_1914.pkl --gradient_ascent_method adam --sign;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack pgd  --model-name tartanvo_1914.pkl --gradient_ascent_method adam --sign --attack_t_crit weighted_rms;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack pgd  --model-name tartanvo_1914.pkl --gradient_ascent_method adam --sign --attack_t_crit reverse_weighted_rms;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_momentum --sign;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_momentum;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_adam --sign;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_adam;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_momentum --sign --anneal_method cosine;

srun -c 2 --gres=gpu:1 --pty python code/run_attacks.py --save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 40 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_adam --sign --anneal_method cosine;

