from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

# List of random words for the getnextcandidate endpoint
RANDOM_WORDS = [
    "Pizza", "Mountain", "Ocean", "Guitar", "Elephant", "Rainbow", 
    "Robot", "Symphony", "Diamond", "Waterfall", "Butterfly", 
    "Starlight", "Jupiter", "Python", "Django", "Harmony", 
    "Volcano", "Chocolate", "Telescope", "Adventure"
]

@api_view(['GET'])
def index(request):
    """
    Serve the index.html template when the root API is accessed.
    """
    return render(request, 'index.html')

@api_view(['GET'])
def hello_api(request):
    """
    A simple API endpoint to demonstrate DRF functionality
    """
    return Response({"message": "Hello from the API!"})

@api_view(['POST'])
def goodswipe(request):
    """
    API endpoint for handling a positive swipe
    """
    # In a real app, you would typically process the data from request.data
    # For example, save the positive interaction to a database
    return Response({
        "status": "success", 
        "message": "Positive swipe recorded",
        "data": request.data
    })

@api_view(['POST'])
def badswipe(request):
    """
    API endpoint for handling a negative swipe
    """
    # In a real app, you would process the negative interaction
    return Response({
        "status": "success", 
        "message": "Negative swipe recorded",
        "data": request.data
    })

@api_view(['GET'])
def getnextcandidate(request):
    """
    API endpoint that returns a random word as the next candidate
    """
    random_word = random.choice(RANDOM_WORDS)
    return Response({
        "status": "success",
        "candidate": random_word,
        "id": random.randint(1, 1000)  # Adding a random ID for demo purposes
    })
