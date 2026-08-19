"""
NLP модуль для извлечения и классификации Национальных проектов
"""
import re
from typing import List, Dict, Tuple
from datetime import datetime

try:
    import natasha
    HAS_NATASHA = True
except ImportError:
    HAS_NATASHA = False


class ProjectClassifier:
    """Классификатор текста по Национальным проектам"""
    
    # Предопределенные паттерны для каждого проекта
    PROJECT_KEYWORDS = {
        "Демография": {
            "keywords": [
                "демография", "рождаемость", "семья", "население", "дети",
                "родители", "материнский капитал", "детский сад", "многодетн"
            ],
            "patterns": [
                r"демограф\w*",
                r"рождаемост\w*",
                r"материнск\w*\s+капитал",
                r"детск\w*\s+пособи\w*"
            ]
        },
        "Культура": {
            "keywords": [
                "культура", "музей", "театр", "искусство", "выставка", 
                "библиотека", "кинематограф", "памятник", "культурн"
            ],
            "patterns": [
                r"культур\w*",
                r"музе\w*",
                r"театр\w*",
                r"искусств\w*"
            ]
        },
        "Образование": {
            "keywords": [
                "образование", "школа", "университет", "студент", "учитель",
                "учебн", "образовательн", "педагог", "лицей", "гимназия"
            ],
            "patterns": [
                r"образован\w*",
                r"школ\w*",
                r"университет\w*",
                r"студент\w*"
            ]
        },
        "Здравоохранение": {
            "keywords": [
                "здравоохранение", "больница", "врач", "медицина", "клиника",
                "здоровь", "поликлиник", "МСЧ", "ФАП", "амбулатори"
            ],
            "patterns": [
                r"здравоохран\w*",
                r"больниц\w*",
                r"врач\w*",
                r"медицин\w*"
            ]
        },
        "Наука и университеты": {
            "keywords": [
                "наука", "университет", "исследование", "лаборатория",
                "научн", "НИИ", "научно-исследовательск", "академия"
            ],
            "patterns": [
                r"наук\w*",
                r"университет\w*",
                r"исследован\w*",
                r"лаборатор\w*"
            ]
        },
        "Жилье и городская среда": {
            "keywords": [
                "жилье", "дом", "квартира", "строительство", "город",
                "жилищн", "строител", "благоустройств", "парк", "площадь"
            ],
            "patterns": [
                r"жил\w*",
                r"строител\w*",
                r"квартир\w*",
                r"благоустр\w*"
            ]
        },
        "Экология": {
            "keywords": [
                "экология", "окружающая среда", "природа", "загрязнение",
                "экологич", "окружающ", "парк", "лес", "вода", "воздух"
            ],
            "patterns": [
                r"эколог\w*",
                r"окружающ\w*",
                r"загрязнен\w*",
                r"природ\w*"
            ]
        },
        "Безопасные качественные дороги": {
            "keywords": [
                "дорога", "дорожное", "транспорт", "дорожная безопасность",
                "автодорог", "БКД", "трасса", "ремонт дорог", "асфальт"
            ],
            "patterns": [
                r"дорог\w*",
                r"дорожн\w*",
                r"БКД",
                r"автодорог\w*"
            ]
        },
        "Цифровая экономика": {
            "keywords": [
                "цифровая", "интернет", "технология", "IT", "цифра",
                "цифровизац", "данн", "электронн", "информацион"
            ],
            "patterns": [
                r"цифр\w*",
                r"интернет\w*",
                r"технолог\w*",
                r"информацион\w*"
            ]
        },
        "Малое и среднее предпринимательство": {
            "keywords": [
                "МСП", "бизнес", "предпринимательство", "компания", "фирма",
                "малый бизнес", "грант", "кредит", "финансирование"
            ],
            "patterns": [
                r"бизнес\w*",
                r"предпринима\w*",
                r"МСП",
                r"компани\w*"
            ]
        },
        "Туризм и индустрия гостеприимства": {
            "keywords": [
                "туризм", "туристический", "отель", "гостиница", "туристы",
                "туристич", "курорт", "гостеприимств", "пляж", "агротуризм"
            ],
            "patterns": [
                r"туризм\w*",
                r"туристич\w*",
                r"отель\w*",
                r"гостиниц\w*"
            ]
        },
        "Семья": {
            "keywords": [
                "семья", "дети", "родители", "семейные", "матери", "отцы",
                "материнство", "отцовство", "многодетн", "материнский"
            ],
            "patterns": [
                r"семь\w*",
                r"детей",
                r"родител\w*",
                r"материнск\w*"
            ]
        }
    }
    
    # Маркеры локации Херсонской области
    LOCATION_MARKERS = {
        "cities": ["Херсон", "Геническ", "Каховка", "Чорноморськ", "Скадовськ"],
        "regions": ["Херсонская область", "Херсонской", "Херсонской области", "Kherson"],
        "districts": ["Голопристанський", "Белозерський", "Красноперекопськ"],
        "variations": ["Kherson", "Kherson region", "Kherson Oblast"]
    }
    
    def __init__(self):
        """Инициализация классификатора"""
        if HAS_NATASHA:
            try:
                self.segmenter = natasha.Segmenter()
                self.morph = natasha.MorphVocab()
                self.has_natasha = True
            except Exception as e:
                print(f"Warning: Natasha initialization failed: {e}")
                self.has_natasha = False
        else:
            self.has_natasha = False
    
    def extract_location_markers(self, text: str) -> List[str]:
        """
        Извлечение маркеров локации из текста
        Возвращает список найденных маркеров
        """
        text_lower = text.lower()
        found_markers = []
        
        for marker_type, markers in self.LOCATION_MARKERS.items():
            for marker in markers:
                if marker.lower() in text_lower:
                    found_markers.append(marker)
        
        return list(set(found_markers))  # Удаление дубликатов
    
    def is_kherson_related(self, text: str) -> bool:
        """Проверка, относится ли статья к Херсонской области"""
        markers = self.extract_location_markers(text)
        return len(markers) > 0
    
    def classify_projects(self, text: str, threshold: float = 0.5) -> Dict[str, float]:
        """
        Классификация текста по Национальным проектам
        Возвращает словарь {project_name: confidence_score}
        """
        text_lower = text.lower()
        results = {}
        
        for project_name, project_data in self.PROJECT_KEYWORDS.items():
            score = self._calculate_score(text_lower, project_data)
            
            if score >= threshold:
                results[project_name] = score
        
        return results
    
    def _calculate_score(self, text: str, project_data: Dict) -> float:
        """
        Расчет уверенности классификации для проекта
        Основан на совпадении ключевых слов и regex паттернов
        """
        score = 0.0
        matches = 0
        total_checks = 0
        
        # Проверка ключевых слов
        for keyword in project_data["keywords"]:
            total_checks += 1
            if keyword.lower() in text:
                matches += 1
                score += 0.3
        
        # Проверка regex паттернов
        for pattern in project_data["patterns"]:
            total_checks += 1
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    matches += 1
                    score += 0.5
            except re.error:
                pass
        
        # Нормализация оценки
        if total_checks > 0:
            score = min(score, 1.0)
            score = max(score, 0.0)
        
        return score
    
    def extract_entities(self, text: str) -> Dict:
        """
        Извлечение именованных сущностей (если доступна Natasha)
        """
        entities = {
            "location": [],
            "organization": [],
            "person": []
        }
        
        if not self.has_natasha:
            return entities
        
        try:
            doc = natasha.Doc(text)
            doc.segment(self.segmenter)
            doc.parse_syntax()
            
            for ent in doc.ents:
                if ent.type == "LOC":
                    entities["location"].append(ent.text)
                elif ent.type == "ORG":
                    entities["organization"].append(ent.text)
                elif ent.type == "PER":
                    entities["person"].append(ent.text)
        except Exception as e:
            print(f"Error in entity extraction: {e}")
        
        return entities
    
    def process_article(self, text: str, title: str = "") -> Dict:
        """
        Полная обработка статьи:
        - Проверка локации
        - Классификация по проектам
        - Извлечение сущностей
        """
        full_text = f"{title} {text}"
        
        return {
            "location_markers": self.extract_location_markers(full_text),
            "is_kherson_related": self.is_kherson_related(full_text),
            "national_projects": self.classify_projects(full_text),
            "entities": self.extract_entities(full_text),
            "processed_at": datetime.utcnow()
        }


# Глобальный экземпляр классификатора
classifier = ProjectClassifier()
