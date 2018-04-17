from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, PasswordField, BooleanField, RadioField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class MapForm(FlaskForm):
    # tracer = SelectMultipleField('Tracers', choices=[('oxygen', 'Oxygen'), ('phosphate', 'Phosphate'), ('salinity', 'Salinity')], validators=[DataRequired(message="no tracer")])
    plot_type = RadioField('Plot Type', choices = [('plan', 'Cross Section'), ('EWsection', 'Depth Slice (East-West line)'), ('NSsection', 'Depth Slice (North-South line)')],validators=[DataRequired(message="no plot type")] )
    lat_n = StringField('Lat-northern bound')
    lat_s = StringField('Lat-southern bound')
    lon_w = StringField('Lon-western bound')
    lon_e =StringField('Lon-eastern bound')
    # depth= StringField('Depth (depth slice only)')
    # model_opts = SelectMultipleField('Model Options', choices=[('MiniBatchKMeans', 'Mini Batch KMeans'), ('AgglomerativeClustering', 'Agglomerative Clustering'), ('SpectralClustering', 'Spectral Clustering'), ('AffinityPropagation', 'Affinity Propagation'), ('DBSCAN', 'DBScan'), ('Ward', 'Ward')])
    # sil_coef = RadioField('Sillohuette Coef Plot', choices=[('yes', 'yes'), ('no', 'no')])
    # raw_model = RadioField('Data Visualization Type', choices = [('raw', 'Raw'), ('model', 'Model')], validators=[DataRequired(message="please choose raw or model")])
    submit = SubmitField('Submit')

    # def validate_raw(self, raw, model):
    #     if raw.data == model.data:
    #         raise ValidationError('Please choose between "Raw" or "Model"')

    # def validate_model(self, raw, model):
    #     if raw.data == model.data:
    #         raise ValidationError('Please choose between "Raw" or "Model"')

class MiniForm(FlaskForm):
    hi = StringField('Greeting', validators=[DataRequired()])
    submit = SubmitField('Roger')
    