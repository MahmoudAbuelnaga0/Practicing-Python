class Property:
    def __init__(self, price:str, address:str, link:str) -> None:
        self.price = price
        self.address = address
        self.link = link
        
    def __repr__(self) -> str:
        return f"Price: {self.price}\nAddress: {self.address}\nLink: {self.link}"
    
    def __str__(self) -> str:
        return f"Price: {self.price}\nAddress: {self.address}\nLink: {self.link}"
    
    def get_attributes(self):
        return (self.address, self.price, self.link)