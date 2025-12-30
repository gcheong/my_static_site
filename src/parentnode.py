from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag for ParentNode is not optional")
        if self.children == None or len(self.children) == 0:
            raise ValueError("ParentNode requires at least 1 child")
       
        child_html = ""
        for child in self.children:
            child_html += child.to_html()

        match self.tag:

            case "a":
                return f"<a {self.props_to_html()}>{child_html}</a>"
            case _:
                return f"<{self.tag}>{child_html}</{self.tag}>"
            
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"