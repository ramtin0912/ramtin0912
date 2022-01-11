from marshmallow import Schema, fields

class TransactionFormSchema(Schema):
    ID = fields.Int()
    user_id = fields.Int()
    amount = fields.Int()
    type = fields.Bool()
    time = fields.DateTime()

class CreateUserFormSchema(Schema):
    ID = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    balance = fields.Int(required=False)
    is_admin = fields.Bool(required=False)

class CreateTransactionFormSchema(Schema):
    amount = fields.Int(required=True)
    type = fields.Bool(required=True)

class UpdateUserFormSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=False)

class UpdateUserBalanceFormSchema(Schema):
    balance = fields.Int(required=True)

class ConfirmFormSchema(Schema):
    confirm = fields.Str(required=True)

class LoginInputSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)