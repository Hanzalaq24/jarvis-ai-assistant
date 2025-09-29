#!/usr/bin/env python3
"""
Improved File Operations for JARVIS AI Assistant
Handles create, rename, delete, find, and open file operations with better error handling
"""

import os
import shutil
import subprocess
import platform
from pathlib import Path
from datetime import datetime
import json
import webbrowser

# Detect operating system
CURRENT_OS = platform.system().lower()
IS_WINDOWS = CURRENT_OS == 'windows'
IS_MACOS = CURRENT_OS == 'darwin'
IS_LINUX = CURRENT_OS == 'linux'

class ImprovedFileOperations:
    def __init__(self):
        self.last_search_results = []
        self.default_locations = self._get_default_locations()
    
    def _get_default_locations(self):
        """Get default file locations based on OS"""
        home = Path.home()
        locations = {
            'desktop': home / 'Desktop',
            'documents': home / 'Documents',
            'downloads': home / 'Downloads',
            'pictures': home / 'Pictures',
            'music': home / 'Music',
            'videos': home / 'Videos' if not IS_MACOS else home / 'Movies'
        }
        return locations
    
    def create_file(self, filename, location='desktop', content_type='auto'):
        """
        Create a file with proper error handling
        Args:
            filename: Name of the file to create
            location: Where to create it (desktop, documents, etc.)
            content_type: Type of content to add (auto-detect from extension)
        """
        try:
            # Ensure filename has extension
            if '.' not in filename:
                filename += '.txt'
            
            # Get target directory
            if location in self.default_locations:
                target_dir = self.default_locations[location]
            else:
                target_dir = Path(location) if os.path.isabs(location) else self.default_locations['desktop']
            
            # Ensure directory exists
            target_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = target_dir / filename
            
            # Check if file already exists
            if file_path.exists():
                # Create unique filename
                base_name = file_path.stem
                extension = file_path.suffix
                counter = 1
                while file_path.exists():
                    new_name = f"{base_name}_{counter}{extension}"
                    file_path = target_dir / new_name
                    counter += 1
            
            # Create file with appropriate content
            success = self._create_file_with_content(file_path, content_type)
            
            if success:
                return {
                    'success': True,
                    'message': f"✅ Successfully created '{file_path.name}' in {location}",
                    'path': str(file_path),
                    'name': file_path.name
                }
            else:
                return {
                    'success': False,
                    'message': f"❌ Failed to create '{filename}'",
                    'path': None
                }
                
        except PermissionError:
            return {
                'success': False,
                'message': f"❌ Permission denied: Cannot create '{filename}' in {location}",
                'path': None
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Error creating file: {str(e)}",
                'path': None
            }
    
    def _create_file_with_content(self, file_path, content_type='auto'):
        """Create file with appropriate content based on extension"""
        try:
            extension = file_path.suffix.lower()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            base_name = file_path.stem
            
            # Content templates based on file type
            content_templates = {
                '.txt': f"# {base_name}\n\nCreated by JARVIS on {current_time}\n\nThis is a text document.\n",
                '.md': f"# {base_name}\n\n**Created by JARVIS** on {current_time}\n\n## Content\n\nThis is a markdown document.\n\n- Item 1\n- Item 2\n- Item 3\n",
                '.html': f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{base_name}</title>
</head>
<body>
    <h1>{base_name}</h1>
    <p>Created by JARVIS on {current_time}</p>
    <p>This is an HTML document.</p>
</body>
</html>""",
                '.css': f"""/* {base_name} - Created by JARVIS on {current_time} */

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}}

