FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-full \
    python3-pip

# Set the working directory
WORKDIR /

# Copy the current directory contents into the container at /
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt  --break-system-packages

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches

CMD ["python3", "main.py", "--data-path", "output.parquet"]
