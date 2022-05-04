from pathlib import Path
from typing import List


class Utils:
    @staticmethod
    def get_available_keywords() -> List[str]:
        available_keywords = ["Computer Science", ".NET Development", "Python", "Android App Development",
                              "Angular.js Development", "Django", "Javascript",
                              "Artificial Intelligence (AI)", "ASP.NET Development", "Backend Development", "Big Data",
                              "Blockchain Development", "Cloud Computing", "Computer Vision", "Cyber Security",
                              "Data Entry", "Data Science", "Database Building", "Flutter Development",
                              "Front End Development", "Full Stack Development", "Image Processing",
                              "iOS App Development", "Java Development", "Javascript Development", "Machine Learning",
                              "Mobile App Development", "Node.js Development", "Network Engineering", "PHP Development",
                              "Programming", "Python Development", "Django Development", "Software Development",
                              "Software Testing", "UI/UX Design", "Web Development", "Wordpress Development",
                              "React Native Development", "ReactJS Development", "Product Management",
                              "MERN Stack Development", "Quality Assurance", "Web Design", "Internet of Things (IoT)", ]

        return sorted(available_keywords)

    @staticmethod
    def is_file_extension_supported(path: Path) -> bool:
        return path.suffix == ".csv"

    @staticmethod
    def is_file_path_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def is_parent_path_exists(path: Path) -> bool:
        return path.parent.exists()
