# DON'T CHANGE ME !!!
# latest: 7.4.0-1_sub-fb12779e

FROM docker-registry.guokr.com/apps/fenda-sub-env:7.4.0-1_sub

ADD . /app
WORKDIR /app 

RUN chmod +x ./bin/start.sh

# RUN py.test tests