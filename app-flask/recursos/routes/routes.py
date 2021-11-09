from recursos.controllers.controller import *
from recursos.controllers.error import NotFoundController

routes = {
    "hello_route": "/", "hello_controller": HelloController.as_view("hello"),
    "not_found_route": 404, "not_found_controller": NotFoundController.as_view("not_found")
}
