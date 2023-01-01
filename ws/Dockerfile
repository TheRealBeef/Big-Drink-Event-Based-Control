# Build a docker image with `docker build -t osrf/ros:melodic-rpe .`
# 
FROM osrf/ros:melodic-desktop-full

RUN mkdir -p /home/ws/src
RUN echo "source /opt/ros/melodic/setup.bash" >> /root/.bashrc
WORKDIR /home/ws

USER root
  RUN useradd -m developer && \
    echo "developer:123" | chpasswd && \
    adduser developer sudo

USER developer
  RUN mkdir -p /home/developer/ws/src
  RUN echo "source /opt/ros/melodic/setup.bash" >> /home/developer/.bashrc
  WORKDIR /home/developer/ws
  RUN /bin/bash -c \
    '. /opt/ros/melodic/setup.bash; \
    cd /home/developer/ws; \
    catkin_make'
  RUN echo "source /home/developer/ws/devel/setup.bash" >> /home/developer/.bashrc

ENTRYPOINT ["/bin/bash", "-c"]
