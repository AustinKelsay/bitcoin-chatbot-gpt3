import articles.nakamoto_institute_articles as Nakamoto_institute_articles
import articles.mastering_bitcoin_scrape as Mastering_bitcoin_scrape
import podcasts.chow_collection_scrape as Chow_collection_scrape

if __name__ == '__main__':
    try:
        Mastering_bitcoin_scrape.scrape()
        Chow_collection_scrape.scrape()
        Nakamoto_institute_articles.scrape()
    except Exception as e:
        print("Error")
        print()
        print(e)