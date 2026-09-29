import random

MISSING_ACCOUNT_ID = 999999999

class DepositDataGenerator:
    MIN_AMOUNT = 1000
    MAX_AMOUNT = 9000

    @staticmethod
    def valid_amount() -> float:
        return round(random.uniform(DepositDataGenerator.MIN_AMOUNT, DepositDataGenerator.MAX_AMOUNT), 2)

    @staticmethod
    def invalid_amount() -> float:
        if random.choice([True, False]):
            return round(random.uniform(-1000, DepositDataGenerator.MIN_AMOUNT - 0.01), 2)
        return round(random.uniform(DepositDataGenerator.MAX_AMOUNT + 0.01, DepositDataGenerator.MAX_AMOUNT * 2), 2)


class TransferDataGenerator:
    MIN_AMOUNT = 500
    MAX_AMOUNT = 10000

    @staticmethod
    def valid_amount() -> float:
        return round(random.uniform(TransferDataGenerator.MIN_AMOUNT, TransferDataGenerator.MAX_AMOUNT), 2)

    @staticmethod
    def valid_amount_up_to(limit: float) -> float:
        upper = min(TransferDataGenerator.MAX_AMOUNT, limit)
        return round(random.uniform(TransferDataGenerator.MIN_AMOUNT, upper), 2)

    @staticmethod
    def invalid_amount() -> float:
        if random.choice([True, False]):
            return round(random.uniform(-1000, TransferDataGenerator.MIN_AMOUNT - 0.1), 2)
        return round(random.uniform(TransferDataGenerator.MAX_AMOUNT + 0.1, TransferDataGenerator.MAX_AMOUNT * 2), 2)


class CreditDataGenerator:
    MIN_AMOUNT = 5000
    MAX_AMOUNT = 15000
    MIN_TERM_MONTHS = 1
    MAX_TERM_MONTHS = 60

    @staticmethod
    def valid_amount() -> float:
        return round(random.uniform(CreditDataGenerator.MIN_AMOUNT, CreditDataGenerator.MAX_AMOUNT), 2)

    @staticmethod
    def invalid_amount() -> float:
        if random.choice([True, False]):
            return round(random.uniform(-1000, CreditDataGenerator.MIN_AMOUNT - 0.01), 2)
        return round(random.uniform(CreditDataGenerator.MAX_AMOUNT + 0.01, CreditDataGenerator.MAX_AMOUNT * 2), 2)

    @staticmethod
    def valid_term_months() -> int:
        return random.randint(CreditDataGenerator.MIN_TERM_MONTHS, CreditDataGenerator.MAX_TERM_MONTHS)

