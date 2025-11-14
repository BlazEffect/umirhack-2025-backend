from pony.orm import db_session

from db.models import CropRotationRule, AppetiteLevel, PlantFamily, Crop


@db_session
def create_detailed_seed_data():
    if AppetiteLevel.select().first():
        return

    low_appetite = AppetiteLevel(level_name='low', description='Низкое потребление питательных веществ')
    medium_appetite = AppetiteLevel(level_name='medium', description='Среднее потребление питательных веществ')
    high_appetite = AppetiteLevel(level_name='high', description='Высокое потребление питательных веществ')

    families = {
        'solanaceae': PlantFamily(name='Пасленовые', latin_name='Solanaceae',
                                  description='Томаты, перцы, баклажаны, картофель'),
        'cucurbitaceae': PlantFamily(name='Тыквенные', latin_name='Cucurbitaceae',
                                     description='Огурцы, кабачки, тыквы, арбузы'),
        'brassicaceae': PlantFamily(name='Капустные', latin_name='Brassicaceae',
                                    description='Капуста, редис, редька, горчица'),
        'fabaceae': PlantFamily(name='Бобовые', latin_name='Fabaceae', description='Горох, фасоль, бобы, чечевица'),
        'apiaceae': PlantFamily(name='Зонтичные', latin_name='Apiaceae',
                                description='Морковь, петрушка, сельдерей, укроп'),
        'amaranthaceae': PlantFamily(name='Амарантовые', latin_name='Amaranthaceae',
                                     description='Свекла, шпинат, мангольд'),
        'amaryllidaceae': PlantFamily(name='Луковые', latin_name='Amaryllidaceae',
                                      description='Лук, чеснок, лук-порей'),
        'asteraceae': PlantFamily(name='Астровые', latin_name='Asteraceae', description='Салат, подсолнечник, артишок'),
        'poaceae': PlantFamily(name='Злаки', latin_name='Poaceae', description='Пшеница, рожь, овес, ячмень, кукуруза'),
        'polygonaceae': PlantFamily(name='Гречишные', latin_name='Polygonaceae', description='Гречиха, щавель'),
        'linaceae': PlantFamily(name='Льновые', latin_name='Linaceae', description='Лен'),
        'malvaceae': PlantFamily(name='Мальвовые', latin_name='Malvaceae', description='Хлопчатник')
    }

    crops_data = [
        # Пасленовые (высокий аппетит)
        {'name': 'Томат', 'latin_name': 'Solanum lycopersicum', 'family': 'solanaceae', 'appetite': 'high',
         'crop_type': 'vegetable', 'nutrient_demand': 'high', 'water_demand': 'medium', 'disease_risk': 'high',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        {'name': 'Картофель', 'latin_name': 'Solanum tuberosum', 'family': 'solanaceae', 'appetite': 'high',
         'crop_type': 'root', 'nutrient_demand': 'high', 'water_demand': 'medium', 'disease_risk': 'high',
         'preferred_ph': 'acidic', 'rotation_interval': 4},

        {'name': 'Перец', 'latin_name': 'Capsicum annuum', 'family': 'solanaceae', 'appetite': 'high',
         'crop_type': 'vegetable', 'nutrient_demand': 'high', 'water_demand': 'medium', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        {'name': 'Баклажан', 'latin_name': 'Solanum melongena', 'family': 'solanaceae', 'appetite': 'high',
         'crop_type': 'vegetable', 'nutrient_demand': 'high', 'water_demand': 'medium', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        # Тыквенные (средний-высокий аппетит)
        {'name': 'Огурец', 'latin_name': 'Cucumis sativus', 'family': 'cucurbitaceae', 'appetite': 'high',
         'crop_type': 'vegetable', 'nutrient_demand': 'high', 'water_demand': 'high', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        {'name': 'Кабачок', 'latin_name': 'Cucurbita pepo', 'family': 'cucurbitaceae', 'appetite': 'medium',
         'crop_type': 'vegetable', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        {'name': 'Тыква', 'latin_name': 'Cucurbita maxima', 'family': 'cucurbitaceae', 'appetite': 'medium',
         'crop_type': 'vegetable', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        # Капустные (высокий аппетит)
        {'name': 'Капуста белокочанная', 'latin_name': 'Brassica oleracea', 'family': 'brassicaceae',
         'appetite': 'high',
         'crop_type': 'vegetable', 'nutrient_demand': 'high', 'water_demand': 'high', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 4},

        {'name': 'Редис', 'latin_name': 'Raphanus sativus', 'family': 'brassicaceae', 'appetite': 'low',
         'crop_type': 'root', 'nutrient_demand': 'low', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        # Бобовые (низкий аппетит - обогащают почву)
        {'name': 'Горох', 'latin_name': 'Pisum sativum', 'family': 'fabaceae', 'appetite': 'low',
         'crop_type': 'legume', 'nutrient_demand': 'low', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        {'name': 'Фасоль', 'latin_name': 'Phaseolus vulgaris', 'family': 'fabaceae', 'appetite': 'low',
         'crop_type': 'legume', 'nutrient_demand': 'low', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        {'name': 'Люцерна', 'latin_name': 'Medicago sativa', 'family': 'fabaceae', 'appetite': 'low',
         'crop_type': 'legume', 'nutrient_demand': 'low', 'water_demand': 'low', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        # Зонтичные (средний аппетит)
        {'name': 'Морковь', 'latin_name': 'Daucus carota', 'family': 'apiaceae', 'appetite': 'medium',
         'crop_type': 'root', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        {'name': 'Петрушка', 'latin_name': 'Petroselinum crispum', 'family': 'apiaceae', 'appetite': 'medium',
         'crop_type': 'vegetable', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        # Амарантовые (средний аппетит)
        {'name': 'Свекла', 'latin_name': 'Beta vulgaris', 'family': 'amaranthaceae', 'appetite': 'medium',
         'crop_type': 'root', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        # Луковые (низкий аппетит)
        {'name': 'Лук репчатый', 'latin_name': 'Allium cepa', 'family': 'amaryllidaceae', 'appetite': 'low',
         'crop_type': 'vegetable', 'nutrient_demand': 'low', 'water_demand': 'medium', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        {'name': 'Чеснок', 'latin_name': 'Allium sativum', 'family': 'amaryllidaceae', 'appetite': 'low',
         'crop_type': 'vegetable', 'nutrient_demand': 'low', 'water_demand': 'low', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        # Злаки (средний-высокий аппетит)
        {'name': 'Пшеница', 'latin_name': 'Triticum aestivum', 'family': 'poaceae', 'appetite': 'medium',
         'crop_type': 'grain', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        {'name': 'Кукуруза', 'latin_name': 'Zea mays', 'family': 'poaceae', 'appetite': 'high',
         'crop_type': 'grain', 'nutrient_demand': 'high', 'water_demand': 'high', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 3},

        {'name': 'Ячмень', 'latin_name': 'Hordeum vulgare', 'family': 'poaceae', 'appetite': 'medium',
         'crop_type': 'grain', 'nutrient_demand': 'medium', 'water_demand': 'low', 'disease_risk': 'low',
         'preferred_ph': 'neutral', 'rotation_interval': 2},

        # Технические культуры
        {'name': 'Подсолнечник', 'latin_name': 'Helianthus annuus', 'family': 'asteraceae', 'appetite': 'high',
         'crop_type': 'technical', 'nutrient_demand': 'high', 'water_demand': 'medium', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 5},

        {'name': 'Рапс', 'latin_name': 'Brassica napus', 'family': 'brassicaceae', 'appetite': 'medium',
         'crop_type': 'technical', 'nutrient_demand': 'medium', 'water_demand': 'medium', 'disease_risk': 'medium',
         'preferred_ph': 'neutral', 'rotation_interval': 4}
    ]

    crops = {}
    appetite_map = {'low': low_appetite, 'medium': medium_appetite, 'high': high_appetite}

    for crop_data in crops_data:
        crop = Crop(
            name=crop_data['name'],
            latin_name=crop_data['latin_name'],
            family=families[crop_data['family']],
            appetite_level=appetite_map[crop_data['appetite']],
            crop_type=crop_data['crop_type'],
            nutrient_demand=crop_data['nutrient_demand'],
            water_demand=crop_data['water_demand'],
            disease_risk=crop_data['disease_risk'],
            preferred_ph=crop_data['preferred_ph'],
            recommended_rotation_interval=crop_data['rotation_interval']
        )
        crops[crop_data['name']] = crop

    rules_data = [
        # Хорошие последователи после бобовых
        {'prev': 'Горох', 'next': 'Томат', 'comp': 'good', 'desc': 'Бобовые обогащают почву азотом'},
        {'prev': 'Фасоль', 'next': 'Огурец', 'comp': 'good', 'desc': 'Бобовые - хороший предшественник для тыквенных'},
        {'prev': 'Люцерна', 'next': 'Пшеница', 'comp': 'good', 'desc': 'Многолетние бобовые улучшают структуру почвы'},
        {'prev': 'Люцерна', 'next': 'Кукуруза', 'comp': 'good', 'desc': 'Сидерат обогащает почву органикой'},

        # Плохие последователи (одно семейство)
        {'prev': 'Томат', 'next': 'Картофель', 'comp': 'bad', 'desc': 'Одинаковое семейство - риск болезней'},
        {'prev': 'Картофель', 'next': 'Томат', 'comp': 'bad', 'desc': 'Одинаковое семейство - накопление болезней'},
        {'prev': 'Капуста белокочанная', 'next': 'Редис', 'comp': 'bad',
         'desc': 'Одинаковое семейство - общие вредители'},
        {'prev': 'Капуста белокочанная', 'next': 'Капуста белокочанная', 'comp': 'bad',
         'desc': 'Накопление килы и других болезней'},

        # Хорошие последователи
        {'prev': 'Лук репчатый', 'next': 'Морковь', 'comp': 'good', 'desc': 'Лук отпугивает морковную муху'},
        {'prev': 'Морковь', 'next': 'Лук репчатый', 'comp': 'good', 'desc': 'Смешанные посадки взаимно защищают'},
        {'prev': 'Картофель', 'next': 'Свекла', 'comp': 'good', 'desc': 'Разные типы корневых систем'},
        {'prev': 'Морковь', 'next': 'Горох', 'comp': 'good', 'desc': 'Корнеплоды после бобовых'},
        {'prev': 'Пшеница', 'next': 'Свекла', 'comp': 'good', 'desc': 'Зерновые оставляют хорошую структуру почвы'},
        {'prev': 'Ячмень', 'next': 'Картофель', 'comp': 'good', 'desc': 'Зерновые подавляют сорняки для картофеля'},

        # Плохие последователи
        {'prev': 'Подсолнечник', 'next': 'Подсолнечник', 'comp': 'bad', 'desc': 'Сильное истощение почвы'},
        {'prev': 'Кукуруза', 'next': 'Подсолнечник', 'comp': 'bad', 'desc': 'Обе культуры сильно истощают почву'},
    ]

    for rule_data in rules_data:
        CropRotationRule(
            previous_crop=crops[rule_data['prev']],
            next_crop=crops[rule_data['next']],
            compatibility=rule_data['comp'],
            rule_description=rule_data['desc']
        )
