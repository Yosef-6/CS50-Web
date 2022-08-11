from datetime import datetime, timezone
from logging import exception
from NewsArchive.models import Article,Configuration
import requests

user_configs_everything = Configuration.objects.all().filter(active = True, option = Configuration.Everything)
user_configs_headlines  = Configuration.objects.all().filter(active= True,option = Configuration.Topheadlines)
url_headlines           = 'https://newsapi.org/v2/top-headlines'
url_everything          = 'https://newsapi.org/v2/everything'
payload_everything      = {'q':'','searchIn':'','sources':'','language':'','page':'1','pageSize':'10','sortBy':'relevancy','from':f'{datetime.now().__str__().split(" ")[0]}','apiKey':'insert ur news api key here'}
payload_headlines       = {'q':'','country':'','category':'','sources':'','page':'1','from':f'{datetime.now().__str__().split(" ")[0]}','pageSize':'10','apiKey':'insert ur news api key here'}
response_article = {}
def job():
    for user_e in user_configs_everything:
        edited_payload = payload_everything.copy()
        edited_payload["q"] = user_e.queryString
        edited_payload["searchIn"] = user_e.searchIn
        edited_payload["sources"] = user_e.sources 
        edited_payload["language"] = user_e.language 
        for k in edited_payload.copy().keys():
            if(edited_payload[k] == ''):
                del edited_payload[k] # delete null("") prameters before requestig todays content 
        response_article.clear()
        try:
            response = requests.get(url_everything, params=edited_payload)
            response_article.update(response.json()) 
            if response_article.get("status") == 'ok' and response_article.get("totalResults") > 0:
               for articles in response_article["articles"]:
              
                article_is_present = False
                if hasattr(user_e.config,'MyArticles'):
                  article_is_present = user_e.config.MyArticles.all().filter(title=articles["title"],author=articles["source"]["name"]).count() != 0

                if article_is_present == False:
                  d = datetime.fromisoformat(articles["publishedAt"][:-1]).astimezone(timezone.utc)
                  art =Article(author=articles["source"]["name"]
                  ,title=articles["title"],discription=articles["description"]
                  ,article_url=articles["url"],article_image_url=articles["urlToImage"]
                  ,publishedAt=d,content=articles["content"]
                  ,aggregatedDate = datetime.now().__str__().split(" ")[0]
                  ,viewer= user_e.config)
                  art.save()
                 
               else:
                   if response_article["status"] == 'error':
                      user_e.info = f'Config error: Code: {response_article["code"]}  Message :{response_article["message"]}' 
                      user_e.active = False #no longer active till the user reconfigured the config 
                      user_e.save()
                   else:
                      user_e.info = 'Your Config settings produced 0 results :Edit some fields to start aggregating'
                      user_e.active = False 
                      user_e.save()
        except Exception as e:
             print(e)
             

    for user_h in user_configs_headlines:
        edited_payload  = payload_headlines.copy()
        edited_payload["q"] = user_h.queryString
        edited_payload["category"] = user_h.catagory
        edited_payload["sources"] = user_h.sources 
        edited_payload["country"] = user_h.country
        for k in edited_payload.copy().keys():
            if(edited_payload[k] == ''):
                del edited_payload[k]
        response_article.clear()        
        try:
           response = requests.get(url_headlines, params=edited_payload)
           response_article.update(response.json())
        
           if response_article["status"] == 'ok' and response_article["totalResults"] > 0:
              for articles in response_article["articles"]:
               
               article_is_present = False
               if hasattr(user_h.config,'MyArticles'):
                  article_is_present = user_h.config.MyArticles.all().filter(title=articles["title"],author=articles["source"]["name"]).count() != 0

               if article_is_present == False:
                  d = datetime.fromisoformat(articles["publishedAt"][:-1]).astimezone(timezone.utc)
                  art =Article(author=articles["source"]["name"]
                  ,title=articles["title"],discription=articles["description"]
                  ,article_url=articles["url"],article_image_url=articles["urlToImage"]
                  ,publishedAt=d,content=articles["content"]
                  ,aggregatedDate = datetime.now().__str__().split(" ")[0]
                  ,viewer= user_h.config
                  )
                  art.save()
                
               
           else:
               if response_article["status"] == 'error':
                  user_h.info = f'Config error: Code:{response_article["code"]}  Message :{response_article["message"]}' 
                  user_h.active = False #no longer active till the user reconfigured the config 
                  user_h.save()
               else:
                  user_h.info = 'Your Config settings produced 0 results :Edit some fields to start aggregating'
                  user_h.active = False  #no longer active till the user reconfigured the config 
                  user_h.save()
        except Exception as e:
             print(e)
             

