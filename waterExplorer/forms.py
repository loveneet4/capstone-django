from django import forms

# form for selecting by lake name
class NameForm(forms.Form):
    lake_name = forms.CharField(label = 'Lake Name', max_length = 50)


class AggSearchForm(forms.Form):

    # do not require any field, but be sure one (not 2 or 3) is selected in new clean method below
    country_name = forms.CharField(label = 'Country Name', max_length = 40, required=False) # eventually hopefully be finish text fill in based off country/geoname column contents
    region_name = forms.CharField(label = 'Region Name', max_length = 25, required=False) # drop down with options
    subregion_name = forms.CharField(label = 'Subregion Name', required=False) # drop down with options
    continent_name = forms.CharField(label = 'Continent Name', max_length = 23, required=False) # drop down with options 
    size_class = forms.IntegerField(label = 'Size Range (km^2)', required=False) # fill this out for now, will eventually be drop down of size classes hopefully
    water_type = forms.CharField(label = 'Water Body Type', required=False) # will eventually be drop down of options (no selection = all)    

    # override default clean method. only one of the above fields needs to be filled out
    # rules: at least one field has to be filled. the first 4 fields are mutually exclusive
    # can fill one of the first 4 and leave the size/type blank or fill it in as well
    # can also leave first four blank and fill in one or both of the last two
    #* how to deal with this in views? a lot of if's?


    def clean(self):
        cleaned_data = super(AggSearchForm, self).clean() # use built in clean method first
        country_name = cleaned_data.get("country_name")
        region_name = cleaned_data.get("region_name")
        continent_name = cleaned_data.get("continent_name")
        subregion_name = cleaned_data.get("subregion_name")        
        size_class = cleaned_data.get("size_class")
        water_type = cleaned_data.get("water_type")

        # check to be sure no more than one of the location-based fields is selected
        if (country_name and region_name) or (country_name and continent_name) or (region_name and continent_name) \
         or (country_name and subregion_name) or (region_name and subregion_name) or (continent_name and subregion_name): # better way to do this?

            raise forms.ValidationError('Please only fill in one of the following fields: Country Name, Region Name, Subregion Name, Continent Name')

        # check to be sure at least one of the 6 fields is selected
        if not (country_name or region_name or subregion_name or continent_name or size_class or water_type): # and 1 of the 6 needs to be selected
            raise forms.ValidationError('Please fill out at least one field') 