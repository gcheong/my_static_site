from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        
        match self.tag:

            case "a":
                return f"<a {self.props_to_html()}>{self.value}</a>"
            case "img":
                return f"<img {self.props_to_html()}</img>"
            case _:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"