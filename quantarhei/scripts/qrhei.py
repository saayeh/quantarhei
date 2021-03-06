# -*- coding: utf-8 -*-
import argparse
import subprocess

from quantarhei import Manager

    
def main():

    parser = argparse.ArgumentParser(
            description='Quantarhei Package Driver')
 
    parser.add_argument("script", metavar='script', type=str,
                        help='script file to be processed')    
    parser.add_argument("-v", "--version", action="store_true",
                        help="shows Quantarhei package version")
    parser.add_argument("-i", "--info", action='store_true', 
                        help="shows detailed information about Quantarhei"+
                        " installation")
    parser.add_argument("-s", "--silent", action='store_true', 
                        help="no output from qrhei script itself")
    parser.add_argument("-p", "--parallel", action='store_true', 
                        help="executes the code in parallel")
    parser.add_argument("-n", "--nprocesses", type=int, default=0,
                        help="number of processes to start")
    
    args = parser.parse_args() 
    
    
    nprocesses = args.nprocesses
    flag_parallel = args.parallel
    flag_silent = args.silent

    #
    # show longer info
    #
    if args.info:
        print("")
        print("qrhei: Quantarhei Package Driver")
        print("")
        print("MPI parallelization enabled: ", flag_parallel)
        if not args.version:
            print("Quantarhei package version: ", Manager().version)
            
    #
    # show just Quantarhei version number
    #
    if args.version:
        print("Quantarhei package version: ", Manager().version)

    ###########################################################################    
    #
    # Running a script
    #
    ###########################################################################
    
    #
    # Script name
    # 
    scr = args.script

    #
    # Greeting 
    #
    if not flag_silent:
        print("Running Quantarhei (python) script file: ", scr)

    
    #
    # Run serial or parallel 
    #
        
    if flag_parallel:
        
        #
        # get parallel configuration
        #
        cpu_count = 0
        try:
            import multiprocessing
            cpu_count = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass        
        
        prl_exec = "mpirun"
        prl_n = "-n"
        
        if cpu_count != 0:
            prl_np = cpu_count
        else:
            prl_np = 4
            
        if nprocesses != 0:
            prl_np = nprocesses
        
        engine = "qrhei -s "
        
        # running MPI with proper parallel configuration
        prl_cmd = prl_exec+" "+prl_n+" "+str(prl_np)+" "
        cmd = prl_cmd+engine+scr
        if not flag_silent:
            print("System reports", cpu_count,"processors")
            print("Starting parallel execution with",prl_np,
            "processes (executing command below)")
            print(cmd)
            print("")
        p = subprocess.Popen(cmd,
                             shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        if not flag_silent:
            print(" --- output below ---")
        
        # read and print output
        for line in iter(p.stdout.readline, b''):
        #for line in p.stdout.readlines():
            ln = line.decode()
            # line is returned with a \n character at the end 
            # ln = ln[0:len(ln)-2]
            print(ln, end="", flush=True)
            
        retval = p.wait()    
        
    else:
        
        if not flag_silent:
            print(" --- output below ---")
        # running the script within the same interpreter
        exec(open(scr).read(), globals())
        
        retval = 0        
        
    #
    # Saying good bye
    #
    if retval == 0:
        if not flag_silent:
            print(" --- output above --- ")
            print("Finshed sucessfully; exit code: ", retval)
    else:
        print("Warning, exit code: ", retval)
        
    
