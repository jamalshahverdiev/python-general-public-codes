FROM python:3.8-alpine
RUN adduser -u 1001 -S appuser
WORKDIR /app
ADD ./templates /app/templates/
ADD ./src /app/src/
COPY ["requirements.txt", "pipedrive_api.py", "./"]
RUN pip install -r requirements.txt && chown -R appuser /app
USER appuser
EXPOSE 8080
CMD ["python", "/app/pipedrive_api.py"]