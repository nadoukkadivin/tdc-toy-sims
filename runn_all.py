import subprocess
import sys
import os
from pathlib import Path

def run_script(script_path, args="", timeout=60, capture_output=False, use_agg_backend=False):
    """
    Run a script with optional timeout, output capture, and Matplotlib backend override.
    
    Args:
        script_path: Relative/absolute path to .py file (e.g., 'core/residues_demo.py').
        args: Command-line args (str, space-separated).
        timeout: Seconds before killing (None = no timeout).
        capture_output: If True, capture and print stdout/stderr.
        use_agg_backend: If True, set MPLBACKEND=Agg for non-interactive plots.
    
    Returns:
        Tuple: (success: bool, output: str or None).
    """
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False, None
    
    print(f"\n=== Running {script_path} {args} ===")
    
    # Optional: Override Matplotlib backend for headless/non-blocking runs
    env = os.environ.copy()
    if use_agg_backend:
        env['MPLBACKEND'] = 'Agg'  # Saves plots without GUI; set via env var or flag
    
    cmd = [sys.executable, script_path] + args.split()  # Safe, no shell=True
    try:
        result = subprocess.run(
            cmd, 
            timeout=timeout, 
            capture_output=capture_output,
            text=True,
            env=env
        )
        if result.returncode != 0:
            print(f"❌ Error running {script_path} (code: {result.returncode})")
            if capture_output:
                print(f"Stdout: {result.stdout.strip()}")
                print(f"Stderr: {result.stderr.strip()}")
            return False, result.stdout + result.stderr if capture_output else None
        print(f"✅ {script_path} completed successfully")
        if capture_output and result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True, result.stdout if capture_output else None
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout for {script_path} (increase via timeout arg)")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def main():
    # Customize: List of scripts (supports subdirs; add paths as needed)
    scripts = [
        "residues_demo.py",  # Core TDC residues/multi-domain sim
        "universality_demo.py",  # Dr collapse plot/validation
        # e.g., "eg1/tdc_eg1_toysim.py",  # Bioelectronic hybrid
        # "eg2/tdc_eg2_toysim.py",  # Gut-brain chain
    ]
    
    successful = 0
    total = len(scripts)
    agg_mode = os.getenv('USE_AGG_BACKEND', 'false').lower() == 'true'  # Env var: USE_AGG_BACKEND=true python run_all.py
    
    for script in scripts:
        success, output = run_script(
            script, 
            args="", 
            timeout=60, 
            capture_output=True,  # Capture for validation scripts like residues_demo
            use_agg_backend=agg_mode
        )
        if success:
            successful += 1
    
    print(f"\n=== Summary ===")
    print(f"✅ {successful}/{total} scripts ran successfully")
    if successful < total:
        print("❌ Check errors above—e.g., missing deps or paths.")
    if agg_mode:
        print("📊 Plots saved to files (non-interactive mode).")
    else:
        print("🖼️ Plots displayed via GUI (close windows to continue).")

if __name__ == "__main__":
    main()
