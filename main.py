import youtube_dl
from flask import Flask, flash, render_template, request, session, send_file
from wtforms import Form, validators, StringField
import tempfile
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'c85db1d3af3753874a2f917aaec1271698ed850ef2037761'
dirpath = tempfile.gettempdir()

class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])


@app.route("/URL-Submit", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        if form.validate() == True:
            name = request.form['name']
            with youtube_dl.YoutubeDL() as ytdl:
                info = ytdl.extract_info(name)
                sc_artist = info['uploader']
                sc_artist = sc_artist.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                sc_title = info['title']
                sc_title = sc_title.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                sc_ext = info['ext']
                sc_ext = sc_ext.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                ytdl_format_options = {'format': 'bestaudio/best', 'outtmpl': dirpath + "\\" + sc_artist + " - " + sc_title + "." + sc_ext,'quiet':True}
            with youtube_dl.YoutubeDL(ytdl_format_options) as ytdl:
                ytdl.download([name])
                info = ytdl.extract_info(name)
                sc_artist = info['uploader']
                sc_artist = sc_artist.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                sc_title = info['title']
                sc_title = sc_title.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                sc_ext = info['ext']
                sc_ext = sc_ext.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                return send_file(filename_or_fp= dirpath + "\\" + sc_artist + " - " + sc_title + "." + sc_ext,mimetype='audio/mpeg',as_attachment= True, attachment_filename=sc_artist + " - " + sc_title + "." + sc_ext)
        else:
            flash('Error: Please input valid name')
    session.clear() 
    return render_template('hello.html', form=form)


@app.route('/',methods=['GET', 'POST'])
def home():

    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        return render_template('hello.html')

@app.route('/signed-in', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return render_template('hello.html')


    else:
        flash('wrong password!')
        return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
        app.run(debug=True)
