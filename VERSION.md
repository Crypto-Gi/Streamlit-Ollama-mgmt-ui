# Streamlit Ollama UI - Version 2.0.0

**Release Date:** March 13, 2025

## Key Features

- Elegant, Apple-inspired dark mode Streamlit dashboard
- Real-time API integration with Ollama server
- Connection management with status indicators
- Model management operations:
  - Load models into VRAM with customizable keep-alive duration
  - Unload models from VRAM
  - Delete models with confirmation
- Model interaction through chat interface
- Server status monitoring

## Components

- Overview page with model summary
- Model Management with streamlined operation interface
- Model Interaction for chat with models
- Server Status with real-time metrics

## Dependencies

Listed in `requirements.txt`:
- streamlit
- requests
- pandas
- plotly

## Contributors

- Project initiated by User
- Development assistance by Cascade AI

## Version History

## Version 2.0.0 (2025-03-13)

### New Features
- **Enhanced Running Models Display**:
  - Added unload buttons directly on the main dashboard for each running model
  - Updated time remaining display to HH:MM:SS format
  - Auto-refresh every 5 seconds for live monitoring

- **Improved Model Management**:
  - Added "4 hours" option for model keep-alive duration
  - Added custom minutes input option for precise control over model expiration
  - Better error handling and success messages

## Version 1.0.0 (2025-03-13)

### Initial Release Features
- Elegant, Apple-inspired dark mode Streamlit dashboard
- Real-time API integration with Ollama server
- Connection management with status indicators
- Model management operations:
  - Load models into VRAM with customizable keep-alive duration
  - Unload models from VRAM
  - Delete models with confirmation
- Model interaction through chat interface
- Server status monitoring

## Future Enhancements (Planned)

- Enhanced visualization options
- Batch model operations
- Additional API features integration
- Performance metrics tracking
