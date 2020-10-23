FROM python:3

RUN mkdir /code
WORKDIR /code

COPY . /code
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
