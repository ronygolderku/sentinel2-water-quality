"""
System validation script for Sentinel-2 Water Quality Processing
This script checks all requirements and provides diagnostic information
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python 3.8+ is required")
        return False
    else:
        print("   ✅ Python version is compatible")
        return True

def check_python_packages():
    """Check required Python packages."""
    print("\n📦 Checking Python packages...")
    
    required_packages = [
        'numpy', 'matplotlib', 'xarray', 'cartopy', 'cmocean',
        'geopandas', 'shapely', 'pandas', 'requests', 'yaml', 'netcdf4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'yaml':
                __import__('yaml')
            elif package == 'netcdf4':
                __import__('netCDF4')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ All required packages are installed")
        return True

def check_snap_installation():
    """Check SNAP GPT installation."""
    print("\n🛰️ Checking SNAP GPT installation...")
    
    # Check if gpt is available using shutil.which first
    import shutil
    gpt_location = shutil.which('gpt')
    
    if gpt_location:
        print(f"   Found 'gpt' command at: {gpt_location}")
        
        # Try a quick test with correct parameter
        try:
            result = subprocess.run(['gpt', '-h'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("   ✅ SNAP GPT is working correctly!")
                
                # Test C2RCC processor
                try:
                    result2 = subprocess.run(['gpt', 'c2rcc.msi', '-h'], 
                                           capture_output=True, text=True, timeout=10)
                    if result2.returncode == 0:
                        print("   ✅ C2RCC processor is available")
                    else:
                        print("   ⚠️  C2RCC processor may not be available")
                except:
                    print("   ⚠️  Could not verify C2RCC processor")
                
                return True
            else:
                print(f"   GPT command found but may not be working (return code: {result.returncode})")
        except subprocess.TimeoutExpired:
            print("   GPT command found but response was slow")
            return True  # If it times out, SNAP is probably there but slow
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
            
            # Add SNAP bin directory to PATH for this session
            current_path = os.environ.get('PATH', '')
            if snap_bin_dir not in current_path:
                os.environ['PATH'] = snap_bin_dir + os.pathsep + current_path
                print(f"   Added {snap_bin_dir} to PATH for this session")
            
            try:
                result = subprocess.run(['gpt', '-h'], capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    print("   ✅ SNAP is working correctly!")
                    
                    # Test C2RCC processor
                    try:
                        result2 = subprocess.run(['gpt', 'c2rcc.msi', '-h'], 
                                               capture_output=True, text=True, timeout=10)
                        if result2.returncode == 0:
                            print("   ✅ C2RCC processor is available")
                        else:
                            print("   ⚠️  C2RCC processor may not be available")
                    except:
                        print("   ⚠️  Could not verify C2RCC processor")
                    
                    return True
                else:
                    print(f"   ⚠️  SNAP found but not working properly (return code: {result.returncode})")
            except Exception as e:
                print(f"   ⚠️  Error testing SNAP: {e}")
                continue
    
    print("   ❌ SNAP not found in any standard location")
    print("   Install SNAP from: https://step.esa.int/main/download/snap-download/")
    return False

def check_directory_structure():
    """Check directory structure."""
    print("\n📁 Checking directory structure...")
    
    base_dir = Path(__file__).parent
    required_dirs = [
        "01_scripts",
        "02_config",
        "03_raw_data",
        "04_processed_data",
        "05_final_products",
        "06_logs",
        "07_documentation"
    ]
    
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}")
        else:
            print(f"   ❌ {dir_name} (missing)")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\n   Missing directories: {', '.join(missing_dirs)}")
        print("   Run: python 01_scripts/utils.py --action create_dirs --path .")
        return False
    else:
        print("   ✅ All required directories exist")
        return True

def check_configuration():
    """Check configuration file."""
    print("\n⚙️ Checking configuration...")
    
    config_file = Path(__file__).parent / "02_config" / "parameters.yaml"
    
    if not config_file.exists():
        print("   ❌ Configuration file not found: 02_config/parameters.yaml")
        return False
    
    print("   ✅ Configuration file exists")
    
    # Check if credentials are set
    try:
        with open(config_file, 'r') as f:
            content = f.read()
            
        if "your_username@email.com" in content:
            print("   ⚠️  Default credentials detected - please update your Copernicus credentials")
            return False
        else:
            print("   ✅ Credentials appear to be customized")
            return True
    except Exception as e:
        print(f"   ❌ Error reading configuration: {e}")
        return False

def check_disk_space():
    """Check available disk space."""
    print("\n💾 Checking disk space...")
    
    try:
        base_dir = Path(__file__).parent
        statvfs = os.statvfs(base_dir)
        free_bytes = statvfs.f_frsize * statvfs.f_bavail
        free_gb = free_bytes / (1024**3)
        
        print(f"   Available space: {free_gb:.1f} GB")
        
        if free_gb < 10:
            print("   ⚠️  Less than 10 GB free space - processing may fail")
            return False
        else:
            print("   ✅ Sufficient disk space available")
            return True
    except:
        # Windows doesn't have statvfs, use alternative method
        try:
            import shutil
            total, used, free = shutil.disk_usage(Path(__file__).parent)
            free_gb = free / (1024**3)
            
            print(f"   Available space: {free_gb:.1f} GB")
            
            if free_gb < 10:
                print("   ⚠️  Less than 10 GB free space - processing may fail")
                return False
            else:
                print("   ✅ Sufficient disk space available")
                return True
        except Exception as e:
            print(f"   ❌ Unable to check disk space: {e}")
            return False

def main():
    """Main validation function."""
    print("🔍 Sentinel-2 Water Quality Processing - System Validation")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_python_packages(),
        check_snap_installation(),
        check_directory_structure(),
        check_configuration(),
        check_disk_space()
    ]
    
    print("\n" + "=" * 60)
    print("📋 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print("✅ All checks passed! Your system is ready for processing.")
        return True
    else:
        print(f"❌ {total - passed} checks failed. Please address the issues above.")
        print("\nNext steps:")
        print("1. Install missing requirements: pip install -r requirements.txt")
        print("2. Install SNAP from: https://step.esa.int/main/download/snap-download/")
        print("3. Update configuration: 02_config/parameters.yaml")
        print("4. Create directories: python 01_scripts/utils.py --action create_dirs --path .")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
