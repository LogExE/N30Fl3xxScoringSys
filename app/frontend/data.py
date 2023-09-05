""" Значения полей и словари для конвертирования данных в нужный для модели формат """


# Семейное положение
NAME_FAMILY_STATUS_rus = [
    "Холост/не в браке", "Женат/замужем", "Фактический брак", "Разведен/разведена", "Вдовец/вдова"
]
NAME_FAMILY_STATUS_eng = [
    "Single / not married", "Married", "Civil marriage", "Separated", "Widow"
]
NAME_FAMILY_STATUS_dict = dict(zip(NAME_FAMILY_STATUS_rus, NAME_FAMILY_STATUS_eng))


# Тип жилья
NAME_HOUSING_TYPE_rus = [
    "Собственный дом/квартира", "С родителями", "Муниципальная квартира",
    "Съемная квартира", "Офисная квартира", "Кооперативная квартира"
]
NAME_HOUSING_TYPE_eng = [
    "House / apartment", "With parents", "Municipal apartment",
    "Rented apartment", "Office apartment", "Co-op apartment"
]
NAME_HOUSING_TYPE_dict = dict(zip(NAME_HOUSING_TYPE_rus, NAME_HOUSING_TYPE_eng))


# Тип образования
NAME_EDUCATION_TYPE_rus = [
    "Среднее/средне-специальное образование", "Высшее образование",
    "Неполное высшее образование", "Неполное среднее образование",
    "Академическая степень"
]
NAME_EDUCATION_TYPE_eng = [
    "Secondary / secondary special", "Higher education",
    "Incomplete higher", "Lower secondary", "Academic degree"
]
NAME_EDUCATION_TYPE_dict = dict(zip(NAME_EDUCATION_TYPE_rus, NAME_EDUCATION_TYPE_eng))


# Тип занятости
OCCUPATION_TYPE_rus = [
    "Рабочий", "Основной персонал", "Бухгалтер", "Менеджер", "Водитель", "Продавец",
    "Уборщик", "Кулинарный персонал", "Частный персонал", "Медицинский персонал",
    "Персонал службы безопасности", "Высококвалифицированный технический персонал",
    "Официант/бармен", "Низкоквалифицированный рабочий", "Агент по недвижимости", "Секретарь",
    "IT-персонал", "HR-персонал", "Другое"
]
OCCUPATION_TYPE_eng = [
    'Laborers', 'Core staff', 'Accountants', 'Managers', 'Drivers',
    'Sales staff', 'Cleaning staff', 'Cooking staff', 'Private service staff',
    'Medicine staff', 'Security staff', 'High skill tech staff',
    'Waiters/barmen staff', 'Low-skill Laborers', 'Realty agents', 'Secretaries',
    'IT staff', 'HR staff', 'Other'
]
OCCUPATION_TYPE_dict = dict(zip(OCCUPATION_TYPE_rus, OCCUPATION_TYPE_eng))

# Тип организации
ORGANIZATION_TYPE_rus = [
    "Бизнес", "Школа", "Правительство", "Религия", "Другое", "Электричество", "Медицина",
    "Самозанятые", "Транспорт", "Строительство", "Жилье", "Детский сад", "Торговля",
    "Промышленность", "Военные", "Услуги", "Министерство безопасности", "Экстренная служба",
    "Безопасность", "Университет", "Полиция", "Почта", "Сельское хозяйство", "Ресторан",
    "Культура", "Гостиница", "Банк", "Страхование", "Мобильная связь", "Юридические услуги",
    "Реклама", "Клининг", "Телеком", "Риэлтор"
]
ORGANIZATION_TYPE_eng = [
    'Business', 'School', 'Government', 'Religion', 'Other', 'Electricity',
    'Medicine', 'Self-employed', 'Transport', 'Construction', 'Housing',
    'Kindergarten', 'Trade', 'Industry', 'Military', 'Services',
    'Security Ministries', 'Emergency', 'Security', 'University', 'Police',
    'Postal', 'Agriculture', 'Restaurant', 'Culture', 'Hotel', 'Bank', 'Insurance',
    'Mobile', 'Legal Services', 'Advertising', 'Cleaning', 'Telecom', 'Realtor'
]
ORGANIZATION_TYPE_dict = dict(zip(ORGANIZATION_TYPE_rus, ORGANIZATION_TYPE_eng))


# Тип дохода
NAME_INCOME_TYPE_rus = [
    "Студент", "Работающий", "Коммерческий партнер", "Госслужащий", "Пенсионер", "Безработный"
]
NAME_INCOME_TYPE_eng = [
    "Student", "Working", "Commercial associate", "State servant", "Pensioner", "Unemployed"
]
NAME_INCOME_TYPE_dict = dict(zip(NAME_INCOME_TYPE_rus, NAME_INCOME_TYPE_eng))
