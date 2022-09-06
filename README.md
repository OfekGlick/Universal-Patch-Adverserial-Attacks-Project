# Universal-Patch-Adverserial-Attacks-Project
Deep Learning final project

Need to do:
1. Cross validation- 3 sets train,1  eval and 1 test.
2. Find a way to somehow create a path from the cross validation (as every train and eval will create pertubation). Don't use mean!
One idea is to use the pertubation with the highest ratio between it to clean.
3. Find a way to use the rotation matrix in the loss critria.
4. Test the ADAM optimizer preformance in the current setting.
5.Try and understand APGD.


6/9/22
1. I've heard from a few people that we shouldn't do cross validation, Yaniv recommended agaisnt it in one of the office hours, I am thinking of simply implementing to train-test folder-wise
2. See 1.
3. Have we changed anything in the loss criteria? Let's brain storm.