.container {{
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}""",
                '.js': f"""// {base_name} - Created by JARVIS on {current_time}

console.log('Hello from {base_name}!');

// Your JavaScript code here
function main() {{
    console.log('JARVIS created this file on {current_time}');
}}

main();""",
                '.py': f"""#!/usr/bin/env python3
# {base_name} - Created by JARVIS on {current_time}

def main():
    print("Hello from {base_name}!")
    print("Created by JARVIS on {current_time}")

if __name__ == "__main__":
    main()""",
                '.json': json.dumps({
                    "name": base_name,
                    "created_by": "JARVIS",
                    "created_on": current_time,
                    "description": "JSON file created by JARVIS",
                    "data": {}
                }, indent=2),
                '.csv': f"Name,Value,Created By,Created On\n{base_name},Sample Data,JARVIS,{current_time}\n"
            }
            
            # Get content or use default
            content = content_templates.get(extension, content_templates['.txt'])
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error creating file content: {e}")
            return False
    
    def find_files(self, search_term, max_results=20):
        """
        Enhanced file search with better performance and results
        """
        try:
            matches = []
            search_term_lower = search_term.lower()
            
            # Priority search locations
            search_locations = [
                self.default_locations['desktop'],
                self.default_locations['documents'],
                self.default_locations['downloads'],
                self.default_locations['pictures'],
                Path.home(),
            ]
            
            # Add system-specific locations
            if IS_WINDOWS:
                # Add drives
                for drive_letter in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
                    drive_path = Path(f"{drive_letter}:/")
                    if drive_path.exists():
                        search_locations.append(drive_path)
            elif IS_MACOS:
                search_locations.extend([
                    Path('/Applications'),
                    Path('/System/Applications')
                ])
            else:  # Linux
                search_locations.extend([
                    Path('/usr/bin'),
                    Path('/usr/local/bin'),
                    Path('/opt')
                ])
            
            print(f"🔍 Searching for '{search_term}'...")
            
            for search_dir in search_locations:
                if len(matches) >= max_results:
                    break
                
                try:
                    if not search_dir.exists():
                        continue
                    
                    # Search in current directory
                    for item in search_dir.iterdir():
                        if len(matches) >= max_results:
                            break
                        
                        if search_term_lower in item.name.lower():
                            matches.append({
                                'path': str(item),
                                'name': item.name,
                                'type': 'folder' if item.is_dir() else 'file',
                                'size': item.stat().st_size if item.is_file() else 0,
                                'location': str(search_dir),
                                'parent': str(item.parent)
                            })
                    
                    # For user directories, search recursively with depth limit
                    if any(user_dir in str(search_dir).lower() for user_dir in ['desktop', 'documents', 'downloads']):
                        try:
                            for item in search_dir.rglob(f"*{search_term}*"):
                                if len(matches) >= max_results:
                                    break
                                
                                # Skip hidden files and limit depth
                                if any(part.startswith('.') for part in item.parts):
                                    continue
                                if len(item.parts) - len(search_dir.parts) > 3:
                                    continue
                                
                                matches.append({
                                    'path': str(item),
                                    'name': item.name,
                                    'type': 'folder' if item.is_dir() else 'file',
                                    'size': item.stat().st_size if item.is_file() else 0,
                                    'location': str(search_dir),
                                    'parent': str(item.parent)
                                })
                        except (PermissionError, OSError):
                            continue
                            
                except (PermissionError, OSError):
                    continue
            
            # Store results for potential opening
            self.last_search_results = matches
            
            print(f"✅ Found {len(matches)} matches")
            return {
                'success': True,
                'matches': matches,
                'count': len(matches)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Error searching for files: {str(e)}",
                'matches': [],
                'count': 0
            }
    
    def open_file(self, file_path_or_number):
        """
        Open file using system default application
        Can accept file path or number from search results
        """
        try:
            # Check if it's a number (from search results)
            if isinstance(file_path_or_number, (int, str)) and str(file_path_or_number).isdigit():
                file_number = int(file_path_or_number)
                if not self.last_search_results:
                    return {
                        'success': False,
                        'message': "No recent search results. Please search for files first."
                    }
                
                if 1 <= file_number <= len(self.last_search_results):
                    file_path = self.last_search_results[file_number - 1]['path']
                    file_name = self.last_search_results[file_number - 1]['name']
                else:
                    return {
                        'success': False,
                        'message': f"Invalid number. Choose between 1 and {len(self.last_search_results)}"
                    }
            else:
                file_path = str(file_path_or_number)
                file_name = Path(file_path).name
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'message': f"File not found: {file_path}"
                }
            
            # Open file based on OS
            if IS_WINDOWS:
                if Path(file_path).is_dir():
                    subprocess.run(['explorer', file_path], check=True)
                else:
                    os.startfile(file_path)
            elif IS_MACOS:
                subprocess.run(['open', file_path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', file_path], check=True)
            
            return {
                'success': True,
                'message': f"✅ Opened '{file_name}' successfully",
                'path': file_path
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'message': f"Failed to open file: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error opening file: {str(e)}"
            }
    
    def delete_file(self, filename_or_path, permanent=False):
        """
        Delete file or folder (to trash by default)
        """
        try:
            # If it's just a filename, search for it first
            if not os.path.isabs(filename_or_path) and not os.path.exists(filename_or_path):
                search_result = self.find_files(filename_or_path, max_results=5)
                if not search_result['success'] or not search_result['matches']:
                    return {
                        'success': False,
                        'message': f"Could not find '{filename_or_path}' to delete"
                    }
                
                if len(search_result['matches']) == 1:
                    file_path = search_result['matches'][0]['path']
                    file_name = search_result['matches'][0]['name']
                else:
                    # Multiple matches - return options
                    matches_text = "\n".join([
                        f"{i+1}. {match['name']} ({match['path']})" 
                        for i, match in enumerate(search_result['matches'][:5])
                    ])
                    return {
                        'success': False,
                        'message': f"Multiple files found:\n{matches_text}\nPlease be more specific."
                    }
            else:
                file_path = filename_or_path
                file_name = Path(file_path).name
            
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'message': f"File not found: {file_path}"
                }
            
            path_obj = Path(file_path)
            item_type = "folder" if path_obj.is_dir() else "file"
            
            if permanent:
                # Permanent deletion
                if path_obj.is_dir():
                    shutil.rmtree(file_path)
                else:
                    path_obj.unlink()
                return {
                    'success': True,
                    'message': f"✅ Permanently deleted {item_type} '{file_name}'"
                }
            else:
                # Move to trash
                try:
                    # Try using send2trash if available
                    import send2trash
                    send2trash.send2trash(file_path)
                    return {
                        'success': True,
                        'message': f"✅ Moved {item_type} '{file_name}' to trash"
                    }
                except ImportError:
                    # Fallback methods
                    if IS_MACOS:
                        # Use AppleScript
                        script = f'tell application "Finder" to delete POSIX file "{file_path}"'
                        result = subprocess.run(['osascript', '-e', script], 
                                              capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            return {
                                'success': True,
                                'message': f"✅ Moved {item_type} '{file_name}' to trash"
                            }
                    
                    # Manual trash folder method
                    trash_path = Path.home() / '.Trash' if IS_MACOS else Path.home() / '.local/share/Trash/files'
                    if trash_path.exists():
                        import time
                        timestamp = int(time.time())
                        trash_item_path = trash_path / f"{file_name}_{timestamp}"
                        shutil.move(file_path, str(trash_item_path))
                        return {
                            'success': True,
                            'message': f"✅ Moved {item_type} '{file_name}' to trash"
                        }
                    else:
                        return {
                            'success': False,
                            'message': f"Could not access trash. Use permanent deletion if needed."
                        }
                        
        except PermissionError:
            return {
                'success': False,
                'message': f"Permission denied: Cannot delete '{filename_or_path}'"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error deleting file: {str(e)}"
            }
    
    def rename_file(self, old_name, new_name):
        """
        Rename file or folder
        """
        try:
            # If old_name is not a full path, search for it
            if not os.path.isabs(old_name) and not os.path.exists(old_name):
                search_result = self.find_files(old_name, max_results=5)
                if not search_result['success'] or not search_result['matches']:
                    return {
                        'success': False,
                        'message': f"Could not find '{old_name}' to rename"
                    }
                
                if len(search_result['matches']) == 1:
                    old_path = Path(search_result['matches'][0]['path'])
                else:
                    matches_text = "\n".join([
                        f"{i+1}. {match['name']} ({match['path']})" 
                        for i, match in enumerate(search_result['matches'][:5])
                    ])
                    return {
                        'success': False,
                        'message': f"Multiple files found:\n{matches_text}\nPlease be more specific."
                    }
            else:
                old_path = Path(old_name)
            
            if not old_path.exists():
                return {
                    'success': False,
                    'message': f"File not found: {old_name}"
                }
            
            new_path = old_path.parent / new_name
            
            if new_path.exists():
                return {
                    'success': False,
                    'message': f"Name '{new_name}' already exists in the same location"
                }
            
            old_path.rename(new_path)
            
            return {
                'success': True,
                'message': f"✅ Renamed '{old_path.name}' to '{new_name}'",
                'old_name': old_path.name,
                'new_name': new_name,
                'path': str(new_path)
            }
            
        except PermissionError:
            return {
                'success': False,
                'message': f"Permission denied: Cannot rename '{old_name}'"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error renaming file: {str(e)}"
            }
    
    def create_folder(self, folder_name, location='desktop'):
        """
        Create a new folder
        """
        try:
            # Get target directory
            if location in self.default_locations:
                target_dir = self.default_locations[location]
            else:
                target_dir = Path(location) if os.path.isabs(location) else self.default_locations['desktop']
            
            # Ensure parent directory exists
            target_dir.mkdir(parents=True, exist_ok=True)
            
            folder_path = target_dir / folder_name
            
            # Check if folder already exists
            if folder_path.exists():
                # Create unique folder name
                counter = 1
                while folder_path.exists():
                    new_name = f"{folder_name}_{counter}"
                    folder_path = target_dir / new_name
                    counter += 1
            
            folder_path.mkdir(parents=True, exist_ok=True)
            
            return {
                'success': True,
                'message': f"✅ Successfully created folder '{folder_path.name}' in {location}",
                'path': str(folder_path),
                'name': folder_path.name
            }
            
        except PermissionError:
            return {
                'success': False,
                'message': f"Permission denied: Cannot create folder '{folder_name}' in {location}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error creating folder: {str(e)}"
            }
    
    def take_photo_and_open(self):
        """
        Take a photo and automatically open it
        """
        try:
            import cv2
            
            # Try different camera indices
            camera_indices = [0, 1, 2]
            cam = None
            
            for index in camera_indices:
                try:
                    cam = cv2.VideoCapture(index)
                    if cam.isOpened():
                        ret, test_frame = cam.read()
                        if ret and test_frame is not None:
                            break
                        else:
                            cam.release()
                            cam = None
                except:
                    if cam:
                        cam.release()
                    cam = None
                    continue
            
            if cam is None:
                return {
                    'success': False,
                    'message': "No camera found or camera is not accessible"
                }
            
            # Set camera properties
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            # Capture frame
            ret, frame = cam.read()
            
            if ret and frame is not None:
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"JARVIS_photo_{timestamp}.jpg"
                
                # Save to Pictures folder
                pictures_dir = self.default_locations['pictures']
                pictures_dir.mkdir(parents=True, exist_ok=True)
                photo_path = pictures_dir / filename
                
                # Save the image
                success = cv2.imwrite(str(photo_path), frame)
                cam.release()
                
                if success:
                    # Automatically open the photo
                    open_result = self.open_file(str(photo_path))
                    
                    return {
                        'success': True,
                        'message': f"✅ Photo captured and opened: {filename}",
                        'path': str(photo_path),
                        'opened': open_result['success']
                    }
                else:
                    return {
                        'success': False,
                        'message': "Failed to save the captured photo"
                    }
            else:
                cam.release()
                return {
                    'success': False,
                    'message': "Failed to capture photo from camera"
                }
                
        except ImportError:
            return {
                'success': False,
                'message': "Camera functionality not available. Please install opencv-python: pip install opencv-python"
            }
        except Exception as e:
            if 'cam' in locals() and cam:
                cam.release()
            return {
                'success': False,
                'message': f"Error capturing photo: {str(e)}"
            }

# Global instance
file_ops = ImprovedFileOperations()

# Convenience functions for backward compatibility
def create_file(filename, location='desktop'):
    return file_ops.create_file(filename, location)

def find_files(search_term, max_results=20):
    return file_ops.find_files(search_term, max_results)

def open_file(file_path_or_number):
    return file_ops.open_file(file_path_or_number)

def delete_file(filename_or_path, permanent=False):
    return file_ops.delete_file(filename_or_path, permanent)

def rename_file(old_name, new_name):
    return file_ops.rename_file(old_name, new_name)

def create_folder(folder_name, location='desktop'):
    return file_ops.create_folder(folder_name, location)

def take_photo_and_open():
    return file_ops.take_photo_and_open()