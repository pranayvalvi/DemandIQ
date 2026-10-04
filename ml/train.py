import subprocess
import sys
import os

def run_script(script_path):
    print(f"\n{'='*50}\nRunning {script_path}...\n{'='*50}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors/Warnings:\n{result.stderr}")
    if result.returncode != 0:
        print(f"Script {script_path} failed!")
        sys.exit(1)

def main():
    scripts = [
        os.path.join("ml", "src", "train_linear_regression.py"),
        os.path.join("ml", "src", "train_random_forest.py"),
        os.path.join("ml", "src", "train_xgboost.py"),
        os.path.join("ml", "src", "evaluate_models.py")
    ]
    
    for script in scripts:
        run_script(script)
        
    print("\nAll models trained and evaluated successfully!")

if __name__ == "__main__":
    main()
