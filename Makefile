.PHONY: build-services
build-services:
	docker build -t kiwitcms/kerberos -f tests/Dockerfile.kerberos tests/
	docker build -t kiwitcms/with-kerberos -f tests/Dockerfile.kiwitcms tests/

.PHONY: run-services
run-services:
	docker compose up -d
	docker cp krb5_kiwitcms_org:/tmp/application.keytab .
	docker cp ./application.keytab web_kiwitcms_org:/Kiwi/application.keytab
	rm ./application.keytab
	docker exec -u 0 -i web_kiwitcms_org /bin/bash -c 'chown 1001:root /Kiwi/application.keytab'
	@echo "=== add the following to client's /etc/hosts & /etc/krb5.conf ==="
	@echo "--- web.kiwitcms.org ---"
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_kiwitcms_org
	@echo "--- krb5.kiwitcms.org ---"
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' krb5_kiwitcms_org

.PHONY: verify-curl-with-kerberos
verify-curl-with-kerberos:
	# make sure curl supports Negotiate authentication
	curl -V | egrep -i "GSS-Negotiate|GSS-API|Kerberos"

.PHONY: verify-web-login
verify-web-login: verify-curl-with-kerberos
	# grab the page
	curl -k -L -o /tmp/curl.log --negotiate -u: \
	     -b /tmp/cookie.jar -c /tmp/cookie.jar \
	    https://web.kiwitcms.org:8443/login/kerberos/

	# verify user has been logged in
	cat /tmp/curl.log | grep 'Kiwi TCMS - Dashboard'
	cat /tmp/curl.log | grep 'Test executions'
	cat /tmp/curl.log | grep 'Your Test plans'

	# verify username is 'travis', e.g. taken from 'travis@KIWITCMS.ORG' principal
	cat /tmp/curl.log | grep '<a href="/accounts/travis/profile/" target="_parent">My profile</a>'
