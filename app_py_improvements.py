#!/usr/bin/env python3
"""
Specific improvements to add to your existing app.py file
These functions will replace or enhance your current file operations
"""

# Add these imports at the top of your app.py file
try:
    from improved_file_operations import file_ops
    from improved_command_processor import command_processor
    IMPROVED_FILE_OPS_AVAILABLE = True
    print("✅ Improved file operations loaded successfully!")
except ImportError:
    IMPROVED_FILE_OPS_AVAILABLE = False
    print("⚠️ Improved file operations not available - using fallback methods")

def enhanced_capture_photo():
    """Enhanced photo capture that automatically opens the photo"""
    if IMPROVED_FILE_OPS_AVAILABLE:
        result = file_ops.take_photo_and_open()
        return result['message']
    else:
        # Fallback to your existing capture_photo function
        return capture_photo()

def enhanced_file_search(search_term):
    """Enhanced file search with better results and user interaction"""
    if IMPROVED_FILE_OPS_AVAILABLE:
        result = file_ops.find_files(search_term)
        if result['success'] and result['matches']:
            response = f"I found {result['count']} file(s) matching '{search_term}', sir:\n\n"
            
            for i, match in enumerate(result['matches'][:10], 1):
                file_type = "📁" if match['type'] == 'folder' else "📄"
                size_info = ""
                if match['type'] == 'file' and match['size'] > 0:
                    size_mb = match['size'] / (1024 * 1024)
                    if size_mb < 1:
                        size_info = f" ({match['size']} bytes)"
                    else:
                        size_info = f" ({size_mb:.1f} MB)"
                
                response += f"{i}. {file_type} {match['name']}{size_info}\n   📍 {match['path']}\n\n"
            
            response += "Would you like me to open any of these files, sir? Just say 'open 1' or 'open file 2'."
            return response
        else:
            return f"Sorry sir, I couldn't find any files matching '{search_term}'."
    else:
        # Fallback to your existing search
        return handle_file_search_command(search_term.lower(), search_term)

def enhanced_create_file(filename, location='desktop'):
    """Enhanced file creation with better error handling"""
    if IMPROVED_FILE_OPS_AVAILABLE:
        result = file_ops.create_file(filename, location)
        if result['success']:
            return f"{result['message']}\n\nWould you like me to open '{result['name']}' now, sir?"
        else:
            return result['message']
    else:
        # Fallback to your existing create file function
        return handle_create_file_command(f"create file {filename}", f"create file {filename}")

def enhanced_process_command(command, language='en'):
    """
    Enhanced version of your process_command function
    Add this logic to your existing process_command function
    """
    
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
    
    # ENHANCED FILE OPERATIONS - HIGHEST PRIORITY
    if IMPROVED_FILE_OPS_AVAILABLE:
        file_result = command_processor.process_file_command(command_lower, original_command)
        if file_result:
            return file_result
    
    # ENHANCED PHOTO CAPTURE
    if any(phrase in command_lower for phrase in ['take photo', 'capture photo', 'take picture']):
        return enhanced_capture_photo()
    
    # Continue with your existing AI processing and other commands...
    # ... rest of your existing process_command logic ...

# Add these route handlers to your Flask app

