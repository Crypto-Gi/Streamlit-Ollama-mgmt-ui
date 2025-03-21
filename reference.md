
# Ollama API Reference

This document outlines the key Ollama API endpoints needed for model management.

## Core Endpoints

### 📋 View detailed model information
- **Endpoint**: `GET /api/show`
- **Parameters**: 
  ```json
  {
    "name": "model_name:tag"
  }
 ```
```

- Description : Returns detailed information about a specific model including parameters, template format, and system information.
### 🚀 List running models
- Endpoint : GET /api/tags
- Parameters : None required
- Description : Returns a list of all available models with their metadata.
### 🗑️ Delete models
- Endpoint : DELETE /api/delete
- Parameters :
  ```json
  {
    "name": "model_name:tag"
  }
   ```
- Description : Removes a model from your local storage.
### ⬇️ Pull models from Ollama library
- Endpoint : POST /api/pull
- Parameters :
  ```json
  {
    "name": "model_name:tag",
    "stream": true  // Optional: for streaming progress updates
  }
   ```
  ```
- Description : Downloads a model from the Ollama library to your local machine.
### 🔄 Get Ollama version
- Endpoint : GET /api/version
- Parameters : None required
- Description : Returns information about the Ollama server version.
### 💾 Load models into VRAM with customizable keep-alive timer
- Endpoint : POST /api/generate
- Parameters :
  ```json
  {
    "model": "model_name:tag",
    "prompt": "",  // Empty prompt just to load the model
    "keep_alive": "5m"  // Customizable timer (e.g., "5m" for 5 minutes)
  }
   ```
  ```
- Description : Loads the model into VRAM and keeps it there for the specified duration.
### 🛑 Force remove models from VRAM
- Endpoint : POST /api/generate
- Parameters :
  ```json
  {
    "model": "model_name:tag",
    "prompt": "",
    "keep_alive": "0"  // Setting to "0" forces immediate unloading
  }
   ```
  ```
- Description : Forces the model to be unloaded from VRAM immediately