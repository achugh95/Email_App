# Email App
- Email Application using Python(Django).
- A provision to upload the list of Email ID's via a CSV File.
- ELK Stack for logging.
- After every 30 minutes, an automated email is sent to the Admin with all the email statistics of the day i.e. total email sent and timestamp of each email.

# Set up:

1. Elastic Search
- Download
- Run bin\elasticsearch.bat
- http://localhost:9200

2. LogStash
- Download Non-Sucking Service Manager (NSSM)
- Download LogStash
- Create a Logstash configuration file called “config.json” and place it in the “bin” directory with the following contents: input { tcp { port => 5959 codec => json } } output { elasticsearch { hosts => ["localhost:9200"] } }
- Run bin/logstash -f logstash.conf

3.  Kibana
- Download
- Open config/kibana.yml in an editor and set elasticsearch.hosts to point at your Elasticsearch instance as: 
- elasticsearch.hosts: ["http://localhost:9200"]
- Run bin\kibana.bat
- http://localhost:5601
- Create an index on Kibana : logstash-*

4. Celery
- Message Broker
- Download Redis # We may use RabbitMQ or Amazon SQS, but the respective settings will have to modified accordingly in the Python Code
- Run the server : redis-server
- For Windows, an additional package is required : eventlet. This can be installed via pip. 
- pip install eventlet
- celery -A your_app_name worker --pool=eventlet
- When we run our Django server and the periodic task kicks in via beat, we may run into an ssl error.
- Solution : Delete the following arguments :"*args, **kwargs" from the file eventlet\green\ssl.py.

- Email_App\myvenv\Lib\site-packages\eventlet\green\ssl.py

    if _is_under_py_3_7:
        return super(GreenSSLSocket, cls).__new__(cls)
    else:
        if not isinstance(sock, GreenSocket):
            sock = GreenSocket(sock)
        with _original_ssl_context():
            ret = _original_wrap_socket(
                sock=sock.fd,
                keyfile=keyfile,
                certfile=certfile,
                server_side=server_side,
                cert_reqs=cert_reqs,
                ssl_version=ssl_version,
                ca_certs=ca_certs,
                do_handshake_on_connect=False,
*args, **kw										# Delete it! No commenting. 

)
ret.keyfile = keyfile
ret.certfile = certfile
ret.cert_reqs = cert_reqs
ret.ssl_version = ssl_version
ret.ca_certs = ca_certs
ret.class = GreenSSLSocket
return ret

# Make sure all the below mentioned services are running
elasticsearch
logstash
kibana
redis-server

# To install the Django dependencies
- pip install django-requirements.txt

# Complete the Database migrations
- python manage.py makemigrations
- python manage.py migrate

# Run the following commands in two separate command prompts to start the Periodic Emails (after every 30 mins the Admin).
- celery -A tasks beat --loglevel=info
- celery -A tasks worker --pool=eventlet --loglevel=info
