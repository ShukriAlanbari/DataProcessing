from validations import Validation as Vald
class Location:
    def __init__(self, longitude, latitude, country):
        if Vald.validate_float(longitude):
            self.longitude = longitude
        else:
            raise ValueError("[!] Bad value - Enter the Longitude°.")
        if Vald.validate_float(latitude):
            self.latitude = latitude
        else:
            raise ValueError("[!] Bad value - Enter the Latitude°.")
        if Vald.validate_str_alpha(country):
            self.country = country
        else:
            raise ValueError("[!] Bad value - Enter the Country.")
    def __str__(self):
        return f"Lat:{self.latitude}°,Long:{self.longitude}°,"\
                f"Ctry:{self.country}"
