from flask import Flask, render_template, request, url_for, flash
from datetime import datetime
import time
import os
import smtplib
import threading
from pytube import YouTube


app = Flask(__name__)
app.secret_key = 'qwdiOKLWF2342JKEd'
def delete_file(name):
	direction = '/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/'
	time.sleep(20)
	os.remove(f'{direction}{name}')

@app.route('/', methods=['POST', 'GET'])
def index():	
	if request.method == "POST":
		variable_i = open('variable.txt', 'r')
		i = int(variable_i.read())
		variable_i.close()
		link = request.form['link']
		yt = YouTube(link)
		titolo = yt.title
		descrizione = yt.description
		preview = yt.thumbnail_url
		try:
			if request.form['video'] == 'Scarica video':
				yt.streams.filter(file_extension='mp4').first().download('/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos')
				file_name = f'test{i}.mp4'
				os.rename(f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/{titolo}.mp4', f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/test{i}.mp4')
				variable_i = open('variable.txt', 'w')
				variable_i.write(str(i+1))
				variable_i.close()
				threading.Thread(target=delete_file, name="Thread1", args=[file_name]).start()
				flash('File in arrivo')
				return render_template('index.html', titolo=titolo, descrizione=descrizione, preview=preview, file_name=file_name)
		except Exception:
			pass
	
		if request.form['audio'] == 'Scarica audio':
			gay_list = yt.streams.filter(only_audio=True).first()
			yt.streams.filter(only_audio=True).first().download('/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos')
			extension = str(gay_list)
			ext = extension[37:41]
			if ext == "webm":
				print(ext)
				file_name = f'test{i}.{ext}'
			else: 
				ext = extension[37:40]
				file_name = f'test{i}.{ext}'
			os.rename(f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/{titolo}.{ext}', f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/test{i}.mp4')
			variable_i = open('variable.txt', 'w')
			variable_i.write(str(i+1))
			variable_i.close()
			threading.Thread(target=delete_file, name="Thread1", args=[file_name]).start()
			flash('File in arrivo')
			return render_template('index.html', titolo=titolo, descrizione=descrizione, preview=preview, file_name=file_name)
	else:
		return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def yt_download():
	variable_i = open('variable.txt', 'r')
	i = int(variable_i.read())
	variable_i.close()
	link = request.form['link']
	yt = YouTube(link)
	titolo = yt.title
	descrizione = yt.description
	preview = yt.thumbnail_url
	try:
		if request.form['video'] == 'Scarica video':
			yt.streams.filter(file_extension='mp4').first().download('/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos')
			file_name = f'test{i}.mp4'
			os.rename(f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/{titolo}.mp4', f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/test{i}.mp4')
			variable_i = open('variable.txt', 'w')
			variable_i.write(str(i+1))
			variable_i.close()
			threading.Thread(target=delete_file, name="Thread1", args=[file_name]).start()
			return render_template('download.html', titolo=titolo, descrizione=descrizione, preview=preview, file_name=file_name)
	except Exception:
		pass
	
	if request.form['audio'] == 'Scarica audio':
		gay_list = yt.streams.filter(only_audio=True).first()
		yt.streams.filter(only_audio=True).first().download('/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos')
		extension = str(gay_list)
		ext = extension[37:41]
		if ext == "webm":
			print(ext)
			file_name = f'test{i}.{ext}'
		else: 
			ext = extension[37:40]
			file_name = f'test{i}.{ext}'
		os.rename(f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/{titolo}.{ext}', f'/Users/nontuopc01/Desktop/PyTube [TEST] V0.1 ALPHA/static/videos/test{i}.mp4')
		variable_i = open('variable.txt', 'w')
		variable_i.write(str(i+1))
		variable_i.close()
		threading.Thread(target=delete_file, name="Thread1", args=[file_name]).start()
		return render_template('download.html', titolo=titolo, descrizione=descrizione, preview=preview, file_name=file_name)

	

@app.route('/contact', methods=["POST", "GET"])
def contattaci():
	if request.method == "POST":
		nome = request.form['name']
		email = request.form['email']
		message = request.form['text']
		sender_email = "mrchela123@gmail.com"
		receiver_email = "telegiver1@gmail.com"
		sender_password = "Asokina76"
		email_text = f"""\
		Subject: Richiesta da URL Shorter

		E arrivata una richiesta da parte di\n
		Nome Cognome: {nome}\n 
		Email: {email}\n
		Testo del messaggio: {message}"""
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(sender_email, sender_password)
		server.sendmail(sender_email, receiver_email, email_text)
		flash('La sua domanda é stata inviata ai nostri admin!')
		return render_template('contact.html')
	return render_template('contact.html')




