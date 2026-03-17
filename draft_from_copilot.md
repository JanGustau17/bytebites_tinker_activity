classDiagram
    class Customer {
        +String name
        +List~Transaction~ pastPurchaseHistory
        +verifyUser() Boolean
    }

    class FoodItem {
        +String name
        +Float price
        +String category
        +Integer popularityRating
    }

    class Menu {
        +List~FoodItem~ allItems
        +filterByCategory(category: String) List~FoodItem~
    }

    class Transaction {
        +List~FoodItem~ selectedItems
        +computeTotalCost() Float
    }

    Customer "1" --> "*" Transaction : has
    Menu "1" *-- "*" FoodItem : holds
    Transaction "1" o-- "*" FoodItem : stores