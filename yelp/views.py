# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
#import pandas as pd
#import json
#from surprise import SVD, evaluate
#from surprise import Reader, Dataset
import random

from django.shortcuts import render
from django.template import loader

from .models import YelpUsers, YelpCategories, Restaurants, YelpCombo, Combine


#tot_info1 = pd
#reviews_matrix1 = pd
reader = Reader(rating_scale=(0.5, 5.0))

# Create your views here.
def index(request):
    """
    with open('yelp_dataset/yelp_academic_dataset_business.json') as f:
        business = [json.loads(line) for line in f]

    # get the restaurant information
    restaurant_id = []
    for item in business:
        if item.get('state') == 'OH' or item.get('city') == 'Cleveland':
            restaurant_id.append(item.get('business_id'))
    restaurants_info = []
    for item in business:
        if item.get('business_id') in restaurant_id:
            restaurants_info.append([item.get('business_id'), item.get('name'), item.get('categories')])
    global reviews_matrix
    reviews_matrix = pd.read_csv('yelp_dataset/reviews_matrix_no_text.csv')
    data = pd.DataFrame(reviews_matrix)
    data.columns = ['business_id', 'user_id', 'stars', 'funny', 'useful', 'cool']
    reviews_business = {}
    reviews_matrix = data.values
    for item in reviews_matrix:
        try:
            reviews_business[item[0]] = reviews_business[item[0]] + ' ' + item[1]
        except KeyError:
            reviews_business[item[0]] = item[1]

    # reorder the restaurants and combine restaurants info
    # print(type(reviews_business))
    reviews_business_df = pd.DataFrame(list(reviews_business.items()), columns=['business_id', 'user_id'])

    restaurants_info_df = pd.DataFrame(restaurants_info, columns=['business_id', 'name', 'categories'])
    global tot_info
    tot_info = pd.merge(reviews_business_df, restaurants_info_df, on='business_id', how='left')
    tot_info = tot_info.drop(['user_id'], axis=1)

    cat_list = ['Nightlife', 'Bars', 'American (Traditional)', 'American (New)', 'Pizza', 'Sandwiches', 'Burgers',
                'Breakfast & Brunch', 'Coffee & Tea', 'Italian', 'Mexican', 'Chinese', 'Ice Cream & Frozen Yogurt',
                'Seafood', 'Steakhouses', 'Barbeque', 'Japanese', 'Mediterranean', 'Sushi Bars', 'Donuts',
                'Asian Fusion',
                'Juice Bars & Smoothies', 'Bagels', 'Tex-Mex', 'Middle Eastern', 'Greek', 'Thai']
    global indexing
    indexing = {}
    for i in cat_list:
        indexing[i] = []

    tot_info = tot_info.values

    request.session['userResults'] = {}

    # get the indices of each category
    for index, item in enumerate(tot_info):
        if item[2] is not None:
            cats = item[2].split(', ')
            for i in cats:
                #print(i)
                try:
                    indexing[i].append(index)
                except:
                    continue

    reader = Reader(rating_scale=(0.5, 5.0))

    # The columns must correspond to user id, item id and ratings (in that order).
    # collaborative filtering using SVD
    reviews_matrix = pd.read_csv('yelp_dataset/reviews_matrix_no_text.csv')
    data = Dataset.load_from_df(reviews_matrix[['user_id', 'business_id', 'stars']], reader)
    data.split(n_folds=5)

    #user_id = 'yyPHK6khPa4-ErV9U32x3A'


    tot_info = pd.merge(reviews_business_df, restaurants_info_df, on='business_id', how='left')
    tot_info = tot_info.drop(['user_id'], axis=1)

    global restaurants
    restaurants = tot_info['name']
    global indices
    indices = pd.Series(range(len(tot_info['name'])), index=tot_info['name'])


    file = open('yelp_dataset/cosine_sim.txt', 'r')
    global cosine_sim
    cosine_sim = [[float(num) for num in line.split(' ')] for line in file]
"""
    yelp_user_list = YelpUsers.objects.all()
    cats = YelpCategories.objects.order_by('name')
    template = loader.get_template('yelp/index.html')
    context = {
        'yelp_user_list': yelp_user_list,
        'yelp_cats_list': cats
    }
    #output = ', '.join(n.name for n in yelp_user_list)

    #tot_info1 = tot_info


    return HttpResponse(template.render(context, request))


