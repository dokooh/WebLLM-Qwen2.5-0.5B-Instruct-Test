# 🤖 WebLLM Qwen2.5-0.5B-Instruct Test

A comprehensive setup for running **Qwen2.5-0.5B-Instruct** using both **WebLLM** (browser-based) and **Transformers** (Python-based) implementations with deterministic configuration.

## 🎯 Overview

This project demonstrates how to:
- ✅ Set up and run **Qwen2.5-0.5B-Instruct** using WebLLM in a web browser
- ✅ Run the same model using Python Transformers library
- ✅ Configure **deterministic responses** (temperature=0.0) for reproducible results
- ✅ Generate **extended responses** (300-400 tokens) for detailed outputs
- ✅ Compare performance between browser and Python implementations

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/dokooh/WebLLM-Qwen2.5-0.5B-Instruct-Test.git
cd WebLLM-Qwen2.5-0.5B-Instruct-Test
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv "Qwen2.5-0.5B-Instruct"

# Activate (Windows)
Qwen2.5-0.5B-Instruct\Scripts\activate

# Activate (Linux/Mac)
source Qwen2.5-0.5B-Instruct/bin/activate
```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install transformers torch psutil

# Install WebLLM (Node.js required)
npm install
```

### 4. Run WebLLM (Browser)

```bash
python launch_webllm.py
```

### 5. Run Python Version

```bash
python test_qwen_model.py
```

## 📁 Project Structure

```
├── 📄 README.md                          # This file
├── 🌐 webllm_standalone.html             # WebLLM browser interface
├── 🐍 launch_webllm.py                   # WebLLM launcher script
├── 🧪 test_qwen_model.py                 # Basic Transformers test
├── 🔬 test_deterministic_qwen.py         # Deterministic testing suite
├── 🛑 stop_webllm_helper.py              # WebLLM stop helper
├── 🛑 stop_webllm_simple.py              # Simple stop script
├── 🛑 stop_webllm.py                     # Advanced stop script
├── 📊 package.json                       # Node.js configuration
├── 📋 CONFIGURATION_SUMMARY.md           # Detailed settings
├── 📖 STOP_WEBLLM_README.md              # Stop scripts guide
└── 🗂️ node_modules/                      # WebLLM dependencies
```

## 🎮 Usage Examples

### WebLLM (Browser Interface)

```bash
# Launch WebLLM in browser
python launch_webllm.py

# Stop WebLLM (helper with instructions)
python stop_webllm_helper.py
```

**Features:**
- 🌐 Runs entirely in web browser
- ⚡ WebAssembly + WebGPU acceleration
- 💬 Interactive chat interface
- 📊 Real-time progress tracking
- 🎯 Automatic initial testing

### Python Transformers

```bash
# Basic test
python test_qwen_model.py

# Comprehensive deterministic testing
python test_deterministic_qwen.py
```

**Features:**
- 🐍 Native Python implementation
- 🔬 Deterministic behavior verification
- 📏 Extended response testing
- 🧪 Multiple prompt validation

## ⚙️ Configuration

### Deterministic Settings (Applied to Both)

```python
# WebLLM Configuration
{
    "temperature": 0.0,      # No randomness
    "max_tokens": 300,       # Extended responses
    "do_sample": False       # Deterministic
}

# Transformers Configuration  
{
    "temperature": 0.0,      # No randomness
    "max_new_tokens": 300,   # Extended responses
    "do_sample": False       # Deterministic
}
```

### Model Information

- **Model**: `Qwen/Qwen2.5-0.5B-Instruct`
- **WebLLM Format**: `Qwen2.5-0.5B-Instruct-q4f16_1-MLC`
- **Quantization**: 4-bit with FP16 (WebLLM)
- **Size**: ~500MB model weights

## 🧪 Testing & Validation

### Deterministic Testing

The project includes comprehensive testing to verify deterministic behavior:

```bash
python test_deterministic_qwen.py
```

