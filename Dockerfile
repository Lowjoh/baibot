#######################################
#                                     #
# Stage 1: building                   #
#                                     #
#######################################

FROM docker.io/rust:1.88.0-slim-bookworm AS build

RUN apt-get update && apt-get install -y build-essential pkg-config libssl-dev libsqlite3-dev

WORKDIR /app

COPY . /app

RUN cargo build --release

#######################################
#                                     #
# Stage 2: packaging                  #
#                                     #
#######################################

FROM docker.io/debian:bookworm-slim

RUN apt-get update && apt-get install -y ca-certificates sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python and dependencies for the proxy
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask requests
RUN apt-get clean && rm -rf /var/lib/apt/lists/*


# Copy the proxy script
COPY proxy.py /app/proxy.py

RUN mkdir -p /app/data

WORKDIR /app

COPY --from=build /app/target/release/baibot .
COPY config.yml /app/config.yml

ENTRYPOINT ["/bin/sh", "-c"]

# Change the CMD to run the proxy
CMD ["python3", "/app/proxy.py"]
