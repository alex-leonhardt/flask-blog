FROM debian:latest

RUN apt-get update && apt-get install -y python-dev python-pip supervisor

RUN mkdir -p /opt/blog/log
RUN useradd -r blog

ADD requirements.txt /opt/blog/requirements.txt
RUN pip install -r /opt/blog/requirements.txt

ADD conf /opt/blog/conf
ADD posts /opt/blog/posts
ADD static /opt/blog/static
ADD templates /opt/blog/templates

ADD docker-start.sh /opt/blog/docker-start.sh
RUN chmod 640 /opt/blog/conf/blog.yaml && chmod 755 /opt/blog/docker-start.sh
ADD start-scripts/supervisord.conf /etc/supervisor/supervisord.conf
ADD start-scripts/supervisor_blog.conf /etc/supervisor/conf.d/blog.conf

ADD *.py /opt/blog/
ADD *.md /opt/blog/
RUN chown -R blog:blog /opt/blog

WORKDIR /opt/blog

EXPOSE 5000

CMD ["/opt/blog/docker-start.sh"]
