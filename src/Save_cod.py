





transaction_categories = [
            trans for trans in transaction
            if (
                    search_word_lower in str(trans.get("description", "")).strip() or
                    search_word_lower in str(trans.get("from", "")).strip() or
                    search_word_lower in str(trans.get("to", "")).strip()
            )
        ]

        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {(count_operations_by_category(transaction_categories, words_users))}")

if not transaction_categories:
    print("По вашему запросу транзакции не найдены.")
    return