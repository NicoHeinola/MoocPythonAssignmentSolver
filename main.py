import sys
from MoocAPI import MoocAPI
from DriverManager import DriverManager

if __name__ == '__main__':
    # Makes sure geckodriver is installed
    if not DriverManager.driver_exists():
        print("Geckodriver missing")
        download_driver = input("Do you want to download geckodriver? (Y/N)").lower()
        if download_driver == "y":
            DriverManager.download_driver()
        else:
            sys.exit()

    mooc_api = MoocAPI()
    while True:
        user: str = input("Username: ")
        password: str = input("Password: ")

        method: str = input("Get answers or solve assignments? (G/S)").lower()

        if method == "g":
            success: bool = mooc_api.get_answers(user, password)
        else:
            success: bool = mooc_api.set_answers(user, password)

        if success:
            print("Success!")
            break
        else:
            restart = input("There was an error! Do you want to restart? (Y/N)")
            if restart == "n":
                break
