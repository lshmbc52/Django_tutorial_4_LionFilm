from django.shortcuts import render
from .models import Film, Review, Comment
# Create your views here.
def review_list(request):
    # 리뷰 목록
    reviews = Review.objects.select_related('film', 'author').all()
    context = {
        'reviews':reviews
    }
    return render(request, 'film_review/review_list.html',context)