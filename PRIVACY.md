# Privacy Policy

This plugin processes your text prompts to generate images using the ModelScope Qwen-Image AI model. Here's how your data is handled:

## Data Processing

- **Text Prompts**: Your text descriptions are sent to ModelScope's Qwen-Image API to generate corresponding images
- **API Communication**: The plugin communicates with ModelScope servers (https://api-inference.modelscope.cn) to process image generation requests
- **Generated Images**: Images are temporarily downloaded and processed by the plugin, then returned to your Dify workflow
- **Processing Mode**: Uses asynchronous task processing with polling to ensure reliable image generation

## Data Storage

- **No Local Storage**: The plugin does not permanently store your text prompts or generated images locally
- **Temporary Processing**: All data processing is temporary and happens only during the image generation process
- **API Key Security**: Your ModelScope API key is stored securely within your Dify environment and is not logged or transmitted elsewhere

## Third-Party Services

- **ModelScope API**: Your text prompts are sent to ModelScope's image generation service to create images
- **Network Communication**: The plugin requires internet connectivity to communicate with ModelScope's servers
- **Service Provider**: ModelScope (Alibaba DAMO Academy) processes your requests according to their privacy policy

## Data Retention

- The plugin does not retain any user data after task completion
- Generated images are temporarily processed and immediately returned to your workflow
- No persistent storage of prompts, images, or user information within the plugin
