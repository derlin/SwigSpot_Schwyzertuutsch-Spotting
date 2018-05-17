from flask import Flask

from blueprints.langid import blueprint_langid

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

app.register_blueprint(blueprint_langid)

# -- jinja

# colors = ['#bcf4cb', '#d2d4f4', '#a8f4f4', '#f4c0bc', 'transparent']
colors = ['#bcf4cb', '#d2d4f4', '#a8f4f4', '#f4c0bc', '#ffff00']


def format_proba(proba, labels=None, sep="<br>"):
    if labels:
        return sep.join(["%s: %.3f" % t for t in zip(labels, proba)])
    else:
        return sep.join(["%.3f" % t for t in proba])


def get_color(label, probas=None):
    color = colors[label]
    if color.startswith('#') and probas is not None:
        color += '%02x' % (int(probas[label] * 255))
    return color


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.globals.update(color=get_color)
    app.jinja_env.globals.update(format_proba=format_proba)
    app.run(port=8080, debug=True)
