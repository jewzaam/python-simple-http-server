# python-simple-http-server
Just a simple server to test out openshift python s2i.

# OpenShift Prep

## minishift
```
# start minishift and log in
minishift start
eval $(minishift oc-env)
oc login -u developer -p whatever
```

## other openshift
You'll need to login.  Login with token can be retrieved from the console.

```
oc login https://<hostname>:<port> --token=<token>
```

## oc project
If you don't have one you want to use yet.  Can use any project.

```
oc new-project test-project
```

# Setup
1. Build
2. Deploy
3. Verify
4. Rebuild
5. Teardown

## Build

```
# create stuff
oc create -f buildconfig.yml

# wait for build to complete
while true;
do
    echo -n "."
    oc get builds | grep -v NAME | awk '{print $4}' | grep Complete && break
    sleep 5
done
```

##  Deploy
```
# create secret, dc, route, and svc
oc create secret generic test --from-literal=password=nothingreal
oc create -f deploymentconfig.yml
oc create -f route.yml
oc create -f service.yml
```

## Verify
```
# verify can hit the service
oc get route python-simple-http-server | grep -v NAME | awk '{print "curl http://" $2}' | sh

# verify logs (should see the 'password' and curl to /)
oc get pods | grep Running | awk '{print "oc logs po/" $1}' | sh
```

## Rebuild
Manual:
```
oc start-build buildconfigs/python-simple-http-server
```

Webhook:
Details left to the reader.  Generic webhook is enabled in this repo.  Secret is in the build config.  OpenShift console will give you the URL to hit for the hook.  For more info, see [OpenShift Triggers](https://docs.openshift.com/container-platform/3.9/dev_guide/builds/triggering_builds.html#webhook-triggers).
```
APPLICATION=python-simple-http-server
HOOK_SECRET=`grep secret buildconfig.yml | awk '{print $2}' | sed 's/"//g'`
URL=`oc status | grep 'server http' | sed "s#In project \([^ ]*\) on server \([^ ]*\)#\2/oapi/v1/namespaces/\1/buildconfigs/$APPLICATION/webhooks/$HOOK_SECRET/generic#g"`
echo "curl -X POST $URL"
```

## Teardown
```
oc get all | grep python-simple-http-server | grep -v "Terminating" | awk '{print "oc delete " $1 " &"}' | sh
wait
```

# GOTYAS
Changes in a secret will NOT trigger a rebuild.  Changes to configMaps should trigger a rebuild.

This is not setup for high availability.  If that's a requirement, look at scaling to 2+ pods and adding health checks.
