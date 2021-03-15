FROM openzwave/openzwave-control-panel

USER root
RUN groupadd --gid 987 ttyUSB \
    && usermod -aG ttyUSB ozwcp_user
USER ozwcp_user
