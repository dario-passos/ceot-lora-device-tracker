from apps.modules.device import DeviceProfile, Device
from datetime import datetime
from apps.modules.client import Client
import config as config, secret
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
if __name__ == "__main__":
    START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())

    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    # d = Device('L1', dp, client, 'Arvores')
    # # print(d.query_all_fields(START ))
    # # print(d.query_field('tmp', START ))
    # # print(d._query_interval_mean('tmp', 'mean', '7', START ))
    # print(d.get_current_avg('LHT65'))
    df = pd.DataFrame(columns=list(config.LHT65_FIELDS.keys()))
    for d in range(0, config.MAX_LHT65_DEVICES+1):
        d = Device(f'L{d}', dp, client, 'Arvores')
        tmp = []
        for k, v in config.LHT65_FIELDS.items():
            r,_ = d.get_last_value(k)
            if r != None:
                tmp.append(r)
        # df = pd.concat([df, tmp], ignore_index=True, axis=0)
        # print(tmp)
        if len(tmp) > 0:
            df.loc[len(df)] = tmp
    print(df.mean())
        # print(f'L{d}')


