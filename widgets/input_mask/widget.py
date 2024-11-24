from django.forms.widgets import Input, Media


class InputMask(Input):
    input_type = "text"

    def __init__(self, pattern: str):
        super().__init__(
            attrs={
                "data-mask": pattern,
            }
        )

    @property
    def media(self):
        return Media(
            js=["input-mask/vanilla-masker.js", "input-mask/vanilla-masker.init.js"]
        )
