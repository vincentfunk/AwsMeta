import requests
import sys
import awsData

# input control
if sys.argv[1][0] == '-':
    options = sys.argv[1]
    url = sys.argv[2]
    port = sys.argv[3] if len(sys.argv) == 4 else '80'
else:
    options = None
    url = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) == 3 else '80'

address = url + ':' + port

# initial request
try:
    head = requests.get(address)
except requests.exceptions.ConnectionError:
    print("Could not connect, Exiting")
    sys.exit(1)

# recursive requests
print("Running...", end='\n\n')
parent = [awsData.AwsData(data, address, parent=None, skp=options) for data in head.text.replace('/', '').split('\n') if data != '']

# output
for start in parent:
    start.display()

