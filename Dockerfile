# Use the official Ubuntu 20.04 image as the base
FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt requirements.txt
RUN pip3 install --default-timeout=100 -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set the default command to run when the container starts
CMD [ "handler.handler" ]
