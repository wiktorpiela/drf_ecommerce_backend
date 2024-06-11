from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from product.models import Product

class NewOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        data = request.data

        order_items = data['order_items']

        if order_items and len(order_items)==0:
            return Response({'error': 'No order items. Please add at least one product'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # create order
            total = sum(item['price'] * item['quantity'] for item in order_items)
            order = Order.objects.create(
                user=user,
                street=data['street'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code'],
                phone_no=data['phone_no'],
                country=data['country'],
                total_amount=total
            )

            # create order items and set order to order items
            for i in order_items:
                try:
                    product = Product.objects.get(id=i['product'])
                    item = OrderItem.objects.create(
                        product=product,
                        order=order,
                        name=product.name,
                        quantity=i['quantity'],
                        price=i['price'],
                    )

                    # update product stock
                    product.stock -= item.quantity
                    product.save()
                    print('here ----------------------------------------------------------------------------------------------')
                except Product.DoesNotExist:
                    return Response({'error': f"Product of id {i['product']} doesn't exist."})

            print(order.total_amount)
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)

