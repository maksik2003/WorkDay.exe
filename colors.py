class color_theme:
    """
    Класс, содержащий в себе цвета, которые будут использоваться в процессе работы.\n
    По умолчанию создается класс, с базовыми цветами (те, которые я прописал).\n
    Если пользователь хочет, то он может выбрать для себя цвета:\n
    Для того, чтобы использовать персональную цветовуую схему, необходимо добавить запись в табл. themes\n
    """
    def __init__(self):
        self.white   = '#FFFFFF'
        self.black   = '#1C1D22'
        self.brown   = '#252525'
        self.red     = '#DF5D5D'
        self.blue    = '#75B2EF'
        self.grey    = '#808080'

        self.green   = '#5ddf8b'
        self.yellow  = '#dddf5d'

        self.text_color         = self.white
        self.background         = self.black
        self.rectangle          = self.brown
        self.hover              = self.blue
        self.hover_negative     = self.red
        self.non_active_color   = self.grey
        self.indicator_border   = self.white
        self.text_color_inverse = self.white

        # dddf5d - желтый
        # 5ddf8b - зеленый

    def my_theme(self,
                text_color: str = '#00FF00',
                background: str = '#00FF00',
                rectangle: str = '#00FF00',
                hover: str = '#00FF00',
                hover_negative: str = '#00FF00',
                non_active_color: str = '#00FF00',
                indicator_border: str = '#00FF00',
                text_color_inverse: str = '#00FF00'):
                
        self.text_color         = text_color
        self.background         = background
        self.rectangle          = rectangle
        self.hover              = hover
        self.hover_negative     = hover_negative
        self.non_active_color   = non_active_color
        self.indicator_border   = indicator_border
        self.text_color_inverse = text_color_inverse