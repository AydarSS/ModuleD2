from django import template


register = template.Library()


CENSURED_WORDS = {
   'гегемонии': 'г********',
   'льготы': 'л*****',
   'травму': 'т*****',
}


def multiple_replace(target_str, replace_values):
   # получаем заменяемое: подставляемое из словаря в цикле
   for i, j in replace_values.items():
      # меняем все target_str на подставляемое
      target_str = target_str.replace(i, j)
   return target_str

@register.filter()
def censura (value):
   if isinstance(value, str):
      censured_value = multiple_replace(value,CENSURED_WORDS)
   else:
      raise ValueError("Это не число")

   return censured_value