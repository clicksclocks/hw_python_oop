from dataclasses import dataclass
from typing import Dict, Type, Optional


@dataclass(repr=False, eq=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOURS_TO_MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories '
                                  f'в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: InfoMessage = InfoMessage(type(self).__name__,
                                           self.duration,
                                           self.get_distance(),
                                           self.get_mean_speed(),
                                           self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_SPEED_MULTIPLIER: int = 18
    CALORIES_SPEED_SUBTRACTOR: int = 20

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 - self.CALORIES_SPEED_SUBTRACTOR)
                                 * self.weight
                                 / self.M_IN_KM
                                 * self.duration
                                 * self.HOURS_TO_MINUTES)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_FORCE_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                 * self.weight
                                 + (self.get_mean_speed()**2 // self.height)
                                 * self.CALORIES_FORCE_MULTIPLIER
                                 * self.weight)
                                 * self.duration
                                 * self.HOURS_TO_MINUTES)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_SPEED_ADDITER: float = 1.1
    CALORIES_PULSE_MULTPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.get_mean_speed()
                                 + self.CALORIES_SPEED_ADDITER)
                                 * self.CALORIES_PULSE_MULTPLIER
                                 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    workout_types_dict: Dict[str, Type[Training]]
    workout_types_dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking}
    try:
        return workout_types_dict[workout_type](*data)
    except KeyError:
        print(f'Тип тренировки {workout_type} не найден.')
    except TypeError:
        print('Неверное представление данных о тренировке.')
    return None


def main(training: Training) -> None:
    """Главная функция."""
    if training is not None:
        info: InfoMessage = training.show_training_info()
        message: str = info.get_message()
        print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('BOX', [400, 1]),
        ('WLK', [6000, 1, 60])
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
