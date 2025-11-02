from datetime import datetime, date
from typing import List, Dict, Any
from ..schemas.task_schema import TaskResponse

def format_date(date_obj: date) -> str:
    """Format date to string"""
    return date_obj.strftime("%Y-%m-%d")

def format_datetime(datetime_obj: datetime) -> str:
    """Format datetime to string"""
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

def generate_client_update(tasks: List[TaskResponse], format_template: str = None) -> str:
    """Generate client update summary from tasks"""
    if not tasks:
        return "No tasks completed today."
    
    if format_template:
        # Use custom format template
        task_list = "\n".join([f"- {task.task_title}: {task.task_desc or 'Completed'}" for task in tasks])
        return format_template.replace("{tasks}", task_list).replace("{date}", format_date(tasks[0].date))
    else:
        # Default format
        date_str = format_date(tasks[0].date)
        task_list = "\n".join([f"• {task.task_title}" + (f": {task.task_desc}" if task.task_desc else "") for task in tasks])
        
        return f"""Daily Update - {date_str}

Tasks Completed:
{task_list}

Total tasks completed: {len(tasks)}"""

def validate_email_format(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized.strip()

def paginate_results(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }