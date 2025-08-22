IMAGE_NAME ?= annotator-ui
TAG ?= latest
CONTAINER_NAME ?= annotator-ui-container
PORT ?= 3000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(TAG) ./frontend

# Run the Docker container
run:
	docker run --rm --name $(CONTAINER_NAME) -p $(PORT):3000 $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Clean up Docker image and container
clean: stop
	docker rmi -f $(IMAGE_NAME):$(TAG) || true

# Rebuild and run the container
rebuild: clean build run