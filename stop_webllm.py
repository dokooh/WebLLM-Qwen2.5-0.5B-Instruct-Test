#!/usr/bin/env python3
"""
Python script to stop WebLLM and clean up browser processes
"""

import psutil
import os
import sys
import time
from pathlib import Path

def find_browser_processes():
    """Find running browser processes that might be running WebLLM"""
    browser_names = [
        'chrome.exe', 'msedge.exe', 'firefox.exe', 'opera.exe',
        'brave.exe', 'vivaldi.exe', 'safari.exe', 'iexplore.exe'
    ]
    
    browser_processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] and proc.info['name'].lower() in browser_names:
                # Check if the process has WebLLM-related content
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'webllm' in cmdline.lower() or 'qwen' in cmdline.lower():
                    browser_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline
                    })
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    
    return browser_processes

def find_python_server_processes():
    """Find Python HTTP server processes that might be serving WebLLM"""
    python_servers = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'] or [])
                cwd = proc.info['cwd'] or ''
                
                # Check for HTTP server or WebLLM launcher
                if any(keyword in cmdline.lower() for keyword in [
                    'http.server', 'socketserver', 'webllm', 'launch_webllm'
                ]):
                    python_servers.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline,
                        'cwd': cwd
                    })
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    
    return python_servers

def stop_process(pid, name):
    """Safely stop a process by PID"""
    try:
        proc = psutil.Process(pid)
        print(f"  🛑 Stopping {name} (PID: {pid})")
        proc.terminate()
        
        # Wait for graceful termination
        try:
            proc.wait(timeout=5)
            print(f"  ✅ {name} stopped gracefully")
            return True
        except psutil.TimeoutExpired:
            print(f"  ⚠️ Force killing {name}")
            proc.kill()
            proc.wait()
            print(f"  ✅ {name} force stopped")
            return True
            
    except psutil.NoSuchProcess:
        print(f"  ✅ {name} already stopped")
        return True
    except psutil.AccessDenied:
        print(f"  ❌ Access denied stopping {name}")
        return False
    except Exception as e:
        print(f"  ❌ Error stopping {name}: {e}")
        return False

def clear_browser_cache():
    """Clear browser cache related to WebLLM (optional)"""
    print("\n🧹 Browser Cache Cleanup:")
    
    # Common browser cache locations for WebLLM content
    cache_patterns = [
        "webllm",
        "qwen",
        "mlc-ai"
    ]
    
    print("  ℹ️ Cache cleanup is optional and browser-specific")
    print("  💡 You may manually clear browser cache if needed")
    
    return True

def cleanup_temp_files():
    """Clean up temporary files created by WebLLM"""
    print("\n🗑️ Cleaning temporary files:")
    
    temp_files = [
        "webllm_results.json",
        ".webllm_cache",
        "mlc_cache"
    ]
    
    cleaned = 0
    for temp_file in temp_files:
        file_path = Path(temp_file)
        if file_path.exists():
            try:
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                print(f"  ✅ Removed {temp_file}")
                cleaned += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {temp_file}: {e}")
    
    if cleaned == 0:
        print("  ℹ️ No temporary files found to clean")
    
    return True

def show_running_status():
    """Show what WebLLM-related processes are currently running"""
    print("🔍 Checking for running WebLLM processes...")
    
    browsers = find_browser_processes()
    servers = find_python_server_processes()
    
    if not browsers and not servers:
        print("  ✅ No WebLLM processes found running")
        return False
    
    if browsers:
        print(f"\n🌐 Found {len(browsers)} browser process(es) with WebLLM content:")
        for proc in browsers:
            print(f"  • {proc['name']} (PID: {proc['pid']})")
    
    if servers:
        print(f"\n🐍 Found {len(servers)} Python server process(es):")
        for proc in servers:
            print(f"  • {proc['name']} (PID: {proc['pid']})")
            if proc['cwd']:
                print(f"    Working directory: {proc['cwd']}")
    
    return True

def main():
    """Main function to stop WebLLM"""
    
    print("🛑 WebLLM Stop Script")
    print("=" * 40)
    
    # Check current status
    has_processes = show_running_status()
    
    if not has_processes:
        print("\n🎉 WebLLM is not currently running!")
        return True
    
    print("\n❓ Do you want to stop these processes? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response not in ['y', 'yes']:
            print("🚫 Operation cancelled")
            return False
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled")
        return False
    
    print("\n🛑 Stopping WebLLM processes...")
    
    # Stop browser processes
    browsers = find_browser_processes()
    if browsers:
        print(f"\n🌐 Stopping {len(browsers)} browser process(es):")
        for proc in browsers:
            stop_process(proc['pid'], proc['name'])
    
    # Stop Python server processes  
    servers = find_python_server_processes()
    if servers:
        print(f"\n🐍 Stopping {len(servers)} Python server process(es):")
        for proc in servers:
            stop_process(proc['pid'], proc['name'])
    
    # Wait a moment for processes to stop
    time.sleep(2)
    
    # Clean up files
    cleanup_temp_files()
    clear_browser_cache()
    
    # Final check
    print("\n🔍 Final status check...")
    final_check = show_running_status()
    
    if not final_check:
        print("\n✅ WebLLM stopped successfully!")
        print("🎯 All processes terminated and temporary files cleaned")
        return True
    else:
        print("\n⚠️ Some processes may still be running")
        print("💡 You may need to manually close browser tabs or restart the browser")
        return False

def force_stop():
    """Force stop all WebLLM processes without confirmation"""
    print("⚡ Force stopping all WebLLM processes...")
    
    browsers = find_browser_processes()
    servers = find_python_server_processes()
    
    all_stopped = True
    
    for proc in browsers + servers:
        if not stop_process(proc['pid'], proc['name']):
            all_stopped = False
    
    cleanup_temp_files()
    
    return all_stopped

if __name__ == "__main__":
    print("🚀 WebLLM Stop Utility")
    
    # Check for force flag
    if len(sys.argv) > 1 and sys.argv[1] in ['--force', '-f']:
        success = force_stop()
    else:
        success = main()
    
    if success:
        print("\n🎉 WebLLM shutdown completed!")
    else:
        print("\n⚠️ WebLLM shutdown completed with warnings")
        exit(1)