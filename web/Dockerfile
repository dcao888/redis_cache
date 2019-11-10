FROM python:3.7-slim-stretch

# set timezone to New York
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# run container as executable cmd 
ENTRYPOINT ["python"] 

# default arg passed to cmd
CMD ["app.py"]
