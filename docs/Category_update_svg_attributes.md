# Category.update_svg_attributes(self, **kwargs)

## Possíveis atributos
- width
- height
- viewBox
- fill_svg: Atributo 'fill' para o SVG
- fill_path: Atributo 'fill' para o SVG

## Uso

`> from features.stores.models import Category`

`> c = Category.objects.last()`

`> c.update_svg_attributes(width="10", height="10")`
