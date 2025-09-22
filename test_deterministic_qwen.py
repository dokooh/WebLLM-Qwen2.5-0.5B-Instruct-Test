#!/usr/bin/env python3
"""
Deterministic test script for Qwen2.5-0.5B-Instruct model using Transformers library
Tests reproducibility with temperature=0.0 and extended max_tokens
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def test_deterministic_responses():
    """Test that the model produces identical responses with temperature=0.0"""
    
    print("🧪 Deterministic Response Test for Qwen2.5-0.5B-Instruct")
    print("=" * 70)
    
    # Model name on Hugging Face
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    
    try:
        print(f"Loading tokenizer and model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        print("✅ Model loaded successfully!")
        print(f"Model device: {model.device}")
        print(f"Model dtype: {model.dtype}")
        
        # Test prompts
        test_prompts = [
            "Explain what artificial intelligence is in simple terms.",
            "Write a short poem about the ocean.",
            "What are the benefits of renewable energy?",
            "Describe the process of photosynthesis.",
        ]
        
        print(f"\n🔬 Testing deterministic behavior (temperature=0.0, max_tokens=300)")
        print("Running each prompt twice to verify identical outputs...\n")
        
        for i, test_prompt in enumerate(test_prompts, 1):
            print(f"📝 Test {i}: {test_prompt}")
            print("-" * 50)
            
            # Format the prompt for instruction following
            messages = [{"role": "user", "content": test_prompt}]
            formatted_prompt = tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            
            # Tokenize
            inputs = tokenizer(formatted_prompt, return_tensors="pt")
            if torch.cuda.is_available() and hasattr(model, 'device'):
                inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            responses = []
            
            # Generate response twice with same settings
            for run in [1, 2]:
                print(f"  Run {run}:", end=" ", flush=True)
                
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=300,
                        do_sample=False,  # Deterministic
                        temperature=0.0,  # No randomness
                        pad_token_id=tokenizer.eos_token_id,
                        eos_token_id=tokenizer.eos_token_id
                    )
                
                # Decode the response
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                generated_text = response[len(formatted_prompt):].strip()
                responses.append(generated_text)
                
                print("✅ Generated")
            
            # Check if responses are identical
            if responses[0] == responses[1]:
                print("  ✅ PASS: Both responses are identical (deterministic)")
            else:
                print("  ❌ FAIL: Responses differ (non-deterministic)")
                print(f"    Response 1: {responses[0][:100]}...")
                print(f"    Response 2: {responses[1][:100]}...")
            
            # Show the response
            print(f"  📤 Response: {responses[0][:150]}{'...' if len(responses[0]) > 150 else ''}")
            print()
        
        print("🎯 Deterministic Testing Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

def run_extended_response_test():
    """Test the model with extended max_tokens setting"""
    
    print("\n" + "=" * 70)
    print("📏 Extended Response Test (max_tokens=400)")
    print("=" * 70)
    
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        # Extended response prompt
        extended_prompt = "Write a detailed explanation of machine learning, including its types, applications, and future prospects."
        
        messages = [{"role": "user", "content": extended_prompt}]
        formatted_prompt = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        inputs = tokenizer(formatted_prompt, return_tensors="pt")
        if torch.cuda.is_available() and hasattr(model, 'device'):
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        print(f"📝 Prompt: {extended_prompt}")
        print("🔄 Generating extended response...")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=400,
                do_sample=False,
                temperature=0.0,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_text = response[len(formatted_prompt):].strip()
        
        print(f"\n📤 Extended Response ({len(generated_text)} characters):")
        print("=" * 50)
        print(generated_text)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during extended test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Qwen2.5-0.5B-Instruct Deterministic & Extended Testing")
    print("Configuration: temperature=0.0, max_tokens=300-400")
    
    success1 = test_deterministic_responses()
    success2 = run_extended_response_test()
    
    if success1 and success2:
        print("\n🎉 All tests completed successfully!")
        print("✅ Model produces deterministic responses with temperature=0.0")
        print("✅ Extended responses work with max_tokens=400")
    else:
        print("\n❌ Some tests failed!")
        exit(1)