from datetime import date, datetime

from flask_admin.contrib.sqla import ModelView

from wtforms.validators import DataRequired, Email

from app import admin, db
from app.models import Product, Category, User, CartProduct, Cart, Order, CategoryFeature, ProductFeature, Testimonial


def date_format(view, value):
    if type(value) == date:
        return value.strftime('%d-%m-%Y')
    return value.strftime('%d-%m-%Y %H:%M:%S')


class UserAdmin(ModelView):
    """ User admin editor """
    can_delete = False
    column_list = ('id', 'username', 'email')
    column_sortable_list = ('id', 'username', 'email')
    column_searchable_list = ('username', 'email')
    column_labels = {
        'cart_product': 'Cart products',
        'cart_id': 'Carts',
        'order': 'Orders',
        'testimonial': 'Testimonials'
    }
    form_columns = ('username', 'email', 'cart_product', 'cart_id', 'order', 'testimonial', 'password_hash')
    form_args = {
        'username': {
            'validators': [DataRequired()]
        },
        'email': {
            'validators': [DataRequired(), Email()]
        }
    }
    form_widget_args = {
        'password_hash': {
            'disabled': True
        },
        'cart_product': {
            'disabled': True
        },
        'cart_id': {
            'disabled': True
        },
        'order': {
            'disabled': True
        },
        'testimonial': {
            'disabled': True
        }
    }


class CategoryAdmin(ModelView):
    """ Category admin editor """
    can_delete = False
    column_list = ('id', 'name', 'slug')
    column_sortable_list = ('id', 'name', 'slug')
    column_searchable_list = ('name', 'slug')
    column_labels = {'feature': 'Features'}
    form_columns = ('name', 'slug', 'products', 'feature')
    form_args = {
        'name': {
            'validators': [DataRequired()]
        },
        'slug': {
            'validators': [DataRequired()]
        }
    }


class ProductAdmin(ModelView):
    """ Product admin editor """
    can_delete = False
    edit_template = 'admin/edit_product.html'
    column_list = ('id', 'category.name', 'title', 'slug', 'price')
    column_sortable_list = ('id', 'title', 'slug', 'price', 'category.name')
    column_searchable_list = ('title', 'description', 'slug', 'price', 'category.name')
    column_labels = {
        'category.name': 'Category',
        'feature_id': 'Features',
        'image_path': 'Image'
    }
    form_columns = ('title', 'slug', 'category', 'description', 'price', 'image_path', 'feature_id')
    form_args = {
        'title': {
            'validators': [DataRequired()]
        },
        'slug': {
            'validators': [DataRequired()]
        },
        'category': {
            'validators': [DataRequired()]
        },
        'description': {
            'validators': [DataRequired()]
        },
        'price': {
            'validators': [DataRequired()]
        }
    }
    form_widget_args = {
        'image_path': {
            'disabled': True
        }
    }


class CartAdmin(ModelView):
    """ Cart admin editor """
    can_create = False
    can_delete = False
    column_list = ('id', 'owner.username', 'total_products', 'final_price', 'for_anonymous_user', 'in_order')
    column_sortable_list = ('id', 'owner.username', 'total_products', 'final_price', 'for_anonymous_user', 'in_order')
    column_searchable_list = ('owner.username', 'total_products', 'final_price')
    column_labels = {
        'owner.username': 'Owner'
    }
    form_columns = ('owner', 'total_products', 'final_price', 'for_anonymous_user', 'in_order', 'order', 'products')
    form_widget_args = {
        'owner': {
            'disabled': True
        },
        'total_products': {
            'disabled': True
        },
        'final_price': {
            'disabled': True
        },
        'for_anonymous_user': {
            'disabled': True
        },
        'in_order': {
            'disabled': True
        },
        'order': {
            'disabled': True
        },
        'products': {
            'disabled': True
        }
    }


class CartProductAdmin(ModelView):
    """ CartProduct admin editor """
    can_create = False
    can_delete = False
    column_list = ('id', 'user.username', 'cart.id', 'product.title', 'qty', 'final_price')
    column_sortable_list = ('id', 'user.username', 'cart.id', 'product.title', 'qty', 'final_price')
    column_searchable_list = ('user.username', 'product.title', 'final_price')
    column_labels = {
        'user.username': 'User',
        'cart.id': 'Cart ID',
        'product.title': 'Product',
        'qty': 'Quantity'
    }
    form_columns = ('user', 'cart', 'product', 'qty', 'final_price')
    form_widget_args = {
        'user': {
            'disabled': True
        },
        'cart': {
            'disabled': True
        },
        'product': {
            'disabled': True
        },
        'qty': {
            'disabled': True
        },
        'final_price': {
            'disabled': True
        }
    }


