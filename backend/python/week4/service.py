# bridge between views and repository ( business logic layer )
from .repository import product_category_repository, product_repository
from .csv_helper import read_csv_file


# some rules used
# 1. brand is compulsary now
# 2. if category is missing use Miscellaneous
# 3. category title should be unique
# 4. category cannot be deleted if products belong to it
# 5. CSV rows should be validated before insertion


# category related business logic
class ProductCategoryService:
    # creating category
    def create(self, data):
        existing_category = product_category_repository.get_by_title(
            data["title"])
        if existing_category:
            return {"error": "Category with this title already exists"}

        return product_category_repository.create(data)

    # get category by id
    def get(self, id):
        return product_category_repository.get(id)

    # list all categories
    def list_all(self, filters=None, sort_by=None):
        return product_category_repository.list_all(filters=filters, sort_by=sort_by)

    # update category
    def update(self, id, data):
        category = product_category_repository.get(id)
        if not category:
            return {"error": "Category not found"}
        # avoid duplicating
        existing_category = product_category_repository.get_by_title(
            data["title"])
        if existing_category and existing_category.id != id:
            return {"error": "Another category with this title already exists"}
        else:
            return product_category_repository.update(id, data)

    # delete category
    def delete(self, id):
        category = product_category_repository.get(id)
        if not category:
            return {"error": "Category not found"}
        product_in_category = product_repository.list_by_category(category)
        if product_in_category.count() > 0:
            return {"error": "Cannot delete category because products are assigned to it"}
        else:
            return product_category_repository.delete(id)

    # get products belonging to same category_id
    def get_products(self, category_id, filters=None, sort_by=None):
        category = product_category_repository.get(category_id)
        if not category:
            return {"error": "Category not found"}
        else:
            return product_repository.list_by_category(category, filters=filters, sort_by=sort_by)

    # add products to a category
    def add_product_to_category(self, category_id, product_id):
        category = product_category_repository.get(category_id)
        if not category:
            return {"error": "Category not found"}
        else:
            product = product_repository.get(product_id)
            if not product:
                return {"error": "Product not found"}
            else:
                return product_repository.assign_to_category(product, category)

    # remove product from category
    def remove_product_category(self, category_id, product_id):
        category = product_category_repository.get(category_id)
        if not category:
            return {"error": "Category not found"}
        else:
            product = product_repository.get(product_id)
            if not product:
                return {"error": "Product not found"}
            if not product.category or product.category.id != category.id:
                return {"error": "Product does not belong to this category"}
            return product_repository.remove_from_category(product)


# product related business logic
class ProductService:
    # creating Miscellaneous category for "no category" products
    def get_default_category(self):
        default_category = product_category_repository.get_by_title(
            "Miscellaneous")
        if not default_category:
            default_category = product_category_repository.create({
                "title": "Miscellaneous",
                "description": "Default category for uncategorized products"
            })
        return default_category

    # creating products
    def create(self, data):
        # brand is compulsary now
        if not data.get("brand") or not str(data["brand"]).strip():
            return {"error": "Brand is required"}
        category_id = data.get("category_id")
        if category_id is not None:
            category_obj = product_category_repository.get(category_id)
            if not category_obj:
                return {"error": "Category not found"}
        else:
            # if category is not defined then go to misc
            category_obj = self.get_default_category()
        product_data = {
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "brand": data["brand"].strip(),
            "quantity": data["quantity"],
            "category": category_obj,
        }
        return product_repository.create(product_data)

    # get product by id
    def get(self, id):
        return product_repository.get(id)

    # list all products
    def list_all(self, filters=None, sort_by=None):
        return product_repository.list_all(filters=filters, sort_by=sort_by)
