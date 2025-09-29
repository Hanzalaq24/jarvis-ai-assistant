#!/usr/bin/env python3
"""
File System Diagnostic Tool for JARVIS
This script will help identify file system management issues
"""

import os
import sys
import platform
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking File System Dependencies...")
    
    dependencies = {
        'send2trash': 'File deletion to trash',
        'watchdog': 'File system monitoring',
        'pathlib': 'Path operations (built-in)',
        'os': 'OS operations (built-in)',
        'shutil': 'File operations (built-in)'
    }
    
    missing_deps = []
    
    for dep, description in dependencies.items():
        try:
            if dep in ['pathlib', 'os', 'shutil']:
                # Built-in modules
                __import__(dep)
                print(f"✅ {dep}: {description}")
            else:
                __import__(dep)
                print(f"✅ {dep}: {description}")
        except ImportError:
            print(f"❌ {dep}: {description} - NOT INSTALLED")
            missing_deps.append(dep)
    
    return missing_deps

def check_permissions():
    """Check file system permissions"""
    print("\n🔐 Checking File System Permissions...")
    
    # Test locations
    test_locations = [
        Path.home() / 'Desktop',
        Path.home() / 'Documents',
        Path.home() / 'Downloads',
        Path.home(),
        Path.cwd()  # Current directory
    ]
    
    permissions = {}
    
    for location in test_locations:
        if location.exists():
            # Test read permission
            try:
                list(location.iterdir())
                read_perm = True
            except PermissionError:
                read_perm = False
            
            # Test write permission
            try:
                test_file = location / 'jarvis_test_file.tmp'
                test_file.write_text('test')
                test_file.unlink()  # Delete test file
                write_perm = True
            except (PermissionError, OSError):
                write_perm = False
            
            permissions[str(location)] = {
                'read': read_perm,
                'write': write_perm
            }
            
            status = "✅" if read_perm and write_perm else "⚠️" if read_perm else "❌"
            print(f"{status} {location}: Read={read_perm}, Write={write_perm}")
        else:
            print(f"❌ {location}: Does not exist")
    
    return permissions

def check_system_info():
    """Check system information"""
    print("\n💻 System Information...")
    
    system_info = {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'Python Version': sys.version,
        'Current Directory': os.getcwd(),
        'Home Directory': str(Path.home()),
        'Desktop Exists': (Path.home() / 'Desktop').exists()
    }
    
    for key, value in system_info.items():
        print(f"📋 {key}: {value}")
    
    return system_info

def test_file_operations():
    """Test basic file operations"""
    print("\n🧪 Testing File Operations...")
    
    test_dir = Path.cwd() / 'jarvis_test'
    test_results = {}
    
    try:
        # Test 1: Create directory
        test_dir.mkdir(exist_ok=True)
        test_results['create_dir'] = True
        print("✅ Directory creation: SUCCESS")
    except Exception as e:
        test_results['create_dir'] = False
        print(f"❌ Directory creation: FAILED - {e}")
    
    try:
        # Test 2: Create file
        test_file = test_dir / 'test.txt'
        test_file.write_text('JARVIS file system test')
        test_results['create_file'] = True
        print("✅ File creation: SUCCESS")
    except Exception as e:
        test_results['create_file'] = False
        print(f"❌ File creation: FAILED - {e}")
    
    try:
        # Test 3: Read file
        if test_file.exists():
            content = test_file.read_text()
            test_results['read_file'] = True
            print("✅ File reading: SUCCESS")
        else:
            test_results['read_file'] = False
            print("❌ File reading: FAILED - File doesn't exist")
    except Exception as e:
        test_results['read_file'] = False
        print(f"❌ File reading: FAILED - {e}")
    
    try:
        # Test 4: Delete file
        if test_file.exists():
            test_file.unlink()
            test_results['delete_file'] = True
            print("✅ File deletion: SUCCESS")
        else:
            test_results['delete_file'] = False
            print("❌ File deletion: FAILED - File doesn't exist")
    except Exception as e:
        test_results['delete_file'] = False
        print(f"❌ File deletion: FAILED - {e}")
    
    try:
        # Test 5: Delete directory
        if test_dir.exists():
            test_dir.rmdir()
            test_results['delete_dir'] = True
            print("✅ Directory deletion: SUCCESS")
        else:
            test_results['delete_dir'] = False
            print("❌ Directory deletion: FAILED - Directory doesn't exist")
    except Exception as e:
        test_results['delete_dir'] = False
        print(f"❌ Directory deletion: FAILED - {e}")
    
    return test_results

def main():
    """Run complete file system diagnostic"""
    print("🤖 JARVIS File System Diagnostic Tool")
    print("=" * 50)
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    # Check permissions
    permissions = check_permissions()
    
    # Check system info
    system_info = check_system_info()
    
    # Test file operations
    test_results = test_file_operations()
    
    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 30)
    
    if missing_deps:
        print(f"❌ Missing Dependencies: {', '.join(missing_deps)}")
        print("   Install with: pip install " + " ".join(missing_deps))
    else:
        print("✅ All dependencies installed")
    
    # Check if any location has write permissions
    has_write_access = any(perm['write'] for perm in permissions.values())
    if has_write_access:
        print("✅ File system write access available")
    else:
        print("❌ No write access to common locations")
    
    # Check test results
    all_tests_passed = all(test_results.values())
    if all_tests_passed:
        print("✅ All file operation tests passed")
    else:
        failed_tests = [test for test, result in test_results.items() if not result]
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
    
    print("\n🔧 RECOMMENDATIONS:")
    
    if missing_deps:
        print("1. Install missing dependencies:")
        print(f"   pip install {' '.join(missing_deps)}")
    
    if not has_write_access:
        print("2. Check file permissions - you may need to:")
        print("   - Run as administrator/sudo")
        print("   - Check folder permissions")
        print("   - Try a different location")
    
    if not all_tests_passed:
        print("3. File operations failed - check:")
        print("   - Disk space")
        print("   - Antivirus software blocking")
        print("   - File system corruption")
    
    print("\n✨ If all tests pass, your file system should work with JARVIS!")

if __name__ == "__main__":
    main()