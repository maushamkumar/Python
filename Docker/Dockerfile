# Base Image 
FROM python:3.9

# Work directory 
WORKDIR /app

# Copy 
COPY . /app

# run 
RUN pip install -r requirements.txt

# port 
EXPOSE 5000

# command 
CMD ["python", "./app.py"]