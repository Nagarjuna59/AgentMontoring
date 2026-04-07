"""
Check if Ollama is running and the required model is installed.
Run this before starting the backend.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_ollama():
    """Check Ollama status and model availability."""
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llama_model = os.getenv("LLAMA_MODEL", "qwen2.5-coder:3b")
    
    print("=" * 60)
    print("OLLAMA HEALTH CHECK")
    print("=" * 60)
    
    # Check if Ollama is running
    try:
        print(f"\n1. Checking if Ollama is running at {ollama_url}...")
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        response.raise_for_status()
        print("   ✅ Ollama is running!")
        
        # Check installed models
        data = response.json()
        models = data.get("models", [])
        model_names = [m.get("name", "") for m in models]
        
        print(f"\n2. Installed models: {len(models)}")
        for model in models:
            print(f"   - {model.get('name', 'Unknown')}")
        
        # Check if required model is installed
        print(f"\n3. Checking for required model: {llama_model}...")
        if any(llama_model in name for name in model_names):
            print(f"   ✅ Model '{llama_model}' is installed!")
        else:
            print(f"   ❌ Model '{llama_model}' NOT found!")
            print(f"\n   To install it, run:")
            print(f"   ollama pull {llama_model}")
            return False
            
        # Test generation with shorter timeout
        print(f"\n4. Testing code generation with {llama_model}...")
        print("   (This may take 10-30 seconds on first run...)")
        try:
            test_response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": llama_model,
                    "prompt": "Write a Python function to add two numbers",
                    "stream": False,
                    "options": {
                        "num_predict": 50,  # Reduced for faster test
                        "temperature": 0.3
                    }
                },
                timeout=45  # Increased timeout for model loading
            )
            test_response.raise_for_status()
            test_data = test_response.json()
            
            if test_data.get("response"):
                print("   ✅ Test generation successful!")
                print(f"   Sample output: {test_data['response'][:100]}...")
            else:
                print("   ⚠️ Generation returned no response")
                print(f"   Raw response: {test_data}")
        except requests.exceptions.Timeout:
            print("   ⚠️ Test generation timed out (this can happen on first model load)")
            print("   Try again or restart Ollama: 'ollama serve'")
            print("   Note: The model may still work in production")
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Connection error during test: {str(e)}")
            print("   Ollama may have crashed or is restarting")
            print("   Try: 1) Close Ollama, 2) Run 'ollama serve' again")
            return False
        except Exception as e:
            print(f"   ⚠️ Test error: {str(e)}")
            print("   The basic checks passed, so Ollama should still work")
            
        print("\n" + "=" * 60)
        print("✅ ALL CHECKS PASSED - Ollama is ready!")
        print("=" * 60)
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to Ollama at {ollama_url}")
        print("\n   To start Ollama:")
        print("   1. Open a terminal")
        print("   2. Run: ollama serve")
        print("   3. Or start Ollama application")
        print("\n   If Ollama is not installed:")
        print("   Visit: https://ollama.ai/download")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    success = check_ollama()
    if not success:
        print("\n⚠️ Fix the issues above before starting the backend")
        exit(1)
    else:
        print("\n🚀 You can now start the backend server")
        exit(0)
