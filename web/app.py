# app.py


from flask import Flask
from flask import request, render_template, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


from models import *

from flask_wtf import FlaskForm
from forms import MapForm, MiniForm


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        post = Post(text)
        db.session.add(post)
        db.session.commit()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # flash(request.method)
    return render_template('index.html', posts=posts)


@app.route('/gallery')
def gallery():
    user = {'username': 'Jordan'}
    posts = [
        {
            'tracer': {'tracername': 'Oxygen'},
            'body': 'figure1',
            'img': 'NSsection_15_raw_O.png'
        },
        {
            'tracer': {'tracername': 'Phosphate'},
            'body': 'figure2',
            'img': 'NSsection-15_raw_P.png'
        }
    ]
    return render_template('gallery.html', title = 'Gallery', user = user, posts = posts)


@app.route('/miniform', methods=['GET', 'POST'])
def miniform():
    if request.method == 'POST':
        # flash(request.method)
        form = request.form
        # flash(form)
        posts = [
        {
            'tracer': {'tracername': 'Oxygen'},
            'body': form['hi'],
            'img': 'NSsection_15_raw_O.png'
        },
        {
            'tracer': {'tracername': 'Phosphate'},
            'body': 'Hello!',
            'img': 'NSsection-15_raw_P.png'
        }
    ]
        return render_template('hi.html', title = 'hi', posts = posts)
        # return redirect('/hi')
        # instead, let's try returning render_template with 
    return render_template('miniform.html', title='Mini Form')


from chem_ocean import Build_Map as bm
from chem_ocean import Plot_Raw2 as pr
from chem_ocean import plan_modelcomp as md
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import io
import base64

def makefig(fig):
        img = io.BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        plot_url2 = base64.b64encode(img.getvalue()).decode('ascii')
        return plot_url2

@app.route('/map_form2', methods=['GET', 'POST'])
def map_form2():
    if request.method == 'POST':
        form = request.form
        tracer_figs=[]
        # flash(form)
        img = io.BytesIO()
        plot_url = True
        
        tracers = form.getlist('tracer') 
        # flash(tracers)
        if len(tracers) <1:
            # flash('map')
            fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(13, 7), facecolor='w')
            _map, _fig, ax = bm.build_map('y', 'merc', float(form['lat_s']), float(form['lat_n']), float(form['lon_w']), float(form['lon_e']), 'c', fig, ax1, 111, 'lrbt')
            plot_url = makefig(_fig)

        if len(tracers) >0:
            if form['traj_type'] == "plan":
                _depth= float(form['depth'])
                lonLine =-15
            else:
                _depth=1500
                lonLine =-15

            for tracer in tracers:
                plot_url2 = True
                _fig = pr.plotRaw(float(form['lat_s']), float(form['lat_n']), float(form['lon_w']), float(form['lon_e']), [tracer], form['traj_type'], depth = _depth)#, lonTraj = (float(form['lon_w']), float(form['lon_e'])), latLimits = (float(form['lat_s']), float(form['lat_n'])))
                _fig.savefig(img, format='png')
                img.seek(0)
                plot_url2 = base64.b64encode(img.getvalue()).decode('ascii')
                tracer_figs.append({'tracername': tracer, 'tracerfig': plot_url2 })

            if len(form['modelraw']) >0:
                _x, _y, _feat_data, _basemap, _xLab, _yLab, _latLon_params = pr.getRaw(float(form['lat_s']), float(form['lat_n']), float(form['lon_w']), float(form['lon_e']), tracers, form['traj_type'], depth = _depth)#, lonTraj = (float(form['lon_w']), float(form['lon_e'])), latLimits = (float(form['lat_s']), float(form['lat_n'])))
                model_data = md.test_clustering3(_x, _y, _feat_data, _xLab, _yLab, 6, _latLon_params, _basemap, form['model_opts'])
                pred_dict, _fig = md.plot_model_output(_x, _y, _xLab, _yLab, float(form['lat_s']), float(form['lat_n']), float(form['lon_w']), float(form['lon_e']), _latLon_params, model_data[form['model_opts']], form['model_opts'], form['traj_type'], sil = form['sil_coef'])
                _fig.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode('ascii')
                # flash(form['model_opts'])

        return render_template('map.html', title = 'Map', metadata=form, tracerfigs=tracer_figs, plot_url=plot_url)#, plot_url2=plot_url2)

    return render_template('map_form2.html', title='Map Form')


if __name__ == '__main__':
    app.run()
