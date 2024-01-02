# Python base image
FROM python:3.10

LABEL maintainer="Lewis Munyi"

LABEL environment="production"

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1

# Set the working directory inside the container
WORKDIR /api

# Copy the application code to the working directory
COPY . .

# Uncomment the following lines if you are using Pip not poetry
# Install the Python dependencies
#RUN pip install -r requirements.txt

# Install poetry & packages
RUN curl -sSL https://install.python-poetry.org | python3 -

# Update path for poetry
ENV PATH="${PATH}:/root/.local/bin"

# https://python-poetry.org/docs/configuration/#virtualenvscreate
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction

# Create app database
RUN touch avatars_as_a_service/database/aaas.sqlite.db

# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]