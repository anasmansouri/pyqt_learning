class ManagementOfServices:
    def __init__(self, top_service_class=None, sub_service_class=None):
        self.top_service_classes = ['Upload Download Management', 'Stored Data Transmission',
                                    'Diagnostic and Communication Management',
                                    'Remote Activation Of Routine', 'Input Output Control', 'Data Transmisson']
        self.top_service_class = top_service_class
        self.sub_service_class = sub_service_class

    def fill_infos(self, text):
        for service in self.top_service_classes:
            if text == service:
                self.top_service_class = text
                return False
        else:
            if self.top_service_class is not None:
                self.sub_service_class = text
            return True
