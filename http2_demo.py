from hyper import HTTPConnection, HTTP20Connection

host = '10.186.229.104'
port_uportal = '8643'
uri_uportal = '/ucrest/ccc/up/corp/123456/sms/send'
base_url = 'https://'+host+':'+port_uportal+uri_uportal
print(base_url)
# conn = HTTPConnection(ip_port_uportal)
# conn.request('POST', base_url)
# resp = conn.get_response()

# print(resp.read())

conn2 = HTTP20Connection(host=host, port=port_uportal, secure=True)
response = conn2.request('POST',base_url)
resp = conn2.get_response(response)
print (resp.status)
print (resp.read())
