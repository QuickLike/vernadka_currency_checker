import matplotlib.pyplot as plt


def draw_graph(data: list | tuple, interval: str = 'daily'):
    time, buy_amount, sell_amount = [], [], []
    for row in data:
        if interval == 'daily':
            time.append(row[2].split(' ')[1][:-7])
            plt.figure(figsize=(19.20, 10.80))
        elif interval == 'weekly':
            time.append(f'{row[3]} {row[2].split(" ")[1][:-7]}')
            plt.figure(figsize=(38.40, 10.80))
        else:
            raise ValueError(f'Недопустимое значение переменной interval: {interval}\nДопустимые значения: "daily", '
                             f'"weekly"')
        buy_amount.append(row[0])
        sell_amount.append(row[1])
    plt.plot(time, buy_amount, label='Покупка')
    plt.plot(time, sell_amount, label='Продажа')
    plt.legend()
    filename = f'{interval}.png'
    try:
        plt.savefig(filename)
    except Exception as e:
        return e
    plt.close()
    return filename


def main():
    test_data = [(90.0, 91.5, '2024-06-13 23:49:35.253116', 'Четверг'), (91.0, 92.5, '2024-06-13 23:50:06.061601', 'Четверг'), (89.0, 91.0, '2024-06-13 23:50:29.720256', 'Четверг'), (89.5, 92.0, '2024-06-13 23:50:43.189495', 'Четверг'), (88.5, 90.5, '2024-06-13 23:50:55.021763', 'Четверг')]
    print(draw_graph(test_data, interval='weekly'))


if __name__ == '__main__':
    main()
