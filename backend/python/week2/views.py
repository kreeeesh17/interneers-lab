# view : code that runs when a client hits an endpoint i.e receives http request and decides what to do
# eg GET/products/, PUT/products/1

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .store import product_store


class ProductListCreateAPIView(APIView):
    # list all product
    def get(self, request):
        products = product_store.list_all()
        product_data = []
        for product in products:
            product_data.append(product.to_dict())
        # output serialisation
        # without many = true DRF would expect one product
        serializer = ProductSerializer(product_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a product
    def post(self, request):
        # input serialisation
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = product_store.create(serializer.validated_data)
            response_serializer = ProductSerializer(product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    # get specific product
    def get(self, request, product_id):
        product = product_store.get(product_id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(product.to_dict())
            return Response(serializer.data, status=status.HTTP_200_OK)

    # update one product
    def put(self, request, product_id):
        existing_product = product_store.get(product_id)
        if not existing_product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND,)
        else:
            # validate new data first
            serializer = ProductSerializer(data=request.data)
            if (serializer.is_valid()):
                updated_product = product_store.update(
                    product_id, serializer.validated_data)
                response_serializer = ProductSerializer(
                    updated_product.to_dict())
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete data
    def delete(self, request, product_id):
        deleted = product_store.delete(product_id)
        if not deleted:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND,)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
