from flask import Flask, render_template, request, url_for, flash
import time
import os
import smtplib
import threading
from pytube import YouTube


app = Flask(__name__)
app.secret_key = 'qwdiOKLWF2342JKEd'

#The main page route
@app.route('/', methods=['POST', 'GET'])
def index():
	#Check if the user sended a request to download a file, if he doesn't just return the index page	
	if request.method == "POST":
		#the variable i it's a number that is added at the end of every downloaded file (ex. video4.mp4) 4 is i
		variable_i = open('variable.txt', 'r')
		i = int(variable_i.read())
		variable_i.close()
		link = request.form['link']
		#Check if the youtube link is valid
		try:
			yt = YouTube(link)
		except Exception:
			flash('Video non disponibile')
			return render_template('index.html')
		titolo = yt.title
		descrizione = yt.description
		preview = yt.thumbnail_url
		video_name = f'video{i}'
		#Check if the user selected download video
		if 'video' in request.form:
			if request.form['video'] == 'Scarica video':
				download_file(link=link, titolo=titolo, preview=preview, yt=yt, i=i, file='video')
				file_name = f'{video_name}.mp4'
				flash("File in arrivo")
				return render_template('index.html', titolo=titolo, preview=preview, file_name=file_name)
		#Check if the user selected download audio
		elif 'audio' in request.form:
			if request.form['audio'] == 'Scarica audio':
				download_file(link=link, titolo=titolo, preview=preview, yt=yt, i=i, file='audio')
				extension = str(yt.streams.filter(only_audio=True).first())
				#Find the file format (like .mp3)
				ext = extension[37:41]
				if ext == "webm":
					file_name = f'{video_name}.{ext}'
				else: 
					ext = extension[37:40]
					file_name = f'{video_name}.{ext}'
				flash("File in arrivo")
				return render_template('index.html', titolo=titolo, preview=preview, file_name=file_name)
	else:
		return render_template('index.html')

@app.route('/contact', methods=["POST", "GET"])
def contattaci():
	#Check if the user sended the request, if he didn't just return the contact template
	if request.method == "POST":
		nome = request.form['name']
		email = request.form['email']
		message = request.form['text']
		email_text = f"""\
		Subject: Richiesta da URL Shorter

		E arrivata una richiesta da parte di\n
		Nome Cognome: {nome}\n 
		Email: {email}\n
		Testo del messaggio: {message}"""
		send_email(email_text)
		flash('La sua domanda é stata inviata ai nostri admin!')
		return render_template('contact.html')
	return render_template('contact.html')

#Error handlers to show a custom error page instead of '<h1>Not Found(404)<h1>'

@app.errorhandler(404)
def not_found(error):
	return render_template('error.html', h1='Il tuo file non é stato trovato', h4='Ricordati che dopo il convertimento hai 5 minuti per scaricare il file'), 404

@app.errorhandler(400)
def bad_request(error):
	return render_template('error.html', h1='Non riusciamo a elaborare la tua richiesta', h4="Riprova piú tardi o contatta il <a href='/contact'>nostro team tencico</a>"), 400

@app.errorhandler(500)
def bad_request(error):
	return render_template('error.html', h1='Errore interno nel nostro server', h4="Riprova piú tardi o contatta il <a href='/contact'>nostro team tencico</a>"), 500

#A function to delete the downloaded videos/songs after 400 seconds

def delete_file(name):
	direction = 'static/videos/'
	time.sleep(400)
	os.remove(f'{direction}{name}')
	return 'ok'

#The function the send email to me if a user uses the /contact page

def send_email(email_text):
	sender_email = "mrchela123@gmail.com"
	receiver_email = "telegiver1@gmail.com"
	sender_password = "Asokina76"
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(sender_email, sender_password)
	server.sendmail(sender_email, receiver_email, email_text)
	return 'ok'

#The function for increase the i variable by one

def increase_i(i):
	variable_i = open('variable.txt', 'w')
	variable_i.write(str(i+1))
	variable_i.close()
	return 'ok'

#The function to download the file

def download_file(link, titolo, preview, file, i, yt):
	video_name = f'video{i}'
	if file == 'video':
		yt.streams.filter(file_extension='mp4').first().download('static/videos', filename=video_name)
		file_name = f'{video_name}.mp4'
	elif file == 'audio':
		yt.streams.filter(only_audio=True).first().download('static/videos', filename=video_name)
		extension = str(yt.streams.filter(only_audio=True).first())
		#Find the file format (like .mp3)
		ext = extension[37:41]
		if ext == "webm":
			file_name = f'{video_name}.{ext}'
		else: 
			ext = extension[37:40]
			file_name = f'{video_name}.{ext}'
	increase_i(i=i)
	#Start the timer to delete the file
	threading.Thread(target=delete_file, name="Thread1", args=[file_name]).start()
	return 'ok'