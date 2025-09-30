import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

from bfs import edmonds_karp


def create_logistics_graph():
    """Створює граф логістичної мережі з правильною структурою"""
    G = nx.DiGraph()

    # Вершини:
    # 0, 1 - Термінали 1, 2
    # 2, 3, 4, 5 - Склади 1, 2, 3, 4
    # 6-19 - Магазини 1-14

    # Додаємо ребра згідно з таблицею
    edges = [
        # Термінал 1 -> Склади
        (0, 2, 25),  # Термінал 1 -> Склад 1
        (0, 3, 20),  # Термінал 1 -> Склад 2
        (0, 4, 15),  # Термінал 1 -> Склад 3
        # Термінал 2 -> Склади
        (1, 4, 15),  # Термінал 2 -> Склад 3
        (1, 5, 30),  # Термінал 2 -> Склад 4
        (1, 3, 10),  # Термінал 2 -> Склад 2 (виправлено з 15 на 10)
        # Склад 1 -> Магазини
        (2, 6, 15),  # Склад 1 -> Магазин 1
        (2, 7, 10),  # Склад 1 -> Магазин 2
        (2, 8, 20),  # Склад 1 -> Магазин 3
        # Склад 2 -> Магазини
        (3, 9, 15),  # Склад 2 -> Магазин 4
        (3, 10, 10),  # Склад 2 -> Магазин 5
        (3, 11, 25),  # Склад 2 -> Магазин 6
        # Склад 3 -> Магазини
        (4, 12, 20),  # Склад 3 -> Магазин 7
        (4, 13, 15),  # Склад 3 -> Магазин 8
        (4, 14, 10),  # Склад 3 -> Магазин 9
        # Склад 4 -> Магазини
        (5, 15, 20),  # Склад 4 -> Магазин 10
        (5, 16, 10),  # Склад 4 -> Магазин 11
        (5, 17, 15),  # Склад 4 -> Магазин 12
        (5, 18, 5),  # Склад 4 -> Магазин 13
        (5, 19, 10),  # Склад 4 -> Магазин 14
    ]

    return G, edges


def create_capacity_matrix():
    """Створює матрицю пропускної здатності для мережі"""
    # 20 вершин: 2 термінали + 4 склади + 14 магазинів
    matrix = [[0] * 20 for _ in range(20)]

    # Термінал 1 (0) -> Склади
    matrix[0][2] = 25  # Склад 1
    matrix[0][3] = 20  # Склад 2
    matrix[0][4] = 15  # Склад 3

    # Термінал 2 (1) -> Склади
    matrix[1][3] = 10  # Склад 2
    matrix[1][4] = 15  # Склад 3
    matrix[1][5] = 30  # Склад 4

    # Склад 1 (2) -> Магазини
    matrix[2][6] = 15  # Магазин 1
    matrix[2][7] = 10  # Магазин 2
    matrix[2][8] = 20  # Магазин 3

    # Склад 2 (3) -> Магазини
    matrix[3][9] = 15  # Магазин 4
    matrix[3][10] = 10  # Магазин 5
    matrix[3][11] = 25  # Магазин 6

    # Склад 3 (4) -> Магазини
    matrix[4][12] = 20  # Магазин 7
    matrix[4][13] = 15  # Магазин 8
    matrix[4][14] = 10  # Магазин 9

    # Склад 4 (5) -> Магазини
    matrix[5][15] = 20  # Магазин 10
    matrix[5][16] = 10  # Магазин 11
    matrix[5][17] = 15  # Магазин 12
    matrix[5][18] = 5  # Магазин 13
    matrix[5][19] = 10  # Магазин 14

    return matrix


