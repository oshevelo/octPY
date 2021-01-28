from datetime import *


class DiscountCartDto:

    nominal = None
    status = None
    valid_date_end = None
    cart = None
    code = None

    def get_nominal(self) -> float:
        return self.nominal

    def get_status(self) -> bool:
        return self.status

    def get_valid_date_end(self) -> datetime:
        return self.valid_date_end

    def get_cart(self) -> int:
        return self.cart

    def get_code(self) -> str:
        return self.code

    def set_nominal(self, nominal: float) -> None:
        self.nominal = nominal

    def set_status(self, status: bool) -> None:
        self.status = status

    def set_valid_date_end(self, valid_date_end: datetime) -> None:
        self.valid_date_end = valid_date_end

    def set_cart(self, cart: int) -> None:
        self.cart = cart

    def set_code(self, code: str) -> None:
        self.code = code
