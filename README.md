# emotion-docker

## Prerequisites

Make sure you have the following installed:

- Python 3.10
- Pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/benedictchuajj/emotion-docker.git
   ```

2. Change into the project directory:

   ```bash
   cd emotion-docker
   ```

3. Download the zipped folder containing the emotion and sentiment models from [Teams](https://nusu.sharepoint.com/:u:/r/teams/2023SummerInternshipNLPChatbot-Benedict/Shared%20Documents/General/emotion_docker_models.zip?csf=1&web=1&e=isoShh), and unzip it in this directory

## Usage (Local)

1. Build the docker image:

   ```bash
   docker build -t emotion .
   ```
   Note: If you are rebuilding the images several times, make sure to delete the older images as each image is around 8GB <br/><br/>

2. Run the image in a container:
    ```bash
   docker run -p 9000:8080 emotion
   ```
   This runs the docker image locally as a container on local port 9000, where 8080 is the container port. <br/><br/>

3. Open a separate terminal and invoke the main function of the container:
    ```bash
    curl --request POST \           
    --url http://localhost:9000/2015-03-31/functions/function/invocations \
    --header 'Content-Type: application/json' \
    --data '{"sentence": "nice to meet you, my name is bob :)"}'
     ```

    You should receive an output similar to the following
    ```bash
    {"statusCode": 200, 
    "sentiment_score": 0.7384703792631626, 
    "emotion": "joy", 
    "top5_emotions": [
        {"name": "joy", "value": 0.5143717527389526}, 
        {"name": "others", "value": 0.169914111495018}, 
        {"name": "anger", "value": 0.1594364047050476}, 
        {"name": "sadness", "value": 0.15627767145633698}
    ]}
    ```


## Usage (AWS Lambda)

Follow the instructions in [AWS docs](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-lambda-functions-with-container-images.html) to upload the docker image in Amazon ECR which can then be created into a Lambda function.
