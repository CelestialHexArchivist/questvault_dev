import os
import sys
from pathlib import Path

def verify_structure():
    """Verify project structure and print diagnostic information"""
    current_dir = Path.cwd()
    script_dir = Path(__file__).parent.absolute()
    
    print("\n=== Directory Information ===")
    print(f"Current Directory: {current_dir}")
    print(f"Script Directory: {script_dir}")
    
    print("\n=== Python Path ===")
    for p in sys.path:
        print(f"Path: {p}")
    
    print("\n=== Directory Structure ===")
    try:
        core_dir = script_dir / 'core'
        if core_dir.exists():
            print("✓ core/ directory exists")
            # Check core directory contents
            core_contents = list(core_dir.glob('*'))
            print("\ncore/ contents:")
            for item in core_contents:
                print(f"  - {item.name}")
            
            # Check specific files
            files_to_check = [
                ('__init__.py', 'Package initialization'),
                ('logger.py', 'Logging module'),
                ('theme.py', 'Theme definitions'),
                ('url_manager.py', 'URL management'),
            ]
            
            print("\nRequired files:")
            for filename, description in files_to_check:
                file_path = core_dir / filename
                status = '✓' if file_path.exists() else '✗'
                print(f"{status} {filename:<15} - {description}")
        else:
            print("✗ core/ directory not found!")
            
        print("\n=== File Permissions ===")
        if core_dir.exists():
            try:
                with open(core_dir / '__init__.py', 'r') as f:
                    print("✓ Can read __init__.py")
            except Exception as e:
                print(f"✗ Cannot read __init__.py: {e}")
                
            try:
                with open(core_dir / 'logger.py', 'r') as f:
                    print("✓ Can read logger.py")
            except Exception as e:
                print(f"✗ Cannot read logger.py: {e}")
        
    except Exception as e:
        print(f"Error during verification: {e}")
    
    print("\n=== Import Test ===")
    try:
        sys.path.insert(0, str(script_dir))
        from core.logger import setup_logger
        print("✓ Successfully imported setup_logger")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        # Try alternative import paths
        try:
            sys.path.append(str(Path(__file__).parent))
            from core.logger import setup_logger
            print("✓ Successfully imported setup_logger (alternative path)")
        except ImportError as e:
            print(f"✗ Alternative import also failed: {e}")
        
    print("\n=== Environment ===")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")

if __name__ == "__main__":
    verify_structure()
    
    print("\nIf you see any ✗ marks above, those indicate issues that need to be fixed.")
    print("Please share this output so we can help resolve any issues.") 