# syntax=docker/dockerfile:1

FROM python:3.8
WORKDIR /app
RUN python -m pip install --upgrade pip wheel setuptools
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5005:5005
CMD ["flask", "run", "--host=0.0.0.0", "--port=5005" ]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD [ "python3", "-m" , "http.server"]