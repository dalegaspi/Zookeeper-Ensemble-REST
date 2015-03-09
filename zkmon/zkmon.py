from flask import Flask
from flask import Response
from flask import request
from flask import json
import yaml
import logging
import logging.config
import telnetlib

app = Flask(__name__)
APP_CFG = 'app.yaml'
LOG_CFG = 'logging.yaml'

logger = logging.getLogger()
with open(LOG_CFG, 'rt') as f:
    config = yaml.load(f)
logging.config.dictConfig(config)

try:
    logger.info('loading application configuration')
    with open(APP_CFG, 'rt') as f:
        app_config = yaml.load(f)

except Exception as ex:
    logger.exception(ex)

# functions

# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > \
           request.accept_mimetypes['text/html']

def get_zk_cmd_exec(host, port=2181, cmd='stat'):
    resp = ''
    try:
        t = telnetlib.Telnet(host=host, port=port)
        t.write(cmd.encode('ascii'))
        resp = t.read_all();
    except Exception as ex:
        logger.exception(ex)
        resp = 'error: {0}'.format(ex.message)
        return None

    return dict(host=host, response=resp)

def get_cluster_cmd_exec(env, port=2181, cmd='srvr'):
    zks = app_config['envs'].get(env, None)
    if zks is None:
        return None
    else:
        cluster_status = []
        for host in [zk['ip'] for zk in zks['members']]:
            #cluster_status.append(format_zk_response(host, get_zk_cmd_exec(host, cmd=cmd)))
            cluster_status.append(get_zk_cmd_exec(host, cmd=cmd))

        # return '\n'.join(cluster_status)
        return cluster_status

def make_http_response(payload):
    if request_wants_json():
        return json.jsonify(zookeepers=payload)
    else:
        return Response('\n'.join(['host: {0}\n{1}\n----\n'.format(z['host'], z['response']) for z in payload]),
                        status=200, mimetype='text/plain')
# routes

def format_zk_response(host, r):
    return 'host: {0}\n{1}\n----\n'.format(host, r)

@app.route('/')
def hello_world():
    return 'zk monitor v0.21'

@app.route('/zk/<host>', defaults={'cmd': 'srvr'})
@app.route('/zk/<host>/<cmd>')
def zkmon_single_get_status(host, cmd):
    return make_http_response([get_zk_cmd_exec(host, cmd=cmd)])

@app.route('/cluster')
def zkmon_list_envs():
    return make_http_response('\n'.join(app_config['envs'].keys()))

@app.route('/cluster/<cluster>', defaults={'cmd': 'srvr'})
@app.route('/cluster/<cluster>/<cmd>')
def zkmon_cluster_get_status(cluster, cmd):
    return make_http_response(get_cluster_cmd_exec(cluster, cmd=cmd))

if __name__ == '__main__':
    logger.info('zkmon services v0.1')
    app.run(host='0.0.0.0', port=1338)
