import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest


username = nexusiqServer['username']
password = nexusiqServer['password']
httpRequest = HttpRequest(nexusiqServer, username, password)


policiesUrl = '/api/v2/policies/'
response = httpRequest.get(policiesUrl, contentType='application/json')
print "About to read Policy List"
policyList = json.loads(response.getResponse())
print json.dumps(policyList, indent=4)
dataa = []
apps = {}
for item in policyList['policies']:
  policyID = item['id']
  policyName = item['name']
  appName = ''
  url = '/api/v2/policyViolations?p=%s' % policyID
  response = httpRequest.get(url, contentType='application/json')
  print "About to get violations from the response"
  print response.getResponse()
  violations = json.loads(response.getResponse())
  for app in violations['applicationViolations']:
    appName = app['application']['name']
    policyName = ''
    violationsArray = []
    for policyViolation in app['policyViolations']:
      policyName = policyViolation['policyName']
      violationObject = {
          'appName'   : appName,
          'stageId'   : policyViolation['stageId'],
          'reportUrl' : policyViolation['reportUrl'],
      }
      violationsArray.append(violationObject)

    appObject = {
      policyName : violationsArray
    }
    apps.update(appObject)
   
data = json.dumps(apps)
print data