def analyze_max_flow():
    """Основна функція для аналізу максимального потоку"""
    print("=" * 80)
    print("ЗАВДАННЯ 1: ЗАСТОСУВАННЯ АЛГОРИТМУ МАКСИМАЛЬНОГО ПОТОКУ")
    print("=" * 80)

    # Створюємо матрицю пропускної здатності
    capacity_matrix = create_capacity_matrix()

    # Створюємо граф для візуалізації та аналізу
    G, edges = create_logistics_graph()
    for u, v, cap in edges:
        G.add_edge(u, v, capacity=cap, weight=cap)

    print("\n1. СТРУКТУРА МЕРЕЖІ:")
    print("-" * 40)
    print("Вершини графа:")
    print("  Термінали: 0 (Термінал 1), 1 (Термінал 2)")
    print("  Склади: 2 (Склад 1), 3 (Склад 2), 4 (Склад 3), 5 (Склад 4)")
    print("  Магазини: 6-19 (Магазини 1-14)")
    print(f"\nЗагальна кількість вершин: {len(capacity_matrix)}")
    print(
        f"Загальна кількість ребер: {sum(len([x for x in row if x > 0]) for row in capacity_matrix)}"
    )

    # Розрахунок максимального потоку для кожної пари Термінал -> Магазин
    print("\n2. РОЗРАХУНОК МАКСИМАЛЬНОГО ПОТОКУ (ТЕРМІНАЛ -> МАГАЗИН):")
    print("-" * 60)
    print(f"{'Термінал':<12} | {'Магазин':<10} | {'Фактичний Потік':<15}")
    print("-" * 60)

    terminal_flows = {1: 0, 2: 0}
    store_flows = {}
    all_flows = []

    # Розрахунок для кожного терміналу до кожного магазину
    for terminal in [0, 1]:  # Термінал 1 і 2
        for store in range(6, 20):  # Магазини 1-14
            flow = edmonds_karp(capacity_matrix, terminal, store)
            if flow > 0:
                terminal_num = terminal + 1
                store_num = store - 5
                print(
                    f"Термінал {terminal_num:<3} | Магазин {store_num:<2} | {flow:<15}"
                )
                terminal_flows[terminal_num] += int(flow)
                if store_num not in store_flows:
                    store_flows[store_num] = 0
                store_flows[store_num] += int(flow)
                all_flows.append((terminal_num, store_num, int(flow)))

    # Аналіз з використанням мережевого потоку
    print("\n3. АНАЛІЗ З ВИКОРИСТАННЯМ МЕРЕЖЕВОГО АЛГОРИТМУ:")
    print("-" * 55)

    # Створюємо суперджерело та суперстік
    source = 20
    sink = 21

    # Додаємо суперджерело з великою пропускною здатністю до терміналів
    G.add_edge(source, 0, capacity=1000)  # До терміналу 1
    G.add_edge(source, 1, capacity=1000)  # До терміналу 2

    # Додаємо від магазинів до суперстоку
    for store in range(6, 20):
        G.add_edge(store, sink, capacity=1000)

    # Розрахунок максимального потоку через всю мережу
    max_flow_value, flow_dict = nx.maximum_flow(G, source, sink, capacity="capacity")

    print(f"Максимальний потік через всю мережу: {max_flow_value}")

    # Детальний аналіз потоків
    print("\n4. ДЕТАЛЬНА ТАБЛИЦЯ ПОТОКІВ:")
    print("-" * 50)
    print(f"{'Термінал':<12} | {'Магазин':<10} | {'Потік':<8}")
    print("-" * 50)

    terminal_totals = {1: 0, 2: 0}
    store_totals = {}

    # Аналіз потоків через мережу
    for terminal_idx in [0, 1]:
        terminal_num = terminal_idx + 1
        if terminal_idx in flow_dict:
            for warehouse in flow_dict[terminal_idx]:
                if warehouse in [2, 3, 4, 5] and flow_dict[terminal_idx][warehouse] > 0:
                    wh_flow = flow_dict[terminal_idx][warehouse]
                    if warehouse in flow_dict:
                        for store in flow_dict[warehouse]:
                            if (
                                store >= 6
                                and store <= 19
                                and flow_dict[warehouse][store] > 0
                            ):
                                store_flow = flow_dict[warehouse][store]
                                actual_flow = min(wh_flow, store_flow)
                                if actual_flow > 0:
                                    store_num = store - 5
                                    print(
                                        f"Термінал {terminal_num:<3} | Магазин {store_num:<2} | {actual_flow:<8}"
                                    )
                                    terminal_totals[terminal_num] += int(actual_flow)
                                    if store_num not in store_totals:
                                        store_totals[store_num] = 0
                                    store_totals[store_num] += int(actual_flow)

    return terminal_totals, store_totals, capacity_matrix, G, max_flow_value


