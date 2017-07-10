FROM centos:latest
MAINTAINER Vessel Maintainers

ENV USER_NAME=www-data \
    USER_UID=1001 \
    BASE_DIR=/home/www-data
ENV HOME=${BASE_DIR}

RUN curl https://copr.fedorainfracloud.org/coprs/g/ansible-service-broker/ansible-service-broker/repo/epel-7/group_ansible-service-broker-ansible-service-broker-epel-7.repo -o /etc/yum.repos.d/asb.repo

RUN yum update  -y \
    && yum install -y epel-release \
    && yum install -y mediawiki123 php-pgsql ImageMagick git php-pecl-apcu php-intl postgresql mediawiki-container-scripts \
    && yum clean all

RUN mkdir -p ${BASE_DIR} ${BASE_DIR}/etc \
             && useradd -u ${USER_UID} -r -g 0 -M -d ${BASE_DIR} -b ${BASE_DIR} -s /sbin/nologin -c "www-data user" ${USER_NAME} \
             && mkdir -p ${BASE_DIR}/httpd/{logs,run,html,conf}  \
             && cp /etc/httpd/conf/{httpd.conf,magic} ${BASE_DIR}/httpd/conf \
             && cp -R /var/www/mediawiki123 ${BASE_DIR}/httpd/ \
             && mkdir ${BASE_DIR}/tmp \
             && cp -R /etc/httpd/conf.modules.d ${BASE_DIR}/httpd/conf.modules.d \
             && cp -R /etc/httpd/conf.d ${BASE_DIR}/httpd/conf.d \
             && chown -R ${USER_NAME}:0 ${BASE_DIR}/httpd \
             && chmod 777 ${BASE_DIR}/httpd/mediawiki123/{cache,images} \
             && chmod 777 ${BASE_DIR}/tmp \
             && chmod -R g+rw ${BASE_DIR} /etc/passwd \
             && cp /usr/share/mediawiki-container-scripts/mediawiki123.conf.example \
                ${BASE_DIR}/httpd/conf.d/mediawiki123.conf

RUN sed -i -e 's/Listen 80/Listen 8080/' \
           -e "s@ServerRoot \"/etc/httpd\"@ServerRoot ${BASE_DIR}/httpd@" \
           -e 's@DocumentRoot "/var/www/.*"@DocumentRoot mediawiki123/@' \
           -e "s@/var/www@${BASE_DIR}/httpd@" ${BASE_DIR}/httpd/conf/httpd.conf

RUN echo "PidFile run/httpd.pid" >> ${BASE_DIR}/httpd/conf/httpd.conf
RUN echo "DefaultRuntimeDir run/" >> ${BASE_DIR}/httpd/conf/httpd.conf
RUN ln -s /usr/lib64/httpd/modules/ ${BASE_DIR}/httpd/modules

EXPOSE 8080

USER ${USER_UID}

RUN sed "s@${USER_NAME}:x:${USER_UID}:@${USER_NAME}:x:\${USER_ID}:@g" /etc/passwd > ${BASE_DIR}/etc/passwd.template

ENTRYPOINT ["entrypoint.sh"]
