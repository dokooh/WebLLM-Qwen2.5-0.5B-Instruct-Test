#!/usr/bin/env python3
"""
Test script for Qwen2.5-0.5B-Instruct model using Transformers library
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def download_and_test_qwen_model():
    """Download and test the Qwen2.5-0.5B-Instruct model"""
    
    print("Starting Qwen2.5-0.5B-Instruct model download and test...")
    print("-" * 60)
    
    # Model name on Hugging Face
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    
    try:
        print(f"Loading tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        print(f"Loading model {model_name}...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        print("Model and tokenizer loaded successfully!")
        print(f"Model device: {model.device}")
        print(f"Model dtype: {model.dtype}")
        
        # Test the model with a simple prompt
        print("\nTesting the model with a simple prompt...")
        test_prompt = "Hello! How are you today?"
        
        # Format the prompt for instruction following
        messages = [
            {"role": "user", "content": test_prompt}
        ]
        
        # Apply chat template
        formatted_prompt = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        print(f"Input prompt: {test_prompt}")
        print(f"Formatted prompt: {formatted_prompt}")
        
        # Tokenize and generate
        inputs = tokenizer(formatted_prompt, return_tensors="pt")
        
        # Move inputs to same device as model
        if torch.cuda.is_available() and hasattr(model, 'device'):
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        print("\nGenerating response...")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=False,
                temperature=0.0,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (remove the input prompt)
        generated_text = response[len(formatted_prompt):].strip()
        
        print(f"\nModel response: {generated_text}")
        print("\n" + "="*60)
        print("✅ Qwen2.5-0.5B-Instruct model test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during model loading or testing: {str(e)}")
        return False

def check_system_info():
    """Display system information"""
    print("System Information:")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device count: {torch.cuda.device_count()}")
        print(f"Current CUDA device: {torch.cuda.current_device()}")
        print(f"CUDA device name: {torch.cuda.get_device_name()}")
    print("-" * 60)

if __name__ == "__main__":
    print("Qwen2.5-0.5B-Instruct Model Test")
    print("=" * 60)
    
    check_system_info()
    success = download_and_test_qwen_model()
    
    if success:
        print("\n🎉 All tests passed! The Qwen2.5-0.5B-Instruct model is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")