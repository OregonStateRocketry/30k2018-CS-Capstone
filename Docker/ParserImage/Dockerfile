FROM resin/rpi-rasbian:latest

#ENTRYPOINT []

RUN apt-get -q update 		\
	&& apt-get -qy install 	\
		curl 		\
		pip3		\
		python3		\
	&& rm -rf /var/lib/apt/lists/*

COPY ../../Database/ /home/pi/Capstone/Database/

WORKDIR /home/pi/Capstone/Database

RUN pip3 install -r requirements.txt

CMD ["python3", "parser.py"]
