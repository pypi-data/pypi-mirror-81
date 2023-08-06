# pyopereto
#### Opereto official Python client and CLI tool

#### Installation
```
pip install pyopereto
```
OR
```
python setup.py install
```


#### Using the command line tool

Create a file named opereto.yaml in your home directory containing Opereto access credential:
 
##### Using basic Auth
~/opereto.yaml
```
opereto_host: https://your_opereto_service_url
opereto_user: your_opereto_username
opereto_password: your_opereto_password
```

##### Using token based auth
```
opereto_host: https://your_opereto_service_url
opereto_token: <YOUR_TOKEN>
```

From the command line console, please type:
```
/>opereto -h
```


#### Using the client

```
from pyopereto.client import OperetoClient

my_client = OperetoClient()
```

#### Run the client in debug mode

```
...
...

# add this after invoking the client
import logging
logging.getLogger("pyopereto").setLevel(logging.DEBUG)
```


#### Learn more
* [PyOpereto Documentation](http://pyopereto.s3-website-us-east-1.amazonaws.com/)
* [Opereto REST API](https://operetoapi.docs.apiary.io/#)
* [Opereto Documentation](http://docs.opereto.com)

