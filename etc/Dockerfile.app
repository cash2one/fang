# DON'T CHANGE ME !!!
# latest: 6.7.4-production-806fee6f

FROM docker-registry.guokr.com/apps/fenda-sub-env:6.7.4-production

ADD . /app
WORKDIR /app 

RUN chmod +x ./bin/start.sh

# RUN py.test tests
