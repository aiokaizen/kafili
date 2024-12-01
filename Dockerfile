FROM python:3.10.15

WORKDIR /opt/kafili

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py kafili_setup

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

