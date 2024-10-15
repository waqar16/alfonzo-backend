from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserDeleteView,
    UserActivityOverview,
    MFAUsageStatistics,
    RoleDistribution,
    TemplateOverview,
    MostUsedTemplatesByUser,
    MostUsedTemplatesByLawyer,
    TemplateListView,
    TemplateDetailView,
    CategoryListView,
    CategoryDetailView,
    SubCategoryListView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('analytics/user-activity/', UserActivityOverview.as_view(), name='user-activity-overview'),
    path('analytics/mfa-usage/', MFAUsageStatistics.as_view(), name='mfa-usage-statistics'),
    path('analytics/role-distribution/', RoleDistribution.as_view(), name='role-distribution'),
    path('analytics/templates-overview/', TemplateOverview.as_view(), name='template-overview'),
    path('analytics/most-used-templates-by-user/', MostUsedTemplatesByUser.as_view(), name='most-used-templates-by-user'),
    path('analytics/most-used-templates-by-lawyer/', MostUsedTemplatesByLawyer.as_view(), name='most-used-templates-by-lawyer'),
    path('templates/', TemplateListView.as_view(), name='template-list-create'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),
]
