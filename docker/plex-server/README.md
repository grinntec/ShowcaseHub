# Plex Server Docker Setup

This repository contains a Docker Compose configuration for setting up a Plex server using the [linuxserver/plex](https://hub.docker.com/r/linuxserver/plex) Docker image.

## Overview

This setup allows you to run a Plex Media Server in a Docker container. The server's web interface can be accessed at `http://<your-ip>:32400/web`. Media files are stored on a NAS, and paths to the NAS are mounted into the container.

## Prerequisites

- Docker and Docker Compose installed on your system.
- Access to a NAS or other storage where your media files are stored.

### Environment Variables

- `PUID`: User ID for the Plex process (default: `1000`).
- `PGID`: Group ID for the Plex process (default: `1000`).
- `TZ`: Timezone for the container (default: `Europe/Copenhagen`).
- `VERSION`: Version of the Plex server to use (default: `docker`).
- `PLEX_CLAIM`: Optional claim token to automatically claim the server.

### Volumes

- `/opt/plex`: Configuration files for Plex.
- `/media-share/tv`: Directory for TV shows.
- `/media-share/movies`: Directory for movies.

## Usage

1. Clone this repository:
   ```sh
   git clone https://github.com/grinntec/ShowcaseHub.git
   cd ShowcaseHub/docker/plex-server
   ```

2. Modify the `docker-compose.yaml` file if necessary to suit your environment.

3. Start the Plex server:
   ```sh
   docker-compose up -d
   ```

4. Access the Plex web interface at `http://<your-ip>:32400/web` to complete the setup.

## Notes

- Ensure the volumes specified in the `docker-compose.yaml` file exist on your host system and have the correct permissions.
- You can find more information and configuration options in the [linuxserver/plex](https://hub.docker.com/r/linuxserver/plex) documentation.

## Troubleshooting

If you encounter any issues, check the logs of the Plex container:
```sh
docker logs plex
```

For further assistance, consult the [Plex forums](https://forums.plex.tv/) or the [linuxserver.io](https://www.linuxserver.io/) community.

---

This README file provides an overview and instructions for setting up a Plex server using Docker Compose. Ensure to follow the prerequisites and configuration steps for a smooth setup.
```
