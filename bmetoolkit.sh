#!/bin/bash


curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
conda create -c rdkit  -n my-rdkit-env rdkit
conda activate my-rdkit-env
conda install scikit-learn=0.21.2
pip install tensorflow==1.15rc
conda install -c conda-forge matplotlib=3.1.0
conda install -c pytorch pytorch=1.2.0
conda install -c conda-forge pytables=3.5.2
conda install -c conda-forge pysimplegui
pip install IPython==7.7.0
pip install joblib==0.13.2
pip install keras==2.2.4
pip install runipy==0.1.5
pip install scikit-learn==.21.2
pip install nbconvert==5.6.0
pip install nbformat==4.4.0
pip install PySimpleGUI==4.1.0
pip install matplotlib==3.1.0
pip install numpy==1.16.4
pip install pandas

