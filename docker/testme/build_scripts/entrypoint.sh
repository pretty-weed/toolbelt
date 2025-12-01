#!/usr/bin/env bash
rsync -avz ${WORKING_COPY_DIR}/ ${WORKDIR} >> ${WORKDIR}/ep-log.txt

bash "$@"