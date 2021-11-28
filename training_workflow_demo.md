# training workflow demo
This is a training workflow demo using dataset tox21 on CARC cluster.

---

## Environment Setup
### 1. install conda
- in "~/.bashrc": *module load anaconda3*
- *conda init bash*
- *source ~/.bashrc*

### 2. install chemprop
- *conda create -n chemprop python=3.8*
- *conda activate chemprop*
- *conda install -c conda-forge rdkit*
- *pip install git+https://github.com/bp-kelley/descriptastorus*
- *pip install chemprop*

### 3. support GPU
- *conda install pytorch\==1.8.0 torchvision\==0.9.0 torchaudio\==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge*
- in "~/.bashrc": *module load cuda/11.1-1* & *module load cudnn/8.0.4.30-11.1*

---

## Resources allocation
### 1. request CPU
- *salloc -n 1 -t 30*
### 2. request GPU
- *salloc --partition=gpu --gres=gpu:a100:1 --time=00:30:00 --mem=16GB*

---

## Training Mode
### 1. normal training
- *chemprop_train --data_path train_data/tox21.csv --dataset_type classification --save_dir normal_training*
### 2. normal+RDkit training
- *chemprop_train --data_path train_data/tox21.csv --dataset_type classification --save_dir normal_rdkit_training --features_generator rdkit_2d_normalized --no_features_scaling*
### 3. normal+HyperOpt training
- *chemprop_hyperopt --data_path train_data/tox21.csv --dataset_type classification --num_iters 5 --config_save_path normal_hyperopt_training/config.json*
- retrain with best config: *chemprop_train --data_path train_data/tox21.csv --dataset_type classification --config_path normal_hyperopt_training/config.json --save_dir normal_hyperopt_training/save_model*
### 4. normal+ensemble training
- *chemprop_train --data_path train_data/tox21.csv --dataset_type classification --save_dir normal_ensemble_training --ensemble_size 3*
### 5. hybrid training(e.g. normal+rdkit+hyperopt+ensemble)
- *chemprop_hyperopt --data_path train_data/tox21.csv --dataset_type classification --features_generator rdkit_2d_normalized --no_features_scaling --num_iters 3 --config_save_path normal_rdkit_hyperopt_ensemble_training/config.json --log_dir normal_rdkit_hyperopt_ensemble_training/log --ensemble_size 3*

---

To be continued...
