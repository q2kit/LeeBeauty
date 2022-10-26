from django.db import models

# Create your models here.


class Province(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "provinces"

    def to_json(self):
        return {"id": self.id, "name": self.name}

    def __str__(self):
        return f"{self.id} - {self.name}"


class District(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = "districts"

    def to_json(self):
        return {"id": self.id, "name": self.name}

    def __str__(self):
        return f"{self.id} - {self.name}"


class Commune(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    class Meta:
        db_table = "communes"

    def to_json(self):
        return {"id": self.id, "name": self.name}

    def __str__(self):
        return f"{self.id} - {self.name}"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "users"

    def to_json(self):
        return {
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
        }

    def __str__(self):
        return f"{self.email} - {self.phone}"

    def orders(self):
        return Order.objects.filter(user=self)


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def sub_categories(self):
        return Category.objects.filter(parent=self)

    @property
    def products(self):
        products = Product.objects.filter(category=self)
        for sub_category in self.sub_categories:
            products += sub_category.products

    class Meta:
        db_table = "categories"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent.to_json() if self.parent else None,
        }

    def __str__(self):
        if self.parent:
            return f"{self.parent} - {self.name}"
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    receiver_name = models.CharField(max_length=100, null=True)
    receiver_phone = models.CharField(max_length=100, null=True)
    receiver_address = models.CharField(max_length=100, null=True)
    receiver_province = models.ForeignKey(
        Province, on_delete=models.SET_NULL, null=True
    )
    receiver_district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True
    )
    receiver_commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True)

    status_choices = [
        ("pending", "Đang chờ xử lý"),
        ("processing", "Đang xử lý"),
        ("shipping", "Đang giao hàng"),
        ("delivered", "Đã giao hàng"),
        ("canceled", "Đã hủy"),
    ]

    status = models.CharField(max_length=100, choices=status_choices, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def products(self):
        return OrderProduct.objects.filter(order=self)

    @property
    def total(self):
        return sum([p.total for p in self.products])

    class Meta:
        db_table = "orders"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="image/products", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def images(self):
        return ProductImage.objects.filter(product=self)

    class Meta:
        db_table = "products"

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "category": self.category.to_json(),
            "number_available": self.number_available,
        }


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    size_choices = [
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL"),
        ("27", "27"),
        ("28", "28"),
        ("29", "29"),
        ("30", "30"),
        ("31", "31"),
        ("32", "32"),
        ("33", "33"),
    ]

    color_choices = [
        ("black", "Đen"),
        ("white", "Trắng"),
        ("red", "Đỏ"),
        ("blue", "Xanh Dương"),
        ("yellow", "Vàng"),
        ("green", "Xanh Lá"),
        ("pink", "Hồng"),
        ("gray", "Xám"),
        ("brown", "Nâu"),
        ("purple", "Tím"),
        ("orange", "Cam"),
        ("moss", "Xanh Rêu"),
    ]

    size = models.CharField(max_length=100, choices=size_choices)
    color = models.CharField(max_length=100, choices=color_choices)

    number_available = models.IntegerField()

    class Meta:
        db_table = "product_details"

    def __str__(self):
        return f"{self.product} - {self.size} - {self.color} - {self.number_available}"



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def total(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = "order_products"

    def to_json(self):
        return {
            "order": self.order.to_json(),
            "product": self.product.to_json(),
            "quantity": self.quantity,
        }

    def __str__(self):
        return f"{self.order} - {self.product}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)

    class Meta:
        db_table = "product_images"

    def to_json(self):
        return {"product": self.product.to_json(), "image": self.image}

    def __str__(self):
        return f"{self.product} - {self.image}"


class CartProduct(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart_products"
    )
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def total(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = "cart_products"

    def to_json(self):
        return {
            "cart": self.cart.to_json(),
            "product": self.product.to_json(),
            "quantity": self.quantity,
        }

    def __str__(self):
        return f"{self.cart} - {self.product}"
