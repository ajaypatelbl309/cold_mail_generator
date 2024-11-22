FROM python:3.13
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]