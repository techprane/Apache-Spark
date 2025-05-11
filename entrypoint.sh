#!/usr/bin/env bash
set -euo pipefail

SPARK_WORKLOAD="${1:-}"

echo "SPARK_WORKLOAD: ${SPARK_WORKLOAD}"

if [[ "${SPARK_WORKLOAD}" == "master" ]]; then
    exec start-master.sh --port "${SPARK_MASTER_PORT:-7077}"

elif [[ "${SPARK_WORKLOAD}" == "worker" ]]; then
    exec start-worker.sh "spark://${SPARK_MASTER_HOST:-spark-master}:${SPARK_MASTER_PORT:-7077}"

elif [[ "${SPARK_WORKLOAD}" == "history" ]]; then
    exec start-history-server.sh

else
    echo "Usage: $0 {master|worker|history}"
    exit 1
fi






