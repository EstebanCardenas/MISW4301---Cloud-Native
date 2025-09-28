FROM python:3.13-slim AS base
# Set labels
LABEL course="dann" \
      author="gd.martinez@uniandes.edu.co"
WORKDIR /app
ARG POETRY_VERSION=2.1.1
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml ./
COPY src/ src/
# Install all the dependencies directly on the container
RUN poetry config virtualenvs.create false
# Install no dev dependencies
RUN poetry install --only main

# Image for lambda
# Lambda images uses least-privileged users
FROM public.ecr.aws/lambda/python:3.12 AS runner
WORKDIR /app
# Copy only the necessary files from base
COPY --from=base /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
# Copy application code
COPY --from=base /app/src/ /app/src/
# Set environment
# This could lead into importing issues. TODO re-evaluate how to move libraries from previous stage.
ENV PYTHONPATH="/app/src:/usr/local/lib/python3.13/site-packages"
ENV PYTHONUNBUFFERED=1
# Run the application
CMD [ "entrypoints.queue.main.handler" ]