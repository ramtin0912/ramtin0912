from app.api import api
from app.api.repositories.admin import GetAllUsers, GetUserById, GetUserTransactions, CreateUser, SetTransaction ,\
UpdateUser ,UpdateUserBalance, DeleteUser, DeleteUserTransaction

from app.api.repositories.auth import LoginUser, LoginAdmin, Register

from app.api.repositories.user import GetUserInfo, GetUserTransactionsInfo, MakeTransaction, UpdateUserInfo, SelfDelete

# ADMIN
api.add_url_rule("/admin/users", view_func = GetAllUsers, methods=["GET"])
api.add_url_rule("/admin/users/<int:id>", view_func = GetUserById, methods=["GET"])
api.add_url_rule("/admin/users/<int:id>/transactions", view_func = GetUserTransactions, methods=["GET"])
api.add_url_rule("/admin/users", view_func = CreateUser, methods=["POST"])
api.add_url_rule("/admin/users/<int:id>/transactions", view_func = SetTransaction, methods=["POST"])
api.add_url_rule("/admin/users/<int:id>", view_func = UpdateUser, methods=["PUT"])
api.add_url_rule("/admin/users/<int:id>", view_func = UpdateUserBalance, methods=["PATCH"])
api.add_url_rule("/admin/users/<int:id>", view_func = DeleteUser, methods=["DELETE"])
api.add_url_rule("/admin/users/<int:id>/transaction/<int:t_id>", view_func = DeleteUserTransaction, methods=["DELETE"])

# AUTH
api.add_url_rule("/login", view_func = LoginUser, methods=["POST"])
api.add_url_rule('/admin/login', view_func = LoginAdmin, methods=["POST"])
api.add_url_rule("/register", view_func = Register, methods=["POST"])

# Users
api.add_url_rule("/users", view_func = GetUserInfo, methods=["GET"])
api.add_url_rule("/users/transactions", view_func = GetUserTransactionsInfo, methods=["GET"])
api.add_url_rule("/users/transactions", view_func = MakeTransaction, methods=["POST"])
api.add_url_rule("/users", view_func = UpdateUserInfo, methods=["PUT"])
api.add_url_rule("/users", view_func = SelfDelete, methods=["DELETE"])
api.add_url_rule("/admin/users", view_func = GetAllUsers, methods=["GET"])
api.add_url_rule("/admin/users", view_func = GetAllUsers, methods=["GET"])