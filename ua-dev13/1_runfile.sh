#!/bin/bash
#SBATCH --job-name=dev13
#SBATCH --nodes=1
#SBATCH --time=2-00
#SBATCH --account=bar
#SBATCH --mail-user=emmanuel.branlard@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL              # Send e-mail when job begins, ends or fails
#SBATCH -o slurm-%x-%j.log                      # Output


echo "Working directory is" $SLURM_SUBMIT_DIR
echo "Job name is" $SLURM_JOB_NAME
echo "Job ID is " $SLURM_JOBID
echo "Starting job at: " $(date)

module purge
module load comp-intel mkl 

openfast=../openfast-dev13-3e09b59

$openfast iea22_stab_00.fst & sleep 1 
$openfast iea22_stab_01.fst & sleep 1
$openfast iea22_stab_02.fst & sleep 1
$openfast iea22_stab_03.fst & sleep 1
$openfast iea22_stab_04.fst & sleep 1
$openfast iea22_stab_05.fst & sleep 1
$openfast iea22_stab_06.fst & sleep 1
$openfast iea22_stab_07.fst & sleep 1
$openfast iea22_stab_10.fst & sleep 1
$openfast iea22_stab_11.fst & sleep 1
$openfast iea22_stab_12.fst & sleep 1
$openfast iea22_stab_13.fst & sleep 1
$openfast iea22_stab_14.fst & sleep 1
$openfast iea22_stab_15.fst & sleep 1
$openfast iea22_stab_16.fst & sleep 1
$openfast iea22_stab_17.fst & sleep 1
$openfast iea22_stab_20.fst & sleep 1
$openfast iea22_stab_21.fst & sleep 1
$openfast iea22_stab_22.fst 

wait



echo "Ending job at: " $(date)
