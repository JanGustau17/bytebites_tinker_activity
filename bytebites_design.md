classDiagram
    class Customer {
        +String name
        +List~Transaction~ past_purchase_history
        +verify_user() Boolean
    }

    class FoodItem {
        +String name
        +Float price
        +String category
        +Integer popularity_rating
    }

    class Menu {
        +List~FoodItem~ all_items
        +add_item(item: FoodItem) None
        +filter_by_category(category: String) List~FoodItem~
    }

    class Transaction {
        +List~FoodItem~ selected_items
        +compute_total_cost() Float
    }

    Customer "1" --> "*" Transaction : has
    Menu "1" *-- "*" FoodItem : holds
    Transaction "1" o-- "*" FoodItem : stores
