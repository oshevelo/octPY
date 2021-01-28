from discount.serializers import DiscountPostSerializer


class DiscountRequestAdapter:

    def adapt_serializer_data(self, serializer_data: DiscountPostSerializer) -> [str, int, float]:
        code = str(serializer_data.validated_data['code'])
        cart_number = int(serializer_data.validated_data['cart'])
        cart_amount = float(serializer_data.validated_data['amount_cart'])

        return code, cart_number, cart_amount