**Test Results:**
- ✅ **4/4 prompts** produce identical responses across multiple runs
- ✅ **Temperature=0.0** ensures no randomness
- ✅ **Extended responses** work correctly (up to 400 tokens)
- ✅ **2174 characters** generated in extended test

### Sample Test Prompts

1. "Explain what artificial intelligence is in simple terms."
2. "Write a short poem about the ocean."
3. "What are the benefits of renewable energy?"
4. "Describe the process of photosynthesis."

## 🔧 Requirements

### System Requirements

- **Python**: 3.8+ (3.13 recommended)
- **Node.js**: 14+ (for WebLLM)
- **Browser**: Modern browser with WebAssembly support
- **Memory**: 4GB+ RAM recommended
- **Storage**: 2GB+ free space (for model cache)

### Python Dependencies

```txt
transformers>=4.56.0
torch>=2.8.0
psutil>=7.1.0
```

### Node.js Dependencies

```txt
@mlc-ai/web-llm>=0.2.79
```

## 🌟 Features

### WebLLM Advantages
- 🌐 **Browser-based**: No local installation required
- ⚡ **WebGPU acceleration**: Hardware-optimized inference
- 🔄 **Progressive loading**: Streams model weights
- 💾 **Browser caching**: Faster subsequent loads
- 🖥️ **Cross-platform**: Works on any modern browser

### Transformers Advantages  
- 🐍 **Native Python**: Full ecosystem integration
- 🔬 **Research-friendly**: Easy to modify and experiment
- 📊 **Detailed control**: Fine-grained parameter tuning
- 🧪 **Testing suite**: Comprehensive validation tools
- 🎯 **Reproducible**: Deterministic results guaranteed

## 📊 Performance Comparison

| Implementation | Load Time | Response Time | Memory Usage | Portability |
|---------------|-----------|---------------|--------------|-------------|
| **WebLLM**    | 2-5 min*  | 1-3 sec      | Browser-managed | High |
| **Transformers** | 30-60 sec | 2-5 sec    | ~2GB RAM | Medium |

*First load only (cached afterward)

## 🛠️ Troubleshooting

### WebLLM Issues

```bash
# Check WebLLM status
python stop_webllm_helper.py

# Relaunch WebLLM
python launch_webllm.py

# Clear browser cache if needed (Ctrl+Shift+Del)
```

### Python Issues

```bash
# Check Python environment
python --version

# Reinstall dependencies
pip install --upgrade transformers torch

# Test basic functionality
python test_qwen_model.py
```

### Common Solutions

| Issue | Solution |
|-------|----------|
| Browser won't load WebLLM | Check internet connection, try different browser |
| Python model fails to load | Ensure sufficient RAM (4GB+), check internet |
| Inconsistent responses | Verify temperature=0.0 in configuration |
| Slow performance | Close other applications, restart browser |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Alibaba Cloud**: For the Qwen2.5 model series
- **MLC-AI**: For the WebLLM framework
- **Hugging Face**: For the Transformers library
- **Community**: For testing and feedback

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/dokooh/WebLLM-Qwen2.5-0.5B-Instruct-Test/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/dokooh/WebLLM-Qwen2.5-0.5B-Instruct-Test/discussions)
- 📖 **Documentation**: See project files and comments

## 🎯 Quick Commands Reference

```bash
# Setup
python -m venv "Qwen2.5-0.5B-Instruct"
pip install transformers torch psutil
npm install

# Run WebLLM
python launch_webllm.py

# Run Python version
python test_qwen_model.py

# Test deterministic behavior
python test_deterministic_qwen.py

# Stop WebLLM
python stop_webllm_helper.py

# Check configuration
cat CONFIGURATION_SUMMARY.md
```

---

**🎉 Ready to explore Qwen2.5-0.5B-Instruct with WebLLM!**

Start with `python launch_webllm.py` and enjoy the browser-based AI experience, or use `python test_qwen_model.py` for the Python implementation.

Both are configured for deterministic, reproducible results perfect for testing and development! 🚀