from re import S
from flask import Flask,render_template,Response,request
import csv
import requests
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge,EdgeOptions

app=Flask(__name__)

def web_scraping(user_emotion,sort,asc):
    final_list=[]
    template='https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres={}&sort={},{}'
    url=template.format(user_emotion,sort,asc)
    print(url)
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    results=soup.find_all('div',{'lister-item-content'})
    for i in range (0,10):
        inn_list={}
        actor=[]
        item=results[i]
        mov_title=item.h3.a.text
        mov_time=item.p.find('span',{"runtime"}).text
        genre=item.p.find('span',{"genre"}).text.strip(' \n')
        user_rating=item.find('div',{"ratings-bar"}).strong.text
        num_votes=item.find('p',{"sort-num_votes-visible"}).find_all('span')[-1].text.strip(' \n')
        launch_year=item.h3.find('span',{'lister-item-year text-muted unbold'}).text.strip('()')
        actors=item.find('p',{''}).find_all('a')
        director=actors[0].text
        desc=item.find_all('p',{"text-muted"})
        for i in range(1,len(actors)):
            actor.append(actors[i].text)
        inn_list['mov_title']=mov_title
        inn_list['mov_time']=mov_time
        inn_list['genre']=genre
        inn_list['user_rating']=user_rating
        inn_list['num_votes']=num_votes
        inn_list['launch_year']=launch_year
        inn_list['actor']=actor
        inn_list['director']=director
        inn_list['desc']=desc[-1].text.strip('\n')
        final_list.append(inn_list)
    return final_list

@app.route('/recommendations',methods=['GET','POST'])
def recom():
    if request.method=='POST':
        user_emotion=request.form['emotion']
        sort=request.form['sort']
        asc=request.form['asc']
        list=web_scraping(user_emotion,sort,asc)
        print(list)
    return render_template('final.html',recom=list)

@app.route('/')
def input_page():
    return render_template('input.html')

if __name__=='__main__':
    app.run(debug=True)