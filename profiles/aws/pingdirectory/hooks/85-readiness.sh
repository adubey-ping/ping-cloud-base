#!/usr/bin/env sh

. "${HOOKS_DIR}/utils.lib.sh"

# Verify that server is responsive on its LDAP secure port
beluga_log "readiness: verifying root DSE access"
/opt/liveness.sh || exit 1

# Verify that post-start initialization is complete on this host
beluga_log "readiness: verifying that post-start initialization is complete on ${HOSTNAME}"
POST_START_INIT_MARKER_FILE="${SERVER_ROOT_DIR}"/config/post-start-init-complete
test -f "${POST_START_INIT_MARKER_FILE}" && exit 0 || exit 1
exit 0