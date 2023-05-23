from pymaidol.TemplateBase import TemplateBase

class FirstTemplate(TemplateBase):
    def __init__(self, package_name:str, template: str | None = None, template_file_path: str | None = None) -> None:
        super().__init__(template, template_file_path)
        self.package_name = package_name
        
def main():
    template = FirstTemplate("Pymaidol")
    string = template.Render({"says": "Hello World"})
    print(string)
    
if __name__ == "__main__":
    main()