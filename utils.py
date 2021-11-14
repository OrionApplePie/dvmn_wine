def get_age_declension(number=0):
    """Правильное склонение слова 'год/лет'."""

    if number < 0 or type(number) is not int:
        raise ValueError('Number must be positive integer.')

    if number % 100 in range(11, 20):
        return 'лет'

    if number % 10 in range(2, 5):
        return 'года'

    if number % 10 == 1:
        return 'год'

    return 'лет'
