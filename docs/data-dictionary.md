# TechPath SA - Data Dictionary

## Tables

### `jobs`
Stores job postings gathered from South African sources.
- `id`: Primary Key
- `title`: Job title (e.g., Junior Data Engineer)
- `company`: Hiring organization
- `location`: South African city or remote option
- `description`: Role overview
- `employment_type`: Full-time, contract, etc.
- `experience_level`: Junior, Graduate, Mid-level
- `qualification`: Required academic or certificate background
- `source`: Origin source tracking name

### `skills`
Controlled list of technical skills extracted from job descriptions and requirements.
- `id`: Primary Key
- `name`: Normalized skill name (e.g., Python, AWS)
- `category`: Domain category (Programming, Data, Cloud, DevOps)

### `careers`
Target career profiles with mapped required skill sets.
- `id`: Primary Key
- `name`: Career path title (e.g., Data Engineer)
- `description`: Role summary