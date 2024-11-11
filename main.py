
import pandas as pd
import matplotlib.pyplot as plt

file_path = '/home/katerinsplace/Downloads/data.xlsx'
df = pd.read_excel(file_path, sheet_name='Лист1')

df['receiving_date'] = pd.to_datetime(df['receiving_date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

months = {}
name_month = None
current_month = None

for index, row in df.iterrows():
    if pd.isna(row['client_id']):
        if current_month is not None:
            months[name_month] = pd.DataFrame(current_month)
        current_month = []
        name_month = row['status']
    else:
        current_month.append(row)
if current_month is not None:
    months[name_month] = pd.DataFrame(current_month)

#1
period1 = months['Июль 2021']
total_july_2021 = period1.loc[period1['status'] == 'ОПЛАЧЕНО', 'sum'].sum()
print(total_july_2021)
#859896.4699999997

#2
data_graf = {'Месяц': [], 'Выручка': []}
for name_month, month_df in months.items():
    data_graf['Месяц'].append(name_month)
    data_graf['Выручка'].append(int(month_df.loc[month_df['status'] != 'В РАБОТЕ', 'sum'].sum()))

data_df = pd.DataFrame(data_graf)
data_df.plot(x='Месяц', y='Выручка', kind='line', marker='o')

plt.title('Выручка компании по месяцам', fontsize=14)
plt.xlabel('Месяц', fontsize=12)
plt.ylabel('Выручка', fontsize=12)
plt.grid(True)
plt.show()

#3
period3 = months['Сентябрь 2021']
grouped = period3.groupby('sale')['sum'].sum()
top_manager = grouped.idxmax()
print(top_manager)
#Смирнов

#4
period4 = months['Октябрь 2021']
most_often_type = period4['new/current'].mode()[0]
print(most_often_type)
#текущая

#5
period5 = months['Май 2021']
filtered_df = period5[(period5['document'] == 'оригинал') & (period5['receiving_date'].dt.month == 6)]

res = filtered_df.shape[0]
print(res)
#76

#task
bonuses = {}
numbers_months = {'май': 5, 'июнь': 6, 'июль': 7, 'август': 8, 'сентябрь': 9, 'октябрь': 10}
for period in months:
    number_month = numbers_months[period.split()[0].lower()]
    if number_month < 7:
        for index, row in months[period].iterrows():
            if row['new/current'] == 'новая' \
                and row['status'] == 'ОПЛАЧЕНО' \
                    and row['document'] == 'оригинал' \
                        and row['receiving_date'].month >= 7:
                k = 0.07
                bonuses[row['sale']] = bonuses.get(row['sale'], 0) + row['sum'] * k
            elif row['new/current'] == 'текущая' \
                and row['status'] != 'ПРОСРОЧЕНО' \
                    and row['document'] == 'оригинал' \
                        and row['receiving_date'].month >= 7:
                if row['sum'] >= 10000:
                    k = 0.05
                else:
                    k = 0.03
                bonuses[row['sale']] = bonuses.get(row['sale'], 0) + row['sum'] * k

print()
for name, total in bonuses.items():
    print(f'{name} {int(total)}')
#Петрова 10770
#Иванов 5991
#Кузнецова 4496
#Филимонова 2317
#Селиванов 5297
#Васильев 1037
#Андреев 3945
#Смирнов 6430
#Соколов 269