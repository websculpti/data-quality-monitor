FROM python:3.11-slim
# working directory inside the container
WORKDIR /app
COPY requirements.txt .
# installing dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# copying the project
COPY . .
# this project uses port 8000
EXPOSE 8000
# binding fastapi server 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
