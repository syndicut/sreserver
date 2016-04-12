from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link
from werkzeug.utils import import_string

nav = Nav()

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    app.config['HUB_PLUGINS'] = {}
    Bootstrap(app)
    nav.init_app(app)
    for plugin in app.config['PLUGINS']['enabled']:
        blueprint = import_string('sreserver.plugins.{0}:{1}'.format(plugin, plugin))
        app.register_blueprint(blueprint)
    return app

app = create_app()



@nav.navigation()
def mynavbar():
    return Navbar(
        'SREServer',
        Link('Home', '/'),
        View('Hub', 'hub'),
    )

@app.route("/hub")
def hub():
    plugin_hub_data = {}
    for blueprint_name, config in app.config['HUB_PLUGINS'].iteritems():
        app.logger.debug('Importing {0}'.format(blueprint_name))
        module = import_string('sreserver.plugins.{0}'.format(blueprint_name))
        plugin_hub_data[blueprint_name] = getattr(module, config['function'])()
    return render_template('hub.html', plugin_hub_data=plugin_hub_data)
