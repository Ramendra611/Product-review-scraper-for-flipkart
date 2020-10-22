
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route("/", methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route("/scrap", methods=['POST'])
def index():
    if request.method == 'POST':
            searchString = request.form['content'].replace(" ", "")
            try:
                flipkart_url = "https://www.flipkart.com/search?q=" + searchString
                uClient = uReq(flipkart_url)
                flipkart_page = uClient.read()
                uClient.close()
                flipkart_html = bs(flipkart_page, 'html.parser')  # parsing webpage as html
                bigboxes = flipkart_html.findAll("div", {'class': 'bhgxx2 col-12-12'})
                del bigboxes[0:3]
                box = bigboxes[0]
                product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
                prod_res = requests.get(product_link)
                prod_html = bs(prod_res.text, 'html.parser')
                comment_boxes = prod_html.find_all('div', {'class': '_3nrCtb'})

                # table = db[searchString]  # create a collection in same name as searchString

                reviews = []   #initialising a empty list for reviews

                for commentBox in comment_boxes:
                    try:
                        name = commentBox.div.div.find_all('p', {'class': "_3LYOAd _3sxSiS"})[0].get_text()
                    except:
                        name = 'No Name'

                    try:
                        rating = commentBox.div.div.div.div.text
                    except:
                        rating = 'No Rating'

                    try:
                        commentHead = commentBox.div.div.div.p.text
                    except:
                        commentHead = 'No Heading'

                    try:
                        comtag = commentBox.div.div.find_all('div', {'class': ""})
                        custComment = comtag[0].div.text
                    except:
                        custComment = "No Comment"

                    mydict = {'Product': searchString,
                              'Name': name,
                              'Rating': rating,
                              'Commenthead': commentHead,
                              'Comment': custComment}
                    # x = table.insert_one(mydict)
                    reviews.append(mydict)
                return render_template('results.html', reviews=reviews)
            except:
                return 'Something is wrong'


if __name__ == '__main__':
    app.run()
