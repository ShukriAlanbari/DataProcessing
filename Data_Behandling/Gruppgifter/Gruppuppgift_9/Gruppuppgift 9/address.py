from validations import Validation as Vald

class Address:
    def __init__(self, street_name:str,
                house_apt_num:str,
                zip_code:int,
                city_name:str) -> None:
        
        if Vald.validate_str_alpha(street_name):
            self.street_name = street_name
        else:
            raise ValueError("[!] Bad Value - Street name")
        if Vald.validate_is_alnum(house_apt_num):
            self.house_apt_num = house_apt_num
        else:
            raise ValueError("[!] Bad Value - House or Apartment number")
        if Vald.validate_int(zip_code):
            self.zip_code = zip_code
        else:
            raise ValueError("[!] Bad Value - Zip code")
        if Vald.validate_str_alpha(city_name):
            self.city_name = city_name
        else:
            raise ValueError("[!] Bad Value - City name")

    def __str__(self):
        return f"{self.street_name}, {self.house_apt_num},"\
            f" {self.zip_code}, {self.city_name}"