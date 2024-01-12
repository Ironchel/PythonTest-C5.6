from extensions import ComputationBot


class ApiException(Exception):

    @staticmethod
    def check_number(number):
        try:
            if float(number) < 0:
                pass
        except Exception:
            raise ApiException(
                'Введите пожалуйста сумму больше нуля и цыфрами\n'
                'Пример: "90" или "178.5"')


class ServerException(Exception):

    @staticmethod
    def check_values():
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
        try:
            check_tracking = ComputationBot.show_tracking()
            if not check_tracking:
                raise ServerException('Данные не получены')
        except Exception as e:
            raise ServerException(f'{e}')
        else:
            return check_tracking
