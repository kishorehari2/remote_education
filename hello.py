from base64 import b64encode
from flask import Flask, render_template, request, make_response
from cloudant import Cloudant

import os


USERNAME = '7b942421-2d60-4974-b8a6-6e43cf6e5a9a-bluemix'
PASSWORD = 'd5e563ae558c8f5b045d46de05864e58fbde34d442b65239eaffc3da64983411'
URL = 'https://7b942421-2d60-4974-b8a6-6e43cf6e5a9a-bluemix:d5e563ae558c8f5b045d46de05864e58fbde34d442b65239eaffc3da64983411@7b942421-2d60-4974-b8a6-6e43cf6e5a9a-bluemix.cloudantnosqldb.appdomain.cloud'


client = Cloudant(USERNAME, PASSWORD, url=URL)
# Connect to the account
client.connect()


my_database = client['image']

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# @app.route('/')
# def student():
#     return render_template('student.html')


@app.route('/')
def student():
    return render_template('webcam.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    print("after result")
    if request.method == 'POST':
        results = request.form
    return render_template("result.html", result=results)


@app.route('/up', methods=['POST', 'GET'])
def upload():
    print("hikhfsk")
    file = request.files['file']
    file_name = file.filename
    uploaded_file_content = b64encode(file.read())
    # print(uploaded_file_content)
    # for document in my_database:
        # uploaded_file_content.decode('ascii')
    data = {'file_name': file_name, '_attachments': {file_name : {'data': uploaded_file_content.decode('ascii')}}}
    # data = {file_name : {'data': uploaded_file_content.decode('ascii')}}
        # data = {"data": "hgfghgfg"}
        # data={"id": "jgfsdahgfasdjajf"}
    doc = my_database.create_document(data)
    print(uploaded_file_content)
    if request.method == 'POST':
        results = request.form
        return render_template("result.html", result=results)


@app.route('/download', methods=['POST'])
def download():
	file_name = request.form['filename']
	for document in my_database:
		if (document['file_name'] == file_name):
			file = document.get_attachment(file_name, attachment_type='binary')
			response = make_response(file)
			response.headers['Content-Disposition'] = 'attachment; filename=%s'%file_name
			return response
		else:
			response = 'File not found'
	return response



@app.route('/uploadajax', methods = ['POST'])
def upldfile():
    if request.method == 'POST':
        file_val = request.get_data()
        file_name="hat.jpg"
        # uploaded_file_content = b64encode(file_val.read())
        data = {'file_name': file_name, '_attachments': {file_name : {'data': file_val.decode('ascii')}}}
        doc = my_database.create_document(data)
        print(file_val)
        return render_template('student.html')





if __name__ == '__main__':
    app.run(port=8000, debug=True)  