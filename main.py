import subprocess
import sys
import os
import time

def main():
    print("==================================================")
    print("Automated Execution of All Histogram Scripts")
    print("==================================================")
    
    # Ensure we are in the right directory (should run from root, but handle being inside 'code' too)
    if os.path.exists('code') and os.path.isdir('code'):
        os.chdir('code')
    elif os.path.basename(os.getcwd()) == 'code':
        pass # Already in code directory
    else:
        print("Error: Could not find the 'code' directory. Please run this script from the root of the repository.")
        sys.exit(1)

    scripts = ['plot1.py', 'plot2.py', 'histogram.py', 'selectivity.py']
    processes = []
    
    print("Launching all scripts concurrently. All plots will be generated at once.")
    print("NOTE: Please close all plot windows once you are done viewing them to let the script finish.\n")
    
    for script in scripts:
        print(f" -> Starting {script}...")
        p = subprocess.Popen([sys.executable, script])
        processes.append((script, p))
        # Small delay to stagger database connections and avoid console output mixing too much
        time.sleep(1)
        
    print("\nAll scripts are running. Waiting for completion...")
    
    for script, p in processes:
        p.wait()
        print(f"[{script}] finished with exit code {p.returncode}")
        
    print("\nAll processes completed successfully.")

if __name__ == "__main__":
    main()
