from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 4:
            raise ValidationError(_("Your password must contain at least 4 characters."), code='password_too_short')
        
        # 取消密碼不能與個人資訊相似的限制
        # 取消常用密碼限制
        # 取消完全為數字的密碼限制

    def get_help_text(self):
        return ""