def print_analysis_questions(terminal_totals, store_totals, capacity_matrix):
    """Друкує відповіді на аналітичні запитання"""
    print("\n" + "=" * 80)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("=" * 80)

    print("\n1. Які термінали забезпечують найбільший потік товарів до магазинів?")
    print("-" * 70)
    for terminal, total in sorted(
        terminal_totals.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"Термінал {terminal}: {total} одиниць")

    max_terminal = max(terminal_totals.items(), key=lambda x: x[1])
    print(
        f"Найбільший потік забезпечує Термінал {max_terminal[0]} з {max_terminal[1]} одиницями."
    )

    print(
        "\n2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?"
    )
    print("-" * 85)

    # Знаходимо найменші пропускні здатності
    min_capacities = []
    routes = [
        ("Термінал 1 -> Склад 3", 15),
        ("Термінал 2 -> Склад 2", 10),
        ("Склад 4 -> Магазин 13", 5),
        ("Склад 1 -> Магазин 2", 10),
        ("Склад 2 -> Магазин 5", 10),
        ("Склад 3 -> Магазин 9", 10),
        ("Склад 4 -> Магазин 11", 10),
        ("Склад 4 -> Магазин 14", 10),
    ]

    min_cap = min(route[1] for route in routes)
    min_routes = [route for route in routes if route[1] == min_cap]

    print(f"Найменша пропускна здатність: {min_cap} одиниць")
    print("Маршрути з найменшою пропускною здатністю:")
    for route_name, cap in min_routes:
        print(f"  - {route_name}: {cap} одиниць")

    print("\nВплив на загальний потік:")
    print("- Ці вузькі місця обмежують максимальний потік через мережу")
    print(
        "- Магазин 13 отримує найменше товарів через найменшу пропускну здатність (5 одиниць)"
    )

    print(
        "\n3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання?"
    )
    print("-" * 80)

    if store_totals:
        sorted_stores = sorted(store_totals.items(), key=lambda x: x[1])
        print("Магазини, відсортовані за кількістю отриманих товарів:")
        for store, total in sorted_stores[:5]:  # Показуємо 5 найменших
            print(f"  Магазин {store}: {total} одиниць")

        min_store = sorted_stores[0]
        print(
            f"\nНайменше товарів отримує Магазин {min_store[0]}: {min_store[1]} одиниць"
        )

    print("\nРекомендації для збільшення постачання:")
    print("- Збільшити пропускну здатність Склад 4 -> Магазин 13 з 5 до 15+ одиниць")
    print("- Додати альтернативні маршрути до магазинів з низьким постачанням")
    print("- Оптимізувати розподіл потоків між складами")

    print("\n4. Чи є вузькі місця, які можна усунути для покращення ефективності?")
    print("-" * 75)
    print("Основні вузькі місця:")
    print("- Склад 4 -> Магазин 13 (5 одиниць) - критичне вузьке місце")
    print("- Термінал 2 -> Склад 2 (10 одиниць) - обмежує потік до магазинів 4-6")
    print(
        "- Деякі з'єднання складів з магазинами мають пропускну здатність лише 10 одиниць"
    )

    print("\nРекомендації для усунення вузьких місць:")
    print("1. Збільшити пропускну здатність найкритичніших маршрутів")
    print("2. Додати резервні маршрути між терміналами та складами")
    print("3. Перерозподілити навантаження між складами")
    print("4. Розглянути можливість додавання нових складів або терміналів")


def visualize_network(G, edges):
    """Візуалізація мережі"""
    plt.figure(figsize=(15, 10))

    # Позиції для малювання графа
    pos = {
        0: (1, 3),  # Термінал 1
        1: (5, 3),  # Термінал 2
        2: (1, 2),  # Склад 1
        3: (3, 2),  # Склад 2
        4: (4, 2),  # Склад 3
        5: (6, 2),  # Склад 4
        6: (0, 1),  # Магазин 1
        7: (1, 1),  # Магазин 2
        8: (2, 1),  # Магазин 3
        9: (2.5, 1),  # Магазин 4
        10: (3, 1),  # Магазин 5
        11: (3.5, 1),  # Магазин 6
        12: (4, 1),  # Магазин 7
        13: (4.5, 1),  # Магазин 8
        14: (5, 1),  # Магазин 9
        15: (5.5, 1),  # Магазин 10
        16: (6, 1),  # Магазин 11
        17: (6.5, 1),  # Магазин 12
        18: (7, 1),  # Магазин 13
        19: (7.5, 1),  # Магазин 14
    }

    # Кольори для різних типів вершин
    node_colors = []
    for node in G.nodes():
        if node in [0, 1]:  # Термінали
            node_colors.append("red")
        elif node in [2, 3, 4, 5]:  # Склади
            node_colors.append("yellow")
        else:  # Магазини
            node_colors.append("lightblue")

    # Малювання графа
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=1000,
        font_size=8,
        font_weight="bold",
        arrows=True,
        edge_color="gray",
        arrowsize=20,
    )

    # Додавання підписів ребер з пропускними здатностями
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.title(
        "Логістична мережа: Термінали -> Склади -> Магазини",
        fontsize=14,
        fontweight="bold",
    )
    plt.text(
        0.5,
        0.02,
        "Червоні: Термінали, Жовті: Склади, Блакитні: Магазини",
        transform=plt.gca().transAxes,
        ha="center",
        fontsize=10,
    )
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Виконання основного аналізу
    terminal_totals, store_totals, capacity_matrix, G, max_flow = analyze_max_flow()

    # Друк аналітичних відповідей
    print_analysis_questions(terminal_totals, store_totals, capacity_matrix)

    # Візуалізація мережі
    print("\n" + "=" * 80)
    print("ВІЗУАЛІЗАЦІЯ МЕРЕЖІ")
    print("=" * 80)
    G_viz, edges = create_logistics_graph()
    for u, v, cap in edges:
        G_viz.add_edge(u, v, capacity=cap, weight=cap)
    visualize_network(G_viz, edges)

    print(f"\nЗагальний максимальний потік через мережу: {max_flow} одиниць")
    print("Аналіз завершено!")
