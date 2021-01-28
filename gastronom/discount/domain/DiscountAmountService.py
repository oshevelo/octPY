import abc
from discount.domain.DiscountAmountServiceInterface import DiscountAmountInterface
from discount.domain.Dto import DiscountCartDto


class DiscountAmount(DiscountAmountInterface):

    def calculate_discount_amount_cart(self, cart_amount: float, discount_amount: float) -> float:
        total_discount_amount = round(float(cart_amount) - float(discount_amount), 2)

        if total_discount_amount < 0:
            return 0.0

        return total_discount_amount
        
        
       


class DiscountAmountInterface(abc.ABC):

    @abc.abstractmethod
    def calculate_discount_amount_cart(self, cart_amount: float, discount_amount: float) -> float:
        pass       
        
        
        


class DiscountRepositoryInterface(abc.ABC):

    @abc.abstractmethod
    def find_discount_cart_by_code(self, code: str) -> DiscountCartDto or None:
        pass

    @abc.abstractmethod
    def save_discount_cart(self, discount_info: DiscountCartDto) -> None:
        pass
