#!/bin/bash
for volume in $(docker volume ls -q); do
    echo "Volume: $volume"
    docker ps -a --format '{{.ID}}' | while read cid; do
        if docker inspect "$cid" | grep -q "$volume"; then
            cname=$(docker inspect --format '{{.Name}}' "$cid" | sed 's/\///')
            echo "  Used by container: $cname ($cid)"
        fi
    done
done
