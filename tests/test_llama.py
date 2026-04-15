import asyncio
import httpx
import json

async def test_llama_integration():
    """Test the complete Llama 3.1 integration"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # 1. Create a prompt
        print("1. Creating prompt...")
        response = await client.post(
            f"{base_url}/prompts/",
            json={"name": "llama_test", "description": "Testing Llama 3.1"}
        )
        prompt = response.json()
        print(f"   Created prompt with ID: {prompt['id']}")
        
        # 2. Create a version with Llama-optimized template
        print("2. Creating version...")
        response = await client.post(
            f"{base_url}/prompts/{prompt['id']}/versions",
            json={
                "template": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nAnswer this question concisely: {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                "variables": ["question"],
                "model": "llama3.1:8b",
                "temperature": 0.7
            }
        )
        version = response.json()
        print(f"   Created version {version['version_number']} with ID: {version['id']}")
        
        # 3. Execute the prompt
        print("3. Executing prompt with Llama 3.1...")
        response = await client.post(
            f"{base_url}/executions/execute",
            json={
                "version_id": version['id'],
                "input_variables": {"question": "What is the capital of France?"}
            }
        )
        execution = response.json()
        print(f"   Execution status: {execution['status']}")
        print(f"   Output: {execution.get('output', 'No output')}")
        print(f"   Latency: {execution.get('latency_ms', 'N/A')}ms")
        
        # 4. Evaluate with Llama as judge
        if execution['status'] == 'success':
            print("4. Evaluating with Llama as judge...")
            response = await client.post(
                f"{base_url}/executions/{execution['id']}/evaluate/llm",
                params={"criteria": "accuracy and helpfulness"}
            )
            evaluation = response.json()
            print(f"   LLM Judge Score: {evaluation.get('score')}")
            print(f"   Feedback: {evaluation.get('feedback')}")
        
        print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_llama_integration())