# Celery Workflow: Fetch Data → Process Data → Save Data

## Обзор

Этот проект демонстрирует использование Celery для создания сложных workflow с помощью `chain` и `chord`. Workflow включает три основных этапа:
1. **Fetch Data** - получение данных из внешнего источника
2. **Process Data** - обработка и преобразование данных
3. **Save Data** - сохранение обработанных данных

## Celery Primitives

### Chain (Цепочка)

`chain` позволяет выполнять задачи последовательно, где результат одной задачи передается как аргумент следующей:

```python
from celery import chain

# task1 -> task2 -> task3
result = chain(task1.s(), task2.s(), task3.s())()
```

### Chord (Параллелизм)

`chord` состоит из двух частей:

- **Заголовок (header)** - группа задач, выполняемых параллельно
- **Обратный вызов (callback)** - задача, которая выполняется после завершения всех задач заголовка

```python
from celery import chord, group

# [task1, task2, task3] -> callback
result = chord([task1.s(), task2.s(), task3.s()])(callback.s())
```

## Структура Workflow

### Базовые задачи

#### 1. Fetch Data
```python
@app.task
def fetch_data(source_url):
    """
    Задача для получения данных из внешнего источника
    """
    try:
        response = requests.get(source_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Данные успешно получены из {source_url}")
        print(f"📊 Получено записей: {len(data) if isinstance(data, list) else 1}")
        
        return data
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {str(e)}")
        raise
```

#### 2. Process Data
```python
@app.task
def process_data(raw_data):
    """
    Задача для обработки сырых данных
    """
    try:
        processed_data = []
        
        data_list = raw_data if isinstance(raw_data, list) else [raw_data]
        
        for item in data_list:
            processed_item = {
                'original_data': item,
                'processed_at': datetime.now().isoformat(),
                'data_length': len(str(item)),
                'processed_by': 'celery_worker'
            }
            
            if isinstance(item, dict):
                processed_item['keys_count'] = len(item.keys())
                processed_item['has_id'] = 'id' in item
            elif isinstance(item, list):
                processed_item['items_count'] = len(item)
            
            processed_data.append(processed_item)
        
        print(f"🔧 Обработано записей: {len(processed_data)}")
        return processed_data
    except Exception as e:
        print(f"❌ Ошибка при обработке данных: {str(e)}")
        raise
```

#### 3. Save Data
```python
@app.task
def save_data(processed_data, storage_path="output/data.json"):
    """
    Задача для сохранения обработанных данных
    """
    try:
        import os
        
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump({
                'saved_at': datetime.now().isoformat(),
                'total_records': len(processed_data),
                'data': processed_data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Данные сохранены в {storage_path}")
        print(f"📁 Всего сохранено записей: {len(processed_data)}")
        
        return {
            'status': 'success',
            'saved_path': storage_path,
            'records_count': len(processed_data),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"❌ Ошибка при сохранении данных: {str(e)}")
        raise
```

## Простая цепочка с Chain

Базовый вариант workflow с последовательным выполнением:

```python
from celery import chain

def execute_simple_workflow(source_url, output_path="output/simple_data.json"):
    """
    Простой последовательный workflow
    """
    workflow = chain(
        fetch_data.s(source_url),
        process_data.s(),
        save_data.s(output_path)
    )
    
    return workflow.apply_async()
```

### Преимущества Chain:

- ✅ **Последовательное выполнение** - задачи выполняются в строгом порядке
- ✅ **Передача данных** - результат предыдущей задачи передается следующей
- ✅ **Атомарность** - весь workflow выполняется как единая операция
- ✅ **Простота отладки** - легче отслеживать выполнение по цепочке

## Пример использования

```python
result = execute_simple_workflow(
    source_url="https://api.example.com/data",
    output_path="output/processed_data.json"
)

print(f"Статус задачи: {result.status}")
print(f"Результат выполнения: {result.get()}")
```

## Конфигурация

```python
from celery import Celery

app = Celery('workflow_app', broker='redis://localhost:6379/0')
```

## Логирование

Workflow включает детальное логирование на каждом этапе:

- ✅ **Успешное получение данных** - с указанием источника и количества записей
- 🔧 **Обработка данных** - с подсчетом обработанных записей
- 💾 **Сохранение данных** - с указанием пути файла и количества сохраненных записей
- ❌ **Ошибки** - детальная информация об ошибках на каждом этапе
