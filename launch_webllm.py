#!/usr/bin/env python3
"""
Simple launcher for WebLLM Qwen2.5-0.5B-Instruct test
Opens the standalone HTML file directly in the browser
"""

import webbrowser
import os
from pathlib import Path

def main():
    """Launch WebLLM test in browser"""
    
    print("🚀 WebLLM Qwen2.5-0.5B-Instruct Launcher")
    print("=" * 50)
    
    # Check if the HTML file exists
    html_file = Path("webllm_standalone.html").resolve()
    
    if not html_file.exists():
        print("❌ Error: webllm_standalone.html not found!")
        return False
    
    # Create file:// URL for local file
    file_url = html_file.as_uri()
    
    print(f"📄 HTML file: {html_file}")
    print(f"🌐 Opening URL: {file_url}")
    
    print("\n📋 Instructions:")
    print("1. The browser will open with the WebLLM interface")
    print("2. Wait for Qwen2.5-0.5B-Instruct to load (2-5 minutes)")
    print("3. The model will run an automatic test first")
    print("4. Then you can chat with the model directly")
    print("5. WebLLM runs entirely in your browser!")
    
    print("\n🔍 What to expect:")
    print("✅ Model download and initialization progress")
    print("✅ Automatic test message and response")
    print("✅ Interactive chat interface")
    print("✅ Fast inference after initial load")
    
    try:
        # Open the HTML file in the default browser
        print(f"\n🚀 Launching browser...")
        webbrowser.open(file_url)
        
        print("✅ Browser launched successfully!")
        print("🎉 WebLLM should now be loading in your browser.")
        print("\n💡 Note: First load takes longer due to model download.")
        print("🔧 WebLLM will use WebAssembly + WebGPU for acceleration.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error launching browser: {e}")
        print(f"💡 You can manually open: {html_file}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 WebLLM Qwen2.5-0.5B-Instruct setup complete!")
        print("Check your browser for the running application.")
    else:
        print("\n❌ Setup failed!")
        exit(1)