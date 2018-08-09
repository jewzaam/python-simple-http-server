# python-simple-http-server
Just a simple server to test out openshift python s2i.

# test in minishift
```
# start minishift and log in
minishift start
eval $(minishift oc-env)
oc login -u developer -p whatever

# create stuff
oc new-project test-project
oc create -f buildconfig.yml

# wait for build to complete
while true;
do
    echo -n "."
    oc get builds | grep -v NAME | awk '{print $4}' | grep Complete && break
    sleep 5
done

# create secret, dc, route, and svc
oc create secret generic test --from-literal=password=nothingreal
oc create -f deploymentconfig.yml
oc create -f route.yml
oc create -f service.yml

# verify can hit the service
oc get route simple-python-http-server | grep -v NAME | awk '{print "curl http://" $2}' | sh

# verify logs (should see the 'password' and curl to /)
oc get pods | grep Running | awk '{print "oc logs po/" $1}' | sh
```

# start new build
```
oc start-build buildconfigs/simple-python-http-server
```

# cleanup
```
oc get all | grep simple-python-http-server | grep -v "Terminating" | awk '{print "oc delete " $1}' | sh
```
