import ollama
import time
from typing import Dict, Any, Tuple

def run_prompt(template: str, variables: Dict[str, Any], model: str, temperature: float) -> Tuple[str, float]:
    """Fill template + call Llama 3.1:8B via Ollama"""
    try:
        filled_prompt = template.format(**variables)
    except KeyError as e:
        raise ValueError(f"Missing variable in input: {e}")

    start = time.time()
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": filled_prompt}],
        options={"temperature": temperature}
    )
    latency = time.time() - start

    output = response["message"]["content"]
    return output, latency