from django.test import TestCase
from mystays.models import Stay, UserProfile, Review
from django.contrib.auth.models import User
from django.urls import reverse

class StayModelTests(TestCase):
    #tests to make sure the stay slug is created properly
    def test_stay_slug(self):
        userProfile = createUserToPost()
        stay = Stay(name='Testing Stay Slugs', postedBy=userProfile)
        stay.save()

        self.assertEqual(stay.slug, 'testing-stay-slugs')

    #tests that the default rating for a stay without reviews is 0/10
    def test_overall_rating(self):
        userProfile = createUserToPost()
        stay = Stay(name='Testing Default Rating', postedBy=userProfile)
        stay.save()

        self.assertEqual((stay.propertyRating == 0), True)


class ReviewModelTests(TestCase):
    #tests that the default title for a review without it being set is 'Review'
    def test_default_title(self):
        userProfile = createUserToPost()
        s = add_stay('Stay', userProfile, 7)
        
        review = Review(stay=s, reviewedBy=userProfile)
        review.save()

        self.assertEqual((review.title == 'Review'), True)


class ViewTests(TestCase):
    #tests for the proper response from the homepage if there are no posted stays
    def test_homepage_with_no_stays(self):
        response = self.client.get(reverse('mystays:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There is nowhere to stay.')
        self.assertQuerysetEqual(response.context['best_stays'], [])

    #tests that the top five stays are shown on the homepage
    def test_homepage_popular_stays(self):
        userProfile = createUserToPost()
        add_stay('Third Stay', userProfile, 8)
        add_stay('Top Stay', userProfile, 10)
        add_stay('Fifth Stay', userProfile, 6)
        add_stay('Second Stay', userProfile, 9)
        add_stay('Fourth Stay', userProfile, 7)

        add_stay('Last Stay', userProfile, 5)

        response = self.client.get(reverse('mystays:home'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['best_stays'],
                                 ['<Stay: Top Stay>',
                                  '<Stay: Second Stay>',
                                  '<Stay: Third Stay>',
                                  '<Stay: Fourth Stay>',
                                  '<Stay: Fifth Stay>'])

    #tests that the about us page displays the correct message by checking for the first few words
    def test_about_us(self):
        response = self.client.get(reverse('mystays:about_us'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The objective of MyStays is to')

    #tests for the proper response from the where to stay page if there are no posted stays
    def test_empty_where_to_stay(self):
        response = self.client.get(reverse('mystays:where_to_stay'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There is nowhere to stay.')
        self.assertQuerysetEqual(response.context['stays'], [])

    #tests that the where to stay page displays the posted stays
    def test_where_to_stay(self):
        userProfile = createUserToPost()
        add_stay('Stay1', userProfile, 8)
        add_stay('Stay2', userProfile, 10)
        add_stay('Stay3', userProfile, 6)
        add_stay('Stay4', userProfile, 9)

        response = self.client.get(reverse('mystays:where_to_stay'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Stay1')
        self.assertContains(response, 'Stay2')
        self.assertContains(response, 'Stay3')
        self.assertContains(response, 'Stay4')

    def test_stay_without_reviews(self):
        userProfile = createUserToPost()
        stay = add_stay('Stay Without Review', userProfile)

        response = self.client.get(reverse('mystays:show_stay', kwargs={'stay_name_slug': stay.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Stay Without Review')
        self.assertContains(response, 'A hotel')
        self.assertContains(response, 'gmail@gmail.com')


class PopulationScriptTests(TestCase):
    #tests that the population script populates the intended stays to the database
    def test_stays_populated(self):
        populate_database()
        
        stays = Stay.objects.filter()

        stay_names = map(str, stays)

        self.assertTrue('Sanctum Resort' in stay_names)
        self.assertTrue('Sunrise Hostel' in stay_names)
        self.assertTrue('Riverside Inn' in stay_names)
        self.assertTrue('Northern Country Inn' in stay_names)
        self.assertTrue('Purple Rose Hotel' in stay_names)
        self.assertTrue('Horizons Hotel' in stay_names)

    #tests that the population script populates the intended reviews to the database
    def test_reviews_populated(self):
        populate_database()
        
        reviews = Review.objects.filter()

        review_names = map(str, reviews)

        self.assertTrue('Great hotel!' in review_names)
        self.assertTrue('Nice enough' in review_names)
        self.assertTrue('Beautiful!' in review_names)
        self.assertTrue('A Nice Place to Stay' in review_names)
        self.assertTrue('Not great' in review_names)
        self.assertTrue('Average' in review_names)

    #tests that the population script populates the intended users to the database
    def test_users_populated(self):
        populate_database()
        
        users = UserProfile.objects.filter()

        usernames = map(str, users)

        self.assertTrue('username1' in usernames)
        self.assertTrue('username2' in usernames)


#helper function to create a user
def createUserToPost():
    u = User.objects.get_or_create(username='username')[0]
    u.password='mystaysproject123'
    u.email='2517529M@student.gla.ac.uk'
    u.save()
    u_profile = UserProfile.objects.get_or_create(user=u)[0]
    u_profile.save()

    return u_profile

#helper function to add a stay to the database
def add_stay(name, user, rating=0):
    stay = Stay.objects.get_or_create(name=name, postedBy=user)[0]
    stay.propertyRating = rating
    stay.price = 55
    stay.description = 'A hotel'
    stay.latitude = 55.8642
    stay.longitude = 4.2518
    stay.picture = 'stay_images/default.jpg'
    stay.contacts = 'gmail@gmail.com'
    stay.keyword = 'Glasgow'

    stay.save()
    return stay

#helper function to run the population script
def populate_database():
    try:
        import population_script
    except ImportError:
        raise ImportError(f"{FAILURE_HEADER}The population script could not be imported")

    population_script.populate()



