#!/usr/bin/env python3
"""
WebLLM Stop Helper - Simple instructions and cleanup
"""

import webbrowser
import os
from pathlib import Path

def show_stop_instructions():
    """Show instructions on how to stop WebLLM"""
    
    print("🛑 How to Stop WebLLM")
    print("=" * 30)
    
    print("\n📋 Step-by-Step Instructions:")
    print("1. 🌐 Go to your web browser")
    print("2. 🔍 Find any tabs with WebLLM or Qwen content")
    print("3. 🗙 Close those tabs (Ctrl+W or click the X)")
    print("4. 🔄 Optionally close the entire browser")
    
    print("\n⚡ Quick Browser Shortcuts:")
    print("• Ctrl+W          → Close current tab")
    print("• Ctrl+Shift+W    → Close all tabs")  
    print("• Alt+F4          → Close browser window")
    print("• Ctrl+Shift+Del  → Clear browser cache")
    
def cleanup_webllm_files():
    """Clean up WebLLM temporary files"""
    
    print("\n🧹 Cleaning WebLLM Files:")
    
    files_to_check = [
        "webllm_results.json",
        "webllm_cache",
        ".webllm",
        "mlc_cache"
    ]
    
    cleaned_count = 0
    
    for file_name in files_to_check:
        file_path = Path(file_name)
        
        if file_path.exists():
            try:
                if file_path.is_file():
                    file_path.unlink()
                    print(f"  ✅ Removed file: {file_name}")
                elif file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                    print(f"  ✅ Removed directory: {file_name}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file_name}: {e}")
    
    if cleaned_count == 0:
        print("  ✅ No temporary files found to clean")
    else:
        print(f"  🎯 Cleaned {cleaned_count} file(s)/folder(s)")

def check_webllm_status():
    """Check if WebLLM files are present"""
    
    print("\n🔍 WebLLM Status Check:")
    
    webllm_files = [
        "webllm_standalone.html",
        "webllm_test.html", 
        "launch_webllm.py",
        "package.json",
        "node_modules"
    ]
    
    found_files = []
    for file_name in webllm_files:
        if Path(file_name).exists():
            found_files.append(file_name)
    
    if found_files:
        print(f"  📁 WebLLM installation found ({len(found_files)} files)")
        print("  💡 WebLLM can be restarted with: python launch_webllm.py")
    else:
        print("  ❓ WebLLM installation not found in current directory")

def show_process_info():
    """Show how to manually check for running processes"""
    
    print("\n🔧 Manual Process Check (Optional):")
    print("If you want to check for running processes manually:")
    print()
    print("Windows Command Prompt:")
    print("  tasklist | findstr python")
    print("  tasklist | findstr chrome")
    print("  tasklist | findstr msedge")
    print()
    print("To force-kill a process:")
    print("  taskkill /PID <process_id> /F")
    print("  taskkill /IM chrome.exe /F")

def main():
    """Main function"""
    
    print("🚀 WebLLM Stop Helper")
    print("Simple tool to help stop WebLLM and clean up files")
    print()
    
    # Show how to stop WebLLM
    show_stop_instructions()
    
    # Clean up files
    cleanup_webllm_files()
    
    # Check status
    check_webllm_status()
    
    # Show advanced info
    show_process_info()
    
    print("\n" + "=" * 50)
    print("✅ WebLLM Stop Helper Completed!")
    print()
    print("🎯 Summary:")
    print("• Close WebLLM browser tabs manually")
    print("• Temporary files have been cleaned")
    print("• WebLLM can be restarted anytime")
    print()
    print("💡 If WebLLM is still running after closing browser tabs,")
    print("   try restarting your browser completely.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🚫 Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Try closing browser tabs manually")