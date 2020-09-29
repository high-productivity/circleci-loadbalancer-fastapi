FROM tonydeveloper/python3.7-fastapi:latest

LABEL maintainer="Tony Developer <tonydev031987@gmail.com>"

EXPOSE 8001

# Add demo app
RUN rm /home/*
COPY ./prebuild /home
WORKDIR /home
CMD ["/home/app/start.sh"]
