from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("",views.Home,name="home-page"),
    path("product/",views.Product,name="product-page"),
    path("signup/",views.Signup,name="signup-page"),
    path("login/",views.Login,name="login-page"),
    path("about/",views.About,name="about-page"),
    path("contact/",views.Contact,name="contact-page"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('logout/', views.Logout, name='logout-page'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)