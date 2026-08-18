"""
Skill Normalization and Alias Layer.
Maps user-provided skill names, aliases, and formatting variations to canonical database skill slugs.
"""
import re
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from backend.app.models.skill import Skill


class SkillNormalizer:
    """Normalizes skill names and aliases to canonical database skill slugs."""

    # Built-in alias map for common skill variations
    KNOWN_ALIASES = {
        "html/css": "html-css",
        "html & css": "html-css",
        "html and css": "html-css",
        "htmlcss": "html-css",
        "html": "html-css",
        "css": "html-css",
        "node.js": "nodejs",
        "node js": "nodejs",
        "node": "nodejs",
        "nodejs": "nodejs",
        "express.js": "expressjs",
        "express js": "expressjs",
        "express": "expressjs",
        "expressjs": "expressjs",
        "react.js": "react",
        "react js": "react",
        "react": "react",
        "git/github": "git-github",
        "git & github": "git-github",
        "git and github": "git-github",
        "git github": "git-github",
        "git": "git-github",
        "github": "git-github",
        "scikit learn": "scikit-learn",
        "scikit-learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "xgboost & lightgbm": "xgboost-lightgbm",
        "xgboost/lightgbm": "xgboost-lightgbm",
        "xgboost": "xgboost-lightgbm",
        "lightgbm": "xgboost-lightgbm",
        "matplotlib & seaborn": "matplotlib-seaborn",
        "matplotlib/seaborn": "matplotlib-seaborn",
        "matplotlib": "matplotlib-seaborn",
        "seaborn": "matplotlib-seaborn",
        "rest api": "rest-api-design",
        "rest api design": "rest-api-design",
        "rest apis": "rest-api-design",
        "excel": "excel-advanced",
        "advanced excel": "excel-advanced",
        "excel advanced": "excel-advanced",
        "power bi": "power-bi",
        "powerbi": "power-bi",
        "ml": "machine-learning-fundamentals",
        "machine learning": "machine-learning-fundamentals",
        "deep learning": "deep-learning-fundamentals",
        "dl": "deep-learning-fundamentals",
        "nlp": "nlp-fundamentals",
        "llm": "large-language-models",
        "llms": "large-language-models",
        "rag": "retrieval-augmented-generation",
        "eda": "exploratory-data-analysis",
        "stats": "descriptive-statistics"
    }

    def __init__(self, db: Session):
        self.db = db
        self.slug_lookup = self._build_slug_lookup()

    def _clean_string(self, text: str) -> str:
        """Standardize raw string for lookup."""
        if not text:
            return ""
        s = text.strip().lower()
        # Replace ampersands, slashes, or ' and ' with hyphens
        s = re.sub(r'[\s/&]+', '-', s)
        s = re.sub(r'-and-', '-', s)
        # Remove characters that aren't alphanumeric or hyphens
        s = re.sub(r'[^a-z0-9\-]', '', s)
        # Collapse multiple hyphens
        s = re.sub(r'-+', '-', s)
        return s.strip('-')

    def _build_slug_lookup(self) -> Dict[str, str]:
        """Build bidirectional lookup from database skills and known aliases."""
        lookup = {}
        all_skills = self.db.query(Skill).all()

        for s in all_skills:
            canonical_slug = s.slug.lower()
            lookup[canonical_slug] = canonical_slug
            lookup[s.name.lower()] = canonical_slug

            # Clean name variant
            cleaned_name = self._clean_string(s.name)
            if cleaned_name:
                lookup[cleaned_name] = canonical_slug

            cleaned_slug = self._clean_string(s.slug)
            if cleaned_slug:
                lookup[cleaned_slug] = canonical_slug

        # Add explicit known aliases
        for alias, canonical_slug in self.KNOWN_ALIASES.items():
            lookup[alias.lower()] = canonical_slug
            cleaned_alias = self._clean_string(alias)
            if cleaned_alias:
                lookup[cleaned_alias] = canonical_slug

        return lookup

    def normalize(self, skill_name_or_alias: str) -> Optional[str]:
        """
        Resolve raw user skill string to canonical database skill_slug.
        Returns None if no canonical match found.
        """
        if not skill_name_or_alias:
            return None

        raw = str(skill_name_or_alias).strip().lower()

        # 1. Exact match in lookup
        if raw in self.slug_lookup:
            return self.slug_lookup[raw]

        # 2. Clean string match
        cleaned = self._clean_string(raw)
        if cleaned in self.slug_lookup:
            return self.slug_lookup[cleaned]

        # 3. Known alias direct check
        if raw in self.KNOWN_ALIASES:
            return self.KNOWN_ALIASES[raw]

        return None
