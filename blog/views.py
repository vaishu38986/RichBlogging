from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Subscription, BlogPost, UserSubscription, UserProfile
from .forms import BlogPostForm, SubscriptionForm


def home(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            posts = BlogPost.objects.all()  # Assuming you have a BlogPost model
            return render(request, 'blog/home.html', {'posts': posts, 'user_profile': user_profile})
        except UserProfile.DoesNotExist:
            return redirect('register')  # Redirect to register page if UserProfile doesn't exist
        except UserSubscription.DoesNotExist:
            return redirect('purchase_subscription')  # Redirect to purchase_subscription if UserSubscription doesn't exist
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            UserProfile.objects.get_or_create(user=user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'registration/login.html')


def create_post(request):
    if request.method == 'POST':
        
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.max_post > 0:
                    user_profile.max_post -= 1
                    user_profile.save()
            except UserProfile.DoesNotExist:
                # Handle case where UserProfile doesn't exist for the user
                pass

            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def subscription_plans(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.save()
            return redirect('home')
    else:
        form = SubscriptionForm()
    # plans = Subscription.objects.all()
    plans = Subscription.objects.all()
    print(plans) 
    return render(request, 'subscription/subscription_plans.html', {'plans': plans})
    # return render(request, 'blog/home.html', {'form': form})


def purchase_subscription(request):
#    def purchase_subscription(request):
    if request.method == 'POST':
        selected_plan = request.POST.get('plan')
        user = request.user
        
        # Get or create UserSubscription object for the user
        subscription, created = UserSubscription.objects.get_or_create(user=user)
        plans = Subscription.objects.all()
        for plan in plans:
            
            if selected_plan == plan.name:
                subscription.active = True
                subscription.premium_features = True
                subscription.save()

                user_profile, _ = UserProfile.objects.get_or_create(user=user)
                user_profile.subscription_status = plan.name
                user_profile.active_subscription = True
                user_profile.max_post=plan.max_post
                user_profile.save()

                return redirect('home')
            
        #     elif selected_plan == 'Basic':
        #         subscription.active = True
        #         subscription.max_posts = 10
        #         subscription.premium_features = False
        #         subscription.save()

        #         user_profile, _ = UserProfile.objects.get_or_create(user=user)
        #         user_profile.subscription_status = 'Basic'
        #         user_profile.active_subscription = True
        #         user_profile.save()
        #         return redirect('home')

        #     elif selected_plan == 'Standard Premium':
        #         subscription.active = True
        #         subscription.max_posts = 50
        #         subscription.premium_features = False
        #         subscription.save()

        #         user_profile, _ = UserProfile.objects.get_or_create(user=user)
        #         user_profile.subscription_status = 'Standard Premium'
        #         user_profile.active_subscription = True
        #         user_profile.save()

        # # Redirect to home page with a success message
        #     return redirect('home')

    plans = Subscription.objects.all()    
    return render(request, 'subscription/purchase_subscription.html', {'plans': plans})

