FROM fedora:27

RUN dnf -y update && \
    dnf -y install "@Cinnamon Desktop" \
                   "@KDE" \
                   "@KDE Plasma Workspaces" \
                   "@LibreOffice" \
                   "@LXDE Desktop" \
                   "@LXQt Desktop" \
                   "@Office/Productivity" \
                   "@MATE Desktop" \
                   "@Sugar Desktop Environment" \
                   "@Xfce Desktop" \
                   bind-utils \
                   firefox \
                   fvwm \
                   gimp \
                   hexchat \
                   i3 \
                   ksh \
                   levien-inconsolata-fonts \
                   net-tools \
                   terminator \
                   thunderbird \
                   pidgin \
                   tcsh \
                   tigervnc-server \
                   tmux \
                   twm \
                   xorg-x11-fonts-100dpi \
                   xorg-x11-fonts-ISO8859-1-100dpi \
                   xorg-x11-fonts-Type1 \
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
    && echo fedora | passwd --stdin ${USER_NAME} \
    && chmod -R g=u /etc/passwd
