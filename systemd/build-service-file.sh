#!/usr/bin/env bash

RELATIVE_PATH=$(dirname ${0})
SRC_FILE="${RELATIVE_PATH}/openvpn-status-ws.service.sample"
DIST_FILE="${RELATIVE_PATH}/openvpn-status-ws.service"

if [[ -f "${RELATIVE_PATH}/build-service-file.conf" ]]; then
    source "${RELATIVE_PATH}/build-service-file.conf"
fi

if [[ -f "${SRC_FILE}" ]]; then
    scp "${SRC_FILE}" "${DIST_FILE}"
    sed -i "s/{{{USER}}}/"${USER}"/g" "${DIST_FILE}"
    sed -i "s/{{{GROUP}}}/"$(id -gn ${USER})"/g" "${DIST_FILE}"
    sed -i "s/{{{PYTHON}}}/"$(realpath $(which python3) | sed 's_/_\\/_g')"/g" "${DIST_FILE}"
    sed -i "s/{{{SCRIPT}}}/"$(realpath ${RELATIVE_PATH}/../openvpn_status_ws.py | sed 's_/_\\/_g')"/g" "${DIST_FILE}"

    echo "> Generated service file to: '${DIST_FILE}'"
else
    echo '> Unable to find sample file.'
fi

