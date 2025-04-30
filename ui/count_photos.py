class Count(object):
    '''
    количество загруженных картинок
    '''
    def __init__(self, ui):
        self.ui = ui
        self.count = len(self.ui.photos.photos)
        
        self.ui.photos.photos_updated.connect(self.update_count)
        
        self.count_translate = self.ui._translate('Describer', '{index} фото')
        self.ui.label_count.setText(self.count_translate.format(index=self.count))
        self.update_count()
        self.ui.lang_changed.connect(self.retranslateUi)
        
        
    def retranslateUi(self):
        self.count_translate = self.ui._translate('Describer', '{index} фото')
        self.ui.label_count.setText(self.count_translate.format(index=self.count))
        
        
    def update_count(self):
        self.count = len(self.ui.photos.photos)
        self.ui.label_count.setText(self.count_translate.format(index=self.count))