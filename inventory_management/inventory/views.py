from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache

@api_view(['POST'])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_item(request, item_id):
    cached_item = cache.get(f'item_{item_id}')
    if cached_item:
        return Response(cached_item)
    
    try:
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item)
        cache.set(f'item_{item_id}', serializer.data)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete(f'item_{item_id}')  # Invalidate cache
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        cache.delete(f'item_{item_id}')  # Invalidate cache
        return Response({'message': 'Item deleted'}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
