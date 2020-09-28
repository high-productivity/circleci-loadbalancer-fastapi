FROM tonydeveloper/python3.7-fastapi:latest

LABEL maintainer="Tony Developer <ngocquang19877@gmail.com>"

EXPOSE 8001

# Add demo app
COPY ./prebuild /home
WORKDIR /home
CMD ["/start.sh"]
