FROM fedora:29

RUN dnf -y update && \ 
    dnf -y install git \
                   hostname \
                   net-tools \
                   procps-ng \
                   python2-websockify \
                   python3-websockify \
                   which \
    && dnf clean all
RUN git clone https://github.com/novnc/novnc
RUN ln -sf /novnc/vnc.html /novnc/index.html
ENTRYPOINT /novnc/utils/launch.sh --vnc vnc-desktop:5901
