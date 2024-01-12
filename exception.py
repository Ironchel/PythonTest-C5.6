from extensions import ComputationBot


class ApiException(Exception):
    """The class is created to display user errors"""
    @staticmethod
    def check_number(number):
        """The function checks the amount entered by the user"""
        try:
            if float(number) < 0:
                pass
        except Exception:
            raise ApiException(
                'Введите пожалуйста сумму больше нуля и цыфрами\n'
                'Пример: "90" или "178.5"')


class ServerException(Exception):
    """The class is created to display server errors"""
    @staticmethod
    def check_values():
        """The function checks for errors connecting to the redis database"""
        try:
            check_values = ComputationBot.get_values()
            if not check_values:
                raise ServerException('Данные не получены')
        except Exception as e:
            raise ServerException(f'{e}')
        else:
            return check_values

    @staticmethod
    def check_tracking():
        """The function checks for errors connecting to the redis database"""
        try:
            check_tracking = ComputationBot.show_tracking()
            if not check_tracking:
                raise ServerException('Данные не получены')
        except Exception as e:
            raise ServerException(f'{e}')
        else:
            return check_tracking