@app.route('/api/file/create', methods=['POST'])
def api_create_file():
    """API endpoint for creating files"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        location = data.get('location', 'desktop')
        
        if not filename:
            return jsonify({'success': False, 'message': 'Filename is required'})
        
        if IMPROVED_FILE_OPS_AVAILABLE:
            result = file_ops.create_file(filename, location)
            return jsonify(result)
        else:
            # Fallback
            return jsonify({'success': False, 'message': 'File operations not available'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/file/search', methods=['POST'])
def api_search_files():
    """API endpoint for searching files"""
    try:
        data = request.get_json()
        search_term = data.get('search_term')
        max_results = data.get('max_results', 20)
        
        if not search_term:
            return jsonify({'success': False, 'message': 'Search term is required'})
        
        if IMPROVED_FILE_OPS_AVAILABLE:
            result = file_ops.find_files(search_term, max_results)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'message': 'File search not available'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/file/open', methods=['POST'])
def api_open_file():
    """API endpoint for opening files"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        file_number = data.get('file_number')
        
        if not file_path and not file_number:
            return jsonify({'success': False, 'message': 'File path or number is required'})
        
        if IMPROVED_FILE_OPS_AVAILABLE:
            target = file_number if file_number else file_path
            result = file_ops.open_file(target)
            return jsonify(result)
        else:
            return jsonify({'success': False, 'message': 'File operations not available'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/photo/capture', methods=['POST'])
def api_capture_photo():
    """API endpoint for capturing photos"""
    try:
        if IMPROVED_FILE_OPS_AVAILABLE:
            result = file_ops.take_photo_and_open()
            return jsonify(result)
        else:
            # Fallback to existing photo capture
            result = capture_photo()
            return jsonify({'success': True, 'message': result})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# JavaScript code to add to your jarvis.js file
javascript_additions = """
// Add these functions to your jarvis.js file

// Enhanced file operations
function createFile(filename, location = 'desktop') {
    fetch('/api/file/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            filename: filename,
            location: location
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayMessage(data.message);
            // Ask if user wants to open the file
            if (confirm('Would you like to open the created file?')) {
                openFile(data.path);
            }
        } else {
            displayMessage('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('Error creating file: ' + error.message);
    });
}

function searchFiles(searchTerm) {
    fetch('/api/file/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_term: searchTerm,
            max_results: 20
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.matches.length > 0) {
            let message = `Found ${data.count} file(s) matching '${searchTerm}':\\n\\n`;
            data.matches.slice(0, 10).forEach((match, index) => {
                const fileType = match.type === 'folder' ? '📁' : '📄';
                const sizeInfo = match.type === 'file' && match.size > 0 ? 
                    ` (${(match.size / (1024 * 1024)).toFixed(1)} MB)` : '';
                message += `${index + 1}. ${fileType} ${match.name}${sizeInfo}\\n   📍 ${match.path}\\n\\n`;
            });
            message += 'Click on a file to open it, or say "open 1" to open the first file.';
            displayMessage(message);
            
            // Store search results for opening
            window.lastSearchResults = data.matches;
        } else {
            displayMessage(`Sorry, I couldn't find any files matching '${searchTerm}'.`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('Error searching files: ' + error.message);
    });
}

function openFile(filePathOrNumber) {
    fetch('/api/file/open', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            file_path: typeof filePathOrNumber === 'string' ? filePathOrNumber : null,
            file_number: typeof filePathOrNumber === 'number' ? filePathOrNumber : null
        })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('Error opening file: ' + error.message);
    });
}

function capturePhoto() {
    fetch('/api/photo/capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('Error capturing photo: ' + error.message);
    });
}

// Enhanced command processing
function processEnhancedCommand(command) {
    const commandLower = command.toLowerCase();
    
    // File creation commands
    if (commandLower.includes('create file') || commandLower.includes('make file')) {
        const filename = extractFilename(command, ['create file', 'make file']);
        if (filename) {
            createFile(filename);
            return true;
        }
    }
    
    // File search commands
    if (commandLower.includes('find file') || commandLower.includes('search file')) {
        const searchTerm = extractSearchTerm(command, ['find file', 'search file']);
        if (searchTerm) {
            searchFiles(searchTerm);
            return true;
        }
    }
    
    // File open commands
    if (commandLower.includes('open file') || commandLower.match(/open \\d+/)) {
        const numberMatch = command.match(/open (\\d+)/);
        if (numberMatch) {
            openFile(parseInt(numberMatch[1]));
            return true;
        } else {
            const filename = extractFilename(command, ['open file', 'open']);
            if (filename) {
                // First search, then open
                searchFiles(filename);
                return true;
            }
        }
    }
    
    // Photo capture commands
    if (commandLower.includes('take photo') || commandLower.includes('capture photo')) {
        capturePhoto();
        return true;
    }
    
    return false; // Command not handled
}

function extractFilename(command, prefixes) {
    let filename = command.toLowerCase();
    for (const prefix of prefixes) {
        filename = filename.replace(prefix, '').trim();
    }
    return filename || null;
}

function extractSearchTerm(command, prefixes) {
    let searchTerm = command.toLowerCase();
    for (const prefix of prefixes) {
        searchTerm = searchTerm.replace(prefix, '').trim();
    }
    return searchTerm || null;
}
"""

def show_integration_instructions():
    """Show step-by-step integration instructions"""
    
    print("🔧 Integration Instructions for JARVIS File Operations")
    print("=" * 60)
    
    instructions = [
        {
            "step": 1,
            "title": "Install Required Dependencies",
            "details": [
                "pip install opencv-python  # For photo capture",
                "pip install send2trash     # For safe file deletion",
                "pip install pathlib        # For better path handling"
            ]
        },
        {
            "step": 2,
            "title": "Add Import Statements to app.py",
            "details": [
                "Add these imports at the top of your app.py file:",
                "from improved_file_operations import file_ops",
                "from improved_command_processor import command_processor"
            ]
        },
        {
            "step": 3,
            "title": "Replace File Operation Functions",
            "details": [
                "Replace your existing file functions with enhanced versions:",
                "- Replace capture_photo() with enhanced_capture_photo()",
                "- Replace file search logic with enhanced_file_search()",
                "- Replace file creation with enhanced_create_file()"
            ]
        },
        {
            "step": 4,
            "title": "Update process_command Function",
            "details": [
                "Add file command processing at the beginning:",
                "file_result = command_processor.process_file_command(command_lower, original_command)",
                "if file_result:",
                "    return file_result"
            ]
        },
        {
            "step": 5,
            "title": "Add New API Endpoints",
            "details": [
                "Add the new Flask routes for file operations:",
                "- /api/file/create",
                "- /api/file/search", 
                "- /api/file/open",
                "- /api/photo/capture"
            ]
        },
        {
            "step": 6,
            "title": "Update Frontend JavaScript",
            "details": [
                "Add the JavaScript functions to jarvis.js:",
                "- createFile()",
                "- searchFiles()",
                "- openFile()",
                "- capturePhoto()"
            ]
        }
    ]
    
    for instruction in instructions:
        print(f"\nStep {instruction['step']}: {instruction['title']}")
        print("-" * 40)
        for detail in instruction['details']:
            print(f"  • {detail}")
    
    print(f"\n✅ After integration, your JARVIS will support:")
    print("  • Enhanced file creation with auto-open option")
    print("  • Improved file search across all drives")
    print("  • Better error handling and user feedback")
    print("  • Automatic photo opening after capture")
    print("  • Interactive confirmations for destructive operations")
    print("  • Cross-platform compatibility")

if __name__ == "__main__":
    show_integration_instructions()