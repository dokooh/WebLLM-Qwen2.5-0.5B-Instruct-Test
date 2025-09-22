import { CreateMLCEngine } from "@mlc-ai/web-llm";

async function testQwenWebLLM() {
    console.log("Initializing WebLLM for Qwen2.5-0.5B-Instruct...");
    
    try {
        // Available Qwen models in WebLLM
        const selectedModel = "Qwen2.5-0.5B-Instruct-q4f16_1-MLC";
        
        console.log(`Loading model: ${selectedModel}`);
        
        // Create the MLC engine
        const engine = await CreateMLCEngine(
            selectedModel,
            { 
                initProgressCallback: (report) => {
                    console.log(`Loading progress: ${report.text}`);
                }
            }
        );
        
        console.log("Model loaded successfully!");
        
        // Test the model with a simple prompt
        const testPrompt = "Hello! How are you today?";
        console.log(`\nSending prompt: "${testPrompt}"`);
        
        const messages = [
            {
                role: "user",
                content: testPrompt
            }
        ];
        
        console.log("Generating response...");
        const reply = await engine.chat.completions.create({
            messages: messages,
            max_tokens: 100,
            temperature: 0.7,
        });
        
        const response = reply.choices[0]?.message?.content || "No response generated";
        
        console.log(`\n✅ Model Response: ${response}`);
        console.log("\n🎉 WebLLM test completed successfully!");
        
        // Save results to a file that Python can read
        const results = {
            success: true,
            model: selectedModel,
            prompt: testPrompt,
            response: response,
            timestamp: new Date().toISOString()
        };
        
        // Write results to JSON file
        const fs = await import('fs');
        fs.writeFileSync('webllm_results.json', JSON.stringify(results, null, 2));
        console.log("Results saved to webllm_results.json");
        
    } catch (error) {
        console.error("❌ Error during WebLLM test:", error.message);
        
        // Save error info
        const errorResults = {
            success: false,
            error: error.message,
            timestamp: new Date().toISOString()
        };
        
        const fs = await import('fs');
        fs.writeFileSync('webllm_results.json', JSON.stringify(errorResults, null, 2));
        
        process.exit(1);
    }
}

// Run the test
testQwenWebLLM();