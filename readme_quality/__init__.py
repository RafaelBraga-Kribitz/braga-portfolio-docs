"""BRAGA README Quality Gate.

Standard  -> docs/README_STANDARD.md        (what "great" means)
Manifest  -> manifest/requirements.yaml     (machine-readable contract)
Registry  -> manifest/portfolio.yaml        (declared project facts)
Templates -> templates/*.md                 (starting structure per type)
Blocks    -> blocks/*.md                    (canonical reusable blocks)
Gate      -> readme_quality.audit           (PASS / FAIL / BLOCKED_HUMAN)
Fixer     -> readme_quality.fix             (safe automatic remediation)
Generator -> readme_quality.hero            (design-system hero banner)
Portfolio -> readme_quality.portfolio       (run everything across repos)
"""

__version__ = "1.1.0"
