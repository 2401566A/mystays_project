from django import forms
from mystays.models import Stay, Review, UserProfile, User

#form to upload a stay to the database
class StayForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Name of the stay:")
    picture = forms.ImageField(help_text="Picture of the stay:")
    price = forms.DecimalField(help_text="Starting price of a night in the stay:")
    propertyRating = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    description = forms.CharField(max_length=255, help_text="Brief description:")
    latitude = forms.DecimalField(help_text="Latitude:")
    longitude = forms.DecimalField(help_text="longitude:")
    contacts = forms.CharField(max_length=100, help_text="Contact information:")

    keyword = forms.CharField(max_length=50, help_text="Closest city or town to the stay:")    

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Stay
        fields = ('name', 'picture', 'price', 'description', 'latitude', 'longitude', 'keyword', 'contacts')


#form to leave a review for a stay
class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Review title:")
    comment = forms.CharField(help_text="Please leave a detailed comment about your stay:")
    
    impression = forms.IntegerField(help_text="Overall impression (10=highest, 1=lowest):")
    locationRating = forms.IntegerField(help_text="Location (10=highest, 1=lowest):")
    cleanliness = forms.IntegerField(help_text="Cleanliness (10=highest, 1=lowest):")
    descripAccuracy = forms.IntegerField(help_text="Accuracy of online description (10=highest, 1=lowest):")
    costRating = forms.IntegerField(help_text="Rate the value of the stay relative to the cost (10=highest, 1=lowest):")

    class Meta:
        model = Review
        exclude = ('stay', 'reviewedBy',)

#form to fill in the username, email, and password of a new user
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


#form to fill in the profile picture of a new user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class SearchForm(forms.Form):
    keyword = forms.CharField(help_text="Where would you like to stay?")
