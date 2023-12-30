from rest_framework_nested import routers
from .views import TaskView

app_name = "management"

router = routers.DefaultRouter()

# tasks router
router.register("tasks", TaskView, basename="tasks")

urlpatterns = router.urls
