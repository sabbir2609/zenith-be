from rest_framework_nested import routers
from .views import TaskView, StaffView, RoleView, InventoryView

app_name = "management"

router = routers.DefaultRouter()

# roles router
router.register("roles", RoleView, basename="roles")

# staff router
router.register("staff", StaffView, basename="staff")

# tasks router
router.register("tasks", TaskView, basename="tasks")

# inventory router
router.register("inventory", InventoryView, basename="inventory")

urlpatterns = router.urls