def results(request):
    template = loader.get_template('yelp/results.html')
    if request.method == "POST":

        restaurant = request.POST['restaurant']
        user_id = request.POST["yelp_people"]
        comb = restaurant + user_id
        name = YelpUsers.objects.get(yelp_id=user_id)
        user_id = name.name


        restListComb = YelpCombo.objects.filter(userCat=comb).exists()
        if restListComb:
            test = YelpCombo.objects.get(userCat=comb)
            both = Combine.objects.filter(combo=test).order_by('rank')
            #test = YelpCombo.objects.get(userCat=comb)
            #both = test.names.all()
            context = {
                'restaurants': both,
                'restaurant': restaurant,
                'user': user_id
            }
            print("good to go")
            return HttpResponse(template.render(context, request))
        else:

            send = "You're looking at the results...But you didn't tell us what you were looking for!"

            return HttpResponse(send)

    else:

        send = "You're looking at the results...But you didn't tell us what you were looking for!"

        return HttpResponse(send)


""""
        if comb in request.session['userResults']:

            both = request.session['userResults'][comb]
            print("old combo")
            fun = []
            for i in both:
                print(i)
                fun.append(i)

        else:
            both = get_recommendations(restaurant, user_id)

            fun = []
            for i in both:
                print(i)
                fun.append(i)

            print(fun)
            print(type(fun))
            print("new combo")
            request.session['userResults'][comb] = fun
            request.session.modified = True

        for rest in both:
            restcheck = Restaurants.objects.get(name=rest)
            if not restcheck:
                restcheck = Restaurants(name=rest)
                restcheck.save()


        restListComb = YelpCombo.objects.filter(userCat=comb).exists()
        if not restListComb:
            print("this is the combo", comb)
            restListComb = YelpCombo(userCat=comb)
            restListComb.save()
            count = 0
            for rest in fun:
                print("this is the restuarant in the top 10", rest)
                restcheck = Restaurants.objects.filter(name=rest).exists()
                if not restcheck:
                    restcheck = Restaurants(name=rest)
                    restcheck.save()
                    simRests = get_similar_items(rest,restaurant)
                    for r in simRests:
                        print("this is the similar top 3", r)
                        secondCheck = Restaurants.objects.filter(name=r).exists()
                        if not secondCheck:
                            secondCheck = Restaurants(name=r)
                            secondCheck.save()
                        else:
                            secondCheck = Restaurants.objects.get(name=r)
                        restcheck.similar.add(secondCheck)
                        restcheck.save()
                    restcheck.save()
                else:
                    restcheck = Restaurants.objects.get(name=rest)
                newRestuarantRel = Combine.objects.create(restaurant=restcheck, combo=restListComb, rank=count)
                newRestuarantRel.save()
                count += 1
                #restListComb.names.add(restcheck)
                restListComb.save()
            restListComb.save()
        test = YelpCombo.objects.get(userCat=comb)
        print("hello")
        print(test.names.all())
        print("hello")

        context = {
            'restaurants' : both,
            'restaurant' : restaurant,
            'user' : user_id
        }
        return HttpResponse(template.render(context, request))
        
        """


def similar(request):
    template = loader.get_template('yelp/similar.html')
    rest = (request.GET['val'])
    #cat = 'Greek'
    #rests = get_similar_items(rest,cat)
    #rest = rest.restaurant
    try:
        rest = Restaurants.objects.get(name=rest)
    except:
        send = "You're looking at the results...But we didn't find anything you were looking for, sorry try another!"

        return HttpResponse(send)
    rests = rest.similar.all()
    print(rests)
    context = {
        'restaurant' : rest,
        'restaurants': rests
    }
    return HttpResponse(template.render(context, request))


"""
def get_recommendations(cat, user_id):
    random.seed(1206)
    idx = indexing[cat]
    print(user_id)
    print(cat)
    cat_business_id = tot_info.business_id[idx]
    selected = [ i for i, e in enumerate(reviews_matrix.business_id.tolist()) if e in cat_business_id.tolist() ]
    ratings = reviews_matrix.iloc[ selected ]
    data = Dataset.load_from_df(ratings[['user_id', 'business_id', 'stars']], reader)
    data.split(n_folds=5)
    #random.seed(1206)
    algo = SVD()
    evaluate(algo, data, measures=['RMSE', 'MAE'])
    score = []
    for item in tot_info.business_id[idx]:
        score.append(algo.predict(user_id, item)[3])
    sim_scores = list(enumerate(score))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:10]
    print("yep")
    print(sim_scores[0:10])
    print("yep")
    res_indices = [i[0] for i in sim_scores]
    print("right before the return")
    print(tot_info.name[idx])
    return tot_info.name[idx].iloc[res_indices,]


def get_similar_items(restaurant, cat):
    idx = indices[restaurant]
    try:
        if ( len(idx.tolist()) > 1 ):
            idx = idx.tolist()
            idx = idx[0]
    except:
        pass
    idx1 = indexing[cat]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    subset = [ e for i, e in enumerate(sim_scores) if e[0] in idx1 ]
    sim_scores = subset[1:4]
    res_indices = [ i[0] for i in sim_scores ]
    return restaurants.iloc[res_indices]
"""
