from glob import glob
import os
import subprocess
from sys import argv
import warnings

def compare_restarts(test_run_dir,ref_run_dir):
    restart_files=glob(test_run_dir+'/*RESTART*')
    hydro_files=glob(test_run_dir+'/*HYDRO_RST*')
    nudging_files=glob(test_run_dir+'/*nudgingLastObs*')
    
    #Make a flag for when comparisons actually happen
    comparison_run_check = 0

    #Make a flag for exit codes
    exit_code = 0

    #Compare RESTART files
    restart_out = list()
    print('Comparing RESTART files')
    for test_run_file in restart_files:
        test_run_filename = os.path.basename(test_run_file)
        ref_run_file = glob(ref_run_dir+'/'+test_run_filename)
        if len(ref_run_file) == 0:
            warnings.warn(test_run_filename+' not found in reference run directory')
        else:
            print('Comparing candidate file ' + test_run_file + ' against reference file ' + ref_run_file[0])
            restart_comp_out = subprocess.run(['nccmp', '-dmfq', '-S',\
                                               '-x ACMELT,ACSNOW,SFCRUNOFF,UDRUNOFF,ACCPRCP,ACCECAN,ACCEDIR,ACCETRAN,qstrmvolrt',\
                                               test_run_file,ref_run_file[0]],\
                                              stderr=subprocess.STDOUT)
            if restart_comp_out.returncode != 0:
                print(restart_comp_out.stdout)
            restart_out.append(restart_comp_out)
            comparison_run_check = 1

    #Compare HYDRO_RST files
    hydro_out = list()
    print('Comparing HYDRO_RST files')
    for test_run_file in hydro_files:
        test_run_filename = os.path.basename(test_run_file)
        ref_run_file = glob(ref_run_dir+'/'+test_run_filename)
        if len(ref_run_file) == 0:
            warnings.warn(test_run_filename+' not found in reference run directory')
        else:
            print('Comparing candidate file ' + test_run_file + ' against reference file ' + ref_run_file[0])
            hydro_restart_comp_out = subprocess.run(['nccmp', '-dmfq', '-S',\
                                               '-x ACMELT,ACSNOW,SFCRUNOFF,UDRUNOFF,ACCPRCP,ACCECAN,ACCEDIR,ACCETRAN,qstrmvolrt', \
                                                     test_run_file,ref_run_file[0]],\
                                              stderr=subprocess.STDOUT)
            if hydro_restart_comp_out.returncode != 0:
                print(hydro_restart_comp_out.stdout)
            hydro_out.append(hydro_restart_comp_out)
            comparison_run_check = 1

    #Compare nudgingLastObs files
    nudging_out = list()
    print('Comparing nudgingLastObs files')
    for test_run_file in nudging_files:
        test_run_filename = os.path.basename(test_run_file)
        ref_run_file = glob(ref_run_dir+'/'+test_run_filename)
        if len(ref_run_file) == 0:
            warnings.warn(test_run_filename+' not found in reference run directory')
        else:
            print('Comparing candidate file ' + test_run_file + ' against reference file ' + ref_run_file[0])
            nudging_restart_out = subprocess.run(['nccmp', '-dmfq', '-S',\
                                               '-x ACMELT,ACSNOW,SFCRUNOFF,UDRUNOFF,ACCPRCP,ACCECAN,ACCEDIR,ACCETRAN,qstrmvolrt',\
                                               test_run_file,ref_run_file[0]],\
                                              stderr=subprocess.STDOUT)
            if nudging_restart_out.returncode != 0:
                print(nudging_restart_out.stdout)
            nudging_out.append(nudging_restart_out)
            comparison_run_check = 1

    #Check that a comparison was actually done
    if comparison_run_check != 1:
        print('No matching files were found to compare')
        exit(1)

    #Check for exit codes and fail if non-zero
    for output in restart_out:
        if output.returncode == 1:
            print('One or more RESTART comparisons failed, see stdout')
            exit_code = 1

    #Check for exit codes and fail if non-zero
    for output in hydro_out:
        if output.returncode == 1:
            print('One or more HYDRO_RST comparisons failed, see stdout')
            exit_code = 1

    #Check for exit codes and fail if non-zero
    for output in nudging_out:
        if output.returncode == 1:
            print('One or more nudgingLastObs comparisons failed, see stdout')
            exit_code = 1

    #If no errors exit with code 0
    if exit_code == 0:
        print('All restart file comparisons pass')
        exit(0)
    else:
        exit(1)

def main():
    test_run_dir = argv[1]
    ref_run_dir = argv[2]
    compare_restarts(test_run_dir, ref_run_dir)

if __name__ == "__main__":
    main()
