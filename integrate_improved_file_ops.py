#!/usr/bin/env python3
"""
Integration script to add improved file operations to your existing JARVIS system
"""

# Import the improved modules
from improved_file_operations import file_ops
from improved_command_processor import command_processor

def integrate_with_existing_jarvis():
    """
    This function shows how to integrate the improved file operations
    with your existing app.py process_command function
    """
    
    # Add this to your existing process_command function in app.py
    # Replace the existing file operation handling with this:
    
    def enhanced_process_command(command, language='en'):
        """Enhanced command processing with improved file operations"""
        
        if not command or not command.strip():
            return "I didn't hear anything, sir. Could you please repeat that?"
        
        original_command = command.strip()
        command_lower = command.lower().strip()
        
        print(f"🎤 Processing: '{original_command}'")
        
        # Remove wake words if present
        wake_words = ['hey jarvis', 'jarvis', 'हे जार्विस', 'જાર્વિસ']
        for wake_word in wake_words:
            if command_lower.startswith(wake_word):
                command_lower = command_lower.replace(wake_word, '').strip()
                original_command = original_command[len(wake_word):].strip()
                break
        
        # If empty after wake word removal, greet
        if not command_lower:
            return "Hello! I'm JARVIS, your AI assistant. How may I help you today, sir?"
        
        # PRIORITY 1: File Operations (using improved system)
        file_result = command_processor.process_file_command(command_lower, original_command)
        if file_result:
            return file_result
        
        # PRIORITY 2: Photo capture with auto-open
        if any(phrase in command_lower for phrase in ['take photo', 'capture photo', 'take picture']):
            result = file_ops.take_photo_and_open()
            return result['message']
        
        # PRIORITY 3: AI-First approach for other commands
        # ... rest of your existing AI processing code ...
        
        return "I'm not sure how to help with that, sir. Could you please rephrase your request?"
    
    return enhanced_process_command

def test_improved_file_operations():
    """Test the improved file operations"""
    
    print("🧪 Testing Improved File Operations\n")
    
    # Test 1: Create a file
    print("1. Testing file creation...")
    result = file_ops.create_file("test_document.txt")
    print(f"   Result: {result['message']}")
    
    # Test 2: Find files
    print("\n2. Testing file search...")
    result = file_ops.find_files("test_document")
    if result['success']:
        print(f"   Found {result['count']} files")
        for match in result['matches'][:3]:
            print(f"   - {match['name']} at {match['path']}")
    
    # Test 3: Create a folder
    print("\n3. Testing folder creation...")
    result = file_ops.create_folder("TestFolder")
    print(f"   Result: {result['message']}")
    
    # Test 4: Test command processor
    print("\n4. Testing command processor...")
    test_commands = [
        "create file my_notes.txt",
        "find file test_document",
        "create folder MyProjects",
        "take photo"
    ]
    
    for cmd in test_commands:
        print(f"\n   Command: '{cmd}'")
        result = command_processor.process_file_command(cmd.lower(), cmd)
        if result:
            print(f"   Response: {result[:100]}...")
        else:
            print("   No response (not a file command)")

def show_usage_examples():
    """Show usage examples for the improved file operations"""
    
    print("📚 Usage Examples for Improved File Operations\n")
    
    examples = {
        "Create Files": [
            "create file report.txt",
            "create file presentation.html", 
            "create file script.py",
            "make file notes.md"
        ],
        "Create Folders": [
            "create folder MyDocuments",
            "make folder ProjectFiles",
            "new folder Photos2024"
        ],
        "Find Files": [
            "find file report.txt",
            "search file presentation",
            "locate file script.py",
            "look for file notes"
        ],
        "Open Files": [
            "open file report.txt",
            "open 1",  # from search results
            "launch file presentation.html"
        ],
        "Delete Files": [
            "delete file old_report.txt",
            "remove folder TempFiles",
            "delete file document.pdf permanently"
        ],
        "Rename Files": [
            "rename report.txt to final_report.txt",
            "rename folder OldName to NewName"
        ],
        "Take Photos": [
            "take photo",
            "capture picture",
            "take a photo"
        ]
    }
    
    for category, commands in examples.items():
        print(f"{category}:")
        for cmd in commands:
            print(f"  • {cmd}")
        print()

def main():
    """Main function to demonstrate the improved file operations"""
    
    print("🤖 JARVIS Improved File Operations System")
    print("=" * 50)
    
    # Show usage examples
    show_usage_examples()
    
    # Ask user if they want to run tests
    response = input("Would you like to run the test suite? (y/n): ").lower()
    if response in ['y', 'yes']:
        test_improved_file_operations()
    
    print("\n✅ Integration complete!")
    print("\nTo integrate with your existing JARVIS:")
    print("1. Import the modules: from improved_file_operations import file_ops")
    print("2. Import the processor: from improved_command_processor import command_processor")
    print("3. Add file command processing to your process_command function")
    print("4. Replace existing file operations with the improved versions")

if __name__ == "__main__":
    main()