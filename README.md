# Universal-Patch-Adverserial-Attacks-Project
Deep Learning final project
Structure of folder:
In src there is one folder called Universal-Patch-Adverserial-Attacks-Project.
Inside that folder there is one folder called code.
Those are the additions we made to the original code in terms of code structure.
1. New file called run_attacks_cross_train_eval.py used to run the final model as described in our report.
2. In the code/attacks folder there is a new file called apgd.py which is used to run apgd attacks.
All of the other changes were done to the existing code and were intergrated into it.
In order to repreduce or results, you need to run run_attacks_cross_train_eval.py with the following arguments:
--save_csv --test-dir=VO_adv_project_train_dataset_8_frames --attack_k 100 --attack apgd  --model-name tartanvo_1914.pkl --gradient_ascent_method apgd_momentum --sign --anneal_method exp --save_best_pert
The pertubation we chose will be located in the path:
results/kitti_custom/tartanvo_1914/VO_adv_project_train_dataset_8_frames/train_attack/universal_attack/gradient_ascent/attack_apgd_norm_Linf/opt_whole_trajectory/opt_t_crit_none_factor_1_0_rot_crit_none_flow_crit_none_target_t_crit_none/eval_rms/eps_1_attack_iter_100_alpha_0_05_optimization_method__signed_apgd_momentum_momentum_0.9_anneal_exp/eval_4/adv_best_pert
The folder of results will be created when the sript runs.
In order to run the script there needs to be a folder of data under the folder Universal-Patch-Adverserial-Attacks-Project.
Its also possible to run the same script with the flag --preprocced in case the folder VO_adv_project_train_dataset_8_frames_processed exists in the data folder to save run time.
