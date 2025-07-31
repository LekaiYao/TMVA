```
Before running TMVA_BDTs.py and apply.py, please make sure the input and output paths/names are correct

0.To remove nan or inf entries
  root -l select.C
1.To run TMVA (even when disconnected)
  nohup python3 -u TMVA_BDTs.py test1 > log.txt 2>&1 &
2.To check whether the TMVA is still running
  ps aux | grep 'python3.*TMVA_BDTs.py'
or
  ls -l log.txt
  cat log.txt
3.To get BDT scores for further optimization
  python3 apply.py


```
