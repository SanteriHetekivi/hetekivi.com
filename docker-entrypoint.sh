#!/bin/sh

# Get group and user ids or use defaults.
PUID=${PUID:-911}
PGID=${PGID:-911}

# Change group and user ids.
groupmod -o -g "$PGID" app &&
usermod -o -u "$PUID" app &&

# Change permission for user and group.
chown -R app:app /app &&
chown -R app:app /data &&
chown -R app:app /usr/src/app &&
chmod +x /app/run.sh &&

su -s /bin/bash -c 'id' app &&

# Wait for database.
/app/wait-for-it.sh db:5432 &&
# Running command.
exec gosu app "$@"