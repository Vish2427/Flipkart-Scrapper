class repositoryobject:

    def __init__(self):
        print()

    def getusernameforMongoDB(self):
        username = "mongodb"
        return username

    def getpasswordforMongodb(self):
        password = "mongodb"
        return password

    def getloginclosebutton(self):
        login_close_button = "//body[1]/div[2]/div[1]/div[1]/button[1]"
        return login_close_button

    def getinputsearcharea(self):
        input_searcharea = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/div[1]/input[1]"
        return input_searcharea

    def getsearchbutton(self):
        search_button= "/html[1]/body[1]/div[1]/div/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/button[1]"
        return search_button

    def getproductname(self):
        product_name = "/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/h1[1]/span[1]"
        return product_name

    def getproductnamebyclass(self):
        product_name = "B_NuCI"
        return product_name

    def getorigionalproductprice(self):
        product_price = "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]"
        return product_price

    def getorigionalpricebyclass(self):
        product_price = "_30jeq3"
        return product_price

    def getdiscountpercent(self):
        discount_percent = "_3Ay6Sb"
        return discount_percent

    def getEMIdetails(self):
        emi_detail = "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/span[6]/li/span"
        return emi_detail

    def getViewPlanLinkUsingClass(self):
        viewPlan = "_3IATq1"
        return viewPlan

    def getAvailableOffers(self):
        available_offers1 = "_3TT44I"
        available_offers2 = "WT_FyS"
        return available_offers1, available_offers2

    def getMoreOffers(self):
        more_offer = "IMZJg1"
        return more_offer

    def getMoreOffersUsingClass(self):
        more_offer = "IMZJg1 Okf99z"
        return more_offer

    def getRatings(self):
        rating = "div._3LWZlK._1BLPMq"
        return rating

    def getComment(self):
        comment1 = "_6K-7Co"
        comment_heading = "_2-N8zT"
        return comment1, comment_heading

    def getCustomerName(self):
        comment_date = "_2sc7ZR"
        return comment_date

    def getTotalReviewPage(self):
        total_page_1 = "_2MImiq"
        #total_page_2 ="//body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[13]/div[1]/div[1]/span[1]"
        return total_page_1

    def getMoreReviewUsingClass(self):
        more_review_1 = "_3at_-o"
        more_review_2 = "_3UAT2v"
        return more_review_1, more_review_2

    def getNextFromTotalReviewPage(self):
        next_button = "_1LKTO3"
        return next_button








