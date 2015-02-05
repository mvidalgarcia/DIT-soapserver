
from suds.client import Client as SudsClient

url = 'http://156.35.95.75:5000/soap/someservice?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.echo(str='Hello Do It Together!', cnt=3)
print r

r = client.service.upper(str='ponme en mayus')
print r
