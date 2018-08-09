# python-simple-http-server
Just a simple server to test out openshift python s2i.

# test in minishift
```
minishift start
eval $(minishift oc-env)
oc login -u developer -p whatever

oc new-project test-project
oc create secret generic test --from-literal=password=nothingreal
oc create -f buildconfig.yml
sleep 600
oc new-app simple-python-http-server
```

# start new build
```
oc start-build buildconfigs/simple-python-http-server
```

# cleanup
```
oc get all | grep simple-python-http-server | grep -v "Terminating" | awk '{print "oc delete " $1}' | sh
```
