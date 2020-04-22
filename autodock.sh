#!/bin/sh
wget -nc https://files.rcsb.org/download/6LU7.pdb

grep ATOM 6LU7.pdb > R.pdb
./pymol/bin/pymol R.pdb -c -d "remove resn HOH;h_add acceptors or donors;save temp.pdb"
babel temp.pdb temp.pdbqt -xh
grep ATOM temp.pdbqt > cov_receptor.pdbqt

obabel cov_inhibitor.smi -opdbqt -m --gen3d best -p -xh

./vina --receptor cov_receptor.pdbqt --ligand cov_inhibitor.pdbqt --out cov_out.pdbqt --log ligand.log --exhaustiveness 2 --center_x -10 --center_y 15 --center_z 70 --size_x 10 --size_y 20 --size_z 20  >>output.txt
