FROM centos:8

RUN dnf update -y && dnf upgrade -y && dnf clean packages
RUN dnf install -y python38 python38-libs python38-devel python38-pip make gcc wget openssh-clients openssh-server
RUN dnf install -y libvirt-client libvirt-devel libpq-devel

COPY . /opt/yamatsumi/backend
WORKDIR /opt/yamatsumi/backend

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
