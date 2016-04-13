from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link
from werkzeug.utils import import_string
from babel.dates import format_timedelta
from datetime import date
import time

nav = Nav()

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    app.config['PLUGINS_REGISTRY'] = {}
    Bootstrap(app)
    nav.init_app(app)
    for plugin in app.config['PLUGINS']['enabled']:
        blueprint = import_string('sreserver.plugins.{0}:{1}'.format(plugin, plugin))
        app.register_blueprint(blueprint, url_prefix='/{0}'.format(plugin))
    return app

app = create_app()

@app.template_filter('timedelta')
def timedelta_filter(timestamp):
    now = date.fromtimestamp(time.time())
    return format_timedelta(now-date.fromtimestamp(timestamp))

@nav.navigation()
def mynavbar():
    nav = [
        'SREServer',
        Link('Home', '/'),
        View('Hub', 'hub'),
    ]
    for plugin in app.config['PLUGINS_REGISTRY'].itervalues():
        if 'navbar' in plugin:
            nav += plugin['navbar']
    return Navbar(*nav)

@app.route("/hub")
def hub():
    plugin_hub_data = {}
    for plugin_name, plugin in app.config['PLUGINS_REGISTRY'].iteritems():
        if 'hub_data_func' in plugin:
            plugin_hub_data[plugin_name] = plugin['hub_data_func']()
    return render_template('hub.html', plugin_hub_data=plugin_hub_data)
