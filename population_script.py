import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mystays_project.settings')

import django
django.setup()
from mystays.models import Stay, Review, UserProfile
from django.contrib.auth.models import User

userObjects = []

def populate():
    user1 = {'username': 'username1', 'password': 'password1', 'email': 'user1email@gmail.com'}

    user2 = {'username': 'username2', 'password': 'password2', 'email': 'user2email@gmail.com'}

    users = [user1, user2]
    
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

    purple_rose_hotel_reviews = [
        {'title': 'Not great', 'impression': 3, 'locationRating': 6, 'cleanliness': 4, 'descripAccuracy': 4, 'costRating': 2,
         'comment': 'They should not even call this place a hotel. Absolutely too expensive for the value because it has rude employees and bad room service. Do not stay here.'} ]

    horizons_hotel_reviews = [
        {'title': 'Average', 'impression': 6, 'locationRating': 6, 'cleanliness': 6, 'descripAccuracy': 6, 'costRating': 8,
         'comment': 'Overall a decent hotel. If what you are looking for is an average room to sleep in and mostly friendly staff, stay here. I would stay here again if the time came.'},
        {'title': 'Gary is SO GREAT', 'impression': 9, 'locationRating': 8, 'cleanliness': 9, 'descripAccuracy': 8, 'costRating': 8,
         'comment': 'I had a really nice stay here for about three days. I loved the room decor and the concierge Gary is so nice and helpful.'} ]        
        
    
    
    stays = {'Sanctum Resort': {'reviews': sanctum_resort_reviews, 'price': 128, 'keyword': 'Glasgow',
                                'description': 'A 4-star hotel within walking distance of Glasgow Central. Breakfast and free WiFi included. Nationally ranked steakhouse located on the ground floor.',
                                'latitude': '55.863815', 'longitude': '-4.274903', 'contacts': '+44 7912 123456, sanctumresort@gmail.com'},
            'Sunrise Hostel': {'reviews': sunrise_hostel_reviews, 'price': 24, 'keyword': 'Edinburgh',
                               'description': 'Low cost hostel in the center of Edinburgh. Ideal for travel on a budget. Clean rooms and friendly staff.',
                               'latitude': '55.949702', 'longitude': '-3.191505', 'contacts': '+44 7282 126270, sunrisehostel@gmail.com'},
            'Riverside Inn': {'reviews': riverside_inn_reviews, 'price': 65, 'keyword': 'Stirling',
                              'description': 'Picturesque inn with a riverside view and large garden. Rental cars available to drive to the nearest city of Stirling.',
                              'latitude': '56.003672', 'longitude': '3.895077', 'contacts': '+44 7958 156456, riversideinn@gmail.com'},
            'Northern Country Inn': {'reviews': northern_country_inn_reviews, 'price': 59, 'keyword': 'Inverness',
                              'description': 'Beautiful inn surrounded by forest and country views. Features classically decorated rooms with a fireplace and a room service menu.',
                              'latitude': '57.214580', 'longitude': '-4.615784', 'contacts': '+44 7900 756816, northerncountryinn@gmail.com'},
            'Purple Rose Hotel': {'reviews': purple_rose_hotel_reviews, 'price': 155, 'keyword': 'Saint Andrews',
                                     'description': 'Luxurious and hospitable hotel with gourmet room service and restaurant. Spacious and tastefully decorated rooms with daily cleaning service and friendly staff. The whole family will love their stay here!',
                                     'latitude': '56.342058', 'longitude': '-2.800748', 'contacts': '+44 7903 752345, purplerosehotel@gmail.com'},
            'Horizons Hotel': {'reviews': horizons_hotel_reviews, 'price': 74, 'keyword': 'Glasgow',
                                    'description': 'Reasonably priced hotel with beautifully decorated rooms and attentive staff. Rated a top hotel in Glasgow for five years running. Come stay with us!',
                                    'latitude': '55.86', 'longitude': '-4.251771', 'contacts': '+44 7933 272747, horizonshotel@gmail.com'} }

    for user in users:
        u = add_user(user['username'], user['password'], user['email'])
        print(f'- {u}')
    
    for sta, stay_data in stays.items():
        s = add_stay(sta, stay_data['price'], stay_data['description'], stay_data['latitude'], stay_data['longitude'], stay_data['contacts'], stay_data['reviews'], stay_data['keyword'])
        for r in stay_data['reviews']:
            add_review(s, r['title'], r['impression'], r['locationRating'], r['cleanliness'], r['descripAccuracy'], r['costRating'], r['comment'])

    for s in Stay.objects.all():
        for r in Review.objects.filter(stay=s):
            print(f'- {s}: {r}')

    User.objects.create_superuser('mystays', '2517529M@student.gla.ac.uk', 'mystaysproject123')

def add_review(stay, title, impression, locationRating, cleanliness, descripAccuracy, costRating, comment):
    r = Review.objects.get_or_create(stay=stay, title=title, reviewedBy=userObjects[0])[0]
    r.impression=impression
    r.locationRating=locationRating
    r.cleanliness=cleanliness
    r.descripAccuracy=descripAccuracy
    r.costRating=costRating
    r.comment=comment
    
    r.save()
    return r


def add_stay(name, price, description, latitude, longitude, contacts, reviews, keyword):
    s = Stay.objects.get_or_create(name=name, postedBy=userObjects[1])[0]
    s.price=price
    s.description=description
    s.latitude=latitude
    s.longitude=longitude
    s.contacts=contacts
    s.keyword=keyword
    
    s.save()
    return s

def add_user(username, password, email):
    u = User.objects.get_or_create(username=username)[0]
    u.password=password
    u.email=email
    u.save()
    u_profile = UserProfile.objects.get_or_create(user=u)[0]

    userObjects.append(u_profile)
    
    u_profile.save()
    return u_profile

#Execution begins here
if __name__ == '__main__':
    print('Starting MyStays population script...')
    populate()
            
