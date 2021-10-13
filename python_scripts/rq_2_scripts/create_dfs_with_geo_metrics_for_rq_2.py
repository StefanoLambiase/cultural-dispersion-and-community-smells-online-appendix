import certifi
import ssl

# Imports for geodispersion
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy import distance


# Geo Dispersion part
class CountryData:
    def __init__(self, country_name, latitude, longitude):
        self.country_name = country_name
        self.latitude = latitude
        self.longitude = longitude


def add_geo_dispersion_to_df():
    df =gb.get_projects_with_hofstede_df(gb.PROJECT_WITH_HOFSTEDE_DF_PATH)
    df = add_geo_distance_to_df(df)

    for index, row in df.iterrows():
        if row['geo_distance'] == 0.00:
            countries = row['countries'].split(',')

            result = False
            if len(countries) > 0:
                result = all(elem == countries[0] for elem in countries)
            if result:
                print("All Elements in List are Equal")
                if countries[0] == 'None':
                    df.loc[index, 'geo_distance'] = np.nan
            else:
                print("All Elements in List are Not Equal")

    df.to_csv('../../data/community_analysis/projects_with_cultural_and_geo_metrics.csv', sep=';', index=False)
    return df


def add_geo_distance_to_df(df):
    geo_distance_list = list()
    x = 0
    for index, row in df.iterrows():
        print('PROGRESS: ' + str(x) + '/' + str(len(df.index)))
        x += 1
        countries = row['countries'].split(',')

        if len(countries) > 1:
            country_data_list = list()
            print(len(countries))
            for country in countries:
                if country != 'None':
                    country_data_list.append(get_country_data(country))

            print(len(country_data_list))
            if len(country_data_list) > 1:
                i = 0
                distances_list = list()

                while i != (len(country_data_list) - 1):
                    for j in range(i + 1, len(country_data_list)):
                        location_1 = country_data_list[i]
                        location_2 = country_data_list[j]

                        dis = calculate_geo_distance(location_1, location_2)

                        if not np.isnan(dis):
                            distances_list.append(round(dis, 2))
                    i += 1

                if len(distances_list) > 1:
                    geo_distance = statistics.stdev(distances_list)
                    geo_distance_list.append(geo_distance)
                else:
                    geo_distance_list.append(np.nan)
            else:
                geo_distance_list.append(np.nan)
        elif countries[0] == 'None':
            geo_distance_list.append(np.nan)
        else:
            geo_distance_list.append(0.0)

    df['geo_distance'] = geo_distance_list
    return df


def get_country_data(country):
    for country_elem in country_set:
        if country_elem.country_name == country:
            return country_elem

    try:
        geolocator = Nominatim(user_agent="Stefano_thesis", scheme="http")
        location = geolocator.geocode(country)

        country_data = CountryData(country, location.latitude, location.longitude)

        country_set.add(country_data)
        return country_data
    except Exception as e:
        print("An exception occurred: ", e)
        return


def calculate_geo_distance(location_1, location_2):
    try:
        dis = distance.distance(
            (location_1.latitude, location_1.longitude),
            (location_2.latitude, location_2.longitude)
        ).miles

        return dis
    except Exception as e:
        print("An exception occurred: ", e)
        return np.nan

# ----------------------------------------

country_set = set()
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
add_geo_dispersion_to_df()
