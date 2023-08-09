# Personal Data Detection API

This repository contains an API for detecting personal data in images using deep learning. It also includes a web interface for visualization and utilizing the API functionality.

## Repository Structure

The repository is organized as follows:

- `app.py`: Main file containing the API for personal data detection in images.
- `templates/`: Folder containing the `index.html` file used for the web interface.
- `requirements.txt`: File specifying the dependencies required to run the application.
- `Dockerfile`: File for building the Docker image of the application.
- `aks/`: Folder containing configuration files for deploying the application to Azure Kubernetes Service (AKS).
  - `deployment.yaml`: Configuration file for deploying the service in AKS.
  - `service.yaml`: Configuration file for exposing the service in AKS.

## Usage Instructions

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-user/repository-name.git
   cd repository-name
   ```

   Remember to replace `"your-user"` and `"repository-name"` with your actual GitHub username and repository name. You can also customize the instructions and descriptions as needed.
   
2. Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API and web interface:
   ```bash
   python app.py
   ```

   This will start the API at http://localhost:5000, and you can access the web interface in your browser.
   
5. (Optional) If you want to run the application in a Docker container:
   ```bash
   docker build -t anonymization .
   docker run -p 5000:5000 anonymization
   ```
6. (Optional) AKS Deployment:
   - Ensure you have an AKS instance set up and the docker image is in your ACR.
   - Apply the configuration in the `aks/` folder using `kubectl`:
     ```bash
     kubectl apply -f aks/deployment.yaml
     kubectl apply -f aks/service.yaml
     ```

## Contributions

Contributions are welcome. If you find any bugs or have suggestions for improvement, feel free to open an issue or submit a pull request.
