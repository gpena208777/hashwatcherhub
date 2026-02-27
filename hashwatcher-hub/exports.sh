export APP_HASHWATCHER_HUB_IP="${APP_HASHWATCHER_HUB_IP:-$(hostname -I | awk '{print $1}')}"
export APP_HASHWATCHER_HUB_PORT="8787"
