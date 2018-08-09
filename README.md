# python-simple-http-server
Just a simple server to test out openshift python s2i.

# test in minishift
```
minishift start
eval $(minishift oc-env)
oc login -u developer -p whatever

oc new-project test-project
oc create -f buildconfig.yml
```

# cleanup
```
oc get all | grep simple-python-http-server | grep -v "Terminating" | awk '{print "oc delete " $1}' | sh
```
