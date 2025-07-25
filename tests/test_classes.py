import pytest

from src.main import Category, Product, load_data_from_json


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счетчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def sample_product():
    return Product("Test Product", "Description", 100.0, 5)


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Category Description", [sample_product])


# Тесты для Product
def test_product_init(sample_product):
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Description"
    assert sample_product.price == 100.0
    assert sample_product.quantity == 5


def test_product_str(sample_product):
    assert "Test Product" in str(sample_product)
    assert "100.0" in str(sample_product)
    assert "5" in str(sample_product)


def test_product_repr(sample_product):
    assert "Product" in repr(sample_product)
    assert "Test Product" in repr(sample_product)


# Тесты для Category
def test_category_init(sample_category):
    assert sample_category.name == "Test Category"
    assert len(sample_category.products) == 1


def test_category_str(sample_category):
    assert "Test Category" in str(sample_category)
    assert "1" in str(sample_category)


def test_category_count():
    initial = Category.category_count
    cat = Category("Test", "Desc", [])
    assert Category.category_count == initial + 1


def test_product_count():
    initial = Category.product_count
    p = Product("P", "D", 100, 1)
    cat = Category("Test", "Desc", [p])
    assert Category.product_count == initial + 1


# Тесты для JSON
def test_json_loading():
    categories = load_data_from_json("products.json")
    assert len(categories) == 2
    assert any(
        p.name == "Samsung Galaxy C23 Ultra" for cat in categories for p in cat.products
    )


def test_json_file_not_found():
    with pytest.raises(ValueError):
        load_data_from_json("nonexistent.json")


# Граничные случаи
def test_product_negative_price():
    with pytest.raises(ValueError):
        Product("Test", "Desc", -100.0, 5)


def test_product_zero_price():
    p = Product("Test", "Desc", 0.0, 5)
    assert p.price == 0.0


def test_empty_category():
    cat = Category("Empty", "Desc", [])
    assert len(cat.products) == 0
    assert "0" in str(cat)


def test_category_repr(sample_category):
    assert "Category" in repr(sample_category)
    assert "Test Category" in repr(sample_category)


def test_product_high_quantity():
    p = Product("Test", "Desc", 100.0, 10_000)
    assert p.quantity == 10_000


def test_json_loading_content():
    categories = load_data_from_json("products.json")
    assert (
        len(categories[0].products) == 3
    )  # Проверяем количество товаров в первой категории
    assert categories[0].products[0].name == "Samsung Galaxy C23 Ultra"


def test_category_with_multiple_products():
    p1 = Product("Product 1", "Desc 1", 100.0, 10)
    p2 = Product("Product 2", "Desc 2", 200.0, 20)
    cat = Category("Multi", "Desc", [p1, p2])
    assert len(cat.products) == 2
    assert "2" in str(cat)


def test_product_long_description():
    long_desc = "Очень длинное описание " * 10
    p = Product("Test", long_desc, 100.0, 5)
    assert "Очень длинное описан..." in str(p)  # Проверяем обрезанное описание
    assert "100.0 руб." in str(p)


def test_category_add_product():
    cat = Category("Test", "Desc", [])
    p = Product("New", "Desc", 50.0, 1)
    cat.products.append(p)
    assert len(cat.products) == 1
    assert "1" in str(cat)


def test_category_count_reset():
    initial_count = Category.category_count
    Category.category_count = 0
    cat = Category("Temp", "Desc", [])
    assert Category.category_count == 1
    Category.category_count = initial_count


def test_product_count_reset():
    initial_count = Category.product_count
    Category.product_count = 0
    p = Product("Temp", "Desc", 10.0, 1)
    cat = Category("Temp", "Desc", [p])
    assert Category.product_count == 1
    Category.product_count = initial_count


