FROM python:3.7-slim

RUN python3 --version

RUN pip3 --version

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "search.py" ] 