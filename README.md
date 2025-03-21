# Gemma3 Ollama Tools

This repository provides the necessary `Modelfile` and instructions for enabling native Ollama tool support with Gemma models. Ollama's native tool support allows language models like Gemma to interact with external functions and APIs directly.

## Supported Gemma Model Sizes & Performance
- **Gemma3 1B**: Unable to effectively reason and utilize tool calls.
- **Gemma3 4B**: Struggles with reasoning between tools, suboptimal results.
- **Gemma3 12B and Gemma3 27B**: Excellent reasoning capabilities with native tool use, similar to popular models like Qwen and Mistral.

## Quick Start Guide

Follow these steps to enable tool support in Gemma3 models:

### Step 1: Clone this repository

```bash
git clone https://github.com/IllFil/gemma3-ollama-tools.git
cd gemma3-ollama-tools
```

### Step 2: Create your Custom Gemma3 Model in Ollama

Ensure you have Ollama installed. Then run:

```bash
ollama create gemma3-12b-tools -f ./Modelfile
```

This command builds a custom Gemma model (`gemma3-12b-tools`) with native Ollama tool support integrated.

Replace `gemma3-12b-tools` with your desired model name. The provided `Modelfile` is ready-to-use and already configured for enabling tools.

### Step 3: Run your Custom Model

Start interacting with your custom Gemma model with Ollama:

```bash
ollama run gemma3-12b-tools
```

You can now test your model's capabilities directly within Ollama.

## Example: Gemma Using Tools

Below is a practical example showing how Gemma3-12B utilizes tool calling capabilities:

**User Prompt:**
```json
{
  "role": "user",
  "content": "Find me some information about current AI trends"
}
```

**Gemma3-12B-tools Response (Tool Invocation):**
```json
{
  "role": "assistant",
  "content": "",
  "tool_calls": [
    {
      "function": {
        "name": "get_web_results",
        "arguments": {
          "queries": [
            "current AI trends 2024",
            "latest AI developments",
            "emerging AI technologies"
          ],
          "user_input": "Find me some information about current AI trends"
        }
      }
    }
  ]
}
```

Gemma seamlessly identifies the need for external information and correctly invokes Ollama's native tools.

## Notes

- Gemma3-1B is not recommended for tasks involving complex tool reasoning.
- Gemma3-4B may exhibit inconsistent behavior when using tools.
- For consistent and optimal performance, prefer using Gemma3-12B or Gemma3-27B variants.
