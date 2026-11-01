class BasePage:
    def __init__(self, ui):
        self.ui = ui
    def click(self, selector):
        self.ui.click(selector)
    def text(self, selector):
        return self.ui.text(selector)
    def visible(self, selector):
        return self.ui.visible(selector)
