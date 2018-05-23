import logging

from flask import Blueprint

from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, BooleanField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.widgets import TextArea

import langid
from utils.utils import templated

blueprint_langid = Blueprint('langid', __name__)


class UrlForm(FlaskForm):
    url = StringField(
        'URL',
        validators=[validators.DataRequired(), validators.URL(message='Sorry, this is not a valid URL,')])

    wMin = IntegerRangeField(
        'Min. words',
        default=5,
        validators=[validators.DataRequired(), validators.NumberRange(min=1, max=20)])

    extractor_class = SelectField(
        'Extractor',
        default=langid.EXTRACTORS[0],
        choices=[(i, i) for i in langid.EXTRACTORS],
        validators=[validators.DataRequired()])

    model_class = SelectField(
        'Model',
        default=langid.MODELS[0],
        choices=[(i, i) for i in langid.MODELS],
        validators=[validators.DataRequired()])

    return_raw = BooleanField(
        'Display raw sentences',
        default=False
    )


class TextForm(FlaskForm):

    text = StringField(
        'Text',
        widget=TextArea(),
        validators=[validators.DataRequired()])

    model_class = SelectField(
        'Model',
        default=langid.MODELS[0],
        choices=[(i, i) for i in langid.MODELS],
        validators=[validators.DataRequired()])


@blueprint_langid.route('/', methods=['GET', 'POST'])
@templated('index.html')
def crawl():
    form = UrlForm(request.form)

    if request.method == 'GET':
        return dict(form=form)
    elif not form.validate():
        for f, errs in form.errors.items():
            flash("%s: %s" % (f, "<br>".join(errs)), 'danger')
        return dict(form=form)

    try:
        results = langid.mixed_sentences_from_urls(
            form.url.data.strip(), extractor_name=form.extractor_class.data, model=form.model_class.data,
            with_proba=True, min_words=form.wMin.data, return_raw=form.return_raw.data)
    except Exception as e:
        flash('Something went wrong %s' % e, 'danger')
        logging.exception(e)
        return dict(form=form)
    return dict(form=form, results=results, labels=langid.DEFAULT_LABELS)


@blueprint_langid.route('/text', methods=['GET', 'POST'])
@templated('langid.html')
def predict_text():
    form = TextForm(request.form)

    if request.method == 'GET':
        return dict(form=form)

    elif not form.validate():
        for f, errs in form.errors.items():
            flash("%s: %s" % (f, "<br>".join(errs)), 'danger')
        return dict(form=form)

    results = [[r] for r in langid.lang_of_text(
        form.text.data, model=form.model_class.data, with_proba=True)]
    return dict(form=form, results=results, labels=langid.DEFAULT_LABELS)