def test_json_loading_invalid_data(tmp_path):
    import json

    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text('{"invalid": "data"}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_data_from_json(str(invalid_file))


def test_product_negative_quantity():
    with pytest.raises(ValueError):
        Product("Test", "Desc", 100.0, -5)


def test_json_loading_invalid_format(tmp_path):
    import json

    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text('{"invalid": "data"}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_data_from_json(str(invalid_file))


def test_json_loading_missing_keys(tmp_path):
    import json

    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text('[{"name": "Test"}]', encoding="utf-8")
    with pytest.raises(ValueError):
        load_data_from_json(str(invalid_file))


def test_json_loading_empty_list(tmp_path):
    import json

    file_path = tmp_path / "empty.json"
    file_path.write_text("[]", encoding="utf-8")
    result = load_data_from_json(str(file_path))
    assert len(result) == 0


def test_product_price_precision():
    p = Product("Test", "Desc", 100.123, 5)
    assert p.price == 100.123
    assert "100.123" in str(p)


def test_json_loading_invalid_products_type(tmp_path):
    import json

    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text(
        '[{"name": "Test", "description": "Desc", "products": "not-a-list"}]',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_data_from_json(str(invalid_file))


def test_product_high_precision_price():
    p = Product("Test", "Desc", 100.123456789, 5)
    assert abs(p.price - 100.123456789) < 0.000001


def test_product_non_numeric_price():
    with pytest.raises(ValueError):
        Product("Test", "Desc", "not-a-number", 5)


def test_product_non_integer_quantity():
    with pytest.raises(ValueError):
        Product("Test", "Desc", 100.0, 5.5)


def test_json_loading_invalid_price_type(tmp_path):
    import json

    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text(
        """
    [{
        "name": "Test",
        "description": "Desc",
        "products": [{
            "name": "P1",
            "description": "Desc",
            "price": "not-a-number",
            "quantity": 5
        }]
    }]
    """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_data_from_json(str(invalid_file))


def test_json_loading_invalid_quantity_type(tmp_path):
    import json

    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text(
        """
    [{
        "name": "Test",
        "description": "Desc",
        "products": [{
            "name": "P1",
            "description": "Desc",
            "price": 100.0,
            "quantity": "not-a-number"
        }]
    }]
    """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_data_from_json(str(invalid_file))


def test_json_loading_missing_product_field(tmp_path):
    """Тест на отсутствие обязательного поля в товаре"""
    import json

    file_path = tmp_path / "test.json"
    file_path.write_text(
        """
    [{
        "name": "Cat",
        "description": "Desc",
        "products": [{
            "name": "P1",
            "description": "Desc",
            "price": 100
            # Пропущено quantity
        }]
    }]
    """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_data_from_json(str(file_path))


def test_json_loading_invalid_category_structure(tmp_path):
    """Тест на неверную структуру категории"""
    import json

    file_path = tmp_path / "test.json"
    file_path.write_text(
        """
    [{
        "name": "Cat",
        "description": "Desc"
        # Пропущено products
    }]
    """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_data_from_json(str(file_path))


def test_product_max_values():
    """Тест на максимальные значения"""
    p = Product("Test", "Desc", float("inf"), 2**63 - 1)
    assert p.price == float("inf")
    assert p.quantity == 2**63 - 1


def test_json_loading_file_error(tmp_path):
    """Тест на ошибку при чтении файла"""
    from unittest.mock import patch

    with patch("builtins.open", side_effect=PermissionError("No access")):
        with pytest.raises(ValueError):
            load_data_from_json("any_file.json")


def test_product_init_type_errors():
    """Тест на ошибки типов при создании продукта"""
    with pytest.raises(ValueError):
        Product(None, "Desc", 100, 5)  # None вместо имени
    with pytest.raises(ValueError):
        Product("Name", None, 100, 5)  # None вместо описания


def test_category_init_type_errors():
    """Тест на ошибки типов при создании категории"""
    with pytest.raises(ValueError):
        Category(None, "Desc", [])  # None вместо имени
    with pytest.raises(ValueError):
        Category("Name", None, [])  # None вместо описания
    with pytest.raises(ValueError):
        Category("Name", "Desc", "not a list")  # Не список продуктов


def test_json_loading_empty_fields():
    """Тест на пустые обязательные поля"""
    with pytest.raises(ValueError):
        Product("", "Desc", 100, 5)  # Пустое название
    with pytest.raises(ValueError):
        Category("Name", "", [])  # Пустое описание


def test_json_loading_invalid_nested_types(tmp_path):
    """Тест на неверные типы во вложенных данных"""
    import json

    file_path = tmp_path / "test.json"
    file_path.write_text(
        """
    [{
        "name": 123,  # Не строка
        "description": "Desc",
        "products": []
    }]
    """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_data_from_json(str(file_path))


def test_remove_category(sample_category):
    initial_cat = Category.category_count
    initial_prod = Category.product_count
    product_count = len(sample_category.products)

    # Проверяем успешное удаление
    assert sample_category.remove_category() is True
    assert Category.category_count == initial_cat - 1
    assert Category.product_count == initial_prod - product_count
    assert len(sample_category.products) == 0  # Проверяем очистку продуктов


def test_double_remove_category(sample_category):
    # Первое удаление должно пройти успешно
    sample_category.remove_category()

    # Второе удаление должно вызвать ошибку
    with pytest.raises(ValueError, match="Категория уже удалена"):
        sample_category.remove_category()


def test_remove_category_with_error(monkeypatch):
    cat = Category("Test", "Desc", [Product("P", "D", 100, 1)])

    # Имитируем ошибку при изменении счетчика
    monkeypatch.setattr(Category, "category_count", "invalid_value")

    with pytest.raises(TypeError):
        cat.remove_category()


def test_reactivate_category():
    cat = Category("Test", "Desc", [])
    cat.remove_category()

    cat._is_active = True
    assert cat.remove_category() is True  # Теперь снова можно удалить
