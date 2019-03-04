import youtube_dl
from flask import Flask, flash, render_template, request, session, send_file
from wtforms import Form, validators, StringField
import os
import tempfile
handle, path = tempfile.mkstemp()
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(24).hex()
file_num = os.urandom(10).hex()
class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])


@app.route("/URL-Submit", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    if request.method == 'POST':
            name = request.form['name']
            if form.validate() == True:
                name = request.form['name']
                #ytdl_format_options = {'format': 'bestaudio/best',
                #                       'outtmpl':path + 'song'+ file_num + '.txt',
                #                       'quiet': True}
                with open('/tmp/' + 'song'+ file_num + '.txt', "w") as file:
                    file.write("Test") 
                    file.close() 
                #with youtube_dl.YoutubeDL(ytdl_format_options) as ytdl:
                    #ytdl.download([name])
                    #info = ytdl.extract_info(name)
                    #sc_artist = info['uploader']
                    #sc_artist = sc_artist.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                    #sc_title = info['title']
                    #sc_title = sc_title.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                    #sc_ext = info['ext']
                    #sc_ext = sc_ext.replace(":","").replace("<","").replace(">","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
                    
                    #return send_file(filename_or_fp='/tmp/' + 'song'+ file_num + '.mp3',
                    #                mimetype='audio/mpeg', as_attachment=True,
                    #                attachment_filename=sc_artist + " - " + sc_title + "." + sc_ext)
                    session.clear()
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

