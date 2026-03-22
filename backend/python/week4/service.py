# bridge between views and repository
from .repository import product_category_repository, product_repository
from .csv_helper import read_csv_file


class ProductCategoryService:
    # creating category
    def create(self, data):
        existing_category = product_category_repository.get_by_title(
            data["title"])
        if existing_category:
            return {"error": "Category with this title already exists"}

        return product_category_repository.create(data)

    # get by id
    def get(self, id):
        return product_category_repository.get(id)

    # list all products
    def list_all(self, filters=None, sort_by=None):
        return product_category_repository.list_all(filters=filters, sort_by=sort_by)

    # update
    def update(self, id, data):
        category = product_category_repository.get(id)
        if not category:
            return {"error": "Category not found"}
        existing_category = product_category_repository.get_by_title(
            data["title"])
        if existing_category and existing_category.id != id:
            return {"error": "Another category with this title already exists"}
        else:
            return product_category_repository.update(id, data)

    # delete
    def delete(self, id):
        category = product_category_repository.get(id)
        if not category:
            return {"error": "Category not found"}
        product_in_category = product_repository.list_by_category(category)
        if product_in_category.count() > 0:
            return {"error": "Cannot delete category because products are assigned to it"}
        else:
            return product_category_repository.delete(id)

    # get products with category_id
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
                return {"error": "Product does not belong to this category."}
            return product_repository.remove_from_category(product)
