from flask import Flask, jsonify, render_template, request, redirect,  send_from_directory
import os
import get_caption as gc
from PIL import Image
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
max_size_mb = 1
max_quality = 85
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
# def process_image(image_path):
#     captions = ["Caption 1", "Caption 2", "Caption 3", "Caption 4", "Caption 5"]
#     return captions

# Gmail SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'donotspellthemail@gmail.com'
EMAIL_PASSWORD = 'fzfk ukpb slhs rikf'

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, "robots.txt")

@app.route('/ads.txt')
def static_ads_from_root():
    return send_from_directory(app.static_folder, "ads.txt")

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacypolicy.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('result.html')

def compress_image(file_path):
    try:
        # Open the image file
        with Image.open(file_path) as img:
            # Compress the image with varying quality until it's below 1MB
            quality = max_quality
            while os.path.getsize(file_path) / (1024 * 1024.0) > max_size_mb and quality > 0:
                img.save(file_path, 'JPEG', quality=quality)
                quality -= 5  # Reduce quality by 5 in each iteration
    except Exception as e:
        print(f"Error during compression: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        original_size = os.path.getsize(file_path) / (1024 * 1024.0)  

        if original_size >= max_size_mb:
            compress_image(file_path)

        captions = gc.get_caption_gemini(file_path)

        return jsonify({"captions": captions})

@app.route('/contactus', methods=['GET'])
def contactus():
    return render_template('contactus.html')

@app.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('aboutus.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    print(data)  

    name = data['name']
    phone = data['phone']
    email = data['email']
    subject = data['subject']
    message = data['message']


    # Create email message
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}")
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS


    Usermsg = EmailMessage()
    Usermsg.set_content(f"Thanks for Contacting us.\n We will reply you soon.\nYour subject: {subject} \nYour Message: {message} \nRegards Freecaptions.com")
    Usermsg['Subject'] = f"Successful submission of Contact Us form On Freecaptions.com"
    Usermsg['From'] = EMAIL_ADDRESS
    Usermsg['To'] = email
    # Send email via SMTP
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.send_message(Usermsg)
        server.quit()
        print('Your message has been sent!', 'success')
    except Exception as e:
        print('There was an error sending your message. Please try again later.', 'danger')

    return jsonify({'message': 'Form submitted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
