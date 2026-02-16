"""
AI Sports Content Pipeline - Main Orchestrator
Runs the complete content generation pipeline in sequence.
"""
import subprocess
import time
import sys


def run_script(script_name):
    """Execute a Python script and handle errors."""
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"✓ {script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"✗ An error occurred while executing {script_name}: {e}")
        return False
    return True


def main():
    """Run the content generation pipeline continuously."""
    scripts = ['scrape.py', 'summarize.py', 'translate.py', 'rewrite.py', 'write.py']

    print("Starting AI Sports Content Pipeline...")
    print(f"Pipeline steps: {' -> '.join(scripts)}")
    print("-" * 60)

    while True:
        cycle_start = time.time()

        for script in scripts:
            if not run_script(script):
                print(f"Pipeline stopped due to error in {script}")
                sys.exit(1)

        cycle_duration = time.time() - cycle_start
        print(f"\nCycle completed in {cycle_duration:.2f} seconds")
        print("Waiting 2 minutes before next cycle...\n")

        time.sleep(120)  # Wait for 2 minutes before starting the scripts again


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPipeline stopped by user.")
        sys.exit(0)
