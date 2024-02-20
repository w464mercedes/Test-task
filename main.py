import statistics                                                      # імпортуєм необхідні бібліотеки
from flask import Flask, render_template, request,flash 


app = Flask(__name__)                                                  # створюєм додаток
app.secret_key = '123124123'                                           # задаєм секретний ключ

@app.route('/', methods=['POST','GET'])                                # створюєм дію
def index():
    min = None                                                         # задаєм значення змінним по замовчуванню
    max = None
    median = None
    average = None
    lon_up = None
    lon_down = None
    
    if request.method == "POST":                                       # перевіряєм метод
        file = request.files['file']
        if file:                                                       # перевіряєм наявність файла і зберігаєм його
            filename = file.filename                                    
            file.save(filename)

            with open (filename,'r') as f:                             # завантажуем файл і читаєм його
                data = f.readlines() 

            data = list(map(int, data))                                 # Перетворюєм список на числа

        # Створюєм функцію для знаходження найбільшої послідовністі чисел яка збільшується
            def longest_list_up(data):                                  # приймаєм список чисел
                current_list = [data[0]]                                # поточний список елементів
                longest_list = []                                       # найбільший список елементів

                for i in range(1, len(data)):                           # проходимось змінною по списку 
                    if data[i] > current_list[-1]:                      # перевіряєм чи поточний елемент більший за останній у потоному списку
                        current_list.append(data[i])                    # якщо умова виконується, додаєм елемент до поточного списку
                    else:                                               # в иншому випадку робим перевірку:
                        if len(current_list) > len(longest_list):       # якщо поточний список більший за найдовший, замінюєм найдовший поточним
                            longest_list = current_list
                        current_list = [data[i]]                        # поточний список отримує останній елемент

                if len(longest_list) < len(current_list):               # робим перевірку довжини списку
                    longest_list = current_list                         # якщо найдовший список меньше поточного, вміст поточного записуєм в найдовший
                return longest_list                                     # повертаєм наядовший список елементів


        # Створюєм функцію для знаходження найбільшої послідовністі чисел яка зменшуються
            def longest_list_down(data):                                # приймаєм список чисел
                current_list = [data[0]]                                # поточний список елементів
                longest_list = []                                       # найбільший список елементів

                for i in range(1, len(data)):                           # проходимось змінною по списку 
                    if data[i] < current_list[-1]:                      # перевіряєм чи поточний елемент меньший за останній у потоному списку
                        current_list.append(data[i])                    # якщо умова виконується, додаєм елемент до поточного списку
                    else:                                               # в иншому випадку робим перевірку:
                        if len(current_list) > len(longest_list):       # якщо поточний список більший за найдовший, замінюєм найдовший поточним
                            longest_list = current_list
                        current_list = [data[i]]                        # поточний список отримує останній елемент

                if len(longest_list) < len(current_list):               # робим перевірку довжини списку
                    longest_list = current_list                         # якщо найдовший список меньше поточного, вміст поточного записуєм в найдовший
                return longest_list                                     # повертаєм наядовший список елементів


            lon_up = longest_list_up(data)                              # знаходження найбільшої послідовністі чисел яка збільшується
            lon_down = longest_list_down(data)                          # знаходження найбільшої послідовністі чисел яка зменшуються
            sorted_data = sorted(data)                                  # сортуєм список

            if len(data) % 2 == 0:                                      # перевіряєм чи список має парну кількість чисел
                number = int(len(data) / 2)                             # якщо кількість чисел парна то знаходимо півсуму двох парних чисел
                median = 0.5 * (data[number] + data[number - 1])
            else:                                                       # якщо кількість чисел не парна то знаходим медіану за допомогою функції statistics.median() із бібліотеки statistics
                median = statistics.median(data)
                
            average = sum(data) / len(data)                             # знаходим середнє арифметичне     
            max = sorted_data[-1]                                       # знаходим найбільше число
            min = sorted_data[0]                                        # знаходим найменьше число
        else:                                                           # якщо файл не обрано, виводимо повідомлення що треба обрати файл
            flash('Ви не обрали файл!')                                 # повертаєм шаблон із змінними
    return render_template('index.html',
                           max=max,
                           min=min,
                           median=median,
                           average=average,
                           lon_up=lon_up,
                           lon_down=lon_down)                           
if __name__ == '__main__':                                              # запускаєм сервер
    app.run()