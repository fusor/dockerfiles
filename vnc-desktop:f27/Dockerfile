FROM fedora:27

#Update
RUN dnf -y update && dnf clean all

#Install VNC
RUN dnf -y install tigervnc-server && dnf clean all

#Install Fonts and other useful X packages
RUN dnf -y install levien-inconsolata-fonts \
                   xorg-x11-fonts-100dpi \ 
                   xorg-x11-fonts-ISO8859-1-100dpi \
                   xorg-x11-fonts-Type1 \
                   && dnf clean all

#Install basic window managers
RUN dnf -y install fvwm \
                   i3 \
                   twm \
                   && dnf clean all

#Install Xfce
RUN dnf -y groupinstall "Cinnamon Desktop" \
                        "KDE" \
                        "KDE Plasma Workspaces" \
                        "LXDE Desktop" \
                        "LXQt Desktop" \
                        "MATE Desktop" \
                        "Sugar Desktop Environment" \
                        "Xfce Desktop"

#Install useful tools
RUN dnf -y install bind-utils \
                   firefox \
                   hexchat \
                   net-tools \
                   terminator \
                   thunderbird \
                   pidgin \
                   && dnf clean all

COPY vnc.sh /usr/local/bin
RUN chmod +x /usr/local/bin/vnc.sh
ENTRYPOINT /usr/local/bin/vnc.sh

ENV USER_NAME=vnc \
    USER_UID=1001 \
    BASE_DIR=/home/vnc
ENV HOME=${BASE_DIR}

RUN mkdir -p ${BASE_DIR} \
    && touch /etc/sysconfig/desktop \
    && chmod 777 ${BASE_DIR} /etc/sysconfig/desktop \
    && useradd -u ${USER_UID} -r -g 0 -M -d ${BASE_DIR} -b ${BASE_DIR} -s /bin/bash -c "vnc user" ${USER_NAME} \
    && chmod -R g=u /etc/passwd