class OrderAdmin(ModelView):
    """ Order admin editor """
    can_create = False
    can_delete = False
    column_list = ('id', 'user.username', 'cart.id', 'first_name', 'last_name', 'phone',
                   'address', 'buying_type', 'order_date', 'created_at')
    column_type_formatters = {datetime: date_format, date: date_format}
    column_sortable_list = ('id', 'user.username', 'cart.id', 'first_name', 'last_name', 'phone',
                            'address', 'buying_type', 'order_date', 'created_at')
    column_searchable_list = ('user.username', 'first_name', 'last_name', 'phone', 'address', 'buying_type')
    column_labels = {
        'user.username': 'User',
        'cart.id': 'Cart ID',
        'created_at': 'Created'
    }
    form_choices = {
        'buying_type': [
            ('self', 'self'),
            ('delivery', 'delivery'),
        ]
    }
    form_columns = ('user', 'cart', 'first_name', 'last_name', 'phone', 'address', 'buying_type',
                    'comment', 'order_date', 'created_at')
    form_args = {
        'created_at': {
            'format': '%d-%m-%Y %H:%M:%S'
        },
        'order_date': {
            'format': '%d-%m-%Y'
        }
    }
    form_widget_args = {
        'user': {
            'disabled': True
        },
        'cart': {
            'disabled': True
        },
        'first_name': {
            'disabled': True
        },
        'last_name': {
            'disabled': True
        },
        'phone': {
            'disabled': True
        },
        'address': {
            'disabled': True
        },
        'buying_type': {
            'disabled': True
        },
        'comment': {
            'disabled': True
        },
        'order_date': {
            'disabled': True
        },
        'created_at': {
            'disabled': True
        }
    }


class CategoryFeatureAdmin(ModelView):
    """ CategoryFeature admin """
    column_list = ('id', 'category.name', 'feature_name', 'unit')
    column_sortable_list = ('id', 'category.name', 'feature_name', 'unit')
    column_searchable_list = ('category.name', 'feature_name', 'unit')
    column_labels = {
        'category.name': 'Category'
    }
    form_columns = ('category', 'feature_name', 'unit', 'feature_products')
    form_args = {
        'category': {
            'validators': [DataRequired()]
        },
        'feature_name': {
            'validators': [DataRequired()]
        }
    }


class ProductFeatureAdmin(ModelView):
    """ ProductFeature admin editor """
    column_list = ('id', 'product.title', 'feature.feature_name', 'value', 'feature.unit')
    column_sortable_list = ('id', 'product.title', 'feature.feature_name', 'value', 'feature.unit')
    column_searchable_list = ('product.title', 'feature.feature_name', 'value', 'feature.unit')
    column_labels = {
        'product.title': 'Product',
        'feature.feature_name': 'Feature name',
        'feature.unit': 'Unit'
    }
    form_columns = ('product', 'feature', 'value')
    form_args = {
        'product': {
            'validators': [DataRequired()]
        },
        'feature': {
            'validators': [DataRequired()]
        },
        'value': {
            'validators': [DataRequired()]
        }
    }


class TestimonialAdmin(ModelView):
    """ Testimonial admin editor """
    column_list = ('id', 'user.username', 'appraisal', 'created_at')
    column_sortable_list = ('id', 'user.username', 'appraisal', 'created_at')
    column_searchable_list = ('user.username',)
    column_type_formatters = {datetime: date_format}
    column_labels = {
        'created_at': 'Created',
        'user.username': 'User'
    }
    form_columns = ('user', 'appraisal', 'comment', 'created_at')
    form_args = {
        'created_at': {
            'format': '%d-%m-%Y %H:%M:%S'
        },
        'user': {
            'validators': [DataRequired()]
        },
        'appraisal': {
            'validators': [DataRequired()]
        }
    }
    form_widget_args = {
        'created_at': {
            'disabled': True
        }
    }


admin.add_view(UserAdmin(User, db.session, name='Users'))
admin.add_view(CategoryAdmin(Category, db.session, name='Categories'))
admin.add_view(CategoryFeatureAdmin(CategoryFeature, db.session, name='Features for categories'))
admin.add_view(ProductAdmin(Product, db.session, name='Products'))
admin.add_view(ProductFeatureAdmin(ProductFeature, db.session, name='Features for products'))
admin.add_view(CartAdmin(Cart, db.session, name='Carts'))
admin.add_view(CartProductAdmin(CartProduct, db.session, name='Products in carts'))
admin.add_view(OrderAdmin(Order, db.session, name='Orders'))
admin.add_view(TestimonialAdmin(Testimonial, db.session, name='Testimonials'))
