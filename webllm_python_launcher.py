#!/usr/bin/env python3
"""
Python wrapper to run WebLLM with Qwen2.5-0.5B-Instruct in a web browser
"""

import webbrowser
import http.server
import socketserver
import threading
import time
import os
from pathlib import Path

def start_local_server(port=8080):
    """Start a local HTTP server to serve the WebLLM HTML file"""
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=os.getcwd(), **kwargs)
        
        def end_headers(self):
            # Add CORS headers to allow WebLLM to load
            self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            super().end_headers()
        
        def log_message(self, format, *args):
            # Suppress default logging
            pass
    
    # Find an available port
    for port_attempt in range(port, port + 100):
        try:
            with socketserver.TCPServer(("", port_attempt), Handler) as httpd:
                print(f"🌐 Starting local server on port {port_attempt}")
                print(f"📂 Serving files from: {os.getcwd()}")
                
                # Start server in a separate thread
                server_thread = threading.Thread(target=httpd.serve_forever)
                server_thread.daemon = True
                server_thread.start()
                
                return httpd, port_attempt
                
        except OSError:
            continue
    
    raise RuntimeError("Could not find an available port")

def main():
    """Main function to run WebLLM test"""
    
    print("🚀 WebLLM Qwen2.5-0.5B-Instruct Test Launcher")
    print("=" * 60)
    
    # Check if the HTML file exists
    html_file = Path("webllm_test.html")
    if not html_file.exists():
        print("❌ Error: webllm_test.html file not found!")
        print("Make sure you're running this script from the correct directory.")
        return False
    
    try:
        # Start local server
        httpd, port = start_local_server()
        
        # Construct URL
        url = f"http://localhost:{port}/webllm_test.html"
        
        print(f"🌍 WebLLM test page will open at: {url}")
        print("\n📋 Instructions:")
        print("1. The browser will open automatically")
        print("2. Wait for the model to load (this may take a few minutes)")
        print("3. Once loaded, you can interact with Qwen2.5-0.5B-Instruct")
        print("4. The model will automatically run an initial test")
        print("5. You can then type your own messages and press Enter or click Send")
        print("\n⚠️  Note: Keep this terminal window open while using WebLLM")
        print("❌ Press Ctrl+C to stop the server and close the application")
        
        # Open browser
        print(f"\n🔗 Opening browser...")
        webbrowser.open(url)
        
        print("✅ Browser launched! Check your browser for the WebLLM interface.")
        print("🔄 Server is running... (Press Ctrl+C to stop)")
        
        try:
            # Keep the server running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            httpd.shutdown()
            print("✅ Server stopped successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 WebLLM test completed successfully!")
    else:
        print("\n❌ WebLLM test failed!")
        exit(1)