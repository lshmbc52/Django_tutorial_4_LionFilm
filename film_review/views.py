from django.shortcuts import render, get_object_or_404, redirect
from .models import Film, Review, Comment
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, CommentForm
from django.views import generic

def review_list(request):
    # 리뷰 목록
    reviews = Review.objects.select_related('film', 'author').all()
    context = {
        'reviews':reviews
    }
    return render(request, 'film_review/review_list.html',context)

def review_detail(request, pk):
    # get방식으로 들어오면 그냥 페이지 보여주기
    # 그런데 내부적으로 댓글을 위한 폼이 있습니다
    # 폼의 submit 버튼을 누르면
    # post방식으로 같은 주소(이 review_detail view)로 오되
    # post로 처리할때 방식을 정의하면 되겠습니다.
    if request.method == 'GET':
        review = Review.objects.select_related('film', 'author').get(pk=pk)
        # Comment 입력을 위한 form
        comment_form = CommentForm()
        context = {
            'review':review,            
            'comment_form':comment_form
            }
        return render(request, 'film_review/review_detail.html', context)
    else:
        # 여기서는 comment 입력 처리가 이루어 집니다.
        review=get_object_or_404(Review.objects.select_related('author'), pk=pk)
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review=review
            comment.author=request.user
            comment.save()
            return redirect('review-detail', pk=pk)        

@login_required
def review_create(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.film = film
            review.save()
            return redirect('review-detail', pk=review.pk)
    else:
        form = ReviewForm(initial={'film': film})
    
    return render(request, 'film_review/review_form.html', {
        'form': form,
        'film': film
    })

class FilmListView(generic.ListView):
    model = Film
    template_name = 'film_review/film_list.html'
    context_object_name = 'films'
    paginate_by = 12

    def get_queryset(self):
        queryset = Film.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset.order_by('title')