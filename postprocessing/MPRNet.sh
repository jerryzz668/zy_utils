cd /home/zy/MPRNet/Deraining
conda activate MPR
python train.py
python test.py
python -u image_quality_metrics.py --test_dir results/Rain100H --gt_dir Datasets/test/Rain100H/target > ./log.out
