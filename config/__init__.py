import os
from configparser import ConfigParser


base_path = os.path.dirname(os.path.realpath(__file__))
env_map = {
    'prod': 'prod',
    'PROD': 'prod',
    'production': 'prod',
    'PRODUCTION': 'prod',
    'beta': 'dev',
    'BETA': 'dev',
    'dev': 'dev',
    'develop': 'dev'
}
env = os.getenv('ENV')

cfg = ConfigParser()
cfg.read('{}/{}.ini'.format(base_path, env_map.get(env, 'dev')), encoding='utf-8')

cron_cfg = ConfigParser()
cron_cfg.read('{}/cron.ini'.format(base_path), encoding='utf-8')
