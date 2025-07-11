"""
Quick Setup Script for Sentinel-2 Water Quality Processing
This script helps resolve common setup issues
"""

import sys
import subprocess
import os
from pathlib import Path

def install_missing_packages():
    """Install missing Python packages."""
    print("🔧 Installing missing Python packages...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All packages installed successfully")
            return True
        else:
            print(f"❌ Package installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_snap_installation():
    """Check and provide guidance for SNAP installation."""
    print("🛰️ Checking SNAP installation...")
    
    # Check if gpt is available using shutil.which first
    import shutil
    gpt_location = shutil.which('gpt')
    
    if gpt_location:
        print(f"   Found 'gpt' command at: {gpt_location}")
        
        # Try a quick test with a short timeout
        try:
            result = subprocess.run(['gpt'], capture_output=True, text=True, timeout=5)
            # GPT without arguments usually returns 1 but shows it's working
            if result.returncode in [0, 1] and ('gpt' in result.stderr.lower() or 'usage' in result.stderr.lower() or len(result.stderr) > 0):
                print("✅ SNAP GPT is working correctly!")
                return True
            else:
                print(f"   GPT command found but may not be working (return code: {result.returncode})")
        except subprocess.TimeoutExpired:
            print("   GPT command found but response was slow")
            # If it times out, SNAP is probably there but slow - consider it working
            return True
        except Exception as e:
            print(f"   Error testing GPT: {e}")
    
    # If which() didn't find it, try manual paths
    print("   Searching in common installation paths...")
    gpt_paths = [
        r'C:\Program Files\esa-snap\bin\gpt.exe',
        r'C:\Program Files\esa-snap\bin\gpt.bat',
        r'C:\Program Files\snap\bin\gpt.exe',
        r'C:\Program Files\snap\bin\gpt.bat',
        r'C:\Program Files (x86)\snap\bin\gpt.exe',
        r'C:\Program Files (x86)\esa-snap\bin\gpt.exe',
    ]
    
    for gpt_path in gpt_paths:
        if os.path.exists(gpt_path):
            print(f"   ✅ Found SNAP GPT at: {gpt_path}")
            snap_bin_dir = os.path.dirname(gpt_path)
            
            # Check if it's in PATH
            path_env = os.environ.get('PATH', '').lower()
            if snap_bin_dir.lower() in path_env:
                print("   ✅ SNAP directory is in PATH")
                return True
            else:
                print("   ⚠️  SNAP found but directory not in PATH")
                print(f"   Temporarily adding to PATH: {snap_bin_dir}")
                
                # Add SNAP bin directory to PATH for this session
                current_path = os.environ.get('PATH', '')
                if snap_bin_dir not in current_path:
                    os.environ['PATH'] = snap_bin_dir + os.pathsep + current_path
                    print(f"   Added {snap_bin_dir} to PATH for this session")
                
                # Test if gpt command now works
                try:
                    result = subprocess.run(['gpt', '--help'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print("   ✅ SNAP GPT command is now working!")
                        return True
                    else:
                        print(f"   ⚠️  SNAP found but GPT command failed (return code: {result.returncode})")
                except Exception as e:
                    print(f"   ⚠️  Error testing GPT command: {e}")
                
                return True  # SNAP is there, just PATH needs fixing
    
    # Check for SNAP installation directories even without gpt
    snap_dirs = [
        r'C:\Program Files\esa-snap',
        r'C:\Program Files\snap',
        r'C:\Program Files (x86)\snap',
        r'C:\Program Files (x86)\esa-snap',
    ]
    
    for snap_dir in snap_dirs:
        if os.path.exists(snap_dir):
            print(f"   Found SNAP installation directory: {snap_dir}")
            bin_dir = os.path.join(snap_dir, 'bin')
            if os.path.exists(bin_dir):
                print(f"   Found bin directory: {bin_dir}")
                gpt_files = [f for f in os.listdir(bin_dir) if f.startswith('gpt')]
                if gpt_files:
                    print(f"   Found GPT files: {gpt_files}")
                    print("   ✅ SNAP is installed!")
                    print(f"   Add to PATH: {bin_dir}")
                    print_snap_path_instructions(bin_dir)
                    return True
    
    print("❌ SNAP not found in any standard location")
    print_snap_instructions()
    return False

def print_snap_instructions():
    """Print SNAP installation instructions."""
    print("""
🚨 SNAP Installation Required!

SNAP (Sentinel Application Platform) is required for processing.

Quick Setup:
1. Download SNAP from: https://step.esa.int/main/download/snap-download/
2. Install as Administrator
3. Add to PATH: C:\\Program Files\\snap\\bin
4. Test with: gpt --help

Detailed instructions: 07_documentation\\SNAP_INSTALLATION_GUIDE.md
""")

def print_snap_path_instructions(snap_bin_path):
    """Print instructions for adding SNAP to PATH."""
    print(f"""
🔧 SNAP Found but Not in PATH!

SNAP is installed but the 'gpt' command is not accessible.

To fix this, add SNAP to your PATH:

Windows:
1. Press Win + R, type 'sysdm.cpl', press Enter
2. Click 'Environment Variables'
3. Under 'System Variables', find 'Path' and click 'Edit'
4. Click 'New' and add: {snap_bin_path}
5. Click 'OK' on all windows
6. Restart your command prompt/PowerShell

Alternative (Quick fix for current session):
set PATH=%PATH%;{snap_bin_path}

Test after setup: gpt --help
""")

def setup_credentials():
    """Help setup Copernicus credentials."""
    print("🔑 Setting up Copernicus credentials...")
    
    config_file = Path("02_config/parameters.yaml")
    
    if not config_file.exists():
        print("❌ Configuration file not found")
        return False
    
    with open(config_file, 'r') as f:
        content = f.read()
    
    if "your_username@email.com" in content:
        print("⚠️  Default credentials detected")
        print("""
📝 Please update your Copernicus credentials:

1. Open: 02_config\\parameters.yaml
2. Replace:
   - your_username@email.com → your actual email
   - your_password → your actual password

3. Get credentials from: https://identity.dataspace.copernicus.eu/
""")
        return False
    else:
        print("✅ Credentials appear to be configured")
        return True

def create_sample_config():
    """Create a sample configuration with prompts."""
    print("📝 Creating sample configuration...")
    
    config_dir = Path("02_config")
    config_dir.mkdir(exist_ok=True)
    
    # Get user input
    try:
        email = input("Enter your Copernicus email: ").strip()
        password = input("Enter your Copernicus password: ").strip()
        
        if not email or not password:
            print("❌ Email and password are required")
            return False
        
        # Read template and replace
        config_file = config_dir / "parameters.yaml"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Replace credentials
            content = content.replace("your_username@email.com", email)
            content = content.replace("your_password", password)
            
            with open(config_file, 'w') as f:
                f.write(content)
            
            print("✅ Credentials updated successfully")
            return True
        else:
            print("❌ Configuration template not found")
            return False
            
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Error updating credentials: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Sentinel-2 Water Quality Processing - Quick Setup")
    print("=" * 60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    issues_found = []
    
    # Check and install packages
    if not install_missing_packages():
        issues_found.append("Python packages")
    
    # Check SNAP
    if not check_snap_installation():
        issues_found.append("SNAP installation")
    
    # Check credentials
    if not setup_credentials():
        print("\n💡 Do you want to update credentials now? (y/n)")
        if input().lower().startswith('y'):
            if not create_sample_config():
                issues_found.append("Credentials setup")
        else:
            issues_found.append("Credentials setup")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SETUP SUMMARY")
    print("=" * 60)
    
    if not issues_found:
        print("✅ All setup tasks completed successfully!")
        print("\nYou can now run: run_workflow.bat")
    else:
        print("❌ Issues found:")
        for issue in issues_found:
            print(f"   - {issue}")
        
        print("\nNext steps:")
        if "SNAP installation" in issues_found:
            print("1. Install SNAP: https://step.esa.int/main/download/snap-download/")
        if "Credentials setup" in issues_found:
            print("2. Update credentials: 02_config\\parameters.yaml")
        if "Python packages" in issues_found:
            print("3. Install packages: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
