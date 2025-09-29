#!/usr/bin/env python3
"""
Test script for the improved file operations
Run this to verify everything is working correctly
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from improved_file_operations import file_ops
        print("  ✅ improved_file_operations imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import improved_file_operations: {e}")
        return False
    
    try:
        from improved_command_processor import command_processor
        print("  ✅ improved_command_processor imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import improved_command_processor: {e}")
        return False
    
    return True

def test_file_creation():
    """Test file creation functionality"""
    print("\n🧪 Testing file creation...")
    
    from improved_file_operations import file_ops
    
    # Test creating a text file
    result = file_ops.create_file("test_jarvis_file.txt", "desktop")
    print(f"  Create text file: {result['message']}")
    
    # Test creating a Python file
    result = file_ops.create_file("test_script.py", "desktop")
    print(f"  Create Python file: {result['message']}")
    
    # Test creating a JSON file
    result = file_ops.create_file("test_data.json", "desktop")
    print(f"  Create JSON file: {result['message']}")

def test_file_search():
    """Test file search functionality"""
    print("\n🧪 Testing file search...")
    
    from improved_file_operations import file_ops
    
    # Search for the files we just created
    result = file_ops.find_files("test_jarvis")
    if result['success']:
        print(f"  ✅ Found {result['count']} files matching 'test_jarvis'")
        for match in result['matches'][:3]:
            print(f"    - {match['name']} at {match['path']}")
    else:
        print(f"  ❌ Search failed: {result.get('message', 'Unknown error')}")

def test_folder_creation():
    """Test folder creation functionality"""
    print("\n🧪 Testing folder creation...")
    
    from improved_file_operations import file_ops
    
    result = file_ops.create_folder("JARVIS_Test_Folder", "desktop")
    print(f"  Create folder: {result['message']}")

def test_command_processing():
    """Test command processing functionality"""
    print("\n🧪 Testing command processing...")
    
    from improved_command_processor import command_processor
    
    test_commands = [
        "create file my_test_document.txt",
        "find file test_jarvis",
        "create folder MyTestFolder",
        "delete file nonexistent.txt",
        "rename old_file.txt to new_file.txt"
    ]
    
    for cmd in test_commands:
        print(f"\n  Testing: '{cmd}'")
        result = command_processor.process_file_command(cmd.lower(), cmd)
        if result:
            print(f"    Response: {result[:100]}{'...' if len(result) > 100 else ''}")
        else:
            print("    No response (command not recognized)")

def test_photo_capture():
    """Test photo capture functionality (if camera available)"""
    print("\n🧪 Testing photo capture...")
    
    try:
        import cv2
        print("  OpenCV available - testing camera access...")
        
        # Try to access camera
        cam = cv2.VideoCapture(0)
        if cam.isOpened():
            ret, frame = cam.read()
            cam.release()
            if ret:
                print("  ✅ Camera is accessible and working")
                
                # Test the photo capture function
                from improved_file_operations import file_ops
                print("  Note: Photo capture test skipped to avoid taking actual photos")
                print("  To test photo capture, run: file_ops.take_photo_and_open()")
            else:
                print("  ⚠️ Camera accessible but failed to capture frame")
        else:
            print("  ⚠️ Camera not accessible")
    except ImportError:
        print("  ⚠️ OpenCV not available - photo capture will not work")
        print("  Install with: pip install opencv-python")

def cleanup_test_files():
    """Clean up test files created during testing"""
    print("\n🧹 Cleaning up test files...")
    
    desktop_path = Path.home() / 'Desktop'
    test_files = [
        "test_jarvis_file.txt",
        "test_script.py", 
        "test_data.json"
    ]
    
    test_folders = [
        "JARVIS_Test_Folder",
        "MyTestFolder"
    ]
    
    cleaned_count = 0
    
    # Remove test files
    for filename in test_files:
        file_path = desktop_path / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  ✅ Removed {filename}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {filename}: {e}")
    
    # Remove test folders
    for foldername in test_folders:
        folder_path = desktop_path / foldername
        if folder_path.exists():
            try:
                folder_path.rmdir()
                print(f"  ✅ Removed {foldername}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {foldername}: {e}")
    
    if cleaned_count == 0:
        print("  No test files found to clean up")

def run_all_tests():
    """Run all tests"""
    print("🤖 JARVIS Improved File Operations - Test Suite")
    print("=" * 55)
    
    # Test imports first
    if not test_imports():
        print("\n❌ Import tests failed. Cannot continue.")
        return False
    
    # Run functionality tests
    test_file_creation()
    test_file_search()
    test_folder_creation()
    test_command_processing()
    test_photo_capture()
    
    # Ask if user wants to clean up
    print("\n" + "=" * 55)
    response = input("Would you like to clean up test files? (y/n): ").lower()
    if response in ['y', 'yes']:
        cleanup_test_files()
    
    print("\n✅ Test suite completed!")
    print("\nIf all tests passed, your improved file operations are ready to use.")
    print("You can now integrate them into your JARVIS system using the instructions in app_py_improvements.py")
    
    return True

def show_usage_examples():
    """Show practical usage examples"""
    print("\n📚 Usage Examples:")
    print("-" * 20)
    
    examples = [
        ("Create a text file", "create file my_notes.txt"),
        ("Create a Python script", "create file my_script.py"),
        ("Create a folder", "create folder MyProject"),
        ("Find files", "find file notes"),
        ("Open a file", "open file my_notes.txt"),
        ("Open from search results", "open 1"),
        ("Delete a file", "delete file old_notes.txt"),
        ("Rename a file", "rename notes.txt to important_notes.txt"),
        ("Take a photo", "take photo")
    ]
    
    for description, command in examples:
        print(f"  {description:.<25} '{command}'")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--examples':
        show_usage_examples()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cleanup':
        cleanup_test_files()
        return
    
    success = run_all_tests()
    
    if success:
        show_usage_examples()

if __name__ == "__main__":
    main()