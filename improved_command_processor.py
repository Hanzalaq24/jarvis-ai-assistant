#!/usr/bin/env python3
"""
Improved Command Processor for JARVIS AI Assistant
Handles file operations with better error handling and user interaction
"""

import re
from improved_file_operations import file_ops

class ImprovedCommandProcessor:
    def __init__(self):
        self.file_ops = file_ops
        self.awaiting_confirmation = None
        self.confirmation_data = None
    
    def process_file_command(self, command, original_command):
        """
        Process file-related commands with improved parsing and error handling
        """
        command_lower = command.lower().strip()
        
        # CREATE FILE COMMANDS
        if self._is_create_file_command(command_lower):
            return self._handle_create_file(command_lower, original_command)
        
        # CREATE FOLDER COMMANDS
        elif self._is_create_folder_command(command_lower):
            return self._handle_create_folder(command_lower, original_command)
        
        # FIND FILE COMMANDS
        elif self._is_find_file_command(command_lower):
            return self._handle_find_file(command_lower, original_command)
        
        # OPEN FILE COMMANDS
        elif self._is_open_file_command(command_lower):
            return self._handle_open_file(command_lower, original_command)
        
        # DELETE FILE COMMANDS
        elif self._is_delete_command(command_lower):
            return self._handle_delete_file(command_lower, original_command)
        
        # RENAME FILE COMMANDS
        elif self._is_rename_command(command_lower):
            return self._handle_rename_file(command_lower, original_command)
        
        # TAKE PHOTO COMMANDS
        elif self._is_photo_command(command_lower):
            return self._handle_take_photo(command_lower, original_command)
        
        # CONFIRMATION RESPONSES
        elif self._is_confirmation_response(command_lower):
            return self._handle_confirmation(command_lower)
        
        return None
    
    def _is_create_file_command(self, command):
        """Check if command is for creating a file"""
        patterns = [
            r'create file',
            r'make file',
            r'new file',
            r'create.*\.(txt|pdf|doc|docx|html|css|js|py|json|csv|md)',
            r'make.*\.(txt|pdf|doc|docx|html|css|js|py|json|csv|md)',
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_create_folder_command(self, command):
        """Check if command is for creating a folder"""
        patterns = [
            r'create folder',
            r'make folder',
            r'new folder',
            r'create directory',
            r'make directory'
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_find_file_command(self, command):
        """Check if command is for finding files"""
        patterns = [
            r'find file',
            r'search file',
            r'locate file',
            r'look for file',
            r'search for.*file',
            r'find.*\.(txt|pdf|doc|docx|html|css|js|py|json|csv|md)',
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_open_file_command(self, command):
        """Check if command is for opening files"""
        patterns = [
            r'open file',
            r'launch file',
            r'run file',
            r'open \d+',  # open number from search results
            r'open.*\.(txt|pdf|doc|docx|html|css|js|py|json|csv|md)',
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_delete_command(self, command):
        """Check if command is for deleting files/folders"""
        patterns = [
            r'delete file',
            r'remove file',
            r'delete folder',
            r'remove folder',
            r'delete.*\.(txt|pdf|doc|docx|html|css|js|py|json|csv|md)',
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_rename_command(self, command):
        """Check if command is for renaming files/folders"""
        patterns = [
            r'rename.*to',
            r'rename file.*to',
            r'rename folder.*to',
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_photo_command(self, command):
        """Check if command is for taking photos"""
        patterns = [
            r'take photo',
            r'capture photo',
            r'take picture',
            r'capture picture',
            r'take a photo',
            r'take a picture'
        ]
        return any(re.search(pattern, command) for pattern in patterns)
    
    def _is_confirmation_response(self, command):
        """Check if command is a yes/no confirmation"""
        return command in ['yes', 'y', 'no', 'n', 'ok', 'okay', 'sure', 'cancel', 'abort']
    
    def _handle_create_file(self, command, original_command):
        """Handle file creation commands"""
        # Extract filename from command
        filename = self._extract_filename_from_create_command(command, original_command)
        
        if not filename:
            return "Please specify a filename, sir. For example: 'create file document.txt' or 'create file report.pdf'"
        
        # Ask for location if not specified
        location = self._extract_location_from_command(command)
        if not location:
            location = 'desktop'  # default
        
        result = self.file_ops.create_file(filename, location)
        
        if result['success']:
            # Ask if user wants to open the file
            self.awaiting_confirmation = 'open_created_file'
            self.confirmation_data = {'path': result['path'], 'name': result['name']}
            return f"{result['message']}\n\nWould you like me to open '{result['name']}' now, sir? (yes/no)"
        else:
            return result['message']
    
    def _handle_create_folder(self, command, original_command):
        """Handle folder creation commands"""
        # Extract folder name
        folder_name = self._extract_folder_name_from_command(command, original_command)
        
        if not folder_name:
            return "Please specify a folder name, sir. For example: 'create folder MyDocuments'"
        
        location = self._extract_location_from_command(command) or 'desktop'
        
        result = self.file_ops.create_folder(folder_name, location)
        
        if result['success']:
            # Ask if user wants to open the folder
            self.awaiting_confirmation = 'open_created_folder'
            self.confirmation_data = {'path': result['path'], 'name': result['name']}
            return f"{result['message']}\n\nWould you like me to open the folder now, sir? (yes/no)"
        else:
            return result['message']
    
    def _handle_find_file(self, command, original_command):
        """Handle file search commands"""
        search_term = self._extract_search_term_from_command(command, original_command)
        
        if not search_term:
            return "Please specify what file to search for, sir. For example: 'find file document.pdf'"
        
        result = self.file_ops.find_files(search_term)
        
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
            
            if result['count'] > 10:
                response += f"... and {result['count'] - 10} more files.\n\n"
            
            response += "Would you like me to open any of these files, sir? Just say 'open 1' or 'open file 2' to open a specific file."
            
            return response
        else:
            return f"Sorry sir, I couldn't find any files matching '{search_term}'. I searched across all common locations including Desktop, Documents, Downloads, and system directories."
    
    def _handle_open_file(self, command, original_command):
        """Handle file opening commands"""
        # Check if it's a number from search results
        number_match = re.search(r'open (\d+)|open file (\d+)', command)
        if number_match:
            file_number = int(number_match.group(1) or number_match.group(2))
            result = self.file_ops.open_file(file_number)
        else:
            # Extract filename
            filename = self._extract_filename_from_open_command(command, original_command)
            if not filename:
                return "Please specify which file to open, sir. For example: 'open file document.pdf' or 'open 1' for search results."
            
            # First search for the file
            search_result = self.file_ops.find_files(filename, max_results=5)
            if not search_result['success'] or not search_result['matches']:
                return f"Could not find file '{filename}', sir. Try searching for it first with 'find file {filename}'"
            
            if len(search_result['matches']) == 1:
                result = self.file_ops.open_file(search_result['matches'][0]['path'])
            else:
                # Multiple matches - show options
                response = f"Found {len(search_result['matches'])} files named '{filename}':\n"
                for i, match in enumerate(search_result['matches'], 1):
                    response += f"{i}. {match['name']} ({match['path']})\n"
                response += "\nSay 'open 1' or 'open 2' to open a specific file, sir."
                return response
        
        return result['message']
    
    def _handle_delete_file(self, command, original_command):
        """Handle file deletion commands"""
        filename = self._extract_filename_from_delete_command(command, original_command)
        
        if not filename:
            return "Please specify what to delete, sir. For example: 'delete file document.pdf'"
        
        permanent = 'permanently' in original_command.lower()
        
        # Ask for confirmation before deleting
        self.awaiting_confirmation = 'delete_file'
        self.confirmation_data = {'filename': filename, 'permanent': permanent}
        
        delete_type = "permanently delete" if permanent else "move to trash"
        return f"Are you sure you want to {delete_type} '{filename}', sir? This action cannot be undone. (yes/no)"
    
    def _handle_rename_file(self, command, original_command):
        """Handle file renaming commands"""
        # Extract old and new names from "rename X to Y" format
        match = re.search(r'rename\s+(.+?)\s+to\s+(.+)', command)
        if not match:
            return "Please use the format 'rename [old name] to [new name]', sir. For example: 'rename document.txt to report.txt'"
        
        old_name = match.group(1).strip()
        new_name = match.group(2).strip()
        
        # Remove "file" or "folder" keywords if present
        old_name = re.sub(r'^(file|folder)\s+', '', old_name)
        
        result = self.file_ops.rename_file(old_name, new_name)
        return result['message']
    
    def _handle_take_photo(self, command, original_command):
        """Handle photo capture commands"""
        result = self.file_ops.take_photo_and_open()
        return result['message']
    
    def _handle_confirmation(self, command):
        """Handle yes/no confirmations"""
        if not self.awaiting_confirmation:
            return "I'm not waiting for any confirmation, sir."
        
        is_yes = command in ['yes', 'y', 'ok', 'okay', 'sure']
        is_no = command in ['no', 'n', 'cancel', 'abort']
        
        if not (is_yes or is_no):
            return "Please answer with 'yes' or 'no', sir."
        
        confirmation_type = self.awaiting_confirmation
        data = self.confirmation_data
        
        # Clear confirmation state
        self.awaiting_confirmation = None
        self.confirmation_data = None
        
        if confirmation_type == 'open_created_file' and is_yes:
            result = self.file_ops.open_file(data['path'])
            return f"Opening '{data['name']}', sir. {result['message']}"
        
        elif confirmation_type == 'open_created_folder' and is_yes:
            result = self.file_ops.open_file(data['path'])
            return f"Opening folder '{data['name']}', sir. {result['message']}"
        
        elif confirmation_type == 'delete_file' and is_yes:
            result = self.file_ops.delete_file(data['filename'], data['permanent'])
            return result['message']
        
        elif is_no:
            return "Understood, sir. Operation cancelled."
        
        return "Operation completed, sir."
    
    def _extract_filename_from_create_command(self, command, original_command):
        """Extract filename from create file command"""
        import re
        
        # First, try to find filename patterns (words with extensions or quoted names)
        filename_patterns = [
            r'([a-zA-Z0-9_-]+\.[a-zA-Z0-9]+)',  # filename.ext
            r'"([^"]+)"',  # "quoted filename"
            r"'([^']+)'",  # 'quoted filename'
            r'called\s+([a-zA-Z0-9_.-]+)',  # "called filename.txt"
            r'named\s+([a-zA-Z0-9_.-]+)',   # "named filename.txt"
        ]
        
        command_lower = command.lower().strip()
        filename = None
        
        # Try to extract filename using specific patterns
        for pattern in filename_patterns:
            matches = re.findall(pattern, command_lower)
            if matches:
                # Take the last match (most likely the actual filename)
                filename = matches[-1].strip()
                break
        
        # If no filename found with patterns, try command-based extraction
        if not filename:
            command_patterns = [
                r'create\s+file\s+([a-zA-Z0-9_.-]+)',
                r'make\s+file\s+([a-zA-Z0-9_.-]+)',
                r'new\s+file\s+([a-zA-Z0-9_.-]+)',
            ]
            
            for pattern in command_patterns:
                match = re.search(pattern, command_lower)
                if match:
                    filename = match.group(1).strip()
                    break
        
        # Last resort: look for the last word that could be a filename
        if not filename:
            words = command.split()
            for word in reversed(words):
                # Check if word looks like a filename (has extension or is alphanumeric)
                if '.' in word or (word.isalnum() and len(word) > 1):
                    filename = word
                    break
        
        # Clean up the filename
        if filename:
            # Remove common filler words that might have been captured
            filler_words = ['a', 'an', 'the', 'file', 'called', 'named']
            filename_words = filename.split()
            cleaned_words = [word for word in filename_words if word.lower() not in filler_words]
            if cleaned_words:
                filename = ' '.join(cleaned_words)
            
            # If no extension, add .txt
            if '.' not in filename:
                filename += '.txt'
        
        return filename if filename else None
    
    def _extract_folder_name_from_command(self, command, original_command):
        """Extract folder name from create folder command"""
        import re
        
        # Use regex to properly extract folder name after command keywords
        patterns = [
            r'create\s+folder\s+(.+)',
            r'make\s+folder\s+(.+)',
            r'new\s+folder\s+(.+)',
            r'create\s+directory\s+(.+)',
            r'make\s+directory\s+(.+)',
        ]
        
        folder_name = None
        command_lower = command.lower().strip()
        
        for pattern in patterns:
            match = re.search(pattern, command_lower)
            if match:
                folder_name = match.group(1).strip()
                break
        
        if not folder_name:
            # Last resort: split by spaces and take the last part
            words = command.split()
            if len(words) >= 2:
                folder_name = words[-1]  # Take the last word as folder name
        
        return folder_name if folder_name else None
    
    def _extract_search_term_from_command(self, command, original_command):
        """Extract search term from find file command"""
        import re
        
        # Use regex to properly extract search term after command keywords
        patterns = [
            r'find\s+file\s+(.+)',
            r'search\s+file\s+(.+)',
            r'locate\s+file\s+(.+)',
            r'look\s+for\s+file\s+(.+)',
            r'search\s+for\s+(.+)',
            r'find\s+(.+)',
            r'search\s+(.+)',
        ]
        
        search_term = None
        command_lower = command.lower().strip()
        
        for pattern in patterns:
            match = re.search(pattern, command_lower)
            if match:
                search_term = match.group(1).strip()
                break
        
        if not search_term:
            # Last resort: split by spaces and take everything after the first word
            words = command.split()
            if len(words) >= 2:
                search_term = ' '.join(words[1:])  # Take everything after first word
        
        return search_term if search_term else None
    
    def _extract_filename_from_open_command(self, command, original_command):
        """Extract filename from open file command"""
        filename = command
        for phrase in ['open file', 'launch file', 'run file', 'open']:
            filename = filename.replace(phrase, '').strip()
        
        return filename if filename else None
    
    def _extract_filename_from_delete_command(self, command, original_command):
        """Extract filename from delete command"""
        filename = command
        for phrase in ['delete file', 'remove file', 'delete folder', 'remove folder', 'delete', 'remove']:
            filename = filename.replace(phrase, '').strip()
        
        # Remove "permanently" if present
        filename = filename.replace('permanently', '').strip()
        
        return filename if filename else None
    
    def _extract_location_from_command(self, command):
        """Extract location from command (desktop, documents, etc.)"""
        locations = ['desktop', 'documents', 'downloads', 'pictures', 'music', 'videos']
        for location in locations:
            if location in command:
                return location
        return None

# Global instance
command_processor = ImprovedCommandProcessor()

def process_file_command(command, original_command):
    """Main function to process file commands"""
    return command_processor.process_file_command(command, original_command)