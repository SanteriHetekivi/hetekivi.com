FROM santerihetekivi/python3_handbreak

# Add user app
RUN groupadd --gid "911" -r app \
    && useradd -u "911" -r -g app -d /usr/src/app -c "Docker Image User" app \
    && mkdir /usr/src/app

# Adding entrypoint.
COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat


# Making directories for code and data.
RUN mkdir /app
RUN mkdir /data
RUN mkdir /data/tmp

# Adding code.
WORKDIR /app
COPY ./src/ /app/
RUN chmod +x /app/run.sh

# Updating pip and installing requirements.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Registering entrypoint.
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD "/app/run.sh"