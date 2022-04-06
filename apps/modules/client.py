import urllib3
import certifi

from influxdb_client import InfluxDBClient


class Client:
    def __init__(self, server, port, token, org):
        self.server = server
        self.port = port
        self.token = token
        self.org = org

    def client(self):
        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
            )
        resp = http.request('GET', 'https://us-west-2-1.aws.cloud2.influxdata.com/ping')

        return InfluxDBClient(url=f'{self.server}:{self.port}', token=self.token, org=self.org,
            ssl_ca_cert=certifi.where(), 
            verify_ssl=False
        )







# client = Client(secrets.server, secrets.port, secrets.token, secrets.token).client()




