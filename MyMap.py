import pandas
import geopandas
import folium

tables = pandas.read_csv("Population2021.txt")

# Creates a new variable and only takes the two columns mention below
tables = tables[['Country', 'Population']]

# https://geopandas.org/gallery/plotting_with_geoplot.html
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Deleting specific columns
# https://www.shanelynn.ie/using-pandas-dataframe-creating-editing-viewing-data-in-python/
world=world.drop(['pop_est', 'continent', 'iso_a3', 'gdp_md_est'], axis=1)

# Creates a new variable and only takes the two columns mention below
world=world[["name", "geometry"]]

# # Need to merge world and table data together so we can used both sets of data simultaniously
# Table data is what we want to use to colour each country
# World data has the coordinates
merge_data=world.merge(tables, how="left", left_on=['name'], right_on=['Country'])
# # to drop columns that have no values in them
merge_data=merge_data.dropna(subset=['Population'])
# merge_data=merge_data.dropna(subset=['Country'])
merge_data=merge_data.drop(["name"], axis=1)

# To display all the columns
pandas.set_option("Display.max_columns", 15)
# To display data all together and not on separate lines
pandas.set_option("Display.width", 1000)
# To display all the rows
pandas.set_option("Display.max_rows", 400)

# Folium documentation - https://python-visualization.github.io/folium/modules.html
map = folium.Map(location=[19.43, 13.17], zoom_start=2, tiles = "CartoDB positron", smooth_factor = 1)

data = pandas.read_csv("globalCapitalCities.txt")
# print(data.columns) # command prints only the columns
# puts all the data in "LON"/"LAT" columns in lists
lat = list(data["CapitalLatitude"])
lon = list(data["CapitalLongitude"])
CityName = list(data["CapitalName"])

fgc=folium.FeatureGroup(name="Capital Cities")
# Pass the elements of the data you want to read from find (variables above) as parameters for the For loop.
# Use the Zip method to read all the data from the list created
# you might experience errors with the 'el' variable because its a float type, just add str(el) and the error should disappear
for lt, ln, cc in zip(lat, lon, CityName):
    # Normal default markers
    fgc.add_child(folium.Marker(location=[lt, ln], popup="Capital City: " + str(cc), icon=folium.Icon(color='darkred')))

# To create a parameters for the border lines
# https://www.youtube.com/watch?v=h16O4xt6yBU
borderStyle = {
    'color' : 'black',
    'weight' : 0.3,
    'fillColor' : 'none',
    'fillOpacity' : 0.2
}

# Created a child for the feature group to add in the border lines required
fgl=folium.FeatureGroup(name="Lines")
fgl.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
style_function=lambda y:borderStyle))


def colorPicker(population):
    if population <= 10000000:
        return '#b6c1d5' # Light Grey/Blue more grey
    elif population >= 10000001 and population < 25000000:
        return '#99b5cd' # Light Blue/Grey more blue
    elif population >= 25000001 and population < 50000000:
        return '#779dc5' # Light Blue/Grey even more blue
    elif population >= 50000001 and population < 75000000:
        return '#5e85b6' # Purple/Grey even more blue
    elif population >= 75000001 and population < 200000000:
        return '#5063af' # Purple/Blue more purple
    elif population >= 200000001 and population < 400000000:
        return '#48429d' # Purple 
    elif population >= 1000000000:
        return '#3c2775' # Dark Purple


fgp=folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
               style_function = lambda x: {'fillColor': colorPicker(x['properties']['Population']), 'color':'none', "fillOpacity": 1},
               tooltip = folium.GeoJsonTooltip(fields=('NAME', 'Population'), aliases=('Country:','Population:'))))



map.add_child(fgc)
map.add_child(fgp)
map.add_child(fgl)

folium.LayerControl().add_to(map)


map.save("PopulationMap2021.html")