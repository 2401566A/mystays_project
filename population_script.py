import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mystays_project.settings')

import django
django.setup()
from mystays.models import Stay, Review

def populate():
    sanctum_resort_reviews = [
        {'title': 'Great hotel!', 'impression': 8, 'locationRating': 6, 'cleanliness': 10, 'descripAccuracy': 9, 'costRating': 7,
         'comment': 'Really enjoyed our stay, but it was a hassle to get to the city center. Would recommend.'},
        {'title': 'Would return for another stay', 'impression': 9, 'locationRating': 8, 'cleanliness': 9, 'descripAccuracy': 9, 'costRating': 8,
         'comment': 'Nice rooms, great view, pleased overall'},        
        {'title': 'Friendly and good food', 'impression': 8, 'locationRating': 7, 'cleanliness': 8, 'descripAccuracy': 8, 'costRating': 7,
         'comment': 'The staff was friendly and the restaurant had delicious food.'} ]
    
    sunrise_hostel_reviews = [
        {'title': 'Nice enough', 'impression': 6, 'locationRating': 9, 'cleanliness': 6, 'descripAccuracy': 7, 'costRating': 9,
         'comment': 'Only stayed one night with friends. It was nice enough for passing through.'},
        {'title': 'Terrible and rude service', 'impression': 4, 'locationRating': 7, 'cleanliness': 5, 'descripAccuracy': 5, 'costRating': 8,
         'comment': 'Really rude staff!'},
        {'title': 'Expected', 'impression': 6, 'locationRating': 8, 'cleanliness': 7, 'descripAccuracy': 7, 'costRating': 10,
         'comment': 'You get what you expect for the price.'} ]

    riverside_inn_reviews = [
        {'title': 'Beautiful!', 'impression': 9, 'locationRating': 9, 'cleanliness': 10, 'descripAccuracy': 9, 'costRating': 7,
         'comment': 'Picturesque inn with beautiful rooms. Will definitely stay here again.'},
        {'title': 'Nice, a bit pricey', 'impression': 6, 'locationRating': 4, 'cleanliness': 6, 'descripAccuracy': 6, 'costRating': 5,
         'comment': 'A bit expensive for the services provided. Overall nice though.'},
        {'title': 'Cat', 'impression': 8, 'locationRating': 8, 'cleanliness': 8, 'descripAccuracy': 7, 'costRating': 8,
         'comment': 'There is a really cute stray cat who walks around.'} ]

    northern_country_inn_reviews = [
        {'title': 'A Nice Place to Stay', 'impression': 6, 'locationRating': 7, 'cleanliness': 8, 'descripAccuracy': 6, 'costRating': 6,
         'comment': 'A nice inn, but you can tell it needs maintenance. I enjoyed the country location and even saw a few animals in the trees.'} ]
    
    stays = {'Sanctum Resort': {'reviews': sanctum_resort_reviews, 'price': 128,
                                'description': 'A 4-star hotel within walking distance of Glasgow Central. Breakfast and free WiFi included. Nationally ranked steakhouse located on the ground floor.',
                                'contacts': '+44 7912 123456, sanctumresort@gmail.com'},
            'Sunrise Hostel': {'reviews': sunrise_hostel_reviews, 'price': 24,
                               'description': 'Low cost hostel in the center of Edinburgh. Ideal for travel on a budget. Clean rooms and friendly staff.',
                               'contacts': '+44 7282 126270, sunrisehostel@gmail.com'},
            'Riverside Inn': {'reviews': riverside_inn_reviews, 'price': 65,
                              'description': 'Picturesque inn with a riverside view and large garden. Rental cars available to drive to the nearest cities of Glasgow and Stirling.',
                              'contacts': '+44 7958 156456, riversideinn@gmail.com'},
            'Northern Country Inn': {'reviews': northern_country_inn_reviews, 'price': 59,
                              'description': 'Beautiful inn surrounded by forest and country views. Features classically decorated rooms with a fireplace and a room service menu.',
                              'contacts': '+44 7900 756816, northerncountryinn@gmail.com'} }

    
    for sta, stay_data in stays.items():
        s = add_stay(sta, stay_data['price'], stay_data['description'], stay_data['contacts'], stay_data['reviews'])
        for r in stay_data['reviews']:
            add_review(s, r['title'], r['impression'], r['locationRating'], r['cleanliness'], r['descripAccuracy'], r['costRating'], r['comment'])

    for s in Stay.objects.all():
        for r in Review.objects.filter(stay=s):
            print(f'- {s}: {r}')

def add_review(stay, title, impression, locationRating, cleanliness, descripAccuracy, costRating, comment):
    r = Review.objects.get_or_create(stay=stay, title=title)[0]
    r.impression=impression
    r.locationRating=locationRating
    r.cleanliness=cleanliness
    r.descripAccuracy=descripAccuracy
    r.costRating=costRating
    r.comment=comment
    r.save()
    return r


def add_stay(name, price, description, contacts, reviews):
    s = Stay.objects.get_or_create(name=name)[0]
    s.price=price
    s.description=description
    s.contacts=contacts

    total = 0
    count = 0
    for r in reviews:
       total = total + r['impression']
       count = count + 1

    average = total/count
    s.propertyRating=average
    
    s.save()
    return s

#Execution begins here
if __name__ == '__main__':
    print('Starting MyStays population script...')
    populate()
            
