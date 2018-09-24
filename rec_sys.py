# The Ultimate Recommender System
# Author: Alessandro Gallo 

import math
import numpy as np

def data_movies_1ml(path='ml-1m'):
    
    movies={}
    data = np.loadtxt(path+'/movies.dat', usecols=[0,1], delimiter='::', dtype=object)
    for n in range(len(data)):
        id=data[n][0]
        title=data[n][1]
        movies[id]=title
    
    dataset={}
    data = np.loadtxt(path+'/ratings.dat', usecols=[0,1,2], delimiter='::', dtype=object)
    for n in range(len(data)):
        user=data[n][0]
        movieid=data[n][1]
        rating=data[n][2]
        dataset.setdefault(user,{})
        dataset[user][movies[movieid]]=float(rating)
    return dataset

def data_movies_100k(path='ml-100k'):
    movies={}
    for line in open(path+'/u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title
    train={}
    for line in open(path+'/u1.base'):
        (user,movieid,rating,ts)=line.split('\t')
        train.setdefault(user,{})
        train[user][movies[movieid]]=float(rating)
    test={}
    for line in open(path+'/u1.test'):
        (user,movieid,rating,ts)=line.split('\t')
        test.setdefault(user,{})
        test[user][movies[movieid]]=float(rating)
    dataset2={}
    for line in open(path+'/u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        dataset2.setdefault(user,{})
        dataset2[user][movies[movieid]]=float(rating)
    return train, test, dataset2

new_user={'Edward':{'2001: A Space Odyssey (1968)':5, 'Scream (1996)':3, 'Titanic (1997)':3.5,
                      "Schindler's List (1993)":4.5, 'Home Alone (1990)':3.5, 'Nightmare Before Christmas, The (1993)':4,
                      'Space Jam (1996)':4,'Toy Story (1995)':4.5,}}

def eucl_dist(dataset1,dataset2,user2,user1):
    from math import sqrt
    dic_sim={}
    for movie in dataset2[user2]:
        if movie in dataset1[user1]:
            dic_sim[movie]=1
    if len(dic_sim)==0: return 0
    sum_of_squares=sum_squares(dataset1,user1,dataset2,user2)
    result=1/(1+sum_of_squares)
    return result

def sum_squares(dataset1,user1,dataset2,user2):
    sq=sum([pow(dataset2[user2][movie]-dataset1[user1][movie],2) for movie in dataset2[user2] if movie in dataset1[user1]])
    return sq

simSums={}
totals={}

def totals_simSums(dataset1,dataset2,user1,user2,sim):
    for movie in dataset1[user1]:
        if movie not in dataset2[user2] or dataset2[user2][movie]==0:
            totals.setdefault(movie,0)
            totals[movie]+=dataset1[user1][movie]*sim
            simSums.setdefault(movie,0)
            simSums[movie]+=sim
    return totals,simSums

def scores_fun(totals,simSums):
    scores=[(total/simSums[movie],movie) for movie,total in totals.items()]
    scores.sort()
    scores.reverse()
    return scores

square=0
totsquare=0

def rmse_fun(dataset2,user2,dataset3,scores):
    global square
    global totsquare
    for tupla in scores:
        movscore,movname=tupla
        for movtestname in dataset3[user2]:
            if movname==movtestname:
                square=pow(dataset3[user2][movtestname]-movscore,2)
    totsquare+=square     
    k=len(dataset2)
    rmse=math.sqrt(totsquare/k)     
    return rmse

def predict(dataset1,dataset2,dataset3=None):
    global rmse
    rmse=0
    for user2 in dataset2:
        for user1 in dataset1:
            if user1==user2: continue
            sim=eucl_dist(dataset1,dataset2,user2,user1)
            if sim<=0: continue
            totals,simSums=totals_simSums(dataset1,dataset2,user1,user2,sim)
        scores=scores_fun(totals,simSums)
        if len(dataset2.keys())>10:
            rmse=rmse_fun(dataset2,user2,dataset3,scores)
    return scores,rmse

print "-----------------------------------------------------------------------"
print "                   The Ultimate Recommender System "
print "-----------------------------------------------------------------------\n"
print "The The Ultimate Recommender System can calculate the RMSE of a dataset or recommend a new user some new movies\n"

print"Choose an option:\n"
print "    1) Calculate the RMSE (100k dataset)"
print "    2) Make a recommendation (100k dataset)"
print "    3) Make a recommendation (1ml dataset)"
search_input = raw_input("\n---> ")

if search_input=='1':
    train,test,dataset2=data_movies_100k()
    print "\n The algorithm is working..."
    scores,rmse=predict(train,test,dataset2) 
    print "\nThe RMSE of the algorithm is: "+str(rmse)
    print "\nThanks for using The Ultimate Recommender System\n"
    
elif search_input=='2':
    train,test,dataset2=data_movies_100k()
    print "\n The algorithm is working..."
    scores,rmse=predict(dataset2,new_user)    
    recommended=scores[0:20]
    print "\nMovies recommended for the user: "+str(new_user.keys()[0])+"\n"
    for i in recommended:
        print i[1]
    print "\nThanks for using The Ultimate Recommender System\n"
    
elif search_input=='3':
    print "\n The algorithm is working..."
    dataset=data_movies_1ml()
    scores,rmse=predict(dataset,new_user)       
    recommended=scores[0:20]
    print "\nMovies recommended for the user: "+str(new_user.keys()[0])+"\n"
    for i in recommended:
        print i[1]
    print "\nThanks for using The Ultimate Recommender System\n"
    
else:
    print "\nError: input wrong"
