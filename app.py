
import threading
from wsgiref import simple_server
import seaborn as sns
import os
from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import pandas as pd
from datamongodb import MongoDBmanagement
from Flipkartscrapping import FlipkratScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
rows = {}
collection_name = None

logger = getLog('flipkrat.py')

free_status = True
db_name = 'Flipkart-Scrapper'

app = Flask(__name__)  # initialising the flask app with the name 'app'

#For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("--headless")

#To avoid the time out issue on heroku
class threadClass:

    def __init__(self, expected_review, searchstring, scrapper_object, review_count):
        self.expected_review = expected_review
        self.searchstring = searchstring
        self.scrapper_object = scrapper_object
        self.review_count = review_count
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        global collection_name, free_status
        free_status = False
        collection_name = self.scrapper_object.getReviewsToDisplay(expected_review=self.expected_review,
                                                                   searchstring=self.searchstring, username='mongodb',
                                                                   password='mongodb',
                                                                   review_count=self.review_count)
        logger.info("Thread run completed")
        free_status = True


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchstring = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
        expected_review = int(request.form['expected_review'])
        try:
            review_count = 0
            scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBmanagement(username='mongodb', password='mongodb')
            scrapper_object.openUrl("https://www.flipkart.com/")
            logger.info("Url hitted")
            scrapper_object.login_popup_handle()
            logger.info("login popup handled")
            scrapper_object.searchproduct(searchstring=searchstring)
            logger.info(f"Search begins for {searchstring}")
            if mongoClient.iscollectionpresent(collection_name=searchstring, db_name=db_name):
                response = mongoClient.findallRecords(db_name=db_name, collection_name=searchstring)
                reviews = [i for i in response]
                if len(reviews) > expected_review:
                    result = [reviews[i] for i in range(0, expected_review)]
                    scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv",
                                                        dataframe=pd.DataFrame(result))
                    logger.info("Data saved in scrapper file")
                    return render_template('results.html', rows=result)  # show the results to user
                else:
                    review_count = len(reviews)
                    threadClass(expected_review=expected_review, searchstring=searchstring,
                                scrapper_object=scrapper_object, review_count=review_count)
                    logger.info("data saved in scrapper file")
                    return redirect(url_for('feedback'))
            else:
                threadClass(expected_review=expected_review, searchstring=searchstring, scrapper_object=scrapper_object,
                            review_count=review_count)
                return redirect(url_for('feedback'))

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    try:
        global collection_name
        if collection_name is not None:
            scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBmanagement(username='mongodb', password='mongodb')
            rows = mongoClient.findallRecords(db_name="Flipkart-Scrapper", collection_name=collection_name)
            reviews = [i for i in rows]
            dataframe = pd.DataFrame(reviews)
            scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv", dataframe=dataframe)
            collection_name = None
            return render_template('results.html', rows=reviews)
        else:
            return render_template('results.html', rows=None)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))


@app.route("/graph", methods=['GET'])
@cross_origin()
def graph():
    return redirect(url_for('plot_png'))


@app.route('/a', methods=['GET'])
def plot_png():
    data = pd.read_csv("static/scrapper_data.csv")
    dataframe = pd.DataFrame(data=data)
    #fig=px.histogram(dataframe['rating'],x='rating',category_orders=dict(x=[1,2,3,4,5]))

    #fig.write_image("static/plot.jpeg")


    fig = sns.histplot(data=dataframe['rating'])
    fig.set(xlabel='rating', ylabel='count')
    sfig = fig.get_figure()
    sfig.savefig('static/plot.png', orientation="landscape")

    return render_template('graphs.html')





port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
