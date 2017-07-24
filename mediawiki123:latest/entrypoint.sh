#!/bin/bash

USER_ID=$(id -u)
if [ ${USER_UID} != ${USER_ID} ]; then
  sed "s@${USER_NAME}:x:\${USER_ID}:@${USER_NAME}:x:${USER_ID}:@g" ${BASE_DIR}/etc/passwd.template > /etc/passwd
fi

: ${MEDIAWIKI_SITE_NAME:=MediaWiki}
: ${MEDIAWIKI_SITE_LANG:=en}
: ${MEDIAWIKI_ADMIN_USER:=admin}
: ${MEDIAWIKI_ADMIN_PASS:=rosebud}
: ${MEDIAWIKI_DB_SCHEMA:=wiki}
: ${MEDIAWIKI_SHARED:=/persistent}
: ${MEDIAWIKI_LOGO:=\$wgStylePath/common/images/wiki.png}
: ${DB_TYPE:=postgres}
: ${DB_USER:=postgres}
: ${DB_NAME:=mediawiki}

LOCAL_SETTINGS=${BASE_DIR}/httpd/mediawiki123/LocalSettings.php
IMAGE_DIR=${BASE_DIR}/httpd/mediawiki123/images
if [ -d "$MEDIAWIKI_SHARED" ]; then
  if [ ! -e "$MEDIAWIKI_SHARED/LocalSettings.php" ] && [ ! -z "${DB_HOST}" ]; then
    # If the container is restarted this will fail because the tables are already created
    # but there won't be a LocalSettings.php
    php /usr/share/mediawiki123/maintenance/install.php \
      --confpath ${BASE_DIR}/httpd/mediawiki123 \
      --dbname "$DB_NAME" \
      --dbschema "$MEDIAWIKI_DB_SCHEMA" \
      --dbport "$DB_PORT" \
      --dbserver "$DB_HOST" \
      --dbtype "$DB_TYPE" \
      --dbuser "$DB_USER" \
      --dbpass "$DB_PASSWORD" \
      --installdbuser "$DB_USER" \
      --installdbpass "$DB_PASSWORD" \
      --scriptpath "" \
      --server "http://${MEDIAWIKI_SITE_SERVER}" \
      --lang "$MEDIAWIKI_SITE_LANG" \
      --pass "$MEDIAWIKI_ADMIN_PASS" \
      "$MEDIAWIKI_ADMIN_USER" \
      "$MEDIAWIKI_SITE_NAME"
    echo "session_save_path(\"${BASE_DIR}/tmp\");" >> $LOCAL_SETTINGS
    sed -i -e "s/\$wgEnableUploads = false;/\$wgEnableUploads = true;/" $LOCAL_SETTINGS
    sed -i -e "s/#\$wgHashedUploadDirectory = false;/\$wgHashedUploadDirectory = true;/" $LOCAL_SETTINGS
    grep -q -F "\$wgUploadDirectory" "$LOCAL_SETTINGS" || (echo "\$wgUploadDirectory = \"$IMAGE_DIR\";" >> $LOCAL_SETTINGS)

    mv $LOCAL_SETTINGS $MEDIAWIKI_SHARED/LocalSettings.php
    ln -s $MEDIAWIKI_SHARED/LocalSettings.php $LOCAL_SETTINGS
  elif [ -e "$MEDIAWIKI_SHARED/LocalSettings.php" ]; then
    ln -s $MEDIAWIKI_SHARED/LocalSettings.php $LOCAL_SETTINGS
  fi

  # If the images directory only contains a README, then link it to
  # $MEDIAWIKI_SHARED/images, creating the shared directory if necessary
  if [ "$(ls $IMAGE_DIR)" = "README" -a ! -L $IMAGE_DIR ]; then
    rm -rf $IMAGE_DIR
    mkdir -p "$MEDIAWIKI_SHARED/images"
    ln -s "$MEDIAWIKI_SHARED/images" $IMAGE_DIR
  fi
fi

if [ -e "$LOCAL_SETTINGS" -a "$MEDIAWIKI_UPDATE" = true ]; then
  echo >&2 'info: Running maintenance/update.php';
  php /usr/share/mediawiki123/maintenance/update.php --quick --conf $LOCAL_SETTINGS
fi

if [ -e  "$LOCAL_SETTINGS" ]; then
  sed -i -e '/$wgLogo/c\$wgLogo = '\"$MEDIAWIKI_LOGO'\";' $LOCAL_SETTINGS
fi

/sbin/httpd -DFOREGROUND -f ${BASE_DIR}/httpd/conf/httpd.conf
