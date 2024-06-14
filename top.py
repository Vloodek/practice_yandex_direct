import pandas as pd
import numpy as np

# Загрузка данных из CSV файла с указанием разделителя
file_path = 'path.csv'  # Укажите правильный путь к вашему CSV файлу
df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

# Замена запятых на точки в числовых значениях
df['CTR (%)'] = df['CTR (%)'].str.replace(',', '.').replace('-', '0').astype(float)
df['Ср. цена клика (руб.)'] = df['Ср. цена клика (руб.)'].str.replace(',', '.').replace('-', '0').astype(float)
df['Отказы (%)'] = df['Отказы (%)'].str.replace(',', '.').replace('-', '0').astype(float)
df['Конверсия (%)'] = df['Конверсия (%)'].str.replace(',', '.').replace('-', '0').astype(float)

# Заполнение пропусков нулями
df.fillna(0, inplace=True)

# Нормализация параметров
df['Показы_norm'] = (df['Показы'] - df['Показы'].min()) / (df['Показы'].max() - df['Показы'].min())
df['CTR_norm'] = (df['CTR (%)'] - df['CTR (%)'].min()) / (df['CTR (%)'].max() - df['CTR (%)'].min())
df['Ср. цена клика_norm'] = (df['Ср. цена клика (руб.)'].max() - df['Ср. цена клика (руб.)']) / (df['Ср. цена клика (руб.)'].max() - df['Ср. цена клика (руб.)'].min())
df['Отказы_norm'] = (df['Отказы (%)'].max() - df['Отказы (%)']) / (df['Отказы (%)'].max() - df['Отказы (%)'].min())
df['Конверсия_norm'] = (df['Конверсия (%)'] - df['Конверсия (%)'].min()) / (df['Конверсия (%)'].max() - df['Конверсия (%)'].min())

# Определение динамических весов
# Вес для показа объявлений
df['Weight_Pokazy'] = df['Показы_norm']

# Вес для CTR (если показы низкие, CTR не имеет значения)
df['Weight_CTR'] = df['Показы_norm'] * df['CTR_norm']

# Вес для средней цены клика (если показы низкие, ср. цена клика не имеет значения)
df['Weight_Sr_cena_klika'] = df['Показы_norm'] * df['Ср. цена клика_norm']

# Вес для отказов (если показы низкие, процент отказов не имеет значения)
df['Weight_Otkazy'] = df['Показы_norm'] * df['Отказы_norm']

# Вес для конверсии (если показы низкие, конверсия не имеет значения)
df['Weight_Konversiya'] = df['Показы_norm'] * df['Конверсия_norm']

# Вычисление сводного балла с учетом динамических весов
df['Composite_score'] = (
    df['Показы_norm'] * df['Weight_Pokazy'] +
    df['CTR_norm'] * df['Weight_CTR'] +
    df['Ср. цена клика_norm'] * df['Weight_Sr_cena_klika'] +
    df['Отказы_norm'] * df['Weight_Otkazy'] +
    df['Конверсия_norm'] * df['Weight_Konversiya']
)

# Ранжирование объявлений на основе сводного балла
df['Rank'] = df['Composite_score'].rank(ascending=False)

# Сортировка DataFrame по сводному баллу
df_sorted = df.sort_values(by='Composite_score', ascending=False)

# Вывод самых полезных объявлений
print(df_sorted[['Заголовок', 'Текст', 'Показы', 'CTR (%)', 'Ср. цена клика (руб.)', 'Отказы (%)', 'Конверсия (%)', 'Composite_score', 'Rank']])
