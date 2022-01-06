#!/bin/bash

cd /root/plugin
for bundle in auth register
do
	rm -f ${bundle}.zip
	/opt/tyk-gateway/tyk bundle build -m ${bundle}.json -y -o ${bundle}.zip
	if [[ ! -f ${bundle}.zip ]]
	then
		echo "[WARN]${bundle}.zip not built!"
	else
		if [[ -d vendor ]]; then
			zip -ur ${bundle}.zip vendor/ ./jwt-signing-key.pem
		fi
	fi
done
python3 -m http.server
