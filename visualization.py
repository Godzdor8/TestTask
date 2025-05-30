import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sqlalchemy import func
from datetime import date
from database import SessionLocal
from models import Debtor, Message, MonetaryObligation


def format_rubles(x, _):
    return f'{int(x):,}'.replace(',', ' ') + ' ₽'

def get_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if birth_date.month > today.month or birth_date.month == today.month and birth_date.day > today.day:
        age -= 1

    return age

def show_graph(x, y, xlabel, ylabel, title, horizontal=False):
    plt.figure(figsize=(12, 6))

    if horizontal:
        plt.barh(x, y, color='blue')
        plt.ylabel(xlabel)
        plt.xlabel(ylabel)
        plt.gca().xaxis.set_major_formatter(FuncFormatter(format_rubles))
        plt.gca().invert_yaxis()
    else:
        plt.bar(x, y, color='orange')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_rubles))
        plt.xticks(rotation=45, ha='right', fontsize=8)

    plt.title(title)
    plt.tight_layout()
    plt.show()


def main():
    session = SessionLocal()

    region_data = (
        session.query(Debtor.region, func.sum(MonetaryObligation.debt_sum))
        .select_from(Debtor)
        .join(Message, Message.debtor_id == Debtor.id)
        .join(MonetaryObligation, MonetaryObligation.message_id == Message.id)
        .group_by(Debtor.region)
        .order_by(func.sum(MonetaryObligation.debt_sum).desc())
        .all()
    )
    regions = [r for r, _ in region_data]
    region_sums = [s for _, s in region_data]
    show_graph(regions, region_sums, "Регион", "Сумма задолженности", "Задолженность по регионам", horizontal=True)

    raw_ages = (
        session.query(Debtor.birth_date, func.sum(MonetaryObligation.debt_sum))
        .select_from(Debtor)
        .join(Message, Message.debtor_id == Debtor.id)
        .join(MonetaryObligation, MonetaryObligation.message_id == Message.id)
        .group_by(Debtor.birth_date)
        .all()
    )
    age_bins = {}
    for birth_date, debt in raw_ages:
        age = get_age(birth_date)
        if age and 18 <= age <= 100:
            group = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
            age_bins[group] = age_bins.get(group, 0) + debt
    age_labels = sorted(age_bins.keys(), key=lambda g: int(g.split('-')[0]))
    age_sums = [age_bins[g] for g in age_labels]
    show_graph(age_labels, age_sums, "Возрастная группа", "Сумма задолженности", "Задолженность по возрасту")

    session.close()


if __name__ == "__main__":
    main()
