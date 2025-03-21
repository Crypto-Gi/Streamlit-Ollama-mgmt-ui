import requests
import json
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple, Union


class OllamaAPI:
    """Handler for Ollama REST API interactions"""
    
    def __init__(self, base_url: str):
        """Initialize the API handler with the base URL"""
        self.base_url = base_url
        
    def test_connection(self) -> Tuple[bool, Dict]:
        """Test connection to the Ollama server by fetching version info"""
        try:
            response = self.get_version()
            if "error" in response:
                return False, response
            return True, response
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_version(self) -> Dict:
        """Get Ollama server version information"""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching version: {str(e)}")
            return {"error": str(e)}
    
    def list_models(self) -> List[Dict]:
        """List all available models on the Ollama server"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            st.error(f"Error listing models: {str(e)}")
            return []
    
    def get_model_details(self, model_name: str) -> Dict:
        """Get detailed information about a specific model"""
        try:
            payload = {"name": model_name}
            response = requests.post(f"{self.base_url}/api/show", json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching model details: {str(e)}")
            return {"error": str(e)}
    
    def pull_model(self, model_name: str, stream: bool = True) -> Union[Dict, requests.Response]:
        """Pull a model from the Ollama library"""
        try:
            payload = {"name": model_name}
            
            if stream:
                # Return the raw response object for streaming progress
                return requests.post(f"{self.base_url}/api/pull", 
                                    json=payload, 
                                    stream=True,
                                    timeout=None)
            else:
                # For non-streaming, just return the final result
                response = requests.post(f"{self.base_url}/api/pull", json=payload, timeout=None)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error pulling model: {str(e)}")
            return {"error": str(e)}
    
    def delete_model(self, model_name: str) -> Dict:
        """Delete a model from local storage"""
        try:
            payload = {"name": model_name}
            response = requests.delete(f"{self.base_url}/api/delete", json=payload, timeout=10)
            response.raise_for_status()
            return {"status": "success", "message": f"Model {model_name} deleted successfully"}
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting model: {str(e)}")
            return {"error": str(e)}
    
    def load_model_into_vram(self, model_name: str, keep_alive: str = "5m") -> Dict:
        """Load a model into VRAM with customizable keep-alive timer"""
        try:
            payload = {"model": model_name, "prompt": "", "keep_alive": keep_alive}
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=30)
            
            # First check if there was an HTTP error
            if response.status_code != 200:
                # Try to extract the actual error message from the response body
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", str(response.reason))
                    return {"error": error_message}
                except:
                    # If we can't parse the JSON, fall back to HTTP error
                    return {"error": f"{response.status_code} {response.reason}"}
            
            # If response was successful
            response.raise_for_status()
            return {"status": "success", "message": f"Model {model_name} loaded with keep-alive {keep_alive}"}
        except requests.exceptions.RequestException as e:
            # Extract the actual error message from the exception if possible
            error_msg = str(e)
            if hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    pass
            
            st.error(f"Error loading model: {error_msg}")
            return {"error": error_msg}
    
    def remove_model_from_vram(self, model_name: str) -> Dict:
        """Force remove a model from VRAM by setting keep-alive to 0"""
        return self.load_model_into_vram(model_name, keep_alive="0")
    
    def get_running_models(self) -> List[Dict]:
        """Get list of currently running models and their resource usage"""
        try:
            response = requests.get(f"{self.base_url}/api/ps", timeout=5)
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching running models: {str(e)}")
            return []
    
    def generate_response(self, model_name: str, prompt: str, 
                         temperature: float = 0.7, stream: bool = False,
                         context_length: int = 4096,
                         chat_history: List[Dict] = None) -> Union[Dict, requests.Response]:
        """Generate a response from the specified model"""
        try:
            # Construct options with context length
            options = {
                "num_ctx": context_length
            }
            
            # Base payload
            payload = {
                "model": model_name,
                "temperature": temperature,
                "stream": stream,
                "options": options
            }
            
            # Format prompt with chat history if provided
            if chat_history and len(chat_history) > 0:
                # Format chat history in a conversational format
                formatted_history = ""
                for msg in chat_history:
                    role = msg.get("role", "").lower().strip()
                    content = msg.get("content", "").strip()
                    
                    if role == "user":
                        formatted_history += f"\n\nHuman: {content}"
                    elif role == "assistant":
                        formatted_history += f"\n\nAssistant: {content}"
                
                # Add the current prompt
                formatted_history += f"\n\nHuman: {prompt}\n\nAssistant:"
                payload["prompt"] = formatted_history
            else:
                # Just use the prompt as is
                payload["prompt"] = prompt
            
            if stream:
                # Return the raw response object for streaming
                return requests.post(f"{self.base_url}/api/generate", 
                                    json=payload, 
                                    stream=True,
                                    timeout=None)
            else:
                # Process and return the complete response
                response = requests.post(f"{self.base_url}/api/generate", 
                                        json=payload, 
                                        timeout=None)
                
                # Check if there was an HTTP error
                if response.status_code != 200:
                    # Try to extract the actual error message from the response body
                    try:
                        error_data = response.json()
                        error_message = error_data.get("error", str(response.reason))
                        return {"error": error_message}
                    except:
                        # If we can't parse the JSON, fall back to HTTP error
                        return {"error": f"{response.status_code} {response.reason}"}
                
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.RequestException as e:
            # Extract the actual error message from the exception if possible
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    pass
            
            st.error(f"Error generating response: {error_msg}")
            return {"error": error_msg}
    
    def chat_with_model(self, model_name: str, messages: List[Dict], 
                       temperature: float = 0.7, stream: bool = False) -> Union[Dict, requests.Response]:
        """Chat with a model using the chat API endpoint"""
        try:
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "stream": stream
            }
            
            if stream:
                # Return the raw response object for streaming
                return requests.post(f"{self.base_url}/api/chat", 
                                    json=payload, 
                                    stream=True,
                                    timeout=None)
            else:
                # Process and return the complete response
                response = requests.post(f"{self.base_url}/api/chat", 
                                        json=payload, 
                                        timeout=None)
                
                # Check if there was an HTTP error
                if response.status_code != 200:
                    # Try to extract the actual error message from the response body
                    try:
                        error_data = response.json()
                        error_message = error_data.get("error", str(response.reason))
                        return {"error": error_message}
                    except:
                        # If we can't parse the JSON, fall back to HTTP error
                        return {"error": f"{response.status_code} {response.reason}"}
                
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.RequestException as e:
            # Extract the actual error message from the exception if possible
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    pass
            
            st.error(f"Error in chat: {error_msg}")
            return {"error": error_msg}
