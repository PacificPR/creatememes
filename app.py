from flask import Flask , render_template , redirect , url_for , request , send_file
import requests
import shutil


app = Flask(__name__)
#CORS(app)

URL = "https://api.imgflip.com/get_memes"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    r = requests.get(url=URL)
    data = r.json()
    memes = data["data"]["memes"]
    return render_template("search.html",data=memes)

@app.route("/create",methods=["POST","GET"])
def create():
    if request.method == "POST":
        m_url = request.form.get('meme_url')
        m_id =  request.form.get('meme_id')
        return render_template("create.html",img=m_url,id=m_id)
    else:
        return redirect(url_for(search))

@app.route("/final",methods=["POST","GET"])
def final():
    if request.method == "POST":
        URL = "https://api.imgflip.com/caption_image"
        text_top = request.form.get('top')
        text_bot = request.form.get('bot')
        id = request.form.get('temp_id')
    
        PARAMS = {'template_id':id,'username':'pacificPR','password':'thisis1secret','text0':text_top,'text1':text_bot}
        data = requests.post(url=URL,params=PARAMS)
        fin = data.json() 

        if fin["success"]:
            return render_template("final.html",img=fin["data"]["url"])
        else:
            return "Error Loading Request, Retry ..."
    else:
        return redirect(url_for("search"))

@app.route("/download",methods=["POST","GET"])
def download():
    if request.method == "POST":
        img_url = request.form.get('url')
        filename = "./static/img/meme.jpg"

        r = requests.get(img_url, stream = True)

        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            return send_file(filename,as_attachment=True)
        else:
            return "Couldn't Download File"

    else :
        return " Error Downloading File "

if __name__=="__main__" :
    app.run(debug=True)


