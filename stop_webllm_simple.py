#!/usr/bin/env python3
"""
Simple WebLLM stop script (no external dependencies)
Uses Windows taskkill command to stop browser processes
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def find_browser_processes_simple():
    """Find browser processes using tasklist command"""
    browser_names = [
        'chrome.exe', 'msedge.exe', 'firefox.exe', 'opera.exe',
        'brave.exe', 'vivaldi.exe', 'safari.exe', 'iexplore.exe'
    ]
    
    found_processes = []
    
    for browser in browser_names:
        success, stdout, stderr = run_command(f'tasklist /FI "IMAGENAME eq {browser}"')
        if success and browser.lower() in stdout.lower():
            # Extract process info
            lines = stdout.strip().split('\n')
            for line in lines:
                if browser.lower() in line.lower() and 'PID' not in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            pid = parts[1]
                            found_processes.append({'name': browser, 'pid': pid})
                        except (IndexError, ValueError):
                            continue
    
    return found_processes

def kill_browser_processes():
    """Kill browser processes that might be running WebLLM"""
    print("🔍 Looking for browser processes...")
    
    browsers = find_browser_processes_simple()
    
    if not browsers:
        print("  ✅ No browser processes found")
        return True
    
    print(f"📋 Found {len(browsers)} browser process(es):")
    for proc in browsers:
        print(f"  • {proc['name']} (PID: {proc['pid']})")
    
    print("\n❓ Close all browser windows? This will close ALL instances! (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response not in ['y', 'yes']:
            print("🚫 Skipping browser closure")
            return False
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled")
        return False
    
    print("\n🛑 Closing browser processes...")
    success_count = 0
    
    for proc in browsers:
        print(f"  🛑 Stopping {proc['name']} (PID: {proc['pid']})")
        success, stdout, stderr = run_command(f'taskkill /PID {proc["pid"]} /F')
        
        if success:
            print(f"  ✅ {proc['name']} stopped successfully")
            success_count += 1
        else:
            print(f"  ❌ Failed to stop {proc['name']}: {stderr}")
    
    return success_count == len(browsers)

def kill_python_servers():
    """Kill Python HTTP servers"""
    print("\n🐍 Looking for Python server processes...")
    
    # Look for Python processes with HTTP server keywords
    success, stdout, stderr = run_command('tasklist /FI "IMAGENAME eq python.exe"')
    
    if not success or 'python.exe' not in stdout.lower():
        print("  ✅ No Python processes found")
        return True
    
    print("  📋 Found Python processes (may include servers)")
    
    # For safety, we won't auto-kill Python processes as they might be important
    # Instead, we'll show them and let the user decide
    print("  ⚠️ Manual check recommended - Python processes not auto-terminated")
    print("  💡 If you have a WebLLM server running, press Ctrl+C in its terminal")
    
    return True

def cleanup_files():
    """Clean up WebLLM related files"""
    print("\n🧹 Cleaning up files...")
    
    files_to_clean = [
        "webllm_results.json",
        "webllm_cache"
    ]
    
    cleaned = 0
    for file_name in files_to_clean:
        file_path = Path(file_name)
        if file_path.exists():
            try:
                if file_path.is_file():
                    file_path.unlink()
                else:
                    import shutil
                    shutil.rmtree(file_path)
                print(f"  ✅ Removed {file_name}")
                cleaned += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file_name}: {e}")
    
    if cleaned == 0:
        print("  ✅ No cleanup files found")
    
    return True

def close_webllm_tabs():
    """Instructions to manually close WebLLM tabs"""
    print("\n🌐 To complete WebLLM shutdown:")
    print("  1. 🔍 Check your browser for any WebLLM tabs")
    print("  2. 🗙 Close tabs containing 'webllm' or 'qwen'")
    print("  3. 🔄 Optionally restart your browser for a clean state")
    print("  4. 🧹 Clear browser cache if needed (Ctrl+Shift+Del)")

def main():
    """Main function"""
    
    print("🛑 WebLLM Simple Stop Script")
    print("=" * 45)
    print("⚠️ This will attempt to close browser processes")
    print("💡 Make sure to save any important browser work first!")
    print()
    
    try:
        # Kill browser processes (with confirmation)
        browser_success = kill_browser_processes()
        
        # Check Python servers
        python_success = kill_python_servers()
        
        # Cleanup files
        cleanup_success = cleanup_files()
        
        # Show manual steps
        close_webllm_tabs()
        
        if browser_success and python_success and cleanup_success:
            print("\n✅ WebLLM stop process completed successfully!")
        else:
            print("\n⚠️ WebLLM stop process completed with some issues")
            
        print("\n🎯 WebLLM should now be stopped")
        print("💡 If WebLLM is still running, try closing browser tabs manually")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🚫 Stop operation cancelled")
        return False
    except Exception as e:
        print(f"\n❌ Error during stop operation: {e}")
        return False

def force_mode():
    """Force close browsers without confirmation"""
    print("⚡ FORCE MODE: Closing all browser instances!")
    
    browsers_to_kill = ['chrome.exe', 'msedge.exe', 'firefox.exe', 'opera.exe']
    
    for browser in browsers_to_kill:
        print(f"🛑 Force killing {browser}")
        run_command(f'taskkill /IM {browser} /F')
    
    cleanup_files()
    print("✅ Force stop completed")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--force', '-f']:
        force_mode()
    else:
        main()
    
    print("\n🏁 WebLLM stop script finished")