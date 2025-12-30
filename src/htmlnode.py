class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""

        propStrings = []
        for prop in self.props:
            propStrings.append(f'{prop}="{self.props[prop]}"')
        
        return " ".join(propStrings)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